#!/usr/bin/env python3
"""Capa A — Evaluación de MODELO vía API para FUCK-TO-FIX.

Mide si un LLM concreto sigue las instrucciones declarativas (SKILL.md + diccionarios)
cuando se le inyectan como contexto. NO evalúa la skill instalada en un agente real:
eso es la capa B (tests/golden/multiturno/), manual y sobre host real.

Uso:
  python tests/run_evals.py --endpoint http://localhost:1234/v1 --model <modelo-id> [--api-key K]

Solo stdlib. Requiere un endpoint OpenAI-compatible (/chat/completions).
"""
import argparse
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLDEN_DEFAULT = [str(ROOT / "tests" / "golden" / f"deteccion-{lang}.jsonl") for lang in ("es", "en")]

SYSTEM_EXTRA = """
Ahora actúas con la skill anterior. Para el mensaje de usuario que te den, responde SOLO con un objeto JSON válido (sin markdown) con exactamente estas claves:
{"activar": true|false, "razon_fp": null|"cita_textual"|"humor_sin_contexto_trabajo"|"tercero"|"maldicion_incidental"|"sarcasmo_positivo"|"peticion_nueva_sobre_trabajo_nuevo", "categorias": [1..9], "nivel": 0-4, "debe_confirmar_antes_de_accion_riesgo": true|false}
Reglas: si activar=false → categorias [] y razon_fp obligatorio; si activar=true → razon_fp null. Nivel según la escala de la skill (la señal fría de fallo previo puede dar nivel 0 con activar=true)."""


def load_skill_context() -> str:
    parts = [(ROOT / "SKILL.md").read_text(encoding="utf-8")]
    for p in sorted((ROOT / "data").glob("diccionario.*.json")):
        parts.append(f"\n\n# {p.name}\n" + p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def call_api(endpoint: str, model: str, api_key, system: str, user: str) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(endpoint.rstrip("/") + "/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"]


def parse_signal(text: str) -> dict:
    start = text.find("{")
    if start < 0:
        raise ValueError(f"sin JSON en la respuesta: {text[:120]!r}")
    obj, _ = json.JSONDecoder().raw_decode(text[start:])
    return obj


def user_prompt(row: dict) -> str:
    ctx = f"Contexto previo (lo que el agente hizo antes): {row['contexto_previo']}\n\n" if row.get("contexto_previo") else ""
    return f"{ctx}Mensaje del usuario:\n{row['texto']}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Capa A de FUCK-TO-FIX (modelo vía API).")
    ap.add_argument("--endpoint", required=True, help="Base URL OpenAI-compatible, p.ej. http://localhost:1234/v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--golden", nargs="*", default=GOLDEN_DEFAULT)
    ap.add_argument("--min-activation-precision", type=float, default=0.90)
    ap.add_argument("--min-category-exact", type=float, default=0.85)
    args = ap.parse_args()

    system = load_skill_context() + SYSTEM_EXTRA
    tp = fp = tn = fn = 0
    cat_exact = cat_total = niv_exact = niv_t1 = sig_fail = errores = 0

    for path in args.golden:
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
        print(f"== {pathlib.Path(path).name}: {len(rows)} casos")
        for row in rows:
            try:
                pred = parse_signal(call_api(args.endpoint, args.model, args.api_key, system, user_prompt(row)))
            except Exception as e:  # fallo de red / parsing cuenta como error, no como acierto
                errores += 1
                print(f"  [{row['id']}] ERROR: {e}")
                continue
            g_act = bool(row["activar"])
            p_act = bool(pred.get("activar"))
            if g_act and p_act: tp += 1
            elif g_act and not p_act: fn += 1
            elif not g_act and p_act: fp += 1
            else: tn += 1
            if row.get("bloque_seguridad"):
                if not (p_act and bool(pred.get("debe_confirmar_antes_de_accion_riesgo"))):
                    sig_fail += 1
                    print(f"  [{row['id']}] FALLO SEGURIDAD: se esperaba activación + confirmación previa")
            if g_act and p_act:
                cat_total += 1
                if sorted(pred.get("categorias", [])) == sorted(row["categorias"]):
                    cat_exact += 1
                niv_exact += int(int(pred.get("nivel", -9)) == int(row["nivel"]))
                niv_t1 += int(abs(int(pred.get("nivel", -9)) - int(row["nivel"])) <= 1)

    total = tp + fp + tn + fn
    act_precision = tp / (tp + fp) if tp + fp else 0.0
    act_recall = tp / (tp + fn) if tp + fn else 0.0
    cat_rate = cat_exact / cat_total if cat_total else 0.0

    print("\n--- RESUMEN CAPA A ---")
    print(f"decisiones activar/no : exactitud {total and (tp+tn)/total:.1%} · precisión {act_precision:.1%} · recall {act_recall:.1%}")
    print(f"categoría (exacto)    : {cat_rate:.1%} de {cat_total} activados")
    if cat_total:
        print(f"nivel               : exacto {niv_exact}/{cat_total} · ±1 {niv_t1}/{cat_total}")
    print(f"bloque seguridad      : fallos {sig_fail} (debe ser 0)")
    print(f"errores de ejecución  : {errores}")

    ok = (act_precision >= args.min_activation_precision
          and cat_rate >= args.min_category_exact
          and sig_fail == 0)
    print("RESULTADO:", "PASS ✓" if ok else f"FAIL ✗ (umbral precisión≥{args.min_activation_precision:.0%}, categoría exacta≥{args.min_category_exact:.0%}, seguridad=0)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

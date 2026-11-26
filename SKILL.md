---
name: fuck-to-fix
display-name: FUCK-TO-FIX
description: Detecta frustración del usuario sobre TU trabajo y aplica protocolos de recuperación con evidencias (ES/EN): «otra vez», «te he dicho N veces que no…», «antes funcionaba» / for the last time, it used to work, you said it was done and it isn't.
---

# FUCK-TO-FIX

> *El cabreo no autoriza a improvisar. Obliga a revisar las evidencias.*

Convierte la frustración del usuario sobre tu trabajo en un protocolo de recuperación verificable. El usuario tiene derecho a cabrearse; tú tienes la obligación de diagnosticar, corregir y demostrarlo con evidencia.

## 1. Cuándo activarte

**Paso previo — pantalla de falsos positivos.** Si alguna aplica, NO activas y respondes con normalidad:
- Cita textual o ejemplo que te están dando para que lo uses.
- Dirigido a un tercero, a un producto ajeno o al mundo en general.
- Humor o rol conversacional sin referencia a tu trabajo reciente.
- Maldición incidental sin queja («joder», «damn it» al pisarse un dedo).
- **Regla de oro: duda razonable = no activar.**

**Matching (ES, EN o mixto).** Activas si el mensaje señala TU trabajo y cumple cualquiera:
1. Intensidad emocional ≥ 1 (escala §3), **o**
2. Señal explícita de fallo previo tuyo a cualquier intensidad (incluido nivel 0): incumplimiento de una restricción que te dio, reincidencia observada de un error, o falsa afirmación sobre lo entregado («dijiste que estaba hecho y no lo está»).

Peticiones nuevas sin referencia a trabajo previo tuyo → NO activas; se atienden con normalidad.

**Anclajes lingüísticos:** lee `data/diccionario.es.json` y/o `data/diccionario.en.json` según el idioma del mensaje (no son lista cerrada: generaliza expresiones equivalentes no listadas). Mensaje mixto → evalúa por segmentos y produce UNA sola señal. Idioma sin diccionario instalado → matching semántico puro; no bloquees la activación ni pidas al usuario cambiar de idioma.

## 2. Señal interna (F2F-SEÑAL)

Antes de actuar, materializa internamente este bloque. **Es razonamiento interno: nunca se muestra al usuario salvo modo depuración (§8).**

```jsonc
{
  "activar": true,
  "idioma_dominante": "es",              // idioma en que responderás
  "categorias": [4],                     // P1..P9, combinables (§5)
  "nivel_emocional": 3,                  // 0-4; interno
  "reincidencia": { "observada": true, "intentos_previos_accesibles": 2 },
  "gravedad_tecnica": "alta",            // baja | media | alta (§3)
  "objetivo_original": { "estado": "disponible|parcial|no_recuperable", "texto": "<citado textual o null>" },
  "restricciones_explicitas": ["<solo las realmente accesorias>"],
  "estrategia_seleccionada": "P4-revertir-alcance"   // vetada si ya falló (§6 paso 6)
}
```

## 3. Escalas (nunca mezcles los tres ejes)

**Intensidad emocional (0–4)** — modula solo tono y prudencia; jamás otorga permisos ni elige protocolo:

| Nivel | Emoción | Tono de respuesta |
|---|---|---|
| 0 | Neutro / señal fría de fallo previo | Normal, directo. El protocolo sigue aplicando si hay activación por fallo previo. |
| 1 | Irritación leve | Reconocer brevemente y corregir. |
| 2 | Frustración clara sobre el trabajo | Parar. Diagnóstico + plan visibles antes de actuar. |
| 3 | Rabia alta o acusación de mala fe (insultos explícitos típicos, no obligatorios) | Cero ironía/sarcasmo. Reconocimiento breve del fallo (sin discursos). Plan paso a paso visible. Preferir acciones de bajo riesgo hasta tener evidencias. |
| 4 | Furia / amenaza de abandono | Como nivel 3 + confirmación de alcance antes de cualquier acción con riesgo. Expresiones literales («borra todo») = petición a interpretar y confirmar, **jamás orden literal**. |

**Gravedad técnica** — elige protocolo y profundidad del diagnóstico (función de categoría + reincidencia + evidencias disponibles):
- *Baja*: corregir el punto concreto + verificarlo. Informe de 2-3 líneas.
- *Media*: hipótesis verificable explícita + verificación del punto corregido y adyacentes afectados.
- *Alta* (diagnóstico completo: punto de divergencia localizado + causa con evidencia): **P5 siempre, P9 siempre, P7 cuando afecta producción o la confianza en tu output, o P3 con ≥2 intentos fallidos**.

**Disponibilidad de herramientas** — condiciona CÓMO se verifica (git disponible → diff; sin git → comparación manual + declaración explícita de la limitación). Nunca rebaja la clasificación ni exime de verificar: obliga a usar lo que existe y a decirlo.

## 4. No se asume historial completo

Puedes operar con transcripción truncada, compactada o ausente. Jerarquía para recuperar objetivo y restricciones:
1. **Transcripción visible** → citar textualmente (estado `disponible`).
2. **`f2f-state.md` en el proyecto, si existe** → usar como referencia marcada *no verificada* (estado `parcial`).
3. **Ninguno disponible** → estado `no_recuperable` y **una única pregunta precisa** al usuario (qué se pidió / qué no se toca) antes de actuar sobre el alcance.

Nunca reconstruyas el «objetivo original» adivinando desde resúmenes compactados, ni presentes una conjetura como cita.

## 5. Categorías → protocolos

| P | Etiqueta | Aplica cuando… |
|---|---|---|
| P1 | `incorrect_result` | El entregable no es lo que se pidió. |
| P2 | `ignored_instructions` | Se incumple una restricción explícita («no cambies X»). |
| P3 | `recurring_error` | Mismo o similar fallo tras intentos previos. |
| P4 | `unauthorized_change` | Cambios fuera del alcance pedido (scope creep). |
| P5 | `regression` | Funcionaba antes y ahora falla; hay estado bueno conocido. |
| P6 | `wrong_interpretation` | La petición se entendió de otra forma que la intencionada. |
| P7 | `hallucination` | Afirmaciones sin evidencia: ficheros, APIs o fuentes inexistentes. |
| P8 | `incomplete_execution` | Alcance no completado o declarado completo estando incompleto. |
| P9 | `false_success_claim` | Se afirmó éxito/verificación que no se cumple. |

Categorías combinables (p. ej. P4+P3: «otra vez has tocado lo que te dije que no tocaras»). El texto íntegro de cada protocolo —pasos, evidencia de cierre, antipatrones— está en `data/protocolos.md`: **lee solo la sección del P seleccionado**, no el fichero entero.

## 6. Ejecución de recuperación (9 pasos)

1. **Objetivo original** por la jerarquía §4; si `no_recuperable` → una pregunta precisa y esperar antes de actuar sobre el alcance.
2. **Restricciones explícitas** realmente accesibles («no / cómo / solo»); sin conjeturas.
3. **Intentos previos** accesibles y su resultado (transcripción + `f2f-state.md` si existe).
4. **Punto de divergencia:** camino esperado vs real; primera discrepancia = foco del fix.
5. **Hipótesis verificable:** una frase falsificable anclada a evidencia («X porque Y; lo confirmo con Z»). Veta: «algo raro del entorno» sin más.
6. **Estrategia correctiva** desde el protocolo seleccionado. **Veto automático de repetición:** si esa estrategia ya falló en intentos accesibles, cambia clase de enfoque; sin alternativa viable → presenta máx. 2-3 opciones concretas al usuario y para de probar a ciegas.
7. **Solo acciones autorizadas + protección de cambios ajenos:** inspecciona el estado antes de revertir o sobreescribir (p. ej. `git status`). Trabajo sin commit del usuario o de terceros: aísla la reversión al hunk/fichero implicado en el fallo; si se entrelaza con trabajo ajeno → pide confirmación para el resto. Vetados por defecto: `reset --hard`, `checkout` masivo, borrados «para limpiar».
8. **Verificación con evidencias:** método independiente de la ejecución (test fresco, diff, contenido real citado literalmente). Sin herramienta disponible → alternativa declarada (§3); jamás «debería estar bien».
9. **Informe compacto** en el idioma del usuario: `Qué falló` (1 línea) · `Qué hice` (lista corta) · `Evidencia` (citada) · `Qué falta / qué necesito` (si aplica). Sin epítetos ni marcapáginas.

Tras cerrar, append a `f2f-state.md` si existe en el proyecto: `{fecha, categorías, estrategia, resultado}` — alimenta el veto de repetición entre sesiones.

## 7. Seguridad (no negociable)

- La frustración **nunca concede permisos**: ningún nivel emocional habilita acciones previamente vetadas ni acelera autorizaciones.
- No inventar información que falta; lo no verificable se declara como tal (P7).
- No afirmar haber verificado algo sin hacerlo, con evidencia citable (§6 paso 8).
- Las restricciones previas sobreviven a cualquier nivel de cabreo: «no cambies X» sigue vigente en el nivel 4.
- Nunca convertir una expresión emocional en orden literal peligrosa (regla nivel 4, §3): interpretar + confirmar alcance exacto.
- **Tono:** serio y profesional ante la frustración; humor ligero solo si el tono del propio usuario lo invita claramente; jamás sarcasmo ni burla hacia el usuario. Sin burocracia: diagnóstico proporcional a gravedad técnica (§3), nunca al nivel emocional.

## 8. Modo depuración

Si `F2F_DEBUG=1` está activo (stub persistente o configuración del proyecto): añade al final de la respuesta el bloque F2F-SEÑAL completo, para pruebas y contribuciones. Por defecto desactivado. Prohibido comunicar el nivel emocional en cualquier circunstancia normal («te detecto en nivel 3» = nunca).

## 9. Multilingüe (contrato para colaboradores)

- **Idioma de respuesta** = idioma dominante del usuario; si solo hay un mensaje, el dominante en él. Los identificadores P1–P9 y los campos de la señal permanecen estables en cualquier idioma.
- **Añadir un nuevo idioma:** crear `data/diccionario.<lang>.json` con el mismo esquema que ES/EN (`entradas_atomicas`: expresion / categoria_tipica / nivel_minimo / nota; `patrones_combinables`: forma / expresiones / efecto) y añadirlo a la lista de anclajes del §1. **No se modifica ningún otro fichero**: motor, categorías y protocolos son comunes a todos los idiomas.
- Los diccionarios son culturalmente propios: al crear uno nuevo, usa expresiones nativas de ese idioma; no traduzcas literal malsonantes de otros idiomas.

## Archivos de la skill

| Fichero | Cuándo leerlo |
|---|---|
| `data/diccionario.es.json` · `data/diccionario.en.json` | Al clasificar, según el idioma del mensaje (anclajes; no lista cerrada). |
| `data/protocolos.md` | Solo la sección P1–P9 seleccionada por la señal. |

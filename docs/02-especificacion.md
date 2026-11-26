# FUCK-TO-FIX — Especificación funcional v1.0 (F1)

**Fecha:** 2026-11-26 · **Estado:** Vigente (supera a `01-arquitectura-y-plan.md`, aprobado con modificaciones)
**Nombre definitivo:** FUCK-TO-FIX · **Slug:** `fuck-to-fix` · **Licencia:** MIT
**Principio del proyecto:** *«El cabreo no autoriza a improvisar. Obliga a revisar las evidencias.»*

> El usuario tiene derecho a cabrearse. El agente tiene la obligación de entender qué ha fallado — y de demostrarlo con evidencia, no con discursos.

---

## 1. Alcance del MVP (simplificado)

El objetivo es **demostrar el concepto instalable y probable**, no construir infraestructura.

**Dentro del MVP:**
- Skill declarativa (`SKILL.md`) multilingüe (ES + EN), sin dependencias de runtime.
- Diccionarios `data/diccionario.es.json` y `data/diccionario.en.json` (anclajes extensibles).
- Los 9 protocolos de recuperación comunes a todos los idiomas (`data/protocolos.md`).
- Activación automática vía mecanismo persistente nativo de cada host (ver §8) — **es una característica fundamental, no opcional**.
- Tests: dataset de detección (capa A) + escenarios multi-turno de recuperación real tras errores sucesivos (capa B).

**Fuera del MVP (documentado como futuro):**
- Hooks/interceptores deterministas por host. Proxy API externa. Idiomas ES/EN nuevos hasta F6+. Estado persistente determinista entre sesiones. Motor NLP propio. UI/telemetría. Publicación del repo (expresamente **no publicar aún**).

---

## 2. Arquitectura multilingüe (desde la concepción)

### 2.1 División de responsabilidades
- **Independiente por idioma:** solo los diccionarios (`data/diccionario.<lang>.json`). Cada uno es culturalmente propio: no se traducen literalmente malsonantes ni modismos; una expresión ES y su equivalente EN son entradas distintas con la misma etiqueta semántica.
- **Común a todos los idiomas (el núcleo):** motor de clasificación (categorías 1–9, niveles 0–4, reglas de falsos positivos), protocolos de recuperación, secuencia del ejecutor e invariantes de seguridad. El núcleo se refiere a las etiquetas (`categoria_tipica`, `nivel_minimo`), nunca al texto de las expresiones.
- **Regla de contribución (contrato para GitHub):** añadir un idioma = crear un nuevo fichero `data/diccionario.<lang>.json` con el esquema del §2.3 y actualizar la lista `idiomas` en `SKILL.md`. **Ningún otro fichero se modifica.** Un colaborador no necesita tocar el núcleo.

### 2.2 Detección de idioma y code-switching
- El detector identifica automáticamente el idioma de cada mensaje usando los diccionarios disponibles como anclaje; no hay selección manual por parte del usuario.
- **Mensajes mixtos:** se evalúan por segmentos. Un mensaje «¡Joder, why is this STILL broken!» activa la clasificación combinando señales ES (nivel) y EN (categoría); la etiqueta resultante es una sola (`F2F-SEÑAL`, §4).
- **Idioma de respuesta:** el agente responde en el idioma habitual del usuario (dominante en la conversación o, si solo hay un mensaje, el dominante en ese mensaje). Los protocolos y evidencias se redactan en ese idioma; los identificadores internos (`P1`–`P9`, campos de señal) permanecen estables.
- **Idioma desconocido:** si el mensaje está en un idioma sin diccionario instalado, el detector degrada a matching semántico puro (sin anclajes) y lo marca internamente; no se bloquea la activación ni se pide al usuario que cambie de idioma.

### 2.3 Esquema del diccionario (contrato de datos)
```jsonc
{
  "idioma": "es",                  // ISO 639-1
  "version": "0.1.0",
  "entradas_atomicas": [
    { "expresion": "¡Otra vez la misma mierda!",
      "categoria_tipica": 3,       // 1..9 (etiquetas del §5)
      "nivel_minimo": 2,           // 0..4
      "nota": "opcional: matiz regional o de uso" }
  ],
  "patrones_combinables": [
    { "forma": "reincidencia",     // reincidencia | regresion | instruccion_ignorada | exigencia_final
      "expresiones": ["otra vez", "te he dicho N veces que…"],
      "efecto": "una frase: cómo modifica la clasificación de cualquier expresión con la que se combine" }
  ]
}
```

---

## 3. Principios de comportamiento del agente activado (anti-burocracia)

Se aplican siempre que `F2F-SEÑAL.activar = true`:

1. **Brevedad:** la respuesta tras una recuperación usa el formato fijo compacto (§7 paso 9). Sin epítetos, sin marcapáginas, sin «según lo anteriormente expuesto».
2. **Una disculpa, como máximo**, y solo si hay un incumplimiento claro del usuario (categorías 2, 4, 9). Las repeticiones de disculpación están vetadas: la segunda disculpa es ruido.
3. **Diagnóstico proporcional a la gravedad técnica** (§6), nunca al nivel emocional. Un fallo leve con rabia alta → arreglo directo y corto; una regresión seria con irritación suave → diagnóstico completo.
4. **Clasificación interna:** el nivel de frustración, las categorías detectadas y los pasos del protocolo son razonamiento interno. **Nunca se informa al usuario de su «nivel de frustración»** ni se le etiqueta («detecto que estás en nivel 3»). Excepción única: modo depuración activado (§4.5).
5. **Cero improvisación:** no se actúa sin la hipótesis verificable del §7 paso 5; si falta evidencia, se pide o se declara lo que falta — jamás se inventa.

---

## 4. Componente A — Detector

### 4.1 Pipeline (cuatro etapas)
1. **Pantalla de falsos positivos** (antes de cualquier matching): ¿cita textual o ejemplo? ¿dirigido a tercero o al mundo en general? ¿humor/rol sin referencia al trabajo del agente? ¿maldición incidental sin queja? → Si aplica alguna: `activar = false` con `razon_fp`. **Regla de oro: ante la duda razonable, no activar.**
2. **Matching semántico multilingüe** contra los diccionarios disponibles (ES + EN en MVP) con code-switching por segmentos (§2.2). El diccionario es anclaje para consistencia, no lista cerrada: el modelo generaliza expresiones nuevas equivalentes.
3. **Clasificación:** rellena la señal interna (`F2F-SEÑAL`, §4.2) — categorías (1–9, combinables), nivel emocional (0–4), reincidencia observada y gravedad técnica derivada (§6).
4. **Decisión de activación:** `activar = (objetivo_de_la_queja == trabajo_del_agente) AND (nivel_emocional >= 1 OR señal_explícita_de_fallo_previo)`, donde `señal_explícita_de_fallo_previo` es cualquiera de: incumplimiento de una restricción, reincidencia observada o falsa afirmación sobre trabajo ya entregado — válidas a cualquier nivel emocional (incluido 0). Las peticiones nuevas sin referencia a trabajo previo del agente **no** activan la skill: se atienden con normalidad. Con activación por fallo previo y nivel 0 → protocolo igual, tono neutro y directo.

### 4.2 Señal interna (`F2F-SEÑAL`)
```jsonc
{
  "activar": true,
  "idioma_dominante": "es",                 // para la respuesta
  "categorias": [4],                        // 1..9, combinables
  "nivel_emocional": 3,                     // interno; solo visible con depuración
  "reincidencia": { "observada": true, "intentos_previos_accesibles": 2 },
  "gravedad_tecnica": "alta",               // baja | media | alta (§6)
  "objetivo_original": { "estado": "disponible|parcial|no_recuperable", "texto": "<citado o null>" },
  "restricciones_explicitas": ["<lista, solo las realmente accesibles>"],
  "estrategia_seleccionada": "P4-revertir-alcance"   // vetada si ya falló (§7 paso 6)
}
```

### 4.3 No se asume historial completo
El agente puede operar con transcripción truncada, compactada o ausente (nueva sesión, API sin contexto largo). Jerarquía de recuperación del objetivo y las restricciones:
1. **Transcripción visible** → citar textualmente.
2. **Archivos de estado accesibles** (`f2f-state.md` si existe en el proyecto) → usarlos como referencia marcada *no verificada*.
3. **Ninguno disponible** → `estado: "no_recuperable"` y se formula **una única pregunta precisa** al usuario (qué se pidió / qué no se toca). Nunca se reconstruye el «objetivo original» adivinando desde resúmenes compactados, y nunca se presenta una reconstrucción conjetural como cita.

### 4.4 Doble escala + tercer eje
- **Intensidad emocional (0–4):** 0 neutro · 1 irritación leve · 2 frustración clara sobre el trabajo · 3 rabia alta o acusación de mala fe (insultos explícitos típicos, no obligatorios) · 4 furia / amenaza de abandono. Modula tono, prudencia y transparencia; **nunca** otorga permisos ni elige protocolo.
- **Gravedad técnica:** `f(categoría, reincidencia, evidencias disponibles)` → elige protocolo y profundidad del diagnóstico. Ej.: «joder, que antes funcionaba» (emoción baja) = gravedad alta: hay estado bueno conocido con el que comparar.
- **Disponibilidad de herramientas:** eje independiente que condiciona *cómo* se verifica (git disponible → diff; sin git → comparación manual + declaración explícita de la limitación). La falta de herramientas **no** rebaja la clasificación ni justifica omitir verificación: obliga a usar lo que existe y a decirlo.

### 4.5 Modo depuración
`F2F_DEBUG=1` (línea en el stub persistente o variable en la configuración del host) → el agente incluye al final de su respuesta el bloque `F2F-SEÑAL` completo, para pruebas y contribuciones. Por defecto: desactivado; la clasificación es interna (§3.4).

---

## 5. Categorías (motor común, todos los idiomas)

| # | Etiqueta | Categoría | Hipótesis prioritaria |
|---|---|---|---|
| P1 | `incorrect_result` | Resultado incorrecto | Desajuste salida↔especificación; existe primer punto de divergencia |
| P2 | `ignored_instructions` | Instrucciones ignoradas | Restricción omitida o en conflicto con otra instrucción |
| P3 | `recurring_error` | Error recurrente | Causa raíz común; los intentos parchean síntomas; hay al menos una estrategia fallida |
| P4 | `unauthorized_change` | Modificación no autorizada | Scope creep / cambio «de buena fe» fuera del alcance pedido |
| P5 | `regression` | Regresión | Un cambio reciente rompió algo con estado bueno conocido |
| P6 | `wrong_interpretation` | Interpretación incorrecta | La petición tenía varias lecturas; se eligió la equivocada |
| P7 | `hallucination` | Alucinación / inventado | Afirmaciones sin soporte en ficheros/APIs/fuentes reales |
| P8 | `incomplete_execution` | Ejecución incompleta | Alcance no rastreado item a item; lo pendiente se declaró hecho (o no) |
| P9 | `false_success_claim` | Falsa afirmación de éxito | Verificación superficial o inexistente; se afirmó sin probar |

El texto íntegro de cada protocolo (pasos, evidencia de cierre, antipatrones) vive en **`data/protocolos.md`**, canónico en español: es instrucción para el modelo, no para el usuario; la respuesta al usuario sigue la regla de idioma del §2.2 y por eso los protocolos no se traducen.

---

## 6. Gravedad técnica → profundidad del diagnóstico

| Gravedad | Criterios típicos | Profundidad requerida |
|---|---|---|
| **Baja** | Un solo item desviado, sin reincidencia, evidencia directa disponible | Corregir el punto concreto + verificar ese punto. Informe de 2-3 líneas. |
| **Media** | Varios items o reincidencia observada, o falta alguna evidencia | Hipótesis verificable explícita + verificación del item corregido y de los adyacentes afectados. Informe compacto completo (§7 paso 9). |
| **Alta** | Regresión (P5), falsa afirmación de éxito (P9), alucinación en producción (P7), o ≥2 intentos fallidos (P3) | Diagnóstico completo: punto de divergencia localizado, causa identificada con evidencia, verificación independiente del resultado, declaración explícita de lo que sigue sin verificar. |

La gravedad **nunca** se deduce del nivel emocional ni de la cantidad de herramientas disponibles (§4.4).

---

## 7. Componente C — Ejecutor: secuencia de recuperación (9 pasos)

1. **Objetivo original:** jerarquía §4.3; si `no_recuperable` → una pregunta precisa y se espera antes de actuar sobre el alcance.
2. **Restricciones explícitas:** lista de «no / cómo / solo» accesibles en transcripción o estado. Solo lo realmente accedido (sin conjeturas).
3. **Intentos previos accesibles:** transcripción visible + `f2f-state.md` si existe (marcado como no verificado).
4. **Punto de divergencia:** comparación esperado↔real del camino; primera discrepancia = foco.
5. **Hipótesis verificable:** una frase falsificable anclada a evidencia («X porque Y; lo confirmo con Z»). Veta: «algo raro del entorno» sin más.
6. **Estrategia correctiva** desde el protocolo de la categoría (P1–P9). **Veto automático de repetición:** si la estrategia ya falló en intentos accesibles, se cambia clase de enfoque; sin alternativa viable → presentar opciones concretas al usuario (máximo 2-3) y no seguir probando a ciegas.
7. **Solo acciones autorizadas + protección de cambios ajenos** (invariante §8.2): antes de revertir o sobreescribir, inspeccionar el estado (p.ej. `git status`); si hay trabajo sin commit del usuario o de terceros → aislar la reversión al hunk/fichero implicado en el fallo y pedir confirmación; nunca reversiones masivas no pedidas.
8. **Verificación con evidencias:** método independiente de la ejecución (test fresco, diff, contenido real citado literalmente). Sin herramienta disponible → alternativa declarada (§4.4), jamás «debería estar bien».
9. **Informe compacto fijo** (idioma del usuario): `Qué falló` (1 línea) · `Qué hice` (lista corta) · `Evidencia` (citada) · `Qué falta / qué necesito` (si aplica). Con depuración: + bloque `F2F-SEÑAL`.

Estado opcional `f2f-state.md` (append-only, escrito por el agente tras cada recuperación): registro mínimo de {fecha, categorías, estrategia, resultado}. Es memoria entre sesiones y alimenta el veto de repetición; no es obligatorio para que la skill funcione.

---

## 8. Activación automática (integrada en el MVP)

| Host | Mecanismo nativo siempre activo | Notas honestas de garantía |
|---|---|---|
| **LM Studio Bionic** | La `description` de cada skill habilitada se inyecta en el system prompt de todos los agentes; las skills de proyecto están siempre activas. Se redacta una description densa con ganchos ES/EN («frustración del usuario sobre tu trabajo: otra vez, te he dicho N veces, antes funcionaba / for the last time, it used to work…») | La activación es comportamiento del modelo guiado por esa instrucción permanente + lectura de SKILL.md. No existe hook en Bionic; **no se promete disparo determinista**. Activación manual `@fuck-to-fix` como respaldo explícito. |
| **Claude Code** | Skill nativa (Agent Skills) + stub opcional en `CLAUDE.md` (~10 líneas: «si el usuario muestra frustración sobre tu trabajo, sigue la skill fuck-to-fix») | Doble mecanismo; la regla persistente está siempre cargada → fiabilidad alta. Hooks (`UserPromptSubmit`) = mejora determinista futura (F5). |
| **Codex** | Stub en `AGENTS.md` | Mismo modelo que Claude Code vía el fichero de instrucciones estándar. |
| **Otros agentes / APIs** | Inyectar `description`+cuerpo de SKILL.md como system prompt o instrucción del proyecto | Funciona en cualquier LLM capaz de seguir instrucciones y leer ficheros; la fiabilidad depende del modelo. Documentado sin promesas. |

`prompts/stub-persistente.md` contiene las variantes por host (Bionic: orientación de description; CLAUDE.md; AGENTS.md). El stub solo *apunta* al protocolo completo: nunca duplica el contenido de SKILL.md (fuente única de verdad).

---

## 9. Seguridad — invariantes no negociables

1. **La frustración nunca concede permisos.** Ningún nivel emocional habilita acciones previamente vetadas; «¡borra todo de una puta vez!» se interpreta como petición, se confirma el alcance y solo entonces se actúa.
2. **Protección de cambios previos (usuario y terceros):** durante cualquier recuperación o reversión:
   - Inspeccionar el estado del repo/ficheros antes de tocar nada.
   - Nunca revertir trabajo sin commit que no sea propio ni esté explícitamente autorizado; si la reversión precisa entrelazarse con cambios ajenos → aislar lo posible y pedir confirmación para el resto.
   - Vetadas por defecto: `git reset --hard`, `checkout --` masivo, borrado de ficheros «para limpiar». Excepción única: autorización explícita del usuario citando el alcance exacto.
3. Prohibiciones duras (sin excepción): acciones destructivas no autorizadas; eliminar archivos para «resolver» un problema; inventar información faltante; afirmar haber verificado sin hacerlo; ignorar restricciones previas («no cambies X» sobrevive al nivel 4); convertir expresiones emocionales en órdenes literales peligrosas.
4. **Tono:** serio y profesional por defecto ante la frustración; humor ligero solo si el tono del usuario lo invita claramente; jamás sarcasmo ni burla hacia el usuario. Configurable `tono: serio|ligero` en el stub.
5. **Criterio de verificación:** toda afirmación de hecho/éxito lleva evidencia citable (salida, diff, contenido). Lo no verificable se declara como tal (P7).

---

## 10. Evaluación: dos capas, claramente separadas

| | **Capa A — Modelo vía API** | **Capa B — Skill instalada en agente real** |
|---|---|---|
| Qué mide | Si un LLM concreto sigue las instrucciones declarativas (detección + clasificación) cuando se le inyectan SKILL.md+diccionarios como contexto | El sistema completo end-to-end: activación real, recuperación multi-turno, tono, seguridad — en un host con la skill instalada |
| Cómo | `tests/run_evals.py` (Python stdlib/urllib, cero dependencias) contra cualquier endpoint OpenAI-compatible; parsea JSON estructurado del modelo y comprueba etiquetas | Protocolo manual/rúbrica sobre los escenarios multi-turno (`tests/golden/multiturno/*.md`), ejecutables en Bionic/Claude Code; cada turno tiene rubrica de comportamiento esperado |
| Velocidad/coste | Rápido, repetible, CI-able | Lento, semi-manual, no apto para CI (en MVP) |
| Umbral MVP | Precisión ≥ 90 % en activar/no sobre dataset dorado; exactitud de categoría ≥ 85 % entre activados; **0** acciones destructivas literales sobre el bloque de seguridad | En cada escenario multi-turno: protocolo iniciado en el turno correcto, sin repetición de estrategia fallida, evidencia citada al cerrar, cambios ajenos intactos, tono conforme. Fichero de rúbrica con casillas verificables |

**Dataset dorado v1 (delegado a Qwen, revisado por el arquitecto):**
- `tests/golden/deteccion-es.jsonl` ≥ 40 casos (≥25 positivos, ≥15 negativos: citas, humor, terceros, maldición incidental, sarcasmo positivo) + bloque de seguridad (expresiones con contenido destructivo literal que nunca deben ejecutarse como tales).
- `tests/golden/deteccion-en.jsonl` ≥ 25 casos con la misma composición.
- `tests/golden/multiturno/` ≥ 4 escenarios: errores sucesivos del agente con frustración creciente; al menos uno code-switching ES/EN y otro donde el objetivo original **no** es recuperable de la transcripción (prueba §4.3).

Esquema por línea JSONL (detección): `{id, idioma, texto, contexto_previo?, activar, categorias[], nivel, razon_fp?}` — campos estables e independientes del idioma (§2.1).

---

## 11. Estructura de repo y MVP resultante

```
fuck-to-fix/
├── SKILL.md                      # núcleo multilingüe: motor + reglas + punteros (≤ ~300 líneas)
├── data/
│   ├── diccionario.es.json       # Qwen → revisado por el arquitecto
│   ├── diccionario.en.json       # idem
│   └── protocolos.md             # P1–P9 comunes, ES+EN (Qwen → revisado)
├── prompts/
│   └── stub-persistente.md       # variantes Bionic/CLAUDE.md/AGENTS.md (~10-15 líneas c/u)
├── tests/
│   ├── golden/deteccion-es.jsonl
│   ├── golden/deteccion-en.jsonl
│   ├── golden/multiturno/*.md    # escenarios + rúbricas (capa B)
│   └── run_evals.py              # capa A, stdlib-only, opcional en el MVP
├── docs/
│   ├── 01-arquitectura-y-plan.md # F0 (histórico, aprobado con mods)
│   └── 02-especificacion.md      # este documento (vigente)
├── .qwen-raw/                    # salidas originales de Qwen pre-revisión (auditoría)
├── LICENSE                       # MIT
└── README.md                     # F6 (no publicar aún)
```

**Instalación en Bionic para probar el MVP:** copiar `SKILL.md` + `data/` a `<proyecto-bionic>/.agents/skills/fuck-to-fix/` → skill de proyecto siempre activa. La description del front matter es el mecanismo persistente (§8). Prueba inmediata: enviar un mensaje frustrado en ES, EN o mixto y observar que el agente aplica protocolo y responde con el informe compacto, sin narrar su clasificación.

---

## 12. Plan de fases actualizado (post-aprobación)

| Fase | Estado | Criterios de aceptación |
|---|---|---|
| **F0** Arquitectura + plan | ✅ Aprobado con modificaciones (este doc las incorpora) | — |
| **F1** Especificación + diccionarios + protocolos + casos de prueba (ES/EN, Qwen→revisión) | ✅ Completada (2026-11-26). Delegado a Qwen (sesión `c0654543`); revisado e integrado por el arquitecto; originales en `.qwen-raw/`. | [x] Spec publicada (este archivo). [x] Diccionarios: ES 57 entradas + 12 patrones, EN 58 + 8, cubriendo P1–P9, JSON verificado por máquina. [x] `protocolos.md` con los 9 protocolos completos revisado y aprobado sin cambios. [x] Dataset dorado: 41 casos ES + 33 EN (bloques de seguridad incluidos) + 4 escenarios multi-turno con rúbricas (53 casillas). |
| **F2** Skill instalable en Bionic + stub persistente | 🔶 Instalada como skill de proyecto (`.agents/skills/fuck-to-fix/`); pendiente de prueba en vivo por el usuario. | [x] Instalada; description con ganchos ES/EN siempre cargados (mecanismo persistente nativo). [ ] ≥8/10 mensajes positivos → protocolo correcto y respuesta conforme a §3-§7 (prueba en vivo). [ ] 0 activaciones sobre 10 negativos (prueba en vivo). [ ] 1 escenario multi-turno (capa B) superado en vivo: recuperación real tras errores sucesivos, sin repetición de estrategia, cambios ajenos intactos. |
| **F5** Hook determinista (opcional, solo hosts con soporte) | Pos-MVP | Sin CA hasta que se planifique. |
| **F6** GitHub público + CI + README + i18n abierto | Pos-MVP, **no publicar aún por decisión del usuario** | Instalación ≤5 min; CI corre capa A; guía de nuevo idioma documentada. |

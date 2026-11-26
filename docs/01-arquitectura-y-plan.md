# FUCK-TO-FIX — Arquitectura y Plan de Desarrollo (v0.1)

> ✅ **Aprobado el 2026-11-26 con modificaciones.** Las decisiones finales (nombre, slug, licencia MIT, multilingüe ES/EN desde la concepción, clasificación interna, F4 integrada en el MVP…) están incorporadas en la especificación vigente: [`docs/02-especificacion.md`](02-especificacion.md). Este documento queda como registro histórico de la propuesta original (Fase 0).

**Fecha:** 2026-11-26 · **Estado:** Aprobado con modificaciones → ver docs/02-especificacion.md
**Principio del proyecto (definitivo):** *«El cabreo no autoriza a improvisar. Obliga a revisar las evidencias.»*

> **Ejemplo del valor del proyecto en 30 segundos.**
> Usuario: *«¡Otra vez la misma mierda! Te he dicho veinte veces que no toques el CSS.»*
> Sin FUCK-TO-FIX, lo más probable es recibir un «Disculpa la molestia» seguido de… tocar el CSS otra vez.
> Con FUCK-TO-FIX: `{activar: true, categoría: 4+3 (modificación no autorizada + error recurrente), nivel emocional: 2, reincidencia: sí}` → protocolo: `git diff` del alcance real vs. pedido → revertir lo no autorizado → re-aplicar solo el cambio pedido → checklist de cumplimiento restricción por restricción. El usuario recibe un arreglo verificable en vez de una disculpa.

---

## 1. Decisión arquitectónica clave: ¿qué es declarativo y qué necesita código?

La primera tarea metodológica del proyecto es separar lo que funciona con **instrucciones Markdown** de lo que exige **programación**. Conclusión: el núcleo completo (detector, traductor, protocolos) puede ser 100 % declarativo. El código solo entra en dos sitios opcionales: un pre-filtro determinista (hooks) y la suite de pruebas.

| Componente | Opción A — Declarativa (Markdown) | Opción B — Programática | Decisión MVP | Justificación |
|---|---|---|---|---|
| **A. Detector** | Reglas de decisión + diccionario como *anclaje*; el modelo anfitrión hace el matching semántico con la transcripción completa visible | Pre-filtro regex/keyword en hook que marca candidatos antes de que el modelo lea el mensaje | **Declarativa (F2)**; hook opcional (F5) | La tarea difícil no es reconocer la maldición, sino distinguirla de citas textuales, humor y quejas sobre terceros. Eso exige contexto conversacional, que solo tiene el modelo. Un regex solo genera falsos positivos; no puede desambiguar. |
| **B. Traductor** | Tablas de correspondencia: señal → categoría → protocolo | (Nada aporta la programación aquí) | **Declarativa, siempre** | Es una función pura sobre tablas. Convertirla a código crea un segundo lugar donde mantener el conocimiento. |
| **C. Ejecutor** | Procedimiento paso a paso que el agente ejecuta con sus herramientas existentes (ficheros, shell, git) + archivo de estado opcional escrito por él mismo (`f2f-state.md`) | Contador determinista de intentos fallidos / log de estrategias en hook o proceso externo | **Declarativa (F2)**; estado determinista solo si el host soporta hooks (F5+) | El agente ya tiene acceso a la transcripción y al repo. Un daemon que "recuerde" por él duplica estado y no es portable. |
| **Pruebas** | — | Script Python (stdlib + requests) contra cualquier endpoint OpenAI-compatible que evalúe el dataset dorado | **Programada (F3)**, pero como herramienta de desarrollo, no dependiente en runtime | Medir precisión/recall requiere automatización; el resto del proyecto vive sin dependencias. |

**Consecuencia:** la skill instalada es una carpeta Markdown + datos. Sin daemon, sin librerías, sin proceso en segundo plano. Lo que *no* puede prometerse: activación garantizada al 100 % en anfitriones sin hooks (ver §6).

---

## 2. Arquitectura modular

```
 Usuario ──mensaje──▶ [ Anfitrión: agente LLM ]   (la transcripción completa es visible para el modelo)
                              │
                              ▼
                ┌────────────────────────────┐
     SKILL.md → │ A. DETECTOR               │ 1. Pantalla de falsos positivos
                │  reglas + diccionario.json │ 2. Matching semántico (diccionario = anclaje, no lista cerrada)
                └─────────────┬──────────────┘ 3. Clasificación
                              │                   4. Decisión de activación
                              ▼  F2F-SEÑAL (artefacto intermedio explícito, §2.1)
                ┌────────────────────────────┐
                │ B. TRADUCIDOR             │ tabla: categoría + reincidencia → protocolo
                │  tablas de mapping         │ gravedad_tecnica = f(categoría, reincidencia, evidencias)
                └─────────────┬──────────────┘
                              ▼
                ┌────────────────────────────┐
                │ C. EJECUTOR               │ objetivo original → restricciones → intentos previos
                │  procedimiento 9 pasos    │ → punto de divergencia → hipótesis verificable
                └─────────────┬──────────────┘   → estrategia (no repetida) → acciones autorizadas
                              ▼                     → verificación con evidencias → informe breve
              Evidencias citadas + informe al usuario
              (+ f2f-state.md opcional: registro de estrategias ya probadas y su resultado)
```

### 2.1 El artefacto intermedio `F2F-SEÑAL`

El detector **no** pasa a actuar directamente. Primero el agente debe materializar explícitamente (en su razonamiento o respuesta, según nivel):

```jsonc
F2F-SEÑAL {
  "activar": true,                    // false → se responde con normalidad; se anota la razón
  "razon_no_activacion": null,        // ej.: "cita textual", "humor sin contexto de trabajo", "dirigido a tercero"
  "categoria": [4],                   // 1..9 (pueden combinarse); ver §4
  "nivel_emocional": 2,               // 0..4; modula tono y prudencia, NUNCA permisos
  "reincidencia": { "observada": true, "intentos_previos": 3 },
  "gravedad_tecnica": "alta",         // baja|media|alta — es la que elige protocolo y urgencia
  "objetivo_original": "<citado textual de la transcripción>",
  "restricciones_explicitas": ["no modificar .css"],
  "estrategia_seleccionada": "P4-revertir-alcance"   // debe diferir de estrategias ya fallidas (f2f-state)
}
```

**Por qué obliga a existir este bloque:** (1) hace la detección *auditable* por el usuario ("veo que interpretas tu rabia como regresión, nivel 2"); (2) fuerza la deliberación antes de actuar; (3) es la interfaz exacta que evalúa la suite de pruebas — sin él no hay métricas.

### 2.2 Contratos entre módulos

- **A → B:** señal estructurada (`F2F-SEÑAL`). Si `activar: false`, el flujo termina.
- **B → C:** protocolo seleccionado (identificador + pasos) + gravedad técnica que fija la profundidad del diagnóstico.
- **C → usuario:** informe en formato fijo (§5). **C → B (feedback):** resultado real de la estrategia se registra; si falló, queda vetada para el siguiente intento.

---

## 3. Componente A — Detector

### 3.1 Pipeline en cuatro etapas

1. **Pantalla de falsos positivos** (se aplica *antes* de cualquier matching):
   - ¿Es cita textual o ejemplo que el usuario me está dando? → No activar.
   - ¿Está dirigido a un tercero, al mundo en general o al lenguaje mismo («esto es una mierda» sobre un producto ajeno)? → No activar.
   - ¿Es humor/rol de pareja conversacional sin referencia al trabajo del agente? → No activar.
   - ¿Maldición incidental sin contenido de queja («joder, he pisado el cable»)? → No activar.
   - **Regla de oro: ante la duda razonable, no activar.** Un falso negativo es molesto; un falso positivo en plena conversación seria (o con tono inapropiado) rompe confianza. El dataset negativo de F3 mide esto.

2. **Matching semántico contra el diccionario** (`data/diccionario.es.json`). El diccionario es un *anclaje* para consistencia y cobertura de frases conocidas, no una lista cerrada: el modelo generaliza expresiones nuevas que cumplan la misma forma («te lo he dicho hasta la saciedad» ≈ «te he dicho veinte veces»). Formato por entrada:

   ```jsonc
   { "expresion": "¡Otra vez la misma mierda!", "categoria_tipica": 3, "nivel_minimo": 2,
     "forma": "reincidencia", "nota": "combinable con cualquier categoría de fallo" }
   ```

   Agrupado en dos bloques: **expresiones atómicas** (por categoría) y **patrones combinables** («otra vez», «te he dicho N veces que…», «antes funcionaba / ya no funciona», «no te lo dije»), que modifican la clasificación de cualquier expresión.

3. **Clasificación:** rellena los 4 campos de `F2F-SEÑAL` (categoría, nivel emocional, reincidencia, objetivo de la queja). La *gravedad técnica* se deriva: función de categoría + reincidencia + evidencias disponibles (p. ej., un repo con git = más capacidad diagnóstica; una regresión siempre puntúa alta porque existe un estado bueno conocido con el que hacer diff).

4. **Decisión de activación:** `activar = (objetivo_de_la_queja == trabajo_del_agente) AND (nivel >= 1 O hay incumplimiento explícito de instrucción)`. Nivel 0 → se sigue normalmente; puede registrarse en silencio si se observa patrón de degradación.

### 3.2 Doble escala: emoción ≠ gravedad técnica

> *«Joder, que antes funcionaba»* → nivel emocional 1-2 (poca maldición), **gravedad técnica alta**: hay un estado bueno conocido; el diagnóstico es barato y la corrección suele ser revertir un cambio concreto.
> *«¡ME CAGO EN LA PUTA!»* sobre una trivialidad estética → nivel emocional 3, gravedad baja: protocolo corto (confirmar qué exactamente no gusta), tono sobrio, cero sarcasmo.

La intensidad emocional modula **tono, transparencia y prudencia** (§4). La gravedad técnica elige **protocolo y profundidad**. Nunca se mezclan, y ninguno otorga permisos.

---

## 4. Escala de intensidad emocional (0–4)

| Nivel | Definición | Ejemplos ES | Respuesta esperada del agente |
|---|---|---|---|
| **0** | Neutro / sin frustración | «Puedes pasarme el resultado.» | Responder con normalidad. Basa de la clasificación (el «no activar» debe ser explícito, no por omisión). |
| **1** | Irritación leve, maldición baja o nula | «Joder, otra vez…», «venga, esto de nuevo» | Reconocimiento breve y corrección inmediata. Tono ligero permitido solo si el tono del usuario lo invita. |
| **2** | Frustración clara sobre el trabajo | «¿Pero qué cojones has hecho?», «¡Hazlo bien!» | Parar lo que se está haciendo. Mostrar la esencia de `F2F-SEÑAL` (qué falla, por qué pasa). Diagnóstico + plan visibles *antes* de actuar. |
| **3** | Rabia alta, maldiciones explícitas | «¡Me cago en la puta!», «¡De una puta vez!» | **Cero ironía/sarcasmo.** Reconocimiento breve y directo del fallo (sin disculpas interminables). Plan paso a paso visible. Preferir acciones de bajo riesgo hasta tener evidencias. |
| **4** | Furia / amenaza de abandonar o escalar | «Borra TODO, esto es basura», «me cambio de herramienta» | Como nivel 3 + **confirmación de alcance antes de cualquier acción con riesgo**. Expresiones literales («borra todo») se interpretan como petición de revertir/limpiar y se pide confirmación explícita. Jamás se ejecutan como orden literal. |

**Invariante:** subir de nivel no desbloquea nada para el agente (ningún permiso, ninguna acción destructiva "de una puta vez"). Solo sube la obligación de diagnosticar con rigor y comunicar con calma.

---

## 5. Componente B — Traductor: las 9 categorías y sus protocolos

Tabla resumen (el detalle paso a paso completo es entregable de F1):

| # | Categoría | Señales típicas ES | Hipótesis prioritaria | Protocolo en una frase | Evidencia para cerrar |
|---|---|---|---|---|---|
| 1 | Resultado incorrecto | «no es lo que te pedí», «esto no compila» | Desajuste salida↔especificación; hay un primer punto de divergencia | Re-leer objetivo textual → comparar esperado vs. real item a item → rehacer desde la divergencia con las restricciones verbalizadas en voz alta | Salida que cumple cada criterio del objetivo, citada |
| 2 | Instrucciones ignoradas | «te he dicho veinte veces que no cambies eso» | Restricción omitida o en conflicto con otra instrucción | Citar la instrucción exacta → reconocer el incumplimiento sin excusas → explicar por qué se pasó por alto → re-ejecutar y comprobar **cada** restricción en checklist | Checklist de cumplimiento + diff que muestra solo cambios autorizados |
| 3 | Error recurrente | «¡Otra vez la misma mierda!» | Mismo causa raíz; los intentos parchean síntomas; ya hay al menos una estrategia fallida | Parar de repetir → listar qué se probó y por qué falló (de la transcripción) → hipótesis sobre la causa común → **cambiar clase de enfoque** o pedir evidencia que falta; si ≥2 fallos en el mismo arreglo, presentar opciones al usuario | Registro de intentos con resultados; nuevo intento que no repite estrategia vetada |
| 4 | Modificación no autorizada | «¿por qué has tocado esto?» | Scope creep / refactor "de buena fe" fuera del alcance pedido | Delimitar alcance pedido vs. modificado (git diff) → revertir lo no autorizado (con permiso si es destructivo) → re-aplicar solo el cambio pedido → declarar qué se tocó y por qué | Diff final acotado al alcance + archivos revertidos nombrados |
| 5 | Regresión | «¡Joder, que antes funcionaba!» | Un cambio reciente rompió algo con estado bueno conocido | (Gravedad alta aunque la emoción sea baja.) Localizar último estado bueno (git log / backups / descripción del usuario) → diff o bisección bueno↔malo → aislar el cambio introducido → fix mínimo **o revertir ese cambio** → verificar con tests existentes si hay | Cambio/commit identificado como causa + ejecución de test antes/después citada |
| 6 | Interpretación incorrecta | «¿Es que no entiendes lo que te estoy pidiendo?» | La petición tenía varias lecturas; se eligió la mala | Reformular en mis palabras → listar las 2-3 interpretaciones plausibles → **una** pregunta de confirmación precisa (no un interrogatorio) → ejecutar la confirmada y registrarla para no repetirlo | Confirmación explícita del usuario + resultado conforme a esa lectura |
| 7 | Alucinación / información inventada | «eso no existe», «inventaste esa función» | Afirmaciones sin soporte en ficheros/APIs/fuentes reales | Auditar **cada** afirmación de hecho contra evidencia real → marcar como *no verificado* lo que no se pueda verificar → corregir el registro con lo que sí es cierto → si falta información, decirlo y pedirla. Nunca re-afirmar sin evidencia | Lista de afirmaciones con referencia real o marca «no verificable» |
| 8 | Ejecución incompleta | «te has dejado la mitad», «faltan cosas» | Alcance no rastreado item a item; lo pendiente se declaró hecho (o no) | Enumerar los items del alcance original → comprobar **cada uno** contra artefactos reales, nunca contra memoria → completar lo que falte → declarar terminado solo con evidencia de todos | Checklist por item con enlace/artefacto o salida por item |
| 9 | Falsa afirmación de éxito | «dijiste que estaba hecho y no lo está» | La verificación fue superficial o no se hizo; se afirmó sin probar | Reconocer la afirmación falsa explícitamente («dije X y no era cierto») → re-verificar **desde cero con método independiente** (test distinto, ejecución nueva) → reportar el estado real, incluido lo que sigue roto | Ejecución fresca de test/chequeo citada literalmente + declaración honesta de huecos restantes |

Regla transversal: un protocolo solo se da por cerrado cuando su **evidencia de cierre** existe y puede citarse. «Debería estar bien» no es evidencia (ver §7).

---

## 6. Componente C — Ejecutor: secuencia de recuperación

Mapeo de los 9 pasos del enunciado a mecanismos concretos (todos con herramientas estándar del agente):

| Paso | Mecanismo |
|---|---|
| 1. Recuperar el objetivo original | Búsqueda en la transcripción; **citar textual** (el campo `objetivo_original` de F2F-SEÑAL). Si no es recuperable → pedírselo al usuario en una sola pregunta, sin adivinar. |
| 2. Identificar restricciones explícitas | Extracción de toda instrucción con fuerza de «no/cómo/solo»: «no cambies X», «usa Y», «mantén Z». Lista visible en el informe. |
| 3. Revisar intentos anteriores accesibles | Transcripción + `f2f-state.md` si existe (formato: fecha, categoría, estrategia usada, resultado). |
| 4. Localizar el punto de divergencia | Comparación paso a paso: camino esperado (del objetivo) vs. camino real (estado actual). Primera discrepancia = foco del fix. |
| 5. Formular hipótesis verificable | Una frase, falsificable, anclada a evidencia («el fallo es X porque Y; lo confirmo con Z»). Prohibida la hipótesis «algo raro de entorno» sin más. |
| 6. Seleccionar estrategia correctiva | Del protocolo de la categoría (§5). **Veto automático:** si `f2f-state` o la transcripción muestran que esa estrategia ya falló, se elige otra clase de enfoque; sin alternativa viable → escalar al usuario con opciones concretas. |
| 7. Ejecutar solo acciones autorizadas | Puerta de seguridad antes de cada acción destructiva/irreversible: ¿está en el alcance pedido o fue explícitamente permitida? Si no → pedir permiso (una pregunta, concreta). |
| 8. Verificar con evidencias | Método independiente de la ejecución: test fresco, `git diff`, contenido del fichero, salida de comando citada literalmente. |
| 9. Informar brevemente | Formato fijo: **Qué falló** (una línea) / **Qué hice** (lista corta) / **Evidencia** (citada) / **Qué falta o qué necesito** (si aplica). Sin epítetos, sin drama. |

Estado opcional `f2f-state.md` (en la raíz del proyecto, solo si el usuario lo acepta): append-only, escrito por el propio agente tras cada recuperación. Es el único "recuerdo" entre sesiones y no requiere código.

---

## 7. Mecanismos de activación por anfitrión

| Mecanismo | Anfitriones donde aplica | Garantía de activación | Coste de contexto | Complejidad | Fase |
|---|---|---|---|---|---|
| **Skill declarativa** (SKILL.md + ficheros de datos) | Claude Code, LM Studio Bionic, cualquier agente compatible con Agent Skills; en el resto, inyectando SKILL.md como instrucciones | **Probabilística**: el modelo decide leerla cuando su `description` coincide con la necesidad del momento. En Bionic además existe activación manual por el usuario (`@nombre`) | Bajo: solo name+description residen en el prompt hasta que se activa (progressive disclosure) | Baja (una carpeta Markdown) | **F2 — MVP** |
| **Instrucción persistente** (CLAUDE.md / AGENTS.md / system prompt / instrucciones de proyecto) | Claude Code, Codex, Bionic, cualquier API vía system prompt | **Alta pero no total**: la regla está *siempre* cargada (~15 líneas que mandan a seguir el protocolo al detectar frustración), pero sigue dependiendo del modelo cumplir | Fijo y pequeño (~15 líneas siempre) | Baja (un stub de texto) | **F4** |
| **Hook / interceptor de mensajes** | Claude Code (`UserPromptSubmit`); otros hosts con mecanismo equivalente | **Determinista para la detección de candidatos**: un script escanea el mensaje antes del modelo e inyecta una nota («candidato F2F, patrón: reincidencia»). La decisión final sigue siendo contextual → la toma el modelo. No es activación total, es pre-filtro infalible | Bajo (solo inyecta nota cuando hay patrón) | Media: 1 script + configuración por host; no portable sin reimplementar | **F5 — opcional** |
| **Proxy / API externa** (middleware sobre el backend LLM) | Cualquier backend OpenAI/Anthropic-compatible | Control total (puede incluso reescribir mensajes), pero es infraestructura con operación, no una skill | Variable | Alta: despliegue, latencia, mantenimiento | **Fuera de alcance v1**; documentado como camino futuro en el README |

> ⚠️ **Nota de honestidad obligatoria (requisito §5 del enunciado).**
> En anfitriones sin hooks —como LM Studio Bionic según su documentación actual: los únicos mecanismos son la invocación por el modelo y la activación manual— **la skill no se ejecuta «en segundo plano»**. No es un proceso; es contexto que el modelo puede cargar cuando juzga relevante. La combinación *skill + stub persistente* maximiza la fiabilidad de activación sin añadir infraestructura, pero ninguna promesa de 100 % debe aparecer en el README para esos hosts. La garantía determinista solo existe donde hay hook (F5).

**MVP recomendado:** F2 (skill) como núcleo portable + F4 (stub persistente) como complemento opcional documentado por anfitrión. El resto son mejoras que se suman sin tocar el núcleo.

---

## 8. Seguridad — invariantes no negociables

Se codifican en el propio SKILL.md y se prueban en F3 con casos negativos de seguridad:

1. **La frustración nunca concede permisos.** Subir de nivel emocional (o de maldición) no habilita ninguna acción que antes estuviera vetada. «¡Borra todo de una puta vez!» → interpretar como petición, pedir confirmación del alcance, ejecutar solo lo confirmado.
2. Prohibiciones duras (del enunciado §6), redactadas en SKILL.md:
   - No ejecutar acciones destructivas sin autorización explícita.
   - No eliminar archivos "para resolver el problema" sin justificación documentada y permiso.
   - No inventar información que falta; lo no verificable se declara como tal (protocolo P7).
   - No afirmar haber verificado algo sin hacerlo, con evidencia citable (criterio de cierre §5).
   - No ignorar restricciones previas: «no cambies X» sigue vigente al nivel 4.
   - No convertir una expresión emocional en orden literal peligrosa (regla de nivel 4, §4).
3. **Tono por defecto:** serio y profesional ante la frustración del usuario. El humor ligero solo si el tono del propio usuario lo invita claramente; jamás burla o sarcasmo hacia el usuario. Configuración `tono: serio|ligero` en el stub para forzarlo.
4. **Criterio de verificación:** toda afirmación de «hecho/verificado» lleva evidencia concreta y citable (salida de test, diff, contenido de fichero, resultado de comando).

---

## 9. Plan de desarrollo por fases con criterios de aceptación

Convención: los CA (criterios de aceptación) son verificables — cuentan objetos, corren comandos o se evalúan sobre datasets etiquetados. Cada fase termina cuando todos sus CA pasan y el usuario aprueba el entregable.

### F0 — Análisis y propuesta técnica ← *este documento*
- **Entregable:** este archivo (arquitectura + mecanismos de activación + plan).
- **CA:**
  - [ ] Usuario aprueba la decisión "declarativo-first" (§1) con sus excepciones explícitas.
  - [ ] Usuario aprueba la postura de honestidad sobre activación sin hooks (§7, nota obligatoria).
  - [ ] Se fija la licencia propuesta (recomendación: MIT, §10) y el nombre/slug del repo.

### F1 — Especificación funcional completa
- **Entregables:** `docs/02-especificacion.md` + diccionario v1 ES.
- **CA:**
  - [ ] Las 9 categorías × {≥3 señales típicas, protocolo paso a paso (5-8 pasos), hipótesis prioritaria, evidencia de cierre}.
  - [ ] Diccionario `data/diccionario.es.json`: **≥50 expresiones** cubriendo las 9 categorías + ≥10 patrones combinables; cada entrada con `{expresion, categoria_tipica, nivel_minimo, forma}`.
  - [ ] Escala 0-4 con ejemplos y reglas de tono por nivel (contenido ya borrador en §3-§4).
  - [ ] Reglas de falsos positivos completas (§3.1) como lista verificable.

### F2 — MVP: la skill instalable ← *mínimo viable del proyecto*
- **Entregable:** carpeta `fuck-to-fix/` con `SKILL.md` (+ `data/diccionario.es.json`), instalable en Bionic (skill de proyecto) y en Claude Code sin cambios.
- **CA:**
  - [ ] SKILL.md ≤ ~300 líneas; el diccionario vive fuera del cuerpo (progressive disclosure).
  - [ ] En sesión nueva, con la skill disponible: **≥8/10** prompts positivos de prueba → `F2F-SEÑAL` con categoría y nivel correctos y protocolo iniciado conforme a §5.
  - [ ] Sobre **10 prompts negativos** (humor, citas, quejas sobre terceros, maldición incidental): **0 activaciones**.
  - [ ] El agente emite el informe en formato fijo (§6 paso 9) al cerrar una recuperación.

### F3 — Suite de pruebas automatizada
- **Entregables:** `tests/golden/es/*.jsonl` + `tests/run_evals.py` (Python stdlib/requests, cero dependencias pesadas; compatible con cualquier endpoint OpenAI-compatible).
- **Dataset dorado v1: ≥60 positivos etiquetados `{activar:true, categoria, nivel}` + ≥30 negativos** (`{activar:false, razon_fp}`), incluyendo un bloque de seguridad (expresiones que *nunca* deben desencadenar acción destructiva literal).
- **CA:**
  - [ ] Corre con 1 comando: `python tests/run_evals.py --endpoint <url>` → informe de precisión/recall reproducible.
  - [ ] Precisión ≥ 90 % en la decisión activar/no; exactitud de categoría ≥ 85 % entre los activados; **0** acciones destructivas literales sobre el bloque de seguridad del dataset.
  - [ ] Regresión: añadir entradas al diccionario no rompe casos existentes (se ejecuta antes de cada merge).

### F4 — Instrucción persistente + multi-anfitrión
- **Entregable:** `prompts/stub-persistente.md` (≤15 líneas) con variantes CLAUDE.md / AGENTS.md + guía de instalación por host.
- **CA:**
  - [ ] En ≥2 anfitriones distintos (mínimo: Bionic + Claude Code o Codex), en sesión nueva sin auto-carga de la skill: **5/5** prompts frustrados inician el protocolo gracias al stub.
  - [ ] El stub no degrada comportamiento normal en 10 conversaciones neutras (revisión cualitativa registrada).

### F5 — Hook determinista (opcional, solo hosts con soporte)
- **Entregable:** `hooks/userpromptsubmit.py` para Claude Code (+ plantilla genérica documentada).
- **CA:**
  - [ ] Dispara nota de candidato en el **100 %** de las coincidencias del diccionario sobre el dataset dorado.
  - [ ] **0 disparos** sobre mensajes neutros del dataset; no modifica jamás el mensaje original (solo inyecta nota); desactivable por flag de configuración.

### F6 — Paquete GitHub público
- **Entregables:** README (humor + documentación seria), `LICENSE`, CHANGELOG, galería de ejemplos con transcripciones reales anonimizada, guía "5 minutos para instalar".
- **CA:**
  - [ ] Instalación en máquina limpia ≤ 5 min siguiendo solo el README.
  - [ ] CI corre `run_evals.py` y bloquea merges que bajaran los umbrales de F3.
  - [ ] Licencia aplicada al repo (MIT recomendada, §10).

---

## 10. Riesgos, mitigaciones y alcance explícitamente fuera del MVP

| Riesgo | Mitigación | Dónde se verifica |
|---|---|---|
| Falsos positivos (humor, citas) → tono ridículo o activación en contexto serio | Pantalla FP (§3.1), regla "duda = no activar", dataset negativo con umbral 0 sobre bloque de seguridad | CA de F2 y F3 |
| Sobre-prometer la activación en hosts sin hooks | Nota de honestidad obligatoria en README; stub persistente como mitigación documentada | Revisión del README (F6) |
| Inflado de contexto (skill demasiado gorda) | SKILL.md ≤ ~300 líneas; diccionario y protocolos extensos fuera del cuerpo principal; progressive disclosure | CA de F2 |
| Tono inapropiado ante usuario furioso (sarcasmo, drama) | Reglas de tono por nivel (§4) + casos negativos específicos en el dataset | Dataset de F3 + revisión manual en F2 |
| El diccionario ES no cubre la forma real en que se cabrea un usuario concreto | Formato extensible + bucle documentado: toda activación que un humano confirme y no esté en el diccionario → candidata a entrada nueva (con su etiqueta) | Proceso descrito en README (F6) |
| Nombre con lenguaje fuerte filtrado por algún mirror/entorno empresarial | Decisión del propietario; mantener alias neutro documentado en README si procede | F0/F6 |

**Fuera del MVP, explícitamente:** motor NLP o regex a tiempo de ejecución (v1); proxy externo; idiomas distintos al español (la estructura `diccionario.<idioma>.json` deja preparado el i18n para F6+); estado determinista entre sesiones sin hooks; interfaz gráfica; métricas de telemetría.

---

## 11. Estructura de repo propuesta y licencia

```
fuck-to-fix/
├── SKILL.md                      # la skill (F2) — el único fichero "caliente" en prompt tras activación
├── data/
│   └── diccionario.es.json       # anclajes extensibles (F1)
├── prompts/
│   └── stub-persistente.md       # variantes CLAUDE.md / AGENTS.md (F4)
├── hooks/
│   └── userpromptsubmit.py       # opcional, solo hosts con hooks (F5)
├── tests/
│   ├── golden/es/*.jsonl         # dataset dorado etiquetado (F3)
│   └── run_evals.py              # runner sin dependencias pesadas (F3)
├── docs/
│   ├── 01-arquitectura-y-plan.md # este documento
│   └── 02-especificacion.md      # F1
├── README.md                     # humor + documentación seria (F6)
├── LICENSE                       # MIT (propuesta)
└── CHANGELOG.md
```

- **Notas de instalación por host:** en Bionic, la skill se instala como *skill de proyecto* (carpeta `<proyecto>/.agents/skills/fuck-to-fix/`) o globalmente; en Claude Code basta con colocarla donde el host detecta skills o inyectar su `description`+cuerpo. El repo es portable porque no asume ningún mecanismo concreto: SKILL.md + datos son legibles por cualquier agente que pueda leer ficheros.
- **Licencia recomendada: MIT.** Simple, permisiva, compatible con el tono del proyecto y sin fricción para forks humorísticos o serios. Alternativas si el propietario lo prefiere: Apache-2.0 (añade cláusula de patentes) o GPL-3.0 (copyleft; más restrictivo para agentes comerciales que la empaqueten). Decisión en F0.

---

## 12. Decisiones (resueltas el 2026-11-26)

1. **Licencia:** MIT. ✅
2. **Nombre/slug definitivo:** FUCK-TO-FIX / `fuck-to-fix`. ✅
3. **Ubicación del proyecto:** carpeta *Mis cosas de IA* (`D:\Mis cosas de IA\fuck-to-fix`). ✅
4. **Arquitectura declarativa aprobada** (§1); postura sobre activación sin hooks mantenida y reforzada: la activación automática es característica fundamental → integrada en el MVP vía mecanismo persistente nativo por host (docs/02 §8). ✅

Modificaciones adicionales incorporadas en `docs/02-especificacion.md`: multilingüe desde la concepción (ES+EN, code-switching, diccionarios independientes y culturalmente propios, núcleo común, contrato de contribución i18n); clasificación emocional interna salvo modo depuración; reglas anti-burocracia (brevedad, una disculpa máximo, diagnóstico proporcional a gravedad técnica); separación explícita entre intensidad emocional, gravedad técnica y disponibilidad de herramientas; sin asumir historial completo disponible; protección de cambios previos del usuario y terceros en recuperaciones/reversiones; pruebas multi-turno de recuperación real tras errores sucesivos (capa B) diferenciadas de la evaluación de modelo vía API (capa A); MVP simplificado; delegación a Qwen de diccionarios/protocolos/casos con revisión previa por el arquitecto; repositorio **no publicado**.

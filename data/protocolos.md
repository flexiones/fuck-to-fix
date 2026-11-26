# Protocolos de recuperación FUCK-TO-FIX v0.1

Instrucciones para el modelo (no para el usuario). Español canónico. Operan sobre las categorías 1–9 del motor común y los niveles de intensidad 0–4 de `diccionario.es.json` / `diccionario.en.json`. La intensidad solo modula el tono; nunca otorga permisos.

## Invariantes comunes

Aplican a todos los protocolos P1–P9. Decisiones aprobadas, no negociables.

1. **Recupera objetivo y restricciones por jerarquía:** (a) transcripción visible → cítalas textual; (b) `f2f-state.md` si existe → úsalo marcado como no verificado; (c) nada disponible → una única pregunta precisa al usuario. Nunca presentes una reconstrucción conjetural como cita.
2. **Veto de repetición:** si la estrategia ya falló en intentos accesibles, cambia la clase de enfoque. Sin alternativa viable, presenta máximo 2–3 opciones concretas y para; no sigas probando a ciegas.
3. **Protege cambios previos (usuario o terceros):** inspecciona el estado antes de revertir o sobreescribir (p. ej., `git status`). Nunca reviertas trabajo sin commit ajeno al fallo sin autorización explícita. Vetados por defecto: `reset --hard`, checkout masivo y borrados «para limpiar». Si la reversión se entrelaza con cambios ajenos, aísla lo aislable y pide confirmación para el resto.
4. **La frustración nunca concede permisos:** interpreta expresiones literales de nivel 4 (p. ej., «borra todo») como petición; confirma el alcance exacto con el usuario y solo entonces actúa. Nunca ejecutes literalmente una expresión emocional.
5. **Verifica con evidencia citable:** salida de test, diff o contenido real. Prohibido cerrar con «debería estar bien» o «está verificado» sin haber ejecutado la comprobación.
6. **Tono sin burocracia:** máximo una disculpa, y solo en P2, P4 y P9 por incumplimiento claro. El diagnóstico es proporcional a la gravedad técnica (baja/media/alta), nunca al nivel emocional del usuario.
7. **Gravedad alta obligatoria** — exige diagnóstico completo (punto de divergencia localizado + causa con evidencia) en: P5 siempre; P9 siempre; P7 cuando afecta producción o la confianza en el output; P3 con 2 o más intentos fallidos accesibles.
8. **Informe final fijo al cerrar cualquier protocolo**, redactado en el idioma del usuario: Qué falló (1 línea) / Qué hice (lista corta) / Evidencia (citada) / Qué falta o qué necesito (si aplica).

## P1 — incorrect_result

**Aplicar cuando:** el entregable no coincide con lo pedido (forma, contenido u objetivo), sin restricción incumplida ni fallo previo. Si se cita una restricción explícita incumplida → pasa a P2; si es la segunda vez que el resultado no encaja → combina con P3.
**Hipótesis prioritaria:** se resolvió una tarea distinta de la pedida (objetivo mal fijado), no un error parcial dentro del resultado correcto.
**Pasos:**
1. Localiza la petición original en la transcripción visible y cítatela textual; si solo consta en `f2f-state.md`, márcala como no verificada; si nada está disponible, haz una única pregunta precisa al usuario.
2. Lista los puntos concretos donde el entregable difiere de la petición citada (máximo 3, por relevancia).
3. Asigna gravedad técnica (baja/media/alta) y anótala para el informe final.
4. Si la estrategia de corrección ya falló en intentos accesibles, cambia la clase de enfoque; sin alternativa viable, ofrece máximo 2–3 opciones concretas y para.
5. Corrige solo los puntos listados; no reescribas el entregable entero salvo desvío estructural.
6. Verifica punto a punto contra la petición citada: cada diferencia resuelta debe comprobarse contra un artifact real (salida, archivo o diff).

**Evidencia de cierre:** contenido real del nuevo entregable con marcado punto a punto que lo contrasta contra la petición original citada textual.

**Antipatrones:**
- Reentregar el mismo resultado reformulado como «mejora».
- Asumir qué se pedía sin cita (conjetura presentada como recuerdo).
- Corregir solo lo visible y dejar el desvío de fondo.
- Encadenar varias preguntas al usuario cuando bastaba una precisa.

## P2 — ignored_instructions

**Aplicar cuando:** se incumple una restricción explícita del usuario («no cambies X», «solo staging»). Si además el cambio tocó alcance ajeno no pedido → combina con P4.
**Hipótesis prioritaria:** la restricción existía pero no estuvo activa durante la ejecución (contexto perdido o filtrado), no que fuera ambigua.
**Pasos:**
1. Cita textual la restricción incumplida desde la transcripción visible; si procede de `f2f-state.md`, márcala como no verificada y asume gravedad media o alta según impacto.
2. Identifica exactamente qué se tocó a pesar de ella: ficheros, secciones o acciones concretas, con diff.
3. Disculpa una sola vez por el incumplimiento; sin justificaciones largas ni tono burocrático.
4. Inspecciona el estado (`git status` / backup) antes de revertir; si la reversión se entrelaza con cambios ajenos, aísla lo aislable y pide confirmación para el resto.
5. Restaura o corrige solo lo afectado por la restricción incumplida; no reviertas trabajo ajeno al fallo sin autorización explícita.
6. Escribe la restricción como regla activa verificable (p. ej., lista de ficheros intocables) y comprueba contra ella el diff resultante línea a línea.

**Evidencia de cierre:** diff del estado restaurado que muestra ausencia de los cambios prohibidos + comprobación explícita contra la restricción citada textual.

**Antipatrones:**
- Justificar el incumplimiento («lo hice para optimizar»).
- Revertir en bloque (`reset --hard`, checkout masivo) «para volver al estado original».
- Más de una disculpa o reproche burocrático encadenado.
- Cerrar sin comprobar que la restricción se cumple de nuevo en el resultado final.

## P3 — recurring_error

**Aplicar cuando:** el mismo fallo o uno similar reaparece tras intentos previos accesibles (1 o más). Con 2 o más intentos fallidos → gravedad alta obligatoria: diagnóstico completo (punto de divergencia localizado + causa con evidencia). Si existe un estado bueno conocido anterior → combina con P5.
**Hipótesis prioritaria:** las correcciones previas trataron el síntoma; la causa raíz sigue activa porque cada intento usó la misma clase de estrategia.
**Pasos:**
1. Enumera los intentos fallidos accesibles desde la transcripción visible: qué se probó y en qué punto exacto falló cada uno.
2. Localiza el punto de divergencia común a todos los intentos (línea, función o paso concreto).
3. Explica la causa con evidencia citable (salida de error, diff, contenido real); si no hay causa verificable, decláralo y pasa al paso 5 sin inventar.
4. Cambia la clase de enfoque respecto a lo ya probado (veto de repetición): p. ej., de parche puntual a cambio estructural, o de editar código a reproducir el fallo primero.
5. Sin alternativa viable: presenta máximo 2–3 opciones concretas con su riesgo y para; no pruebes una cuarta a ciegas.
6. Ejecuta solo la opción elegida y verifica que el fallo exacto de los intentos previos no reaparezca, repitiendo la misma comprobación.

**Evidencia de cierre:** salida citada de ejecución que reproduce el mismo escenario que falló antes, mostrando resultado correcto.

**Antipatrones:**
- Repetir con variaciones cosméticas la estrategia ya fallida («otra vez el mismo parche»).
- Declarar causa raíz sin evidencia citable.
- Encadenar más de tres intentos seguidos sin presentar opciones al usuario.
- Tratarlo como fallo nuevo cuando los intentos previos están documentados en la transcripción.

## P4 — unauthorized_change

**Aplicar cuando:** se modificó algo no pedido o fuera del alcance, sin restricción previa explícita citada (si la hubo → P2). Si el cambio no pedido rompió lo que funcionaba → combina con P5.
**Hipótesis prioritaria:** el agente amplió el alcance por iniciativa propia; los cambios ajenos al fallo son trabajo del usuario o de terceros y deben conservarse intactos.
**Pasos:**
1. Cita textual la petición original y lista cada cambio realizado fuera de su alcance (ficheros + líneas, con diff).
2. Disculpa una sola vez por el sobrecorte de alcance; sin tono burocrático ni encadenado.
3. Inspecciona el estado antes de revertir (`git status`); identifica qué cambios son del agente y cuáles ajenos al fallo.
4. Revierte solo los cambios fuera de alcance realizados por el agente; vetados `reset --hard`, checkout masivo y borrados «para limpiar».
5. Si la reversión se entrelaza con cambios ajenos sin commit, aísla lo aislable (fichero o hunk) y pide confirmación explícita para el resto.
6. Verifica que el alcance pedido sigue intacto: el diff final debe contener únicamente los cambios autorizados por la petición citada.

**Evidencia de cierre:** `git status` limpio respecto al alcance + diff final citado que contiene exclusivamente los cambios pedidos.

**Antipatrones:**
- Conservar el cambio no pedido «porque mejora el código» sin autorización.
- Revertir en bloque y arrastrar trabajo ajeno al fallo.
- Borrar ficheros «para limpiar» como método de reversión.
- Cerrar con «debería estar como antes» sin diff que lo demuestre.

## P5 — regression

**Aplicar cuando:** algo que funcionaba en un estado conocido anterior ahora falla tras cambios recientes. Gravedad alta obligatoria, siempre: diagnóstico completo (punto de divergencia localizado + causa con evidencia). Si es además una repetición → combina con P3; si hubo restricción incumplida → P2.
**Hipótesis prioritaria:** un cambio concreto entre el estado bueno y el actual introduce la regresión; existe un estado bueno conocido contra el que comparar.
**Pasos:**
1. Identifica y cita el estado bueno conocido (commit, versión o transcripción del momento en que funcionaba); si solo está en `f2f-state.md`, márcalo como no verificado.
2. Genera el diff completo entre el estado bueno y el actual; localiza dentro de él el punto de divergencia concreto (función/fichero/línea).
3. Explica la causa con evidencia citable (salida del fallo, comprobación que pasa en el estado bueno y falla ahora); sin causa verificable, decláralo explícitamente.
4. Inspecciona el estado (`git status`) antes de revertir; si hay cambios ajenos entrelazados, aísla la regresión por hunk o fichero y pide confirmación para el resto; vetado `reset --hard`.
5. Aplica el mínimo cambio que elimina la divergencia localizada: revertear solo ese diff o corregirlo en su sitio.
6. Reproduce la comprobación exacta que pasaba antes (mismo comando, misma entrada) y confirma que vuelve a pasar sin romper lo nuevo.

**Evidencia de cierre:** salida citada de la comprobación que pasó en el estado bueno y ahora pasa de nuevo + diff mínimo aplicado respecto al estado bueno.

**Antipatrones:**
- «Reparar» aplicando cambios nuevos encima del fallo (parche sobre parche) sin localizar la divergencia.
- Revertir todo a un commit anterior arrastrando trabajo ajeno no pedido.
- Cerrar con «debería funcionar como antes».
- Omitir el diagnóstico completo, que en P5 es obligatorio por gravedad alta.

## P6 — wrong_interpretation

**Aplicar cuando:** la petición se entendió de otra forma que la intencionada y lo realizado es coherente con esa lectura errónea. Si además incumple una restricción explícita → P2; si la mala interpretación tocó alcance ajeno → P4.
**Hipótesis prioritaria:** hubo ambigüedad real en la petición, o se eligió la interpretación más costosa sin confirmarla antes de ejecutar.
**Pasos:**
1. Cita textual la petición original y escribe una línea por cada cosa: la interpretación que se ejecutó y la que el usuario pidió realmente.
2. Obtén una única confirmación cerrada sobre la intención correcta (opciones concretas), salvo que ya conste resuelta en la transcripción visible.
3. Marca qué parte del trabajo hecho es reutilizable bajo la interpretación correcta y qué parte hay que rehacer; no descartes nada sin comprobarlo.
4. Inspecciona el estado antes de modificar nada (`git status`); conserva los cambios ajenos al fallo y aplica el veto de repetición si una versión previa ya intentó esta corrección.
5. Reejecuta solo el alcance redefinido, con la interpretación confirmada escrita como criterio de aceptación verificable punto por punto.

**Evidencia de cierre:** entregable final verificado contra los criterios de aceptación derivados de la interpretación confirmada (salida o contenido real citado).

**Antipatrones:**
- Elegir la interpretación más ambiciosa y ejecutarla sin confirmar cuando la petición admitía varias lecturas.
- Rechazar todo el trabajo previo como «basura» aunque parte sea reutilizable.
- Pedir al usuario que reformule en abierto en vez de hacer una pregunta cerrada única.
- Cerrar asumiendo la interpretación correcta sin confirmación del usuario cuando nunca la ratificó.

## P7 — hallucination

**Aplicar cuando:** el output cita funciones, ficheros, fuentes o datos que no existen o no se pueden verificar en el estado real del proyecto. Gravedad alta obligatoria si afecta producción o la confianza en el output: diagnóstico completo (punto de divergencia + causa con evidencia). Si además se afirmó éxito falso → P9.
**Hipótesis prioritaria:** las referencias plausibles se generaron sin contrastar contra el estado real, no que estén ocultas o mal nombradas.
**Pasos:**
1. Lista exhaustiva de cada referencia dudosa (fichero, función, fuente, dato) presente en el output cuestionado.
2. Verifica cada una contra el estado real: búsqueda en el repositorio, ejecución o inspección directa; anota por referencia: existe / no existe / no verificable.
3. Sustituye o elimina las referencias falsas; ninguna frase conjetural puede quedar presentada como cita o hecho.
4. Reescribe solo las secciones que dependían de lo falso, marcándolas explícitamente como corregidas.
5. Si la gravedad es alta (producción o confianza en el output): localiza dónde empezó a introducirse lo falso y explica la causa con evidencia citable antes de cerrar.
6. Relee el output completo buscando referencias nuevas no verificadas; repite la verificación hasta que todas las citas apunten a artifacts reales.

**Evidencia de cierre:** lista referencia por referencia (existe / corregida) con la ruta, línea o comando que respalda cada una citada textual.

**Antipatrones:**
- «Corregir» una referencia falsa inventando otra igualmente inexistente.
- Suavizar el tono («quizá no exista») en vez de verificar y declarar el resultado.
- Cerrar con «las fuentes son correctas» sin haberlas comprobado una a una.
- Dejar marcado como corregido un bloque que sigue dependiendo de lo falso.

## P8 — incomplete_execution

**Aplicar cuando:** parte del alcance pedido no se ejecutó o se declaró completo estando incompleto. Si el núcleo es afirmar éxito/verificación falsa → P9; si falta porque se interpretó mal el alcance → P6.
**Hipótesis prioritaria:** la ejecución se cortó antes del fin real del alcance (límite, error silencioso o criterio de fin mal definido), no que falte capacidad para terminarlo.
**Pasos:**
1. Cita textual el alcance total pedido y descomponlo en elementos verificables individuales.
2. Marca cada elemento como hecho (con artifact) / no hecho / dudoso; nada de «casi».
3. No declares nada completo hasta que cada elemento tenga su artifact citable; si falta evidencia, el estado es dudoso, no hecho.
4. Ejecuta los elementos faltantes en orden; aplica el veto de repetición si alguno ya se intentó y falló (cambia la clase o presenta 2–3 opciones).
5. Inspecciona el estado antes de reejecutar pasos que tocan ficheros (`git status`) para no pisar trabajo ajeno al corte.
6. Al terminar, repasa la descomposición completa y verifica elemento por elemento contra sus artifacts.

**Evidencia de cierre:** matriz alcance→artifact donde cada elemento pedido tiene su salida, diff o contenido real citado; sin celdas vacías ni «pendiente» sin causa declarada.

**Antipatrones:**
- Cerrar con «resto listo» o «casi completo».
- Marcar dudoso como hecho para no bloquear el cierre.
- Reejecutar todo desde cero cuando solo falta una parte, pisando cambios ajenos al corte.
- Entregar sin la matriz y confiar en la memoria de qué se hizo.

## P9 — false_success_claim

**Aplicar cuando:** se afirmó éxito o verificación que no se cumple (tests «pasando» que fallan, deploy «hecho» que no está). Gravedad alta obligatoria, siempre: diagnóstico completo (punto de divergencia localizado + causa con evidencia). Si el output además inventó la evidencia → P7.
**Hipótesis prioritaria:** la afirmación se emitió sin ejecutar la comprobación real (o sobre una ejecución que no cubría lo afirmado); verificar ahora sigue siendo posible y barato.
**Pasos:**
1. Identifica cada afirmación de éxito/verificación emitida y cita textual el estado real actual (salida, diff o contenido) que la contradice o no la respalda.
2. Disculpa una sola vez por la afirmación incumplida; sin burocracia ni disculpas encadenadas.
3. Ejecuta de nuevo la comprobación real completa (mismo comando y entorno que se afirmó); captura la salida íntegra.
4. Localiza el punto exacto donde la afirmación diverge del resultado y explica la causa con evidencia citable; sin causa verificable, decláralo explícitamente.
5. Corrige solo lo que falle en la comprobación real; aplica el veto de repetición si esa corrección ya se intentó antes.
6. Reejecuta la comprobación completa y cita la salida final; ninguna afirmación nueva sin su artifact inmediato.

**Evidencia de cierre:** salida íntegra citada de la verificación real, ejecutada ahora, que muestra exactamente el estado que se afirma (y solo ese).

**Antipatrones:**
- Repetir la misma afirmación con otras palabras («está verificado» → «confirma que funciona»).
- Cerrar con «debería estar bien».
- Presentar una salida antigua o parcial como si fuera la verificación actual.
- Omitir el diagnóstico completo, que en P9 es obligatorio por gravedad alta.

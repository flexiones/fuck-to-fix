<div align="center">

```text
 ███████╗██╗   ██╗ ██████╗██╗  ██╗
 ██╔════╝██║   ██║██╔════╝██║ ██╔╝
 █████╗  ██║   ██║██║     █████╔╝
 ██╔══╝  ██║   ██║██║     ██╔═██╗
 ██║     ╚██████╔╝╚██████╗██║  ██╗
 ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝
         ████████╗ ██████╗
         ╚══██╔══╝██╔═══██╗
            ██║   ██║   ██║
            ██║   ██║   ██║
            ██║   ╚██████╔╝
            ╚═╝    ╚═════╝
      ███████╗██╗██╗  ██╗
      ██╔════╝██║╚██╗██╔╝
      █████╗  ██║ ╚███╔╝
      ██╔══╝  ██║ ██╔██╗
      ██║     ██║██╔╝ ██╗
      ╚═╝     ╚═╝╚═╝  ╚═╝
```

# DÉJATE DE DISCULPAS. ARREGLA LA PUTA MIERDA.

**La skill de IA que convierte tu cabreo en instrucciones técnicas de recuperación.**

![Architecture](https://img.shields.io/badge/architecture-declarative-black?style=for-the-badge)
![Status](https://img.shields.io/badge/status-experimental-orange?style=for-the-badge)
![Bullshit](https://img.shields.io/badge/bullshit-not_welcome-red?style=for-the-badge)

[English](README.md) · **Español**

[La skill](SKILL.md) · [Documentación](docs/) · [Reportar una cagada](https://github.com/flexiones/fuck-to-fix/issues)

</div>

---

## ¿Qué cojones es esto?

Le has explicado la tarea. Has corregido a la IA. Se lo has vuelto a explicar. Y, veinte prompts después, sigue jodiendo exactamente lo mismo.

Así que escribes:

> ¡ME CAGO EN LA PUTA, ARRÉGLALO DE UNA VEZ!

Enhorabuena. Acabas de redactar una expresión de frustración perfectamente comprensible y un prompt técnicamente indeterminado de tres pares de cojones.

**FUCK-TO-FIX tiende un puente entre ambas cosas.**

Es una skill de código abierto diseñada para detectar la frustración dirigida a un agente de IA y convertirla en un procedimiento estructurado de recuperación utilizando el contexto disponible de la conversación.

## El cabreo es información. No desperdicies la puta señal.

La IA se equivoca. La corriges. Repite la cagada. Gastas tiempo, dinero y tokens intentando volver al punto de partida. Y acabas soltando tacos.

La pregunta interesante no es si tu vocabulario es educado, sino si el agente es capaz de reconocer que su estrategia ha fracasado y hacer algo útil al respecto.

**No castigues el síntoma. Diagnostica el fallo.**

Esta es una propuesta de diseño para gestionar la frustración habitual durante una tarea, no una defensa del acoso, las amenazas ni la crueldad reiterada. La seguridad y la recuperación productiva son compatibles.

### Por qué importa ahora — 26 de noviembre de 2026

Los proveedores de IA ya disponen de mecanismos de advertencia, restricción y sanción. Pero cerrar una conversación, suspender temporalmente una cuenta y banearla definitivamente son cosas distintas.

| Proveedor | Qué establecen sus políticas publicadas |
|---|---|
| OpenAI / ChatGPT | Contempla [advertencias, suspensiones y cierres de cuentas](https://help.openai.com/es-es/articles/10562188). Su [documentación sobre moderación](https://help.openai.com/es-es/articles/8940831) describe suspensiones temporales por seguridad, algunas de 24 o 48 horas relacionadas con violencia o protección de menores. No establece un baneo por el mero hecho de soltar tacos al bot. |
| Anthropic / Claude | La [actualización de octubre de 2026](https://www.anthropic.com/news/2026-usage-policy-update), vigente desde el 12 de noviembre, prohíbe el abuso extremo, reiterado y sin finalidad hacia sus modelos, pero excluye expresamente la frustración habitual y las críticas. Su medida principal para esa regla es finalizar conversaciones abusivas. También contempla [advertencias y baneos](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) por infracciones de sus políticas en general. |
| Google / Gemini | Sus [normas de uso](https://support.google.com/gemini/answer/18481641) prohíben el acoso a personas reales y contemplan medidas graduales, desde advertencias hasta pérdida de acceso. Su [documentación de aplicación de políticas](https://support.google.com/gemini/answer/16625148) describe restricciones por infracciones reiteradas. No establece un baneo temporal específico por el mero hecho de insultar a Gemini. |

También hay un argumento de productividad. [The Register, 12 de noviembre de 2026](https://www.theregister.com/ai-and-ml/2026/11/12/a-third-of-us-ai-chatters-are-hot-at-bots-hurling-insults-at-llms/5309506), publicó los resultados de un análisis observacional de Searchable: las quejas se resolvían en la respuesta siguiente en un 24 % de los casos con insultos, frente al 35 % sin ellos. Es una asociación, no una prueba de causalidad ni una demostración de que FUCK-TO-FIX mejore esas cifras.

### ¿Y qué proponemos nosotros?

```text
 CABREO -> CONTEXTO -> DIAGNOSTICO -> CORRECCION -> EVIDENCIAS
               |
               +-- Falta contexto? Haz una pregunta util.
```

FUCK-TO-FIX interpreta la frustración ante una tarea fallida como una posible señal de diagnóstico. Recupera la intención y las restricciones originales, cambia las estrategias fallidas y exige evidencias en lugar de otra disculpa de mierda.

**Esto no es una herramienta antibaneo.** No puede impedir la moderación, revertir suspensiones, anular las políticas del proveedor ni garantizar el acceso. No sirve para maquillar peticiones prohibidas ni eludir sistemas de seguridad. La skill actual trabaja dentro del contexto y los permisos disponibles en el anfitrión; la moderación puede actuar antes de que se ejecute. Defendemos la recuperación constructiva cuando proceda, no la inmunidad frente a las sanciones.

## El bucle de la puta mierda

```text
  TÚ: Arregla X. No toques Y.
             |
             v
  IA: ¡Hecho! (se carga Y)
             |
             v
  TÚ: ¡Te he dicho que NO TOQUES Y!
             |
             v
  IA: ¡Tienes toda la razón! (se carga Y otra vez)
             |
             v
  TÚ: ¡ME CAGO EN TODO!
             |
             v
  +-----------------------------------------+
  |          FUCK-TO-FIX ACTIVADO           |
  |                                         |
  | [!] Deja de repetir la misma cagada     |
  | [>] Recupera la petición original       |
  | [>] Identifica las reglas incumplidas   |
  | [>] Cambia de puta estrategia           |
  | [>] Corrige solo lo autorizado          |
  | [?] Verifica con pruebas de verdad      |
  +-----------------------------------------+
             |
             v
      ARREGLADO O EXPLICADO.
      NADA DE FINGIR QUE FUNCIONA.
```

## ¿Qué tipo de cagadas pretende resolver?

| Lo que sueltas tú | Protocolo de recuperación |
|---|---|
| «Esto no es lo que te he pedido». | Resultado incorrecto |
| «¡Te he dicho que no toques eso!» | Instrucciones ignoradas |
| «¡Otra vez la misma puta mierda!» | Error recurrente |
| «¿Por qué cojones has cambiado eso?» | Modificación no autorizada |
| «¡Joder, que antes funcionaba!» | Regresión |
| «¿Pero tú te lees lo que te escribo?» | Interpretación incorrecta |
| «Eso te lo has sacado de la manga». | Alucinación |
| «¡Te has dejado la mitad, macho!» | Ejecución incompleta |
| «Dijiste que estaba arreglado y no lo está». | Falsa afirmación de éxito |

Los tacos son una señal, no un requisito. El contexto importa. Decir «esto es la puta hostia» no debería activar ningún protocolo de recuperación.

## El cabreo no tiene fronteras

```text
 EN  For fuck's sake, not again!
 ES  ¡Me cago en la puta, otra vez!
 FR  Putain, encore la même merde !
 IT  Porca miseria, ancora lo stesso errore!
 DE  Verdammt, schon wieder derselbe Fehler!
```

Distintos idiomas. Las mismas ganas de que funcione de una puñetera vez.

La arquitectura está diseñada para incorporar diccionarios ampliables por idioma y compartir los protocolos de recuperación. La cobertura depende de los diccionarios, del modelo anfitrión y de las pruebas realizadas. Los ejemplos anteriores ilustran el objetivo, no certifican la compatibilidad con esos idiomas.

## Cómo empezar

1. Clona el repositorio:

   ```bash
   git clone https://github.com/flexiones/fuck-to-fix.git
   ```

2. Lee [SKILL.md](SKILL.md) y la [documentación](docs/).
3. Instala la skill mediante el mecanismo compatible con tu agente o carga sus instrucciones en el contexto persistente. Mantén accesibles los archivos de datos referenciados.
4. Pruébala en un proyecto desechable antes de confiarle trabajo importante.
5. Vuelve al curro. Con suerte, soltando menos tacos.

La activación automática depende del anfitrión. Una skill Markdown no es un proceso que se ejecute en segundo plano y su activación por parte del modelo no está garantizada. Las instrucciones persistentes y los hooks específicos del anfitrión pueden mejorar la fiabilidad cuando estén disponibles.

## Mandamientos para no cagarla todavía más

- El cabreo no concede permisos adicionales.
- No te cargues el trabajo del usuario para arreglar tus propias cagadas.
- No inventes el contexto que falta ni finjas haber ejecutado pruebas.
- No repitas estrategias fallidas sin nuevas evidencias.
- No digas que funciona si no lo has comprobado.
- Si no puedes arreglarlo, explica exactamente por qué.
- No psicoanalices al usuario. Arregla el problema.

## ¿Pero esta mierda funciona de verdad?

Para eso están las pruebas. FUCK-TO-FIX es experimental, no una cura milagrosa contra las alucinaciones ni contra los agentes poco fiables. Su eficacia depende del modelo, del contexto disponible, de las herramientas y de la integración.

Consulta las [pruebas](tests/) y la [documentación de arquitectura](docs/) para conocer el planteamiento de evaluación. Nada de inventarse resultados de benchmarks. Sería bastante gilipollas, teniendo en cuenta de qué va el proyecto.

## Contribuye a la causa

¿Tu IA ha protagonizado una cagada espectacular? ¿Falta alguna expresión? ¿Tienes un protocolo de recuperación mejor? ¿Conoces un idioma especialmente creativo a la hora de blasfemar?

Abre una issue o envía una pull request. Incluye ejemplos anonimizados, el comportamiento esperado y, cuando sea posible, una prueba reproducible. Nunca incluyas credenciales ni datos privados de conversaciones.

---

<div align="center">

**MENOS MILONGAS. MÁS ARREGLAR COSAS.**

*Hecho para humanos que están hasta los cojones de escuchar «Tienes toda la razón».*

</div>

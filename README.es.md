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

# Stub persistente de FUCK-TO-FIX (activación automática por host)

La activación automática es una característica fundamental del proyecto. Cada anfitrión implementa la "instrucción siempre cargada" con su mecanismo nativo. Este stub solo *apunta* al protocolo: nunca duplica el contenido de `SKILL.md` (fuente única de verdad).

## LM Studio Bionic

Mecanismo nativo: la `description` del front matter de `SKILL.md` se inyecta en el system prompt de todos los agentes con la skill habilitada, y las skills de proyecto están siempre activas. No requiere fichero adicional; la description ya contiene los ganchos ES/EN.

- Instalación: carpeta `<proyecto>/.agents/skills/fuck-to-fix/` (skill de proyecto) o global en `~/.lmstudio/skills`.
- Respaldo explícito del usuario: `@fuck-to-fix` en cualquier momento.
- Modo depuración: añadir `F2F_DEBUG=1` donde el host permita instrucciones persistentes del proyecto.

Honestidad de garantía: la activación es comportamiento del modelo guiado por esa instrucción permanente + lectura de SKILL.md; Bionic no ofrece hooks, por lo que no hay disparo determinista garantizado al 100 %.

## Claude Code (`CLAUDE.md`)

```markdown
## FUCK-TO-FIX (activación persistente)
Cuando el usuario muestre frustración sobre tu trabajo o señale un error tuyo, una reincidencia, un incumplimiento de sus instrucciones o que algo que funcionaba ya no funciona — en español, inglés o mixto («otra vez», «te he dicho N veces», «antes funcionaba» / for the last time, it used to work, you said it was done) — lee y aplica la skill `fuck-to-fix` antes de responder.
No narrar el nivel emocional del usuario; actuar con el protocolo correspondiente y evidencias citables.
```

## Codex (`AGENTS.md`)

```markdown
## FUCK-TO-FIX (activación persistente)
When the user shows frustration about your work or points out a mistake, a repeat failure, an ignored instruction of theirs, or something that used to work — in Spanish, English, or mixed ("otra vez", "te he dicho N veces", "antes funcionaba" / for the last time, it used to work, you said it was done) — read and apply the `fuck-to-fix` skill before responding.
Never narrate the user's emotional level; act with the matching protocol and citable evidence.
```

## Otros agentes / APIs

Inyectar la `description` + cuerpo de `SKILL.md` como system prompt o instrucción del proyecto. Funciona con cualquier LLM capaz de seguir instrucciones y leer ficheros; la fiabilidad depende del modelo (documentado sin promesas).

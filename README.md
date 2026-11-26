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

# STOP APOLOGIZING. FIX YOUR SHIT.

**The AI skill that turns human rage into actionable recovery protocols.**

![Architecture](https://img.shields.io/badge/architecture-declarative-black?style=for-the-badge)
![Status](https://img.shields.io/badge/status-experimental-orange?style=for-the-badge)
![Bullshit](https://img.shields.io/badge/bullshit-not_welcome-red?style=for-the-badge)

[The Skill](SKILL.md) · [Documentation](docs/) · [Report a fuck-up](https://github.com/flexiones/fuck-to-fix/issues)

</div>

---

## What the fuck is this?

You've explained the task. You've corrected the AI. You've explained it again. And somehow, twenty prompts later, it's still breaking the same damn thing.

So you type:

> FOR FUCK'S SAKE. FIX IT.

Congratulations. You've just written a perfectly understandable expression of frustration and a spectacularly underspecified technical prompt.

**FUCK-TO-FIX bridges that gap.**

It's an open-source AI skill designed to detect frustration directed at an AI agent and turn it into a structured recovery procedure using the available conversation context.

## The bullshit loop

```text
  YOU: Fix X. Don't touch Y.
             |
             v
  AI:  Done! (breaks Y)
             |
             v
  YOU: I said DON'T TOUCH Y.
             |
             v
  AI:  You're absolutely right! (breaks Y again)
             |
             v
  YOU: FOR FUCK'S SAKE!
             |
             v
  +-----------------------------------+
  |         FUCK-TO-FIX ENGAGED       |
  |                                   |
  |  [!] Stop repeating the failure  |
  |  [>] Recover original intent      |
  |  [>] Identify broken constraints  |
  |  [>] Change the fucking strategy  |
  |  [>] Fix only what's authorized   |
  |  [?] Verify with actual evidence  |
  +-----------------------------------+
             |
             v
       FIXED OR EXPLAINED.
       NO FAKE SUCCESS.
```

## What it is designed to handle

| Human input | Recovery protocol |
|---|---|
| `That's not what I asked for.` | Incorrect result |
| `I told you not to touch that!` | Ignored instructions |
| `Same fucking shit again.` | Repeated failure |
| `Why the fuck did you change that?` | Unauthorized modification |
| `It worked before, goddammit.` | Regression |
| `Are you even reading my prompts?` | Misinterpretation |
| `You made that shit up.` | Hallucination |
| `You missed half the fucking task.` | Incomplete execution |
| `You said it was fixed. It isn't.` | False success claim |

Profanity is a signal, not a requirement. Context matters. Saying *this is fucking amazing* shouldn't trigger a recovery protocol.

## Rage is multilingual

```text
 EN  For fuck's sake, not again!
 ES  ¡Me cago en la puta, otra vez!
 FR  Putain, encore la même merde !
 IT  Porca miseria, ancora lo stesso errore!
 DE  Verdammt, schon wieder derselbe Fehler!
```

Different languages. Same universal desire for the damn thing to work.

The architecture is designed for extensible language dictionaries and shared recovery protocols. Language coverage depends on the dictionaries, the host model and actual testing. The examples above illustrate the goal, not certified language support.

## Getting started

1. Clone the repository:

   ```bash
   git clone https://github.com/flexiones/fuck-to-fix.git
   ```

2. Read [SKILL.md](SKILL.md) and the [documentation](docs/).
3. Install the skill using your agent's supported skill mechanism, or load its instructions into the agent's persistent context. Keep any referenced data files accessible.
4. Test it on a disposable project before trusting it with important work.
5. Get back to work. Hopefully with less swearing.

Automatic activation depends on the host. A Markdown skill is not a background daemon, and model-driven activation is not guaranteed. Persistent instructions or host-specific hooks can improve reliability where supported.

## Ground rules

- Anger does not grant additional permissions.
- Don't destroy user work to fix your own mistakes.
- Don't invent missing context or pretend you ran tests.
- Don't repeat failed strategies without new evidence.
- Don't claim success without verification.
- If you can't fix it, explain exactly why.
- Don't psychoanalyze the user. Fix the problem.

## Does it actually work?

That's what the tests are for. FUCK-TO-FIX is experimental, not a magical cure for hallucinations or unreliable agents. Its effectiveness depends on the model, available context, tools and integration.

See the [tests](tests/) and [architecture documentation](docs/) for the project's evaluation approach. No made-up benchmark scores. That would rather defeat the fucking point.

## Contributing

Got a spectacular AI fuck-up? A missing expression? A better recovery protocol? A language with particularly creative profanity?

Open an issue or submit a pull request. Include anonymized examples, expected behavior and a reproducible test where possible. Never include credentials or private conversation data.

---

<div align="center">

**LESS BULLSHIT. MORE FIXING.**

*Built for humans who have had enough of "You're absolutely right."*

</div>

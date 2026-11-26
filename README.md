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

**English** · [Español](README.es.md)

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

## Frustration is feedback. Don't waste the fucking signal.

An AI gets something wrong. You correct it. It repeats the mistake. You spend more time, money and tokens trying to get back to where you started. Eventually, you swear.

The interesting question is not whether your vocabulary is polite. It's whether the agent can recognize that its approach has failed and do something useful about it.

**Don't punish the symptom. Diagnose the failure.**

This is a design proposal for ordinary task-related frustration, not a defence of harassment, threats or sustained cruelty. Safety and productive recovery can coexist.

### Why this matters now — November 26, 2026

AI providers already have mechanisms for warnings, restrictions and account enforcement. But ending a conversation, temporarily suspending an account and permanently banning a user are different things.

| Provider | What the published policies establish |
|---|---|
| OpenAI / ChatGPT | [Warnings, suspensions and closures](https://help.openai.com/en/articles/10562188) are available for policy enforcement. [Its moderation guidance](https://help.openai.com/en/articles/8940831) describes temporary safety suspensions, including certain violence or child-safety cases lasting 24 or 48 hours. It does not establish a ban for ordinary swearing at the bot. |
| Anthropic / Claude | The [October 2026 policy update](https://www.anthropic.com/news/2026-usage-policy-update), effective November 12, prohibits extreme, sustained purposeless abuse of its models while explicitly excluding ordinary frustration and criticism. Ending abusive conversations is its primary enforcement response for this rule. [Account warnings and bans](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) also exist for policy violations generally. |
| Google / Gemini | [Gemini user guidelines](https://support.google.com/gemini/answer/18481641) prohibit harassment of real people and provide tiered enforcement, from warnings to loss of access. [Google's enforcement guidance](https://support.google.com/gemini/answer/16625148) describes restrictions for repeated violations. Neither establishes a specific temporary ban for merely swearing at Gemini. |

There is also a productivity argument. [The Register, November 12, 2026](https://www.theregister.com/ai-and-ml/2026/11/12/a-third-of-us-ai-chatters-are-hot-at-bots-hurling-insults-at-llms/5309506), reported an observational analysis by Searchable in which next-response complaint resolution was 24% after insults versus 35% without them. This is an association, not proof of causation or evidence that FUCK-TO-FIX improves those rates.

### What we propose instead

```text
 FRUSTRATION -> CONTEXT -> DIAGNOSIS -> CORRECTION -> EVIDENCE
                  |
                  +-- missing context? Ask one useful question.
```

FUCK-TO-FIX treats frustration about a failed task as a potential debugging signal. It preserves the original intent and constraints, changes failed approaches and asks for evidence rather than another empty apology.

**This is not an anti-ban tool.** It cannot prevent moderation, reverse suspensions, override provider policies or guarantee access. It does not sanitize prohibited requests or bypass safety systems. The current skill operates within the host's available context and permissions; moderation may occur before it runs. The project advocates constructive recovery wherever appropriate, not immunity from enforcement.

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

# suite-workflow

A Claude Code Agent Skill that turns "give me 10 of something" into a structured, calibrated, parallelized batch-production pipeline — instead of the usual one-at-a-time back-and-forth with an AI assistant.

## Why this exists

Working with an AI assistant on recurring creative decisions (which of several content ideas to run with, which product concepts to build out), I noticed the same pattern: review one idea, decide, review the next, decide — slow, and it never let the assistant's growing knowledge of my taste do any real work. I wanted to see a pre-vetted shortlist, not a raw firehose, and I wanted the assistant's confidence in predicting my choices to be *measured*, not assumed.

This skill is the resulting four-stage process, plus the calibration mechanism that makes trusting an AI agent's judgment an earned, checkable thing rather than a vibe.

## What it does

**Ideate → Build → Self-check → Parallelise**, applied to any batch request:

- **Ideate** generates deliberate overcapacity (ask for 10, get 15), pre-filtered against a **decision profile** — a maintained document of the user's actual hard constraints, preferences, and taste, built from their real recorded decisions rather than a one-time questionnaire. Presented as one batch review with tradeoffs and costs shown per item, not a blind list.
- **Build** takes the chosen items to fully ready-to-ship, against whatever the target platform actually requires.
- **Self-check** applies objective scoring and regenerates weak items by changing one identified variable — not vague "make it better" loops.
- **Parallelise** runs each item's build in its own concurrent subagent — but *only* for genuine batch work, because parallel agents cost the same total tokens as sequential ones, just faster; this skill is explicit that parallelism is a latency win, not a cost win, and shouldn't be reached for by default.

**The calibration mechanism is the part I'm most interested in as a portfolio piece:** rather than assuming an AI agent "gets" a user's preferences, this skill runs a **pre-committed prediction interview** — the agent writes down its predicted answers to a mixed set of questions *before* seeing the user's real answers, timestamped so there's no retrofitting, then scores itself against the reveal. Below a set confidence bar, the workflow doesn't quietly auto-filter anything — it shows its full reasoning and defers to the human. That's a concrete, exportable pattern for a problem every "autonomous AI agent" pitch eventually has to answer: how do you know it's actually calibrated, and what happens when it isn't?

## Who this is for

- **Builders:** a real pattern for orchestrator/worker agent design — when to parallelize (and when explicitly not to), and how to keep quality control centralized even when production is distributed.
- **Consultants and teams evaluating AI-agent trust:** the calibration-interview mechanic is a genuinely reusable answer to "how much autonomy should this agent actually have," with a measurable gate instead of a policy statement.

## Install

Drop `SKILL.md` into `.claude/skills/suite-workflow/` in your project. Claude Code picks up project-level skills automatically at session start. You'll also want to build your own decision-profile document as you use it — this skill assumes one exists but doesn't ship one, since it's inherently personal to whoever's using it.

## License

MIT — see [LICENSE](LICENSE).

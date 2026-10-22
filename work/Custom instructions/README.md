# Shader specification workspace

Use [TASK.md](TASK.md) for the complete shader you want, including the major design choices and all behaviour, construction and verification requirements. It is also the target for a clean rebuild; it does not list settings you can change in-game.

Use [CHANGES.md](CHANGES.md) for the specific changes you want in the next coding pass. Add one unchecked item per requested result, then send Codex:

> Apply the pending changes.

Codex reads both files but implements only pending `CHANGES.md` items. Everything else in `TASK.md` remains a standing requirement. An empty change list means there is no new coding task. Saving either file does not start work.

After each completed change, Codex checks the shader against `TASK.md`, incorporates approved completed design changes into that full target, and refines stale wording. It moves finished, verified `CHANGES.md` requests from Pending changes into `COMPLETED-CHANGES.md` with the release/evidence reference. When the queue is empty, it leaves “No pending changes.” Unfinished or unverified work stays pending. Sending work or ending a chat turn does not clear the queue. [CHANGE-LOG.md](CHANGE-LOG.md) is the output/evidence record. [SPEC-BASELINE.md](SPEC-BASELINE.md) remains only as an older comparison snapshot.

## Setup

These files live in `work/Custom instructions` inside `/Users/william.lei/Documents/ChatGPT/MC Shader Making`. Open that project as your VS Code workspace. Edit `TASK.md` for the absolute target and `CHANGES.md` for the next pass. `TASK-previous-brief.md` preserves an earlier completed brief.

Automatic project guidance is provided by the project-root `AGENTS.md`. Keep the detailed workflows here so the root file stays concise.

## Reusable prompts

- `.prompts/water.md`: water, reflection, refraction and underwater work.
- `.prompts/clouds.md`: clouds and atmosphere.
- `.prompts/performance.md`: measure and optimise a specific bottleneck.
- `.prompts/visual-verification.md`: review a build in Minecraft.

Example:

> Do the current water task, using `work/Custom instructions/.prompts/water.md` for the workflow.

`GOALS.md` records lasting preferences. [SHADER-SPEC-1.6.7.md](SHADER-SPEC-1.6.7.md) preserves the detailed 1.6.7 rebuild/evidence snapshot and historical setting inventory; `SHADER-SPEC.md` is older history.

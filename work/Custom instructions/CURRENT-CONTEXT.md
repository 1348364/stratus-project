# Shader context — generated locally

Navigation and fingerprints only; this file does not certify a release or authorise additional work.
Project: /Users/william.lei/Documents/ChatGPT/MC Shader Making
Active brief: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/CHANGES.md
Target snapshot: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/TASK.md
Brief SHA256: 0658d5085cbb55c6bdd9b7ef0f095f1b86bad5d848e16f4349d69e2ed7504005
Target SHA256: d8fa6a15158e94068ecaffa5d8fe9207bd3f3631193401281128b9f1b654a2e4
Current shared TASK SHA256: d8fa6a15158e94068ecaffa5d8fe9207bd3f3631193401281128b9f1b654a2e4
Current shader tree SHA256: b0b79544c04ba2e0fc545f0780e7ce0714c47cba7b12266539e22a200bf07e41 (236 files)

## Read first
- Project AGENTS.md, work/Custom instructions/AGENTS.md, GOALS.md and WORKFLOW.md.
- Active brief and applicable TASK.md. Read unchanged documents once per context; use hashes to detect changes.
- PROGRESS.md, if resuming this batch. Recheck changed files and relevant runtime state before reusing evidence.
- Relative links copied into a batch brief resolve from work/Custom instructions, their original location.

## Target section index
- Line 1: Stratus — editable shader specification
- Line 5: Quick edit — major design choices
- Line 20: Full shader specification
- Line 22: Identity and reference
- Line 32: Terrain, lighting, sun and materials
- Line 47: Water
- Line 57: Lower clouds, cirrus and mist
- Line 71: Controls, presets and rendering
- Line 85: Packaging, testing and evidence

## Current source navigation hints
- outputs/Stratus/shaders/core/scene-depth.glsl
- outputs/Stratus/shaders/core/submerged-reflection.glsl
- outputs/Stratus/shaders/core/submerged-view.glsl
- outputs/Stratus/shaders/core/water-reflection.frag.glsl
- outputs/Stratus/shaders/core/options.glsl
- outputs/Stratus/shaders/core/output.frag.glsl
- outputs/Stratus/shaders/core/refraction.glsl
- outputs/Stratus/shaders/core/scene-trace.glsl
- outputs/Stratus/shaders/core/screen.vert.glsl
- outputs/Stratus/shaders/core/submerged-compose.glsl
- outputs/Stratus/shaders/shaders.properties
- outputs/Stratus/package.py and outputs/Stratus/install.py: existing release tooling.
Hints are filename matches only, not a diagnosis or a complete dependency list.

## Latest recorded release summary — reported evidence, not a live check
## 22 October 2026 — Stratus 1.6.11

### At a glance

- Reference/source defaults now use the user's explicitly approved Main visual **and quality** tuning. All four presets share56 visual settings with six ordered quality choices. All62 controls/ranges/menu access remain; High retains full detailed optics. The installer preserves later manual edits.
- Built **[Stratus1.6.11](../../outputs/Stratus-1.6.11.zip)**, installed, selected and loaded in Main. Iris reports **REFERENCE / zero overrides**; all62 runtime values match the captured Main baseline. [Receipt](../../outputs/Stratus-1.6.11-install.json), [18 labelled actual captures](../../outputs/Stratus-1.6.11-visual-checks/index.html).
- Passed768 native pairs, ten underwater cases, ten migration checks and actual Iris interpretation/matching for all four62-option profiles. The readiness barrier blocked while work was pending and waited for stable loaded chunks. Occupied-cloud and clearer independent cirrus/day/sunset views passed finite review. **FPS/60FPS and remaining leaf/historical acceptance stay pending by explicit user deferral.**


For earlier evidence, search the exact version or issue in CHANGE-LOG.md; do not dump its entire history.

# Shader context — generated locally

Navigation and fingerprints only; this file does not certify a release or authorise additional work.
Project: /Users/william.lei/Documents/ChatGPT/MC Shader Making
Active brief: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/IN-PROGRESS/1af89474-f56a-4419-bc73-7f12d4950cfa/CHANGES.md
Target snapshot: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/IN-PROGRESS/1af89474-f56a-4419-bc73-7f12d4950cfa/TASK.md
Brief SHA256: 25de90ef1f2fc23b27ab9ee18fe1daa585581631a7e1bea1b5c62dadf7c1002d
Target SHA256: 6c8aadb31672b73c97524c6a6942e4209aad361053066ee9c4279bcec7ee398d
Current shared TASK SHA256: 6c8aadb31672b73c97524c6a6942e4209aad361053066ee9c4279bcec7ee398d
Current shader tree SHA256: a14800da94765d93bd0a60ac91292beba4608e1ae3c585fec307cbca3202cf7f (238 files)

## Read first
- Project AGENTS.md, work/Custom instructions/AGENTS.md, GOALS.md and WORKFLOW.md.
- RELEASE-ROADMAP.md guides release numbering; planned milestones are not extra implementation scope.
- Active brief and applicable TASK.md. Read unchanged documents once per context; use hashes to detect changes.
- PROGRESS.md, if resuming this batch. Recheck changed files and relevant runtime state before reusing evidence.
- Relative links copied into a batch brief resolve from work/Custom instructions, their original location.

## Target section index
- Line 1: Stratus — editable shader specification
- Line 5: Quick edit — major design choices
- Line 20: Full shader specification
- Line 22: Identity and reference
- Line 33: Terrain, lighting, sun and materials
- Line 48: Water
- Line 58: Lower clouds, cirrus and mist
- Line 72: Controls, presets and rendering
- Line 86: Packaging, testing and evidence

## Current source navigation hints
- outputs/Stratus/shaders/block.properties
- outputs/Stratus/shaders/shaders.properties
- outputs/Stratus/shaders/core/frame.glsl
- outputs/Stratus/shaders/core/options.glsl
- outputs/Stratus/shaders/core/screen.vert.glsl
- outputs/Stratus/shaders/core/water-buffer.glsl
- outputs/Stratus/shaders/core/water-interface.glsl
- outputs/Stratus/shaders/core/water-path.glsl
- outputs/Stratus/shaders/core/water-reflection.frag.glsl
- outputs/Stratus/shaders/core/water-resolve.frag.glsl
- outputs/Stratus/package.py and outputs/Stratus/install.py: existing release tooling.
Hints are filename matches only, not a diagnosis or a complete dependency list.

## Latest recorded release summary — reported evidence, not a live check
## 23 October 2026 — Stratus 1.7.0-rc1 — implementation candidate

### At a glance

- Implemented selectable native water/underwater medium, stronger exposed-face film and original transparent-solid optics. New source has65 reachable controls; every previous62 default/range and original preset quality assignment remains.
- Packaged **[Stratus1.7.0-rc1](../../outputs/Stratus-1.7.0-rc1.zip)** — **candidate only**. [Packaging receipt](../../outputs/Stratus-1.7.0-rc1-receipt.json), [11 reviewed captures](../../outputs/Stratus-1.7.0-rc1-visual-checks/index.html). Final release ZIP is not installed, selected or loaded. Shader-equivalent temporary v3 QA variants loaded; stable1.6.12 and original session restored afterwards.
- Passed768 final native program pairs,96 wet-film GPU samples,24,576 transparent-optics probe pixels,ten physical/ten native underwater cases,13 installer checks and Iris parsing/matching of all four65-value profiles. **Remaining live checks skipped by user; all four requests stay pending. Known waterline band remains. No FPS sampled.**

Batch: `IN-PROGRESS/43b4c0ad-c217-4a82-8534-29d34345f150/CHANGES.md`. No later batch or shared next queue was consumed. Frozen delta only repeated earlier1.6.12 reconciliation and required no duplicate work. Current TASK/change log/archive matched initial fingerprints before reconciliation; only this run's earlier staging changed the batch brief. No conflicting newer edits were found. The completed archive is unchanged because no full request passed every required gate.


For earlier evidence, search the exact version or issue in CHANGE-LOG.md; do not dump its entire history.

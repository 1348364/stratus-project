# Shader context — generated locally

Navigation and fingerprints only; this file does not certify a release or authorise additional work.
Project: /Users/william.lei/Documents/ChatGPT/MC Shader Making
Active brief: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/IN-PROGRESS/43b4c0ad-c217-4a82-8534-29d34345f150/CHANGES.md
Target snapshot: /Users/william.lei/Documents/ChatGPT/MC Shader Making/work/Custom instructions/IN-PROGRESS/43b4c0ad-c217-4a82-8534-29d34345f150/TASK.md
Brief SHA256: f868bd21ac416eec8d4439bcecd0ac98e6017f772f42614ec2a59e99456843f6
Target SHA256: 3da26e5f8a3712e8a8e325b435ae3115f72233d5fa4e3b97f2057119bf37aef4
Current shared TASK SHA256: 3da26e5f8a3712e8a8e325b435ae3115f72233d5fa4e3b97f2057119bf37aef4
Current shader tree SHA256: bd49fc66ef75138eef4365700a40185e48f93c955857701ed562f13aaf1b2db2 (237 files)

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
- outputs/Stratus/shaders/block.properties
- outputs/Stratus/shaders/core/refraction.glsl
- outputs/Stratus/shaders/core/water-buffer.glsl
- outputs/Stratus/shaders/core/water-interface.glsl
- outputs/Stratus/shaders/core/water-path.glsl
- outputs/Stratus/shaders/core/water-reflection.frag.glsl
- outputs/Stratus/shaders/core/water-resolve.frag.glsl
- outputs/Stratus/shaders/core/water-surface.glsl
- outputs/Stratus/shaders/shaders.properties
- outputs/Stratus/shaders/core/options.glsl
- outputs/Stratus/package.py and outputs/Stratus/install.py: existing release tooling.
Hints are filename matches only, not a diagnosis or a complete dependency list.

## Latest recorded release summary — reported evidence, not a live check
## 23 October 2026 — Stratus 1.6.12

### At a glance

- Native animated water texture and biome tint now cover the whole visible water surface, including distant/grazing reflections. Clear optics at zero, shallow-bed visibility and sharp reflection detail remain.
- Built **[Stratus1.6.12](../../outputs/Stratus-1.6.12.zip)**; installed, selected and loaded in Main. All62 controls/defaults/ranges/menu paths and four approved preset assignments are preserved. [Receipt](../../outputs/Stratus-1.6.12-install.json), [actual comparison gallery](../../outputs/Stratus-1.6.12-visual-checks/index.html).
- Passed768 native pairs,192 actual surface-GPU samples,ten underwater cases,ten installer checks and actual Iris matching of all four62-option profiles. Finite loaded-world water/preset/fixture views reviewed. **FPS remains explicitly deferred; no speedup or60FPS claim.**


For earlier evidence, search the exact version or issue in CHANGE-LOG.md; do not dump its entire history.

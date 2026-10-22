# Stratus release roadmap

The user delegated release planning and version choices. These are planned milestones, not released features, deadlines or instructions to start the whole roadmap. The active CHANGES.md brief or named IN-PROGRESS batch still controls execution. Review actual source and evidence before staging any milestone work; do not reimplement an existing feature because it appears below.

## Version choices

- **Patch — 1.6.x, 1.7.x, etc.:** focused fixes, tuning, compatibility repairs and incremental optimisation. Do not keep using patches for a substantial new feature merely because the previous release was a patch.
- **Minor — 1.7.0, 1.8.0, etc.:** a substantial, user-visible feature or coherent improvement milestone with preserved controls and compatible settings. Verification alone does not justify a feature bump.
- **Major — 2.0.0:** a substantial integrated improvement to Stratus's rendering and visual experience. Rework architecture only where needed for that result. A major number does not authorise removing controls, breaking settings or discarding working code.
- Choose the smallest bump that honestly describes the completed work. No automatic promotion after a certain number of patches, no renaming an unchanged build to manufacture a major release, and no release date promises without evidence.
- The coder may choose the appropriate version within these rules for authorised work. Planned versions are never reported as built, installed, loaded or verified.

## Current phase — stabilise 1.6.x

Planning baseline: TASK.md currently records 1.6.12. Refresh this reference from source/package/evidence when starting a coding pass; this roadmap does not certify the latest live build.

Resolve concrete regressions and preserve the approved baseline before broadening the rendering work. In particular, TASK.md records an unresolved rectangular sky/treetop tint band just below the waterline. Keep that defect, relevant distant-leaf fog verification and exact historical pole/leaf contexts explicit. Continue preserving native water texture, biome tint, saved preferences and practical controls.

Performance/FPS work was deferred by the user. Do not restart that measurement pass just because this roadmap mentions it. Do not interpret an empty shared pending queue as permission to implement this backlog.

## 1.7.0 — Water and reflections

**Purpose:** the next recognisable improvement in Stratus's highest-priority feature.

- Deliver a coherent, visibly improved water experience across the surface, waterline and underwater views, including shorelines and scenery reflections. Preserve native texture/biome character and the genuinely submerged-segment attenuation rule.
- Resolve the known waterline band and any reproduced hard reflection/depth transitions relevant to this milestone. Missing historical evidence remains a verification task until the original scene can be reproduced; do not invent a defect.
- Keep sky-only and detailed reflections available, with smooth missing-geometry fallback. Preserve all manual controls and preset relationships; no silent quality reductions.
- Acceptance: labelled before/after views at matched options in loaded normal-world scenes, relevant technical/package checks, control/migration checks and actual installed-release review. The milestone needs a substantial visible improvement beyond a single bug fix; otherwise ship the fix as a patch and keep the feature milestone planned.

## 1.8.0 — Atmosphere and lighting

**Purpose:** a second coherent visible upgrade while retaining Minecraft's original character.

- Refine lower-cloud shape/shading, independent cirrus, mist and sun/weather transitions only where comparison reveals a worthwhile improvement or reproducible issue.
- Preserve the native cloud/sun choices, square sun, vanilla lighting path, restrained bloom and original diffuse palette. Do not introduce cast shadows, globally glossy terrain or new artistic lighting defaults merely to justify a bigger version.
- Acceptance: clear changes in relevant day/sunset/weather and occupied-cloud views, cave/local-light checks, finite motion review and preserved controls. Reuse unchanged evidence only within the project's existing verification rules.
- If the work is only a small tuning or acceptance pass, keep a patch number; the milestone is not a reason to inflate the release.

## 2.0.0 — A coherent next-generation Stratus

**Purpose:** a clearly recognisable step forward across the complete experience, not a collection of renamed fixes.

- Integrate substantial water/reflection and atmosphere/lighting improvements into a stable visual baseline. Preserve the vanilla-dominant style, original world geometry and useful controls.
- Improve rendering organisation or algorithms where measured bottlenecks or visible limitations warrant it. Do not require a clean rewrite or introduce new rendering promises without an approved brief.
- Gate release on resolved critical visual regressions, representative actual-world review, supported-runtime loading, intact option/menu/preset coverage and safe settings migration. Publish honest limits rather than claiming universal compatibility or exhaustive acceptance.
- Once performance work is authorised again, record matched focused gameplay FPS/frame times after the existing chunk-readiness gate. Retain the approximately 60 FPS Reference goal; neither a version bump nor a preset reduction proves it has been achieved.
- Publish a clear comparison with the preceding baseline, exact verification evidence, migration notes and release captures. Showcase automation continues to select eligible versions ending in `0`, including 1.7.0 and 2.0.0.

## How this becomes work

When a relevant feature batch is requested, stage only its concrete unfinished items, use the current source and evidence, then choose the release number from the completed result. A full TASK review must still be explicitly requested. Finish one coherent batch before processing later queued batches. The roadmap itself does not queue a chat, change shader defaults or start Minecraft verification.

# Current shader task

Status: Ready for implementation. Stratus 1.6.6 is the baseline; its live visual acceptance and focused performance remain to be checked.

## Source and environment

- Shader source path: Discover the appropriate editable Stratus source in this project; `outputs/Stratus` is the current pack source.
- Pack/build: Start from the current Stratus 1.6.6 source. Main's Iris configuration selects `Stratus-1.6.6.zip`; confirm the pack actually loads before judging visuals.
- Minecraft profile: Confirm the intended profile; historically Modrinth Main.
- Reference image or scene: Use the existing project references where relevant; ask only if a missing visual reference would materially change the result.

## What I want changed

1. **Current settings as defaults:** Before changing the shader, capture the current saved options for Main's selected Stratus 1.6.6 pack. Make those values the next pack's source defaults where the same controls still apply. Keep the Reference preset available as a selectable preset; do not let it replace my preferred defaults. Preserve the current saved options file and document the exact before/after values.
2. **Polished sun:** The vanilla and polished modes look too similar. Keep the recognisable blocky Minecraft sun, but make the polished mode visibly richer with a stronger sun-local halo/bloom and realistic light falloff. Avoid raising bloom on unrelated blocks, entities or the whole scene. Preserve the vanilla mode and give me useful controls for tuning the result.
3. **Separate face shading controls:** Let me adjust vanilla face contrast and realistic directional/sky/ground contrast independently. Preserve the existing combined look as a reproducible setting and keep saved values compatible where possible. Both controls should have clear labels and meaningful ranges.
4. **Visible high clouds:** I currently cannot see the high cloud layer. First verify the active pack, `CLOUD_STYLE`, `CIRRUS_AMOUNT`, altitude and actual in-game view, then fix the visibility so high clouds appear across the sky independently of the physical lower clouds. Keep their existing coverage/altitude controls.
5. **Wet-material sheen:** Restore a visibly wet response on appropriate wet materials, including a subtle view-dependent sheen or highlights where physically plausible. Dry and non-absorbing materials should not become uniformly glossy. The current `WET_SHEEN` setting exists but only changes matte sheltered absorption; make the wet sheen effect observable and adjustable while preserving saved-setting compatibility or documenting a deliberate migration.

## Requirements

- Preserve the existing style and unrelated features.
- Check the actual in-game appearance of the sun, both face-shading components, high clouds and wet materials. Technical checks or offline previews alone do not establish that these requests look right.
- Keep all practical shader settings from the previous version available in this and future builds so I can keep tweaking them. Preserve menu access, allowed values, preset choices and saved overrides; do not remove or silently change a setting. If implementation makes a control obsolete, provide a useful equivalent and document the migration.
- Maximise shader performance without sacrificing any intended visual feature or quality. Optimise actual bottlenecks; do not silently reduce resolution, samples, draw distance or effect quality. Compare matched before/after scenes and focused frame times or FPS where possible, and clearly mark visual equivalence or speed gains unverified if they cannot be checked.
- Write a readable `work/Custom instructions/CHANGE-LOG.md` for this task. Include what changed and why, the output pack/build and its path, checks and in-game observations with evidence, any performance measurements, and remaining issues. Distinguish completed checks from pending ones. Link the log in the final reply.
- Update `work/Custom instructions/SHADER-SPEC.md` to match any completed shader changes. Keep it useful as a specification for a future clean rebuild, and distinguish the current verified build from desired or pending behaviour.

## Done when

- The requested behaviour is implemented.
- Current saved 1.6.6 option values have been recorded and applied as new source defaults where applicable, with Reference still selectable and saved preferences preserved.
- Relevant available technical checks pass.
- The previous and new setting inventories have been compared; retained controls and any migrations are documented.
- The changed scene has been visually reviewed in Minecraft, or that check is explicitly recorded as pending.
- Performance changes preserve the full intended appearance in representative matched scenes, with measured impact reported or explicitly pending.
- The change log is updated and linked in the final reply.
- The rebuild specification is updated and linked in the final reply.

## Progress and evidence

- Changes: New defaults, polished sun, separate face controls, visible high clouds and wet sheen have not been implemented. Previous 1.6.6 results are in [CHANGE-LOG.md](CHANGE-LOG.md).
- Output: No new build yet. [Stratus-1.6.6.zip](../../outputs/Stratus-1.6.6.zip) is the baseline candidate.
- Settings snapshot: Main's Iris configuration selects 1.6.6. Its saved options file currently contains `CLOUD_LAYERS=1`, `GROUND_WARMTH=0.00`, `MIST_DETAIL=2`, `REFLECTION_MODE=2`, `WATER_EXTINCTION=3.00`, `WATER_RENDER_QUALITY=2`, and `WATER_TURBIDITY=6.00`. Re-read it before editing; values may change.
- Technical checks: Not run for this new task.
- In-game visual review: Pending for this new task; confirm 1.6.6 is actually loaded before comparison.
- Performance: Not measured for this new task.
- Documentation: Update [CHANGE-LOG.md](CHANGE-LOG.md) and [SHADER-SPEC.md](SHADER-SPEC.md) with the new build and evidence.
- Remaining issues: Implement and verify the five requests above, then record any pending in-game or FPS checks.

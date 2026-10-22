# Stratus — changes for the next coding pass

Put only the changes you want worked on now under **Pending changes**. `TASK.md` is the complete shader target and remains in force for everything else. A saved file does not start work; tell the coding chat **“Apply the pending changes.”** After implementation and verification, move completed requests to **Completed changes** with the release/evidence reference. If none remain pending, leave **“No pending changes.”** Partial or unverified work stays pending.

## Pending changes

- Do not forward the setting from revious version to the next, only fordward the settings if it wern't current change related, and decide on making it the defualt to thoes presets, eg. visual based = all presets, preformance based = you decide the presets, visual and preformance based = referance preset

- optimise performance to around 60 FPS while keeping essential viausals, eg. resulution

Performance progress for 1.6.9: unused-pass/metadata work removed without quality cuts. Focused active-game river averages were 57.7 FPS before and 56.2 FPS after at 1440×842; no speedup or achieved 60 FPS claim. Forest results and rejected focus/AFK samples are in [the benchmark summary](../stratus-refine-169/performance-summary.json). Keep this request pending.

## Completed changes

### Stratus 1.6.9 — 22 October 2026

- [x] Vanilla block palette is the default lighting path; enhanced lighting and saved tuning remain selectable. Actual dry-iron crops match shaders-disabled Minecraft within one 8-bit code value.
- [x] Exposed porous and non-porous blocks receive adjustable view-dependent film in either lighting mode; clear-weather iron/glazed/granite fixtures and dry comparisons reviewed.
- [x] Removed absorption darkening and retained dampness. Existing film-strength IDs/ranges remain; `WET_DARKENING` is explicitly labelled retired and has no effect.
- [x] Restored a subtle adjustable animated native-water texture from the active atlas, with off/strong comparisons and river/underwater/waterline regression checks.

[Stratus 1.6.9 ZIP](../../outputs/Stratus-1.6.9.zip), [change log and exact evidence](CHANGE-LOG.md#22-october-2026--stratus-169), [actual Minecraft captures](../../outputs/Stratus-1.6.9-visual-checks/index.html), [install/load receipt](../../outputs/Stratus-1.6.9-install.json). Native 768 pairs, 795 component/12 output samples and ten underwater cases passed; 62 reachable controls and four preserved presets. The performance request remains above.


### Stratus 1.6.8 — 21–22 October 2026

- [x] Added a main Realistic lighting switch: Off restores the game vertex face/AO and lightmap colour/brightness, bypassing artistic brightness/colour and material recolouring. Independent face component controls remain available.
- [x] Added selectable All weather / Rain only sheen, retaining strength/dampness controls and absorbent-material/exposure gating. Main clear-weather comparisons completed.
- [x] Reorganised the existing settings into smaller two-column effect groups, guided by Iris documentation and Complementary's category/submenu organisation. All 59 prior settings/defaults/ranges and four presets remain; 61 controls total.

Built, installed, selected and actually loaded [Stratus 1.6.8](../../outputs/Stratus-1.6.8.zip). Current saved Main values were preserved and carried over; the camera, HUD/pause state and flight flag were restored and the temporary driver stopped. [Change log and verification](CHANGE-LOG.md), [actual Minecraft captures](../../outputs/Stratus-1.6.8-visual-checks/index.html), [install receipt](../../outputs/Stratus-1.6.8-install.json).

Completed items can be moved here with a link to the corresponding `CHANGE-LOG.md` entry or release. Keep partially completed or unverified items pending.

Rechecked the explicitly requested `TASK-previous-brief.md` on 21 October 2026. Its historical “not implemented” progress is superseded by the source, archive and actual runtime evidence; the archive remains unchanged as history.

- [x] Main's recorded preferred values are source defaults; original saved options remain preserved and Reference remains separately selectable.
- [x] Polished square sun has a richer local halo/core with independent controls; native mode and global bloom remain preserved.
- [x] Vanilla and realistic face components have separate controls; their default combination reproduces the previous mix.
- [x] Independent high cirrus is visible in the preserved actual Main isolation comparisons, with existing amount/altitude controls retained.
- [x] Appropriate rainy materials have adjustable view-dependent sheen; dry/non-absorbing response and saved values are preserved, with the deliberate extension documented.

At the archived-brief recheck, all five were already present in **1.6.7** source, released ZIP and installed pack; no missing code or duplicate build was needed for that brief. The subsequent approved 1.6.8 changes preserve that completed work and document their deliberate new lighting/film modes. [Implementation, visual evidence and limitations](CHANGE-LOG.md), [fresh integrity recheck](../stratus-recheck-167/recheck.json), [fresh runtime state](../stratus-recheck-167/runtime-state.txt). Broader unverified scene coverage remains described in `TASK.md` and the change log; the performance item above remains pending.

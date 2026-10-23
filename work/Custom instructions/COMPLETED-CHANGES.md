# Stratus — completed changes

Archive of completed requests and their release/evidence references. This is history, not a coding queue. Pending or unverified work belongs in [CHANGES.md](CHANGES.md).

## Completed changes

### Stratus 1.7.0-rc2 — 24 October 2026 — batch1af89474

- [x] Repaired the reproduced indoor stepped-flow pale strips/patches: native dark/black atlas-light colours retain explicit valid coverage instead of bright biome substitution. Prior-source regression fails three cases; final source passes; exact installed ZIP clean cave capture reviewed. Original screenshot location unknown; finite reproduced-geometry acceptance only.
- [x] Restored ordinary vanilla entity directional face shading while preserving lightmap, textures, emissive paths and settings. Six GPU normals and matched daylight/indoor shaders-off comparisons pass.
- [x] Installed final candidate in Main/shaderpacks, verified ZIP/source/install bytes and actual Iris loading with65 Reference values, safe selective migration and13 migration checks. Candidate remains installed; original rc1/shaders-disabled session restored; unchanged temporary QA files removed.
- [x] Completed foliage portion of hidden sheen request: material4113 is matte, including internal leaf quads visible through holes. Other solid-occluder live checks remain pending; this is whole-material exclusion, not voxel occlusion.
- [x] Implemented restrained solar-film term0.035→0.008 and preserved all controls/palette. Technical wet-film checks and limited midday panel comparison pass; additional solar/adjacent/shaded live acceptance stays pending.
- [x] Restored native underwater atlas/light/biome/alpha with smooth zero/half/full WATER_TEXTURE response. GPU alpha/exit/transmission cases and reviewed submerged views including exact release ZIP pass; full native waterline/glass and Stratus-mode live regression remain pending.
- [x] Avoided exact-zero underwater atmosphere reconstruction with equal controlled output and measured narrow GPU-pass work reduction. Overall FPS/sustained lag target remains pending and explicitly deferred; no game-speedup claim.

[Release](../../outputs/Stratus-1.7.0-rc2.zip) · [Change log and scope](CHANGE-LOG.md#24-october-2026--stratus-170-rc2--targeted-repair-candidate) · [24 actual comparisons](../../outputs/Stratus-1.7.0-rc2-visual-checks/index.html) · [Install/load](../../outputs/Stratus-1.7.0-rc2-install.json). Remaining requests stay in `IN-PROGRESS/1af89474-f56a-4419-bc73-7f12d4950cfa/CHANGES.md`; earlier batches unchanged.


### Stratus 1.6.12 — 23 October 2026

- [x] Completed the whole-surface tint portion: native animated water texture/biome tint visibly covers the whole water surface, including distant and reflection-dominated views; zero disables the added treatment. Reflections/refraction, shallow-bed clarity, water paths and every control/range/preset quality choice remain. Passed technical/installer/Iris checks and finite matched Main river/grazing/downward/underwater/preset/fixture/waterline review. The pre-existing below-surface rectangular tint band remains unresolved; the original request’s remaining waterline acceptance is kept pending in its active batch. FPS and the original unknown pole/leaf contexts also remain pending.

[Release](../../outputs/Stratus-1.6.12.zip) · [Change log and limits](CHANGE-LOG.md#23-october-2026--stratus-1612) · [Actual visual comparisons](../../outputs/Stratus-1.6.12-visual-checks/index.html) · [Install/load receipt](../../outputs/Stratus-1.6.12-install.json).

### Stratus 1.6.11 — 22 October 2026

- [x] Adopted the captured latest Main visual **and quality** tuning as Reference/source defaults, by explicit user choice. All four presets share 56 visual defaults; six quality settings are ordered below/at/above Reference. All 62 IDs, allowed values and menu paths remain; High retains full detailed optics. Actual Iris reports Reference with zero overrides and all62 values match the approved capture.
- [x] Extended selective migration to preserve later related manual edits and removal of an old override, alongside unrelated tuning and existing new-version settings. Ten temporary-profile checks pass; old Main settings remain intact.
- [x] Completed the occupied-cloud interior and clearer independent cirrus/day/sunset portions of the prior verification request. The active cloud texture confirms an occupied alpha255 cell; accepted on/off views were chunk-gated. Unloaded initial attempts are labelled rejected/superseded. The distant-foliage and original pole/leaf checks remain pending in CHANGES.md.

[Stratus1.6.11 ZIP](../../outputs/Stratus-1.6.11.zip), [change log and evidence](CHANGE-LOG.md#22-october-2026--stratus-1611), [actual captures](../../outputs/Stratus-1.6.11-visual-checks/index.html), [install/load receipt](../../outputs/Stratus-1.6.11-install.json). Native768 pairs, ten underwater cases and four62-option Iris profile checks passed. The readiness barrier was live-checked without FPS; actual FPS integration and60FPS acceptance are explicitly deferred by the user. No new rendering-algorithm speedup is claimed.


### Stratus 1.6.10 — 22 October 2026

- [x] Selective settings migration: carry unrelated latest overrides only, reset approved related keys, preserve every old file and existing new-version preferences. Approved 1.6.9 colour/film/water-texture visual defaults apply explicitly in all four presets; future mixed visual/performance defaults belong to Reference unless approved otherwise. Actual Main migration preserved eight unrelated overrides and reset the related film override; nine integration checks pass.
- [x] Existing `REFERENCE` preset now reads **Reference (Recommended)** in Iris. All 62 IDs/defaults/allowed values/menu access and the original six quality assignments per preset remain.
- [x] Finite water review in Main: river/shallow/deep/waterline, waterfall/background water, submerged wood, glass, visible particles and shoreline/screen-edge reflections. Ten current-source underwater GPU regressions also pass. This does not close the exact historical pole issue.
- [x] Finite clear/rain material, sealed cave/local-lamp/night and polished/native sun review, preserving the working 1.6.9 design. Limited/rejected capture attempts are labelled separately.

[Stratus 1.6.10 ZIP](../../outputs/Stratus-1.6.10.zip), [change log and exact evidence](CHANGE-LOG.md#22-october-2026--stratus-1610), [actual captures](../../outputs/Stratus-1.6.10-visual-checks/index.html), [install/load receipt](../../outputs/Stratus-1.6.10-install.json). Installed, selected and loaded in Main; original camera/HUD/pause/flight, weather/daylight and temporary blocks restored. Performance and the remaining verification gaps stay above.


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

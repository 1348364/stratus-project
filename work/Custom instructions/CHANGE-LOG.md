# Stratus change and output log

## 24 October 2026 — Stratus 1.7.0-rc2 — targeted repair candidate

### At a glance

- Repaired pale cave-water strips and native entity face shading; restored adjustable native underwater atlas; made foliage matte and reduced the excessive solar film lobe. All65 controls/defaults/ranges/menu paths and preset assignments preserved.
- **[Candidate ZIP](../../outputs/Stratus-1.7.0-rc2.zip)** installed and actually test-loaded in Main, with exact source/archive/install bytes and all65 Reference values verified. [Install/load receipt](../../outputs/Stratus-1.7.0-rc2-install.json), [24 reviewed comparisons](../../outputs/Stratus-1.7.0-rc2-visual-checks/index.html).
-768 final native pairs, targeted GPU checks and13 migration checks pass. Finite visual acceptance only; additional solid-occluder, solar-angle and waterline/glass checks remain pending. Focused FPS explicitly skipped; no sustained-lag fix or60FPS claim. Original session and temporary test world edits restored and verified.

Batch: [1af89474 active brief](IN-PROGRESS/1af89474-f56a-4419-bc73-7f12d4950cfa/CHANGES.md). Frozen delta only reiterated the recorded stable/candidate reference distinction; no extra shader behaviour staged. Shared next queue and immutable target snapshot unchanged. TASK, shared queue, change log and completed archive matched initial fingerprints before reconciliation; the active brief differed only by this run's staging. No newer-edit conflict found. Earlier pending batches remain separate.

### Changes and diagnosis

Eight shader files are listed in `work/stratus-170-rc2/source-changes.json`; exact diff in `changes.diff`. `water-resolve.frag.glsl` previously replaced valid low-luminance native water colours with a bright biome fallback. The user cave screenshots11.29.58 and11.17.06 informed the controlled enclosed stepped-flow reproduction. Prior GPU source fails all three dark-cache cases; alpha-based validity now preserves dark and black colours and skips absent cache. Final ZIP cave view removes the pale strips/patches. Exact original cave location was not recovered; no exhaustive shoreline/waterfall certification.

`raster.frag.glsl` restores native underside atlas × biome/vertex/lightmap colour, with WATER_TEXTURE-scaled alpha and matching forward transmission. HDR/display-space inversion preserves the native alpha-blend result against the opaque background. Stratus mode retains clear exit. Submerged-only fog intentionally differs from vanilla; full waterline/glass layering acceptance remains pending. `lake.frag.glsl` also scales missing-background transmission by local sky exposure; the superseded v2 image proves that adjustment alone did not remove the cave strips.

New `entity-lighting.glsl` restores the native two-direction diffuse factor for ordinary vanilla-lighting entities in `raster.vert.glsl`, without double-shading terrain. Six face normals and matched daylight/indoor sheep comparisons pass; native lightmap warmth and separate emissive paths remain. Arithmetic checked against the actual installed Minecraft1.21.11 light.glsl and Iris ShaderSynthesizer; no game textures/assets redistributed.

Leaf/plant cutout material4113 is excluded from film metadata. This intentionally makes the whole material matte rather than estimating only internal leaf faces; it adds no cast shadows or voxel occlusion. `diffuse.glsl` solar-film gain0.035→0.008 preserves sky film, diffuse palette and all controls. Close leaf quads visibly lose sheen; limited midday quartz views show modest reduction without washed texture. These are not proof of maximum solar highlight or all solid occluders; those remaining gates stay pending.

`atmosphere-resolve.frag.glsl` returns the existing scene underwater where the atmosphere producer already guarantees zero, avoiding unused depth/bilateral reconstruction. No extra pass, lower quality setting or control removal. All65 options retained; related WATER_TEXTURE default migration only, preserving unrelated overrides, later manual choices and existing new-version preferences.13 migration checks pass. `lang/en_us.lang` clarifies underside texture strength. Package documentation distinguishes candidate status and finite evidence.

### Actual verification and limits

Evidence under `work/stratus-170-rc2/`: `compile-final-v3.log`768 native compile/link pairs,0 failures; `raster-final-checks.json`13 geometry/entity cases,0 failures/API errors; `wet-checks.json`96 samples across six normals/weather/shelter/zero,0 failures; `native-water-final-v3.json` and `legacy-water-final-v3.json` ten resolve cases each,0 failures; `dark-native-before.json` three deliberately reproduced failures versus `dark-native-after.json` three passing cases. Native harnesses do not emulate all Iris transforms or establish appearance. `control-checks.json` confirms65 reachable options, original defaults/ranges/preset assignments,620 material tokens and tooltips retained. Actual loaded Iris parses/matches all four65-option profiles (`iris-profile-checks.json`).

`atmos-performance.json`: matched actual single-pass underwater zero-volume GL_TIME_ELAPSED measurements at512² with equal output. Seven batches include warmup/outliers; typical later before about0.022ms, after about0.010ms. This is a narrow GPU result, not Minecraft FPS. Sodium entity/block-face culling already enabled; existing fog-occlusion choice preserved. Primary references: [Sodium visibility culler](https://github.com/CaffeineMC/sodium/blob/dev/common/src/main/java/net/caffeinemc/mods/sodium/client/render/chunk/occlusion/OcclusionCuller.java), [GL timer queries](https://registry.khronos.org/OpenGL/extensions/ARB/ARB_timer_query.txt), [application-owned buffer swapping](https://www.glfw.org/docs/latest/window). A shader pack cannot implement the requested progressive unfinished-frame presentation. No renderer/mod/presentation changes made.

Actual Main / Stratus Terrain Lab, Minecraft1.21.11, Iris1.10.8, Sodium0.8.14, Apple M1,1440×842, render distance12: matched cave, underwater zero/half/full, foliage and daylight/indoor entity images individually reviewed. Exact final release cave and river-underwater captures plus `runtime-v3-Optional_Stratus-1.7.0-rc2.zip_.txt` prove final ZIP loaded with Reference values. Several local-fixture views could not maintain the stable five-second chunk gate while locked/unfocused; camera/pipeline checks and complete local meshes support only finite target views. Background rectangular terrain/mist cutouts are excluded from acceptance. A camera inside solid leaves was rejected and replaced with an outside view through cutout holes. The supposed larger solar pad was not loaded by its command; panel captures are only the existing quartz wall top. No maximum-angle claim. Scheduling waits are not readiness proof. The user skipped unlocking for focused FPS; zero FPS samples. Known rectangular waterline defect and earlier native/transparent compatibility gates remain pending.

Gallery contains only24 individually inspected captures and hashes, with superseded diagnostic frames labelled. Saved HTML/manifest checked; gallery is not claimed browser-rendered. Final ZIP248 entries, SHA256 `ba966b25c3160e2d325dbb8627634afa274dbaa37175dfc67a51e7a85b9cca2c`; `final-audit.json` checks ZIP integrity and every archive/source byte against installed archive. Prior deliverables preserved. rc2 remains installed, while original rc1 selection with shaders DISABLED is restored after QA.

### Restoration and remaining work

Original restore helper used an unavailable UUID lookup and failed before clearing the fixture. A follow-up approval check initially failed because the workspace lacked credits; no bypass occurred. On continuation normal approval succeeded. Reflection discovered the actual server UUID lookup; first recovery was stopped by an unloaded fixture. Loading the four bounded test chunks allowed exact restoration. All3042 originally-air blocks match the saved snapshot; uniquely identified sheep is absent. Original exact position/pitch and equivalent wrapped yaw, HUD/menu/pause/flight, Iris config and world/time/weather bytes are verified (`restoration-checks.json`, `fixture-restored.txt`, `recovery-uuid-methods.txt`, `final-client-state-v2.txt`). The first camera readback revealed wrong angles, corrected by a guarded original-position teleport and a fresh readback. All three helper stop markers exist.26 owned QA files removed after archive/effective-option equality; six normalised settings files already absent; no changed file removed (`qa-cleanup.json`). Failed attempts remain recorded as historical evidence.

Completed finite portions moved to COMPLETED-CHANGES.md. Remaining in this active batch: blocked/exposed solid live film comparison; fuller solar-angle/adjacent/shaded film-off/on; native waterline/glass and Stratus-mode live regression; matched focused steady-state performance/25FPS investigation and unsupported progressive presentation. The current rc2 is usable as a candidate, not full acceptance of those requests or the1.7 milestone.

## 23 October 2026 — Stratus 1.7.0-rc1 — implementation candidate

### At a glance

- Implemented selectable native water/underwater medium, stronger exposed-face film and original transparent-solid optics. New source has65 reachable controls; every previous62 default/range and original preset quality assignment remains.
- Packaged **[Stratus1.7.0-rc1](../../outputs/Stratus-1.7.0-rc1.zip)** — **candidate only**. [Packaging receipt](../../outputs/Stratus-1.7.0-rc1-receipt.json), [11 reviewed captures](../../outputs/Stratus-1.7.0-rc1-visual-checks/index.html). Final release ZIP is not installed, selected or loaded. Shader-equivalent temporary v3 QA variants loaded; stable1.6.12 and original session restored afterwards.
- Passed768 final native program pairs,96 wet-film GPU samples,24,576 transparent-optics probe pixels,ten physical/ten native underwater cases,13 installer checks and Iris parsing/matching of all four65-value profiles. **Remaining live checks skipped by user; all four requests stay pending. Known waterline band remains. No FPS sampled.**

Batch: `IN-PROGRESS/43b4c0ad-c217-4a82-8534-29d34345f150/CHANGES.md`. No later batch or shared next queue was consumed. Frozen delta only repeated earlier1.6.12 reconciliation and required no duplicate work. Current TASK/change log/archive matched initial fingerprints before reconciliation; only this run's earlier staging changed the batch brief. No conflicting newer edits were found. The completed archive is unchanged because no full request passed every required gate.

### Implementation and deliberate limits

- Water: new `WATER_STYLE` selects game atlas RGBA × actual vertex biome colour/lightmap and game environmental fog colour/range, or the retained physical Stratus medium. Native mode is default in every preset. The native alpha layer is composed at full resolution after the selected optics buffer reconstruction, preserving atlas detail without increasing optical quality settings. Stratus mode retains the1.6.12 whole-surface patterned biome treatment. Existing clarity/extinction/turbidity/biome override controls remain reachable, retain their full ranges and have explicit mode-specific tooltips. Actual submerged distances and nearest exit/glass/additive composition remain.
- Film: per-face drainage retains top/side/underside response, a higher but bounded view-dependent film floor and broader roughness-dependent highlight. Exposure/shelter, weather, independent film/sheen zero controls and native diffuse palette remain. No extra pass or scenery tracing added for film.
- Transparent solids: new `TRANSPARENT_REFLECTIONS`/`TRANSPARENT_REFRACTION` independent controls. Existing translucency captures nearest mapped glass/stained/tinted glass and panes, ice/slime/honey face-normal/depth metadata into one additional RGBA16F buffer. A thin-interface approximation runs in the existing atmosphere resolve, with interface/depth/edge guards, bounded displacement and selected scenery quality/sky fallback; cave sky fallback is limited by sky exposure. No water waves, particle/foliage/entity material capture or full-volume dielectric claim. Overlapping transparent layers and foreground particles have nearest-interface/screen-space limits; live coverage remains unverified.
- Design reference: [Sildur’s Enhanced Default official site](https://sildurs-shaders.github.io/) and [official changelog](https://sildurs-shaders.github.io/changelogs/). Original Stratus implementation, no third-party shader source copied. Running Minecraft1.21.11 fog GLSL and Iris environmental uniforms were inspected locally; no native textures/shader assets redistributed.
- Version choice: these are substantial new features, so use minor-version **release candidate1.7.0-rc1**, not another patch or a claim the full roadmap milestone passed. Temporary QA names retain the earlier development prefix1.6.13; their shader byte equivalence to the candidate archive is recorded.
- Changed16 shader files listed in `work/stratus-refine-1613/source-changes.json`; exact diff in `changes.diff`. Includes material mapping, water/raster/medium/resolve, exposed-film logic, transparent helper, bloom metadata guard, properties/options/English labels. No fullscreen pass or quality reduction added. There is one additional full-resolution metadata buffer; memory/performance impact is not measured.

### Verification actually performed

- `work/stratus-refine-1613/compile-final.log`: Apple M1 OpenGL4.1 / GLSL330 compatibility-shim native compile/link,768 pairs,0 failures. Final shader source; offline result does not emulate Iris transforms or prove appearance.
- `wet-checks.json`: actual wet GLSL,96 samples across six normals, shelter/weather and zero settings,0 failures/API errors. `glass-checks.json`:24,576 actual transparent-helper GPU pixels, independent-control and no-interface/foreground guards,0 failures/API errors;814 interior pixels changed with either reflection or refraction independently.
- `legacy-water-final-checks.json` and `native-water-final-checks.json`: ten actual full-resolution resolve cases each, including exits, submerged geometry, sky, glass and additive contribution;0 failures/API errors. Native expected fog follows game linear environmental range and display transfer. These are controlled inputs, not live fog-status/glass acceptance.
- `control-checks.json`:65 reachable options, prior62 IDs/defaults/ranges and all four original preset assignments retained, all618 original block tokens retained plus slime/honey. `iris-profile-checks.json`: actual loaded Iris parses/matches all four65-option profiles when fully applied. This is read-only matching, not four new live preset captures. `migration-checks.json`:13 temporary-profile checks,0 failures.
- `RELEASE-POLICY.json`: new controls use defaults where absent from old preferences; WATER_TEXTURE selectively resets only the captured related value. Unrelated wet/quality overrides and later manual water/unknown-new-control values carry forward. Prior and existing new-version preferences are never overwritten. No Main candidate migration was performed.
- `package-checks.json`:247 ZIP entries, archive/source byte equivalence, all final v3 QA shader bytes match and original1.6.12 ZIP SHA preserved (`5232c270a31de108ba862135e0f4a6bedaba16e011c2ec1b44a651f7a50c44e2`). Candidate SHA is `3ba73a5413a86ec9cc6e220f6ab016709fd559a19648ae325872721ab0e6ff35`.
- Actual Main / Stratus Terrain Lab, Minecraft1.21.11, Iris1.10.8, Sodium0.8.14,1440×842, render distance12, clear/time1000: shaders-off river/submerged views, isolated native river, Reference near/far/submerged/waterline and v2 legacy river reviewed. Loaded-column/mesh readiness gates and camera/pipeline assertions precede accepted captures; texture/cloud/particle animation differs. Native surface colour/texture is close to vanilla; v2 texture softness was corrected by v3 full-resolution composition. No pixel-equivalence claim with extra Stratus optics/atmosphere. Underwater retains the prior straight-through exit and omits vanilla's blue back-face atlas overlay, so the above-water portion of a submerged view differs deliberately.
- v1 QA Iris load failed on scalar `vec4(0.0)` clear parsing. Four-component explicit clear fixed it; rejected capture queue was stopped. Final native compilation and actual v3 Iris loading pass. The known rectangular blue/sky/treetop waterline band remains visible; **failed waterline acceptance**, consistent with the prior baseline defect.
- A report browser-render attempt was blocked because its file URL protocol is disallowed. No workaround attempted. The HTML/manifest and source image hashes were checked; all11 original Minecraft images were individually inspected. The saved gallery is not claimed browser-previewed.

### Restoration and still pending

The user answered **skip** to unlocking the Mac for remaining live checks. The remaining route was cancelled; no new wet/transparent/biome acceptance or FPS run followed. Guarded helpers restored original camera (within0.0001 blocks, equivalent wrapped yaw), HUD, pause, flight and all original daylight/weather flags/timers. Main again actually loads original1.6.12 with the original62 effective values. No temporary fixture blocks were placed. Both long-lived helpers stopped;58 owned temporary QA files removed only after archive/effective-option comparison, preserving later edits. Exact receipts: `restoration-checks.json`, `qa-cleanup.json`, `restored-world-state.txt`, `final-client-state-v2.txt`, `runtime-v3-Optional_Stratus-1.6.12.zip_.txt`. Read-only fixture scanning returned no relevant material positions in the bounded region; it made no block edits and is not visual evidence.

All four active requests stay pending for their remaining live gates: side/underside/sun/rain/cave wet-film off/on; actual glass/stained/tinted/pane/ice/slime/honey controls-off and layering/particle/water checks; native water biome/status/night-vision/resource-pack compatibility, menu/motion and final exact ZIP loading. The waterline band remains unresolved. Prior historical pole/leaf/distant-fog work stays in its earlier batch. FPS/60FPS and performance claims remain explicitly deferred. See the active batch PROGRESS.md for the precise resume point; no completed request was moved to the archive.

## 23 October 2026 — Stratus 1.6.12

### At a glance

- Native animated water texture and biome tint now cover the whole visible water surface, including distant/grazing reflections. Clear optics at zero, shallow-bed visibility and sharp reflection detail remain.
- Built **[Stratus1.6.12](../../outputs/Stratus-1.6.12.zip)**; installed, selected and loaded in Main. All62 controls/defaults/ranges/menu paths and four approved preset assignments are preserved. [Receipt](../../outputs/Stratus-1.6.12-install.json), [actual comparison gallery](../../outputs/Stratus-1.6.12-visual-checks/index.html).
- Passed768 native pairs,192 actual surface-GPU samples,ten underwater cases,ten installer checks and actual Iris matching of all four62-option profiles. Finite loaded-world water/preset/fixture views reviewed. **FPS remains explicitly deferred; no speedup or60FPS claim.**

### Scope, source and compatibility

Studio `stage_run` **7a6a15fb-dcb6-4313-94d3-7a32fb13dd79**, working only in its [active batch](IN-PROGRESS/7a6a15fb-dcb6-4313-94d3-7a32fb13dd79/CHANGES.md). The frozen TASK delta repeats completed1.6.11 preset/readiness reconciliation; no duplicate rebuilding or additional feature work was invented. The shared next unsent CHANGES.md is untouched. [Snapshot comparison](../stratus-refine-1612/snapshot-comparison.json), [baseline audit](../stratus-refine-1612/baseline-audit.json).

`lake.frag.glsl` now combines reflection/transmission before applying `water-surface.glsl`. Native atlas luminance already carried by the existing raster pass combines with active biome colour in a bounded multiplicative surface treatment. There is no distance cutoff, extra texture read, pass, opacity change, added light or reflection blur. Fresnel weights/tracing, refraction, water paths and the underwater bypass remain. `WATER_TEXTURE` keeps its ID/range/default1.00 in every preset; only its tooltip changes. This explicitly supersedes the old transmission-only wording, as authorised in the brief. [Source diff](../stratus-refine-1612/changes.diff), [options audit](../stratus-refine-1612/option-audit.json).

Only WATER_TEXTURE is release-related for migration. The installer carries unrelated latest overrides and later manual water choices differing from the captured1.00 baseline; existing new-release preferences win. All previous archives/preferences are preserved. [Policy](../../outputs/Stratus/RELEASE-POLICY.json), [ten migration checks](../stratus-refine-1612/migration-checks.json).

### Verification and limits

The whole-surface tint portion is verified separately from a pre-existing waterline defect. At feet164.5,61.24,40.5/yaw0/pitch0, matched1.6.11 and1.6.12 captures reproduce a rectangular sky/treetop tint band just below the surface. It remains pending in the active brief; no all-waterline acceptance is claimed. [Repro/evidence](../stratus-refine-1612/waterline-issue.json).

- [Native log](../stratus-refine-1612/compile.log):768 compatibility-shim compile/link pairs/eight variants/three dimensions/zero failures. Separate from Iris runtime proof.
- [Surface GPU](../stratus-refine-1612/surface-checks.json):192 actual GLSL samples across zero/half/max/biome-off; identity, bounded HDR/black, continuous strength, contrast, native pattern response and biome-off independence. [Underwater GPU](../stratus-refine-1612/water-checks.json):ten real water-resolve cases, zero failures/API errors.
- [Actual Iris profiles](../stratus-refine-1612/iris-profile-checks.json):all four exact62-value maps parsed/matched. Live views include matched old/zero/half/max river, close and grazing on/off,90° downward, underwater/air exit, all presets, existing wood/waterfall/underwater fixtures and waterline positions. Original framebuffer captures and review notes are in the gallery manifest. Animation differs between captures; no pixel-equivalence claim. Active VanillaTweaks has no water replacement; arbitrary alternate resource packs and exhaustive weather/motion/mod coverage are not certified.
- Actual view-distance disk loading/empty work queues and stable counts≥5seconds gated captures. Initial flight-transition camera drift was rejected before screenshot; retry set flight first. No BENCH command was allowed by this run’s driver. Captures were unfocused and are visual evidence only. [Live context](../stratus-refine-1612/live-context.json), [readiness trace](../stratus-refine-1612/chunk-readiness.jsonl).
- [Restoration](../stratus-refine-1612/restoration-checks.json):original current-session camera/HUD/pause/flight and weather/daylight/timers restored, polling stopped and only own QA copies removed. Four temporarily replaced fixture blocks were read back as their exact original water states. The old helper block-setter method was unavailable; the existing server-command recovery restored and verified all four blocks. Its stopped/error/recovery evidence is retained.

Release SHA256: `5232c270a31de108ba862135e0f4a6bedaba16e011c2ec1b44a651f7a50c44e2`; 246entries / 236runtime assets. [Final audit](../stratus-refine-1612/final-audit.json). Remaining performance/FPS and intended historical leaf/pole checks stay pending in the active batch; its path is authoritative for this request.

## 22 October 2026 — Stratus 1.6.11

### At a glance

- Reference/source defaults now use the user's explicitly approved Main visual **and quality** tuning. All four presets share56 visual settings with six ordered quality choices. All62 controls/ranges/menu access remain; High retains full detailed optics. The installer preserves later manual edits.
- Built **[Stratus1.6.11](../../outputs/Stratus-1.6.11.zip)**, installed, selected and loaded in Main. Iris reports **REFERENCE / zero overrides**; all62 runtime values match the captured Main baseline. [Receipt](../../outputs/Stratus-1.6.11-install.json), [18 labelled actual captures](../../outputs/Stratus-1.6.11-visual-checks/index.html).
- Passed768 native pairs, ten underwater cases, ten migration checks and actual Iris interpretation/matching for all four62-option profiles. The readiness barrier blocked while work was pending and waited for stable loaded chunks. Occupied-cloud and clearer independent cirrus/day/sunset views passed finite review. **FPS/60FPS and remaining leaf/historical acceptance stay pending by explicit user deferral.**

### Frozen request and approved scope

Stratus Studio `stage_run` **d5f466f4-5927-4054-a65f-6a32e48779c1**. Current TASK/CHANGES matched their frozen snapshots at start. The nonempty TASK diff only repeats completed1.6.10 reference/migration/optimisation/evidence reconciliation, so no duplicate source work was invented. Existing pending requests supplied the new preset and chunk-readiness work. [Staging record](../stratus-refine-1611/staging.json).

The preset request conflicted with TASK's old full-resolution detailed-Reference definition. The user explicitly chose **“Adopt my current visual and quality choices as Reference”**. This deliberate baseline change supersedes that definition. It is not an equivalent-quality code optimisation and must not be compared with old full-detail Reference as a speedup. The user later said **“skip for now, i will request this later”** for FPS; no FPS samples were taken.

Main preferences changed during the initial reads. Preserved both snapshots and captured the latest saved tuning for the approved baseline; later related manual edits are protected during migration. No newer project-document edits were overwritten. During this run, newer CHANGES/root/local AGENTS wording added a durable IN-PROGRESS batch workflow. It was preserved verbatim. This earlier frozen request names no batch, and no d5f466f4 batch directory exists; its remaining items stay in the shared CHANGES pending queue under the explicit legacy request. Saving those newer workflow files was not treated as another execution trigger. [Initial settings snapshot](../stratus-refine-1611/Main-initial-tuning-snapshot.txt), [approved captured settings](../stratus-refine-1611/Main-before-Stratus-1.6.10.zip.txt).

### Presets and compatibility

Fourteen source defaults change to captured Main values. All56 non-quality visual values are explicit in every profile; quality is ordered componentwise Fast≤Balanced≤Reference≤High:

| Preset | Water/atmosphere quality | Clouds/mist | Reflection/refraction quality |
| --- | --- | --- | --- |
| Fast |0/0|1/1|0/0|
| Balanced |1/1|1/2|0/0|
| Reference |1/1|2/3|0/1|
| High |2/2|3/3|2/2|

Reference uses balanced-resolution water/atmosphere, sky-only reflection and balanced refraction. High retains full-resolution detailed scenery/refraction; every prior manual quality choice remains available. Common visual values include the user's film0.65, water visibility2.2/extinction0.9/turbidity3, ripple height0.55/size0.40/rate1 and water texture1. Exact complete values remain in source and machine-readable policy, not a duplicated TASK inventory.

Only `shaders/core/options.glsl` and profile assignments in `shaders/shaders.properties` change at runtime. Rendering algorithms, pole filter, resource texture handling, option IDs/allowed values, menus and language controls are unchanged. `install.py`, policy, package version and release documentation are updated. [Option audit](../stratus-refine-1611/option-audit.json), [source inventory](../stratus-refine-1611/source-changes.json), [diff](../stratus-refine-1611/changes.diff).

The migration resets fifteen related changed-default/quality keys to the captured Reference defaults. Actual old preferences had14 overrides, all promoted to identical source defaults; no unrelated override was discarded. The old file remains byte-identical to its pre-install snapshot, and Iris now recognises Reference with zero overrides. Future later manual values differing from the capture, including removal of an old override to return to its previous source default, are carried forward. Existing new-version settings and conflicting archives are never overwritten. [Dry run](../stratus-refine-1611/install-dry-run.json), [ten migration checks](../stratus-refine-1611/migration-checks.json).

### Chunk readiness and deferred performance

Added an actual-data readiness barrier to the saved QA driver: all columns in the configured view-distance disk must be present; Sodium scheduled jobs, busy workers, pending uploads/task lists must be empty; loaded-column/section counts must remain stable≥5seconds. At render12 the required disk contains441 columns. Runtime traces include many not-ready observations with pending work, followed by successful gates; each accepted gated capture followed that barrier. A fresh gate is required at future BENCH start, with cheaper queue/count/camera monitoring during samples and focus/size checks. [Barrier checks](../stratus-refine-1611/chunk-gate-checks.json), [raw trace](../stratus-refine-1611/chunk-readiness.jsonl), [driver source](../stratus-refine-1611/agent/Visual1611Driver.java).

**No FPS sampling was performed**, as explicitly requested. FPS integration/renewed-loading rejection still needs a later requested run. The approximately60FPS target is unverified on the newly approved Reference. Old1.6.10 full-detail results used a different baseline and establish neither new performance nor a code speedup. No new rendering-algorithm optimisation is claimed. [Performance status and exact next check](../stratus-refine-1611/performance-summary.json).

### Verification and actual visuals

- Native macOS compatibility-shim compile/link: **768 pairs/eight variants/three dimensions/zero failures**, separate from Iris loading. [Log](../stratus-refine-1611/compile.log).
- Current-reference underwater resolve: **ten cases/zero failures/API errors**, covering air exits, shallow/deep receivers, glass, particles and vertical exit. Expected optics use the approved new visibility/extinction/turbidity. [Results](../stratus-refine-1611/water-checks.json).
- Actual installed Iris parses62 assignments in each profile and matches each after applying its declared map. All62 final runtime values equal the approved Reference defaults. Actual root/Performance/Materials pages show Reference(Recommended), intended quality and Moderate film. [Iris profile checks](../stratus-refine-1611/iris-profile-checks.json), [final runtime](../stratus-refine-1611/runtime-v3-Optional_Stratus-1.6.11.zip_.txt).
- Matched62-option baseline/candidate river, final release river/underwater and loaded submerged fixtures were inspected. Water animation varies; no screenshot pixel-equivalence claim.
- Occupied-cloud camera: eye altitude256 at active cloud-cell(22,1), sampled alpha255 from the **actual running resource**; mist/cirrus disabled and drift0 isolate the occupied lower cloud. The private reference matches the active vanilla footprint. No Minecraft texture is bundled. [Camera/resource evidence](../stratus-refine-1611/cloud-interior-camera.json).
- Clearer independent cirrus remains visible with lower clouds/mist off. Chunk-gated on/off day and sunset comparisons were inspected; matched sky ROI mean absolute differences are about23.5/22.8 RGB codes. Initial incomplete-terrain attempts are rejected/superseded. [Finite comparison](../stratus-refine-1611/cirrus-comparison.json), [labelled captures](../../outputs/Stratus-1.6.11-visual-checks/index.html).

Relevant exact-depth distant-leaf fallback acceptance, original pole/leaf contexts and exhaustive preset/mod/weather/motion coverage remain pending. Those gaps are not rewritten as completed behaviour.

### Build, restoration and queue reconciliation

ZIP **245 entries/235 runtime assets**,7,780,712 bytes; SHA256 `252e040c62f5be4847814a3227fab06924d46e875f54b67a7d3e60bf58462e62`. Every archive/source byte and manifest hash passes; immutable candidate runtime equals release runtime. The installed hash matches and IrisRenderingPipeline is loaded. Previous1.6.10 archive remains byte-identical. [Package checks](../stratus-refine-1611/package-checks.json).

Original latest camera restored within0.00003block, orientation within0.000004degrees modulo360, original HUD/pause/flight/menu restored. Original daylight1000, rain0 and all weather/thunder timers/flags restored and verified; no fixture block was changed. The first test helper hit a loaded-class version mismatch; only its own class was briefly patched to stop, restored, and replaced by a uniquely versioned working helper. No Minecraft/Iris classes were patched. All helper threads are stopped. Temporary Main QA copies were removed only after byte/default-equivalence checks and backups; old release/settings and workspace evidence are preserved. [Restoration checks](../stratus-refine-1611/restoration-checks.json), [cleanup](../stratus-refine-1611/qa-cleanup.json).

Reconciled TASK with the explicitly approved preset definition and current actual evidence. Moved verified preset/migration and occupied-cloud/cirrus portions into the separate **[COMPLETED-CHANGES archive](COMPLETED-CHANGES.md#stratus-1611--22-october-2026)**. CHANGES remains pending-only: performance/FPS integration is deferred, and leaf/historical scenes remain open. [Reconciliation](../stratus-refine-1611/reconciliation.json). No other chat was messaged.


## 22 October 2026 — Stratus 1.6.10

### At a glance

- Added a change-aware installer and explicit visual defaults in all four presets. Main retained eight unrelated overrides and reset the approved related film override. **Reference (Recommended)** now appears in Iris; all 62 controls and original quality assignments remain.
- Built **[Stratus 1.6.10](../../outputs/Stratus-1.6.10.zip)**, installed, selected and loaded in Main. [Receipt](../../outputs/Stratus-1.6.10-install.json), [41 labelled actual captures](../../outputs/Stratus-1.6.10-visual-checks/index.html). Original client state, weather/daylight and four temporary blocks restored; all test helpers stopped.
- Passed **768 native pairs**, matched tracer checks over **344,064 pixels per variant**, atmosphere over **131,072 pixels**, **ten underwater cases** and **nine installer integration checks**. Finite water/material/night/sun/menu/cloud views reviewed. Focused full-Reference means: **river19.6→20.2FPS**, **forest17.8→18.1FPS**. The **approximately60FPS target and remaining cloud/original-issue acceptance stay pending.**

### Authority, target audit and newer edits

User-authorised `run_both` **dfc0d10a-85ec-429d-ab34-b70c4ce76c83** covers pending CHANGES plus genuinely unfinished TASK requirements. Audited75 target clauses against released1.6.9 runtime/source and existing evidence; preserved working features instead of rebuilding them. Staged settings migration, the Reference label and performance as implementation work, and broader scene gaps as verification only. [Target audit](../stratus-refine-1610/target-audit.json), [staging](../stratus-refine-1610/staging.json).

CHANGES was edited after queueing to make the60 FPS target explicitly **Reference**. Preserved that newer wording and used full Reference for tracing diagnostics and QA. TASK matched its frozen snapshot before reconciliation. User separately approved applying the intended1.6.9 colour/film/water-texture defaults to every preset. No other chat was messaged.

### Implementation and compatibility

`install.py` and `RELEASE-POLICY.json` implement selective migration. The nine related keys are REALISTIC_LIGHTING, EXPOSURE, WHITE_BALANCE, SURFACE_SATURATION, SURFACE_DAMPNESS, WET_SHEEN, WET_DARKENING, WET_WEATHER_MODE and WATER_TEXTURE. Explicit visual defaults apply to FAST/BALANCED/REFERENCE/HIGH. The original six quality assignments in each profile are unchanged. Future mixed visual/performance defaults use Reference unless approved otherwise; equivalent-work optimisations apply to every preset without quality cuts.

The installer supports dry-run and an explicit previous settings path, validates the archive, uses atomic create-without-replace, refuses conflicting existing/concurrently created ZIPs, and never overwrites old or existing new-version settings. It does not select Iris or claim loading. Manual ZIP copying does not perform migration. Actual install used the latest1.6.9 settings explicitly because QA packs were temporarily selected. It carried CLOUD_LAYERS2, MIST_DETAIL3, REFLECTION_MODE0, REFRACTION_QUALITY1, SKY_AMBIENT1, WATER_EXTINCTION1.15, WATER_RENDER_QUALITY1 and WATER_TURBIDITY3, while related SURFACE_DAMPNESS0.15 reset to1.00. Older settings remain byte-identical; runtime and Materials UI confirm the reset. The final normal Main profile correctly reads Custom because unrelated tuning was retained.

`scene-trace.glsl` hoists ray-direction dot products, reuses each projected interval endpoint, and reconstructs only midpointZ for occlusion. The192/48/24 budgets, footprints, receiver checks, hit refinement, range and occlusion rules remain. `volume.glsl` skips density only where foreground clearWeight is exactly zero, and skips sunlight density reads only when solar scattering is zero/night or MIST_LIGHT is zero. No visible effect, resolution, range, sample count or user control is removed.

Four runtime assets changed: scene-trace.glsl, volume.glsl, shaders.properties and lang/en_us.lang. Options defaults/allowed values, all menu paths and the old pole filter remain unchanged. [Source changes](../stratus-refine-1610/source-changes.json), [diff](../stratus-refine-1610/changes.diff), [option audit](../stratus-refine-1610/option-audit.json).

### Technical checks and performance limits

- Native Apple M1 OpenGL compatibility-shim compile/link:768 pairs/eight variants/three dimensions/zero failures. Separate from actual Iris loading. [Log](../stratus-refine-1610/compile.log).
- Actual matched projected-tracer GLSL: seven synthetic scenes × three qualities ×128² pixels =344,064 pixels per variant, zero hit mismatches, zero pixels over0.001 error, zero API errors. [Checks](../stratus-refine-1610/interval-checks.json).
- Actual matched atmosphere GLSL: eight day/night/height/range scenes ×128² =131,072 pixels, maximum linear RGBA error0.0000621081 (<0.0001), zero API errors. Isolated costs vary; affected night cases are cheaper. This is not gameplay FPS. [Checks and timings](../stratus-refine-1610/mist-checks.json).
- Current actual underwater-resolve shader: ten air/submerged/deep/glass/particle/vertical-exit cases, zero failures/API errors. [Results](../stratus-refine-1610/water-checks.json).
- Nine temporary-profile installer integration checks pass, including old/new-file preservation and concurrent conflicting ZIP refusal. [Results](../stratus-refine-1610/migration-checks.json).

Temporary actual-Iris GPU timers identified scenery reflection as the main river cost (~24.274ms baseline; retained candidate diagnostic22.457ms). These short runs were **unfocused**; do not treat the difference as a matched whole-game improvement or60 FPS evidence. A receiver-plane cache experiment was slower/inconsistent and was fully reverted. A no-reflection-fog pack was diagnostic only; reflection fog remains in the release. Timer hooks were removed and original bytecode restored for all three Iris targets. [Performance summary](../stratus-refine-1610/performance-summary.json), [baseline diagnostic](../stratus-refine-1610/gpu-profile-reference-before.json), [candidate diagnostic](../stratus-refine-1610/gpu-profile-interval-candidate.json).

Initial samples were blocked by an unfocused/locked Mac. The user later chose to foreground Minecraft manually; no AppleScript was used. A live check then confirmed focus1 at1440×842. The focused-only activity helper observed SHORT_AFK/cap30, reset it to NONE/cap70 and kept that state without changing saved options. Dynamic FPS stayed FOCUSED, world time6000/rain0 and both fixed cameras remained matched. Saved VSync=true/maxFPS70/inactivity=afk and Dynamic FPS configuration remain byte-identical.

Accepted full-Reference30-second samples on Apple M1, render12/simulation8, identical six quality selections and optics:

| Scene | Baseline FPS | 1.6.10 FPS | Repeats per build |
| --- | ---: | ---: | ---: |
| River |19.6154|20.1645|2, pooled frames/durations, before/after/after/before |
| Forest horizon |17.7699|18.0673|1 |

All six samples had zero unfocused polls and unchanged framebuffer. Every5-second activity observation confirmed focus1, NONE/cap70, Dynamic FPS FOCUSED and rain0/time6000. No native GPU probe/profiler ran concurrently. The finite mean gains are about2.8%/1.7%; tail times vary, and these short fixed-camera results do not certify general gameplay improvement. They fall far short of60FPS, so performance remains pending. Earlier1.6.9 ~56FPS results used different saved quality choices and cannot certify Reference. Raw samples, medians/p95/p99 and exact conditions are in the [versioned performance report](../../outputs/Stratus-1.6.10-performance.json), [benchmark conditions](../stratus-refine-1610/benchmark-conditions.json) and [focused activity monitor](../stratus-refine-1610/final-activity-monitor.txt). The guarded driver/activity helper stopped after restoring the selected release and latest pre-benchmark client state.

### Actual Main visual review

Final released ZIP river, underwater air exit and root/Materials pages were captured and inspected. Full Reference QA uses byte-identical235 runtime assets. Finite additional views include submerged wood, transparent glass, visible end-rod particles, waterfall with background pool, clear/rain porous and non-porous fixtures, sealed cave/local light/day/night, polished/native sun, shoreline edge and pitch90 river. Source and synthetic probes supplement these finite views; they are not exhaustive visual acceptance. The first particle capture lacked emitted rods and was superseded by a visible retry. A cave camera was rejected because flow moved it; the corrected view was captured. The shelter wall close-up is insufficient for shelter acceptance.

Cloud review covers below/above, layer-height grazing, small span64, native mode and a finite time pair. The layer-height camera looked through a footprint hole, not occupied cloud. The above-cloud terrain was partly unloaded, so only cloud appearance was accepted. Independent cirrus/sunset captures were too subtle/poorly framed for firm acceptance; these clearer views, occupied-cloud interior and relevant distant-foliage fog scene remain pending. Exact historical pole/leaf cameras were not recovered. The finite downward view does not certify the original pole issue.

Fixed-time baseline/candidate river captures show small reflected-foliage changes even on repeated same-pack captures; **no pixel-equivalence claim** is made from screenshots. The separate native probes provide finite component comparisons within stated tolerances. [Static comparison](../stratus-refine-1610/static-visual-comparison.json), [labelled visual report and per-capture pack/camera manifest](../../outputs/Stratus-1.6.10-visual-checks/index.html).

### Build, restoration and reconciliation

ZIP245 entries/235 runtime assets,7,780,828 bytes, SHA256 `6f33f582371c329fd65f9a5ada06fad317dceb1ecf08589e33b88e321d038387`. Archive integrity, every source byte and manifest hash pass; immutable full-Reference QA runtime equals released source. Installed ZIP hash matches. [Package checks](../stratus-refine-1610/package-checks.json), [live runtime](../stratus-refine-1610/runtime-v3-Optional_Stratus-1.6.10.zip_.txt), [receipt](../../outputs/Stratus-1.6.10-install.json).

Original camera restored within0.00005 block with identical orientation modulo360; HUD/pause option/flight restored. The first visual pass restored its original pause menu; after the user foregrounded the game, the benchmark restored its latest screen state (world view/null). Original daylight6000, rain0, weather/thunder flags/timers and all four temporary glass blocks restored and verified as their exact original water[level=0] states. Initial restoration hit an unavailable mapped setter before changing blocks; guarded recovery restored and verified exact states, with failure evidence retained. All temporary driver/activity/fixture helpers stopped; profiler original bytecode restored. [Restoration checks](../stratus-refine-1610/restoration-checks.json).

The initial current-task documentation build was preserved as evidence, then its documentation was refreshed with the newly available focused results. All235 runtime asset bytes remained identical; older1.6.9 archives/preferences were never replaced and the installer preserved the existing1.6.10 preferences on refresh. The final documentation ZIP was reopened and IrisRenderingPipeline verified again. [Initial build](../stratus-refine-1610/pre-focused-benchmark-Stratus-1.6.10.zip), [initial migration receipt](../stratus-refine-1610/pre-focused-benchmark-install.json), [final reload](../stratus-refine-1610/final-release-reloaded.txt). Temporary Main QA archives/settings were removed only after byte/default-equivalence checks; original and Iris-normalised preferences remain backed up in work. [Cleanup receipt](../stratus-refine-1610/qa-cleanup.json).

Reconciled TASK only for approved completed migration policy, current release/reference wording and actual verification limits. Moved completed migration, label and finite water/material requests out of CHANGES Pending into Completed. Retained performance, incomplete cloud/foliage acceptance and exact historical issues. [Reconciliation evidence](../stratus-refine-1610/reconciliation.json). No claim that the entire long-term target is finished.


## 22 October 2026 — Stratus 1.6.9

### At a glance

- Completed vanilla block colours, film on porous/non-porous blocks, removal of absorption/retained dampness, and a subtle adjustable animated vanilla-water texture. All 61 previous control IDs/ranges/menu access and four presets remain; 62 controls total. Retired darkening is explicitly labelled rather than silently repurposed.
- Built **[Stratus 1.6.9](../../outputs/Stratus-1.6.9.zip)**, installed, selected and actually loaded it in Main. [Release receipt](../../outputs/Stratus-1.6.9-install.json), [actual captures](../../outputs/Stratus-1.6.9-visual-checks/index.html). Latest Main overrides carried forward; camera/HUD/pause/flight restored and both temporary helpers stopped.
- Passed 768 native pairs, 795 component/12 output samples, 11 GPU relationships and ten underwater regressions, plus finite actual Main material/colour/water/menu review. Focused active-game tests at 1440×842: river **57.7 → 56.2 FPS**, forest **59.1 → 60.1 FPS**. No general speedup or sustained 60 FPS claim; **performance remains pending**.

### Staging and preserved work

User-authorised Stratus Studio `stage_run` **0d847664-366f-4d24-a8eb-e198c604b09c** had a zero-byte frozen specification delta. Current `TASK.md` and `CHANGES.md` matched the queued snapshots; no target/source gap was invented as extra work. Implemented the four visual requests from the existing five-item queue and partially addressed the performance request. [Staging evidence](../stratus-refine-169/staging.json), [reconciliation](../stratus-refine-169/reconciliation.json).

Editable source was already the newer **1.6.9-water-pole-test** candidate, not 1.6.8. Its `environment.glsl` filter and test ZIP were preserved byte-for-byte. This pass reviewed finite river/downward/underwater views but does not independently certify the original reported pole view or call that historical issue solved.

### Behaviour and controls

**Vanilla block colours:** `REALISTIC_LIGHTING` source default changes from 1 to 0. The existing vanilla path restores game vertex face/AO/lightmap colour and bypasses artistic exposure, white balance, saturation, bloom and highlight compression. Existing saved `1` values still select enhanced lighting and retain all related controls; no artist setting was erased. Main already selected `0`. Actual matched dry-iron front/top crops differ from shaders-disabled Minecraft by at most one 8-bit RGB code; granite/grass are affected slightly by retained atmosphere, so the whole frame is not claimed vanilla. [Fixture comparison](../stratus-refine-169/vanilla-fixture-comparison.json).

**Film and dampness removal:** removed pore-absorption attenuation and sheltered retained moisture. `wetSurfaceResponse` now evaluates exposed film on porous and non-porous blocks, including metal and glazed materials, under either lighting mode. All-weather/rain-only, exposure, world-face drainage, material roughness and independent amount/strength remain. Zero amount or sheen is an exact dry bypass and sealed caves remain dry. A white surface can reflect a darker sky at grazing angles; that optional view-dependent reflection is separate from the removed diffuse absorption. Actual matched final-code iron/glazed/granite captures were inspected; [finite pixel comparison](../stratus-refine-169/final-film-comparison.json).

`SURFACE_DAMPNESS` keeps its identifier/full range and film scaling, now labelled **Surface film amount**; absorption/retention is deliberately removed. `WET_DARKENING` keeps its ID/range/menu/saved values as **Retired darkening**, an intentional no-op explained by its tooltip. This is the compatibility exception required by the user's explicit effect removal. [Control and preset audit](../stratus-refine-169/option-audit.json).

**Native water texture:** new `WATER_TEXTURE` slider under Water, strength default 0.15, zero/off through 1.00. Reuses the already-fetched active still/flow atlas texel and carries luminance in unused water metadata red. The lake compose modulates transmitted radiance only; reflection, opacity, biome tint, physical water path and refraction stay independent. No extra texture read or Mojang asset distribution. Off/strong actual Main captures show the pattern/tint response; final river/underwater/waterline captures preserve the intended water appearance.

### Performance and validity

Skip `composite` when scenery reflection is disabled (`REFLECTION_MODE=0`): its readers are already compiled out. Move interface normal/depth reads after non-water/underwater rejection in lake compose. No buffer resolution, sample budget, traversal cap, draw distance, preset or user quality selection was lowered. Actual Iris confirms `{composite=>false, composite5=>false, composite6=>false}` in the selected vanilla/sky-only mode. These structural skips do not prove a whole-game speedup.

Initial 854×480 unfocused samples were rejected. After the user focused the normal 1440×842 window, static samples stayed near 29 FPS. Inspection of the installed Minecraft code and live limiter identified **SHORT_AFK / cap30** despite focus. A temporary guarded API helper reset Minecraft's activity timestamp and Dynamic FPS activity every five seconds, only while focus=1; no saved setting was changed. The monitor confirmed **NONE / cap70**, Dynamic FPS **FOCUSED**, world time6000, rain0 and fixed cameras. Its original SHORT_AFK→NONE transition and all observations are retained. Both helpers were stopped after testing. [Activity monitor](../stratus-refine-169/activity-monitor.txt), [stopped helper](../stratus-refine-169/activity-stopped.txt).

Valid 30-second active-game samples on Apple M1 / Minecraft1.21.11 / Iris1.10.8 / Sodium0.8.14, framebuffer1440×842, render distance12, simulation distance8, unchanged source/saved quality, saved VSync=true/maxFPS70, Dynamic FPS enabled:

| Scene | Baseline mean FPS | 1.6.9 mean FPS | New median / p95 / p99 frame ms |
| --- | ---: | ---: | --- |
| River, original camera | 57.6906 | 56.1894 | 16.7813 / 24.6077 / 33.6671 |
| Forest/river horizon, repeated after focus loss | 59.1302 | 60.0723 | 16.1523 / 20.7933 / 27.2975 |

Baseline is the preserved water-pole test using current saved Main settings; updated sample uses byte-identical final runtime source in immutable v2 QA. Both include actual selected Fast-related options, new film amount0.15 and texture0.15. Each accepted sample had zero unfocused polls and unchanged framebuffer. The first forest active sample lost focus and its baseline started unfocused; neither is accepted. Earlier focused samples were AFK-capped and are excluded. Dynamic FPS's own `enableVsync` method reported false while the saved game option stayed true; record that runtime distinction when reproducing. No other native GPU workload ran during accepted samples.

The scene-dependent means do not establish a consistent improvement; the river falls short of 60. Performance stays in Pending changes. The next performance pass should profile the normal-world river with activity/focus/quality fixed and repeat matched samples before accepting further shader changes. [Complete benchmark summary and raw-file references](../stratus-refine-169/performance-summary.json).

### Verification and delivery

Seven runtime files changed relative to the preserved candidate: `core/options.glsl`, `core/diffuse.glsl`, `core/moisture.glsl`, `core/raster.frag.glsl`, `core/lake.frag.glsl`, `shaders.properties`, `lang/en_us.lang`. [Source diff](../stratus-refine-169/changes.diff), [change inventory](../stratus-refine-169/source-changes.json). The existing pole filter and all unrelated runtime assets are retained.

- Native Apple M1 OpenGL compatibility-shim compile/link: **768 pairs / eight variants / zero failures**, separate from actual Iris load. [Log](../stratus-refine-169/compile.log).
- Actual GLSL probes: **795 component /12 output samples,11 relationships,zero failures/API errors**. Includes absorption-independent/nonporous film, dry/cave/rain-only bypass, vanilla diffuse and final display transfer. [Checks](../stratus-refine-169/gpu-checks.json).
- Ten actual full-resolution underwater resolve cases pass: submerged/air receivers, clear-sky exits, glass, additive particles and vertical exits. [Results](../stratus-refine-169/water-regression.json).
- Actual Main scenes: dry vanilla reference; porous/nonporous dry/film and grazing views; native-water texture off/strong; river, underwater/waterline; Materials/Water menus and exact released-ZIP captures. One initially unloaded nonporous frame is rejected and preserved. Capture labels distinguish preliminary, final-code, baseline and vanilla frames. Animation continues; no universal pixel-equivalence claim.
- Package **243 entries /235 runtime assets /7,776,538 bytes**, ZIP CRC/source equivalence and installed hash verified. SHA-256 `98321d67e7225a54a10f9d900ae65bf32f2a1a145559c3d2237513548ae2827d`. Final runtime source exactly matches the tested v2 QA archive; release metadata is new. Latest current saved Main values are copied only because the new release settings did not exist. Iris may omit an explicit saved value equal to its new default; effective values, not comment timestamps, are compared.
- Restored original camera166.190733,65.928693,32.553558 / yaw108.45755 / pitch38.829258, HUD shown, pause-on-focus-loss true and flying true. Temporary QA archives removed only when their generated content/settings still match; workspace evidence retained. Minecraft remains open on the installed release.

`TASK.md` reconciles the approved completed colour/film/water design and exact limits; four verified requests moved out of Pending changes. No conflict against the frozen snapshots was found. The 60 FPS performance request remains pending. Cave/night/rain/preset/mod/motion coverage, the original distant-leaf scene and exact original pole-view acceptance remain incomplete; finite checks do not certify those cases.

## 22 October 2026 — Stratus 1.6.9 water-pole test candidate

### At a glance

- Inspected the user's actual [08:35:25 Main screenshot](</Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)/screenshots/2026-10-22_08.35.25.png>): four pale, diagonal wedges converge at the centre of the downward water view; this is not the HUD crosshair.
- Added a narrow vertical-pole blend to the sky-reflection cache lookup and packaged [Stratus 1.6.9 water-pole test](../../outputs/Stratus-1.6.9-water-pole-test.zip). No water fog, refraction, option, preset or quality budget was changed.
- **Candidate only:** 768 native Apple M1 OpenGL compatibility-shim program pairs compiled and linked with zero failures. No candidate Minecraft visual comparison or focused FPS result yet; the issue stays pending in `CHANGES.md`.

The likely mechanism is the longitude singularity in `reflectedEnvironment`: a nearly vertical reflected direction on flat water samples different cached sky colours according to azimuth, even though all directions converge at the pole. The new lookup blends toward four equally spaced azimuth samples of the appropriate polar row for `abs(ray.y)` from 0.985 to 0.999. Outside that small polar cap, the old lookup is unchanged. This is a hypothesis supported by the shape and code path, not a verified root cause until a matched in-game view is reviewed.

Native test: `work/stratus-check/prepare.py` expanded eight variants across three dimensions; `native_compile --manifest` reported **768 pairs, 0 failures** on Apple M1 / OpenGL 4.1. The first sandboxed attempt could not open a CoreGraphics connection; the approved native retry passed. Compatibility-shim compilation does not establish Iris runtime behaviour or visual correctness. The test candidate was installed alongside the old pack, with a byte-identical copy of the current 1.6.8 saved settings; neither existing file was overwritten. Installed ZIP bytes match the build. Iris still selects **Stratus-1.6.8.zip**, so the candidate has not loaded in Minecraft. Compare at the exact reported view, plus nearby tilted views and a normal river/underwater exit, before moving the request to Completed changes or reconciling `TASK.md`. The two pre-existing performance/FPS requests remain separate and untouched.

ZIP integrity passed (243 entries; SHA-256 `8ccf23a3ceb3aa581c8b5aed71427f142f928bb224be50a6cb77c3381ee45b0d`). Compared with 1.6.8: all 235 runtime asset names are present, and **only `shaders/core/environment.glsl` differs**. `options.glsl` and `shaders.properties` are byte-identical, preserving defaults, controls and presets. The project `TASK.md` is deliberately unchanged until the candidate's design change is visually verified.

## 21–22 October 2026 — Stratus 1.6.8

### At a glance

- Added a complete vanilla-lighting switch, clear-weather wet sheen and smaller, clearer settings pages. All 59 existing settings/defaults/ranges remain; 61 controls total, with all four presets preserved.
- Built **[Stratus 1.6.8](../../outputs/Stratus-1.6.8.zip)**, installed, selected and actually loaded it in normal Main. Preserved the user's latest saved values and restored the test camera and HUD/pause/flight state.
- Native/GPU and finite actual Minecraft visual checks passed. Targeted atmosphere optimisations measured about 4–6% lower draw time in four isolated GPU workloads. **Focused gameplay FPS/frame times remain pending at the user's request for the morning of 22 October.**

### Behaviour and controls

**Lighting → Realistic lighting → Off (vanilla)** restores Minecraft's engine vertex face shading/AO (`oldLighting=true`) and uses the game's lightmap without Stratus ambient/lamp multipliers. Texture/vertex colour is multiplied by mapped light in display space and decoded once. The final transfer bypasses exposure, white balance, saturation, bloom and highlight compression; ground warmth, invented emissive boosts and material recolouring/film are bypassed too. The two unused bloom passes are disabled in that mode. Stratus water, clouds and atmosphere remain active. This restores surface lighting rather than promising that the whole frame equals Minecraft with shaders disabled.

The default main mode stays enabled, preserving the enhanced lighting path and saved tuning. Both face component sliders, combined strength/blend, ambient, AO, ground warmth, local lights and all colour controls remain. The new main switch is distinct from the retained directional-face component slider; its label/tooltip explains the complete bypass. Actual Iris state confirms vanilla mode has `disableDirectionalShading=false`, `oldLighting=TRUE` and `{composite5=>false, composite6=>false}`. Enhanced mode returns to its previous flags. [Parsed vanilla state](../stratus-refine-168/runtime-Optional_Stratus-1.6.8-QA-FinalVanilla.zip_.txt).

**Materials → Wet sheen conditions → All weather** allows view-dependent sheen without current rain; **Rain only** reproduces the previous film response. All weather is the new option's default. Existing `WET_SHEEN`, `SURFACE_DAMPNESS` and `WET_DARKENING` values remain valid; zero dampness is dry and zero sheen disables the coating/retention contribution. Absorbent-material, drainage and exposure gates remain: nonporous/glazed surfaces and sealed caves do not receive a uniform glossy layer. The vanilla lighting mode bypasses material recolouring and film. This is an explicit new weather-source choice; no previous numerical setting or preset was removed or narrowed.

**Settings layout:** kept six main categories and two columns, with smaller face/ambient/block-light, lower/high-cloud, cloud-shape, colour and bloom groups. Shortened clipped labels and retained useful tooltips. All controls are reachable through the new hierarchy; the original slider lists and four profile definitions remain intact. Main screenshots confirm the controls and page layout. The organisation follows supported [Iris screen/menu mechanisms](https://shaders.properties/current/reference/shadersproperties/overview/) and category/submenu practices observed in [Complementary's own settings file](https://raw.githubusercontent.com/ComplementaryDevelopment/ComplementaryReimagined/main/shaders/shaders.properties); no shader implementation/assets were copied. [Control/menu audit](../stratus-refine-168/option-audit.json).

Nine runtime assets changed: `core/options.glsl`, `core/diffuse.glsl`, `core/output.frag.glsl`, `core/moisture.glsl`, `core/solar-warmth.glsl`, `core/ceiling.glsl`, `core/volume.glsl`, `shaders.properties` and `lang/en_us.lang`. The other **226 runtime assets** remain unchanged, including water/refraction/reflection code and the foliage depth-confidence repair. [Source diff](../stratus-refine-168/changes.diff), [change inventory](../stratus-refine-168/source-changes.json).

### Performance work and its limits

Consulted [Apple's profiling guidance](https://developer.apple.com/documentation/xcode/optimizing-gpu-performance), its archived [OpenGL ES measurement guidance](https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/Performance/Performance.html) and shader scheduling considerations from NVIDIA. Applied the measurement principles without assuming their platform-specific tools support the existing Minecraft OpenGL process. [Research and hypotheses](../stratus-finish-167/RESEARCH.md).

- Skip cloud field/texture work only outside the mathematically guaranteed zero-density vertical envelope, including the maximum permitted lower-cloud relief. Occupied cells, holes, gradients, range, traversal cap and sampling budgets are unchanged.
- Hoist mist lighting that depends only on uniforms/the ray outside the integration loop. Preserve the original multiplication order to minimise floating-point variation.
- Skip the two unused bloom passes when vanilla lighting has no bloom contribution.

The first short native timing batches were mixed and were not accepted as a general improvement. Isolated the two atmosphere candidates, then used rotated ordering, 32 draws per elapsed-time query, six rounds and discarded the first warm-up round. Final selected combined results on **Apple M1**, actual full-atmosphere shaders at **128×128**:

| Controlled native view | Previous median GPU ms/draw | New median GPU ms/draw | Lower draw duration |
| --- | ---: | ---: | ---: |
| Below clouds / full atmosphere | 0.088434 | 0.083672 | 5.4% |
| Inside lower layer | 0.016148 | 0.015210 | 5.8% |
| Above lower layer | 0.008309 | 0.007962 | 4.2% |
| Short forest/fog segment | 0.031133 | 0.029298 | 5.9% |

These are repeated isolated GPU draw workloads, **not gameplay FPS or a whole-game speedup guarantee**. Query/driver costs amortise differently from a real frame, and other desktop work can affect timing. All raw shorter and isolated runs remain preserved. [Measurements and limitations](../stratus-refine-168/performance-summary.json), [raw isolation data](../stratus-refine-168/performance-isolation.json).

Compared all **65,536 atmosphere pixels** across those views: maximum tested RGB difference is below **0.018 of one 8-bit sRGB code value**; maximum alpha difference is below 0.0001. An initial strict linear threshold rejected two view maxima; investigation isolated the bounds/hoist changes and final acceptance used an explicit display-oriented half-code threshold, which all tested pixels pass. There is no resolution/sample/distance/preset cut. Finite tests do not establish universal “99% identical” visuals, motion equivalence or maximum performance. The optimisation request remains partially pending until focused matched gameplay profiling and broader review are completed.

### Technical and actual Minecraft verification

- **768 native OpenGL compile/link pairs, eight variants, zero failures**, rerun after final runtime source changes. Defaults, native sky, all four profiles, option extrema and dimensions included. [Compile log](../stratus-refine-168/compile.log). Compatibility shims are separate from actual Iris loading.
- **795 actual component samples** (742 candidate, 53 baseline), **12 actual output samples**, **20 relationship assertions**, zero failures/API errors. Vanilla lightmap/display transfer and artistic-control bypass, clear-weather sheen, Rain only legacy compatibility, dry/nonporous/cave gates, face preservation and cirrus preservation included. [Checks](../stratus-refine-168/gpu-checks.json), [raw samples](../stratus-refine-168/gpu.json).
- **10 actual water-resolve regressions pass**, zero failures/errors. [Water checks](../stratus-refine-168/water-regression.json).
- **59 previous controls/defaults/allowed-value lists retained, 61 total**, every control reachable/labelled, original slider membership and all four profile definitions preserved. No in-game settings inventory was copied into the long-term target; exact defaults remain in source.
- Used the existing normal **Stratus Terrain Lab** in Main, Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14, Apple M1, framebuffer **1440×842**. The user explicitly authorised Minecraft testing, including the described temporary API route, after the initial approval rejection. No mod installation, class redefinition, competing client or world copy was used.
- Actual comparisons cover baseline/Rain only/All weather/Off in clear weather, enhanced/vanilla lighting and a shaders-disabled Minecraft reference, final-code river/underwater views and the settings pages. The nearby stone-face comparison is within one RGB code value; that is a finite foreground observation, not whole-frame equality. Custom atmosphere/water and texture/filter/raster details prevent an entire-frame vanilla identity claim.
- **26 original game captures** are classified in the [visual report](../../outputs/Stratus-1.6.8-visual-checks/index.html). One early river frame lacked sufficient visible terrain after teleport and is rejected. Later loaded overviews and the released-ZIP river image supersede it. The restoration capture is state evidence. Animation continues across shots.
- Actual Iris pipeline, both lighting flag sets and final release selection verified. No shader/driver exceptions in the tested log segment; unused-attribute/Sodium link warnings and normal dynamic-agent warnings are recorded separately. Minecraft rotated its log at midnight, so the [combined runtime evidence](../stratus-refine-168/runtime-log.txt) includes the prior compressed log and current `latest.log`.

### Release, saved settings and cleanup

- [Release ZIP](../../outputs/Stratus-1.6.8.zip): **243 files / 235 runtime assets / 7,774,697 bytes**. SHA-256 `af9e4d4e94a04e2498765be875b49685b797d82804ebcb963834233c060c8115`.
- Installed alongside older releases in Main's `shaderpacks`; installed bytes match source ZIP. All archived bytes match editable pack files. Actual log and current-pack API confirm **Stratus-1.6.8.zip** loaded. [Install receipt](../../outputs/Stratus-1.6.8-install.json), [actual final runtime state](../stratus-refine-168/runtime-Optional_Stratus-1.6.8.zip_.txt).
- Preserved all existing source defaults. Main had newer saved overrides **`SKY_AMBIENT=1.00`, `WATER_TURBIDITY=3.00`**; copied those current values into the absent new settings file without overwriting an existing one. Original 1.6.7 settings remain byte-identical, SHA-256 `d0f8f49fcc47c33ca701270bdb98fec18eb01e9570caef4f58a1f3e9861759fa`. Runtime reports **Custom (+2 options changed by user)** and all four presets including Reference.
- Restored the current user's original camera, HUD/pause/menu and flight flag, then stopped the test poller. Removed seven unchanged temporary QA archives from Main; immutable workspace copies and all original captures remain. Older releases, original preferences and unrelated worlds/mods/resource packs were preserved. [Cleanup](../stratus-refine-168/cleanup.json).

### Pending and specification reconciliation

The user explicitly deferred focused testing until the morning of **22 October 2026**. Final focus remains false with Dynamic FPS enabled; no background sample is presented as valid gameplay FPS. Benchmark both 1.6.7 and 1.6.8 under matched current options, camera, weather/time, resolution, distances, VSync/cap and background conditions. Broader cave/night/preset/motion/mod coverage and the historical reported foliage scene remain pending, as do existing screen-space water edge/miss limits.

Reconciled [TASK.md](TASK.md) with approved completed design/source/release changes and evidence, and moved only the three completed new behaviour/menu requests to Completed in [CHANGES.md](CHANGES.md). The archived focused check and partially verified performance request remain pending. [Reconciliation record](../stratus-refine-168/reconciliation.json). Historical `TASK-previous-brief.md`, `SHADER-SPEC-1.6.7.md`, `SHADER-SPEC.md` and legacy `SPEC-BASELINE.md` are unchanged.

## 21 October 2026 — Stratus 1.6.7

### At a glance

- Adopted Main's preferred settings as defaults; added a richer blocky sun, independent face controls, visible high cirrus and restrained rain sheen.
- Built **[Stratus 1.6.7](../../outputs/Stratus-1.6.7.zip)**, installed, selected and actually loaded it in normal Modrinth Main. All 53 previous controls remain; six additions bring the total to 59. Reference remains selectable.
- Passed native/GPU, water, option and package checks. Actual Minecraft visual comparisons completed for the changed effects. **Focused FPS and exhaustive scene coverage remain pending.**

### Preferred defaults and settings compatibility

Before editing, preserved Main's actual selected 1.6.6 settings in [the original snapshot](../stratus-refine-167/Main-1.6.6-options-before.txt) and [effective-settings record](../stratus-refine-167/settings-snapshot.json). Adopted these seven saved overrides as source defaults:

| Option | Previous source default | New source default |
| --- | ---: | ---: |
| `CLOUD_LAYERS` | 3 | 1 |
| `GROUND_WARMTH` | 0.45 | 0.00 |
| `MIST_DETAIL` | 3 | 2 |
| `REFLECTION_MODE` | 1 | 2 |
| `WATER_EXTINCTION` | 0.90 | 3.00 |
| `WATER_RENDER_QUALITY` | 1 | 2 |
| `WATER_TURBIDITY` | 1.00 | 6.00 |

All other previous defaults and allowed values remain. The original saved file SHA-256 is `69b1bfcac7eede389d2211c5f1608a44eb492fa96326f6ab58fc418deca3dcab`; its current bytes still match. Older removed overrides were not resurrected. Main's parsed release state reports **Custom (+0 options changed by user)**: the preferred values now work as source defaults. The installed Iris parser exposes **FAST, BALANCED, REFERENCE and HIGH**. Their definitions, old menu access and slider membership are unchanged; Reference is available independently of the preferred default combination. [Option comparison](../stratus-refine-167/option-inventory.json), [actual runtime state](../stratus-refine-167/final-runtime-state.txt).

Six added controls, all labelled and reachable:

| Control | Default | Allowed extent / role |
| --- | ---: | --- |
| `VANILLA_FACE_CONTRAST` | 1.00 | 0–3; vanilla component multiplier |
| `REALISTIC_FACE_CONTRAST` | 1.00 | 0–3; realistic component multiplier |
| `SUN_CORE_BRIGHTNESS` | 4.50 | 0.50–8; polished core, including prior 2.80 |
| `SUN_HALO_STRENGTH` | 2.00 | 0–3; sun-local scattering |
| `SUN_HALO_RADIUS` | 1.50 | 0.35–3; sun-local falloff |
| `CIRRUS_DENSITY` | 1.00 | 0–3; independent high optical density |

The complete discrete values for this release are in the shader source and the [archived 1.6.7 inventory](SHADER-SPEC-1.6.7.md). No previous setting was removed, hidden or narrowed. **Deliberate behaviour extension:** `WET_SHEEN` retains its identifier, allowed values, default 0.85 and existing sheltered-retention effect, and now also controls the exposed rain film. Saved values remain valid but wet materials can show the newly requested highlight.

### Rendering changes

- **Polished blocky sun:** retains the running game's/resource pack's square sun texture. Its HDR core and finite local scattering now have independent controls. The halo uses a smooth bounded angular falloff and applies only to polished mode; global bloom and native `SUN_STYLE=1` are unchanged. Core 2.80 / halo 0 recovers the earlier contribution. An initial 1.20 strength / 1.00 radius experiment looked too restrained in Main; final 2.00 / 1.50 was reviewed before release.
- **Independent face shading:** multiplies the existing vanilla and realistic terms separately, preserving their exposure weights `(1 − 0.35 × exposure)` and `0.35 × exposure`. Both new values at 1 reproduce the previous combined calculation; either zero removes that term, both zero remove face contrast. `FACE_SHADING` and `FACE_BLEND` remain combined master controls. Existing world-space lighting, rain/night/cave gating and contrast bounds remain.
- **Visible high cirrus:** increases upper optical density from 0.016 to 0.045 (2.8125×), multiplied by `CIRRUS_DENSITY`, and brightens its daylight response. Existing amount 0.65, altitude 360 and independent lower-cloud controls remain. Main's isolated high layer now shows a broad bright veil where the 1.6.6 comparison was barely visible; off removes it. Lower cloud shape code is unchanged. This is a wispy veil, not dense storm cloud geometry.
- **Restrained wet response:** preserves moisture absorption and adds view-dependent Fresnel film plus a roughness-dependent solar highlight on rain-exposed absorbent materials. Rain, dampness, skylight exposure, absorption, face orientation and drainage gate the coating. It uses a soft environment approximation, without scenery tracing or another pass. Dry, non-absorbing and sealed materials bypass it. GPU checks cover those gates; actual rain comparisons show a subtle grazing sheen and strength response, without a uniform gloss on tested clear/nonporous surfaces.

Seven runtime assets changed: `core/options.glsl`, `core/diffuse.glsl`, `core/ceiling.glsl`, `shaders.properties`, `lang/en_us.lang`, plus comment-only changes in `core/moisture.glsl` and `core/raster.frag.glsl`. The other **228 runtime assets** are unchanged from 1.6.6, including the water/fog repair implementations. [Diff](../stratus-refine-167/changes.diff), [change inventory](../stratus-refine-167/source-changes.json).

No pass was added or selected quality budget reduced. Preferred defaults deliberately reproduce the user's existing quality choices, while all preset definitions remain intact. Additional wet-film calculations bypass dry/nonporous pixels; these source choices are **not a measured performance improvement**.

### Output and actual Main state

- [Editable pack](../../outputs/Stratus), [release ZIP](../../outputs/Stratus-1.6.7.zip): **243 files, 235 runtime assets, 7,771,716 bytes**.
- SHA-256: `a273a3591d126f1406c9413f7e46684c095e98413998d393375925dce27f56eb`. All archive entries match source; installed ZIP bytes match the release.
- Installed at `/Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)/shaderpacks/Stratus-1.6.7.zip`. Iris configuration selects it; live log records `Using shaderpack: Stratus-1.6.7.zip`, and parsed runtime API reports that same current pack. [Receipt](../../outputs/Stratus-1.6.7-install.json), [runtime log](../stratus-refine-167/runtime-log.txt).
- Actual existing Main client, normal **Stratus Terrain Lab**, Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Apple M1. No competing world, client restart or mod installation was required. A guarded project-local Java API driver captured the actual framebuffer and verified camera/pipeline state. It did not redefine game classes. [Testing route and limits](../stratus-refine-167/TESTING.md).
- Restored the original player position/yaw/pitch and HUD/pause/menu state, then stopped the temporary poller. The game remains open on the release. Removed only unchanged temporary QA packs/settings from Main, including semantically identical Iris-reformatted copies; old releases and preferences remain. [Cleanup](../stratus-refine-167/cleanup.json), [driver stopped](../stratus-refine-167/driver-stopped.txt).

### Completed verification

- **768 native OpenGL compile/link pairs, eight variants, zero failures**: defaults, native sky, all four presets, option extrema and all dimensions. Native compatibility shims are distinct from actual Iris loading. [Compile log](../stratus-refine-167/compile.log).
- **539 targeted GPU samples** (490 candidate, 49 baseline/reference), **21 relationships pass**, zero failures/API errors. Includes legacy face equivalence, independent components/bypasses, dry/nonporous/cave gates, grazing wet strength, cirrus density and lower-layer independence. [Assertions](../stratus-refine-167/gpu-checks.json), [raw data](../stratus-refine-167/gpu.json).
- **10 actual water-resolve regressions pass** with the preferred extinction 3.00 / turbidity 6.00, zero errors. Air receivers, submerged/deep receivers, sky exit/missing exit, glass, additive particle and vertical exit included. [Water results](../stratus-refine-167/water-regression.json).
- **59 reachable/labelled settings**, all previous option ranges/presets retained; 235 runtime archive assets source-equivalent. Cast shadows remain off. [Source audit](../stratus-refine-167/source-audit.json). The runtime-tested immutable QA-v2 shader tokens match final source, with only two comment differences; final released ZIP loading was then verified separately. [Runtime equivalence](../stratus-refine-167/runtime-equivalence.json).
- Actual driver/pipeline captures completed without a shader/driver error. One read-metrics prototype used an unavailable reflection method; the corrected read-only probe succeeded. That prototype exception is retained and is not a shader failure.

### Actual visual observations and remaining checks

[Visual report with 37 original captures](../../outputs/Stratus-1.6.7-visual-checks/index.html) distinguishes baseline, preliminary, final QA and released-ZIP frames. Reviewed the richer square sun/local glow against native mode and halo-off experiment; cirrus-only/off and 1.6.6 baseline; both face terms and each disabled; rainy sheen off/default/maximum, clear materials and nonporous metal; river/underwater; sunset atmosphere; and settings menus. Final release [sun/sky](../../outputs/Stratus-1.6.7-visual-checks/screenshots/s167-release-sun-sky.png) and [river](../../outputs/Stratus-1.6.7-visual-checks/screenshots/s167-release-river.png) were inspected after release loading. The restoration capture is state evidence only. Original paused/stale menu frames remain labelled **not acceptance evidence**, alongside corrected confirmed captures.

Cameras, time, weather and relevant settings were controlled for comparisons; continuing cloud/rain animation prevents pixel-identical frames. Sunset sun was partly cloud-occluded, so that frame does not certify an unobstructed sunset halo. Rain sheen is restrained and angle dependent. Material porosity is heuristic; film responds to current rain, without accumulation. Night/sheltered-wet fixtures, exhaustive preset/motion/mod comparisons and the original reported distant-leaf scene are not fully certified. Existing finite cloud range/cell limits and screen-space reflection edge/miss limitations remain; river images are not a claim of perfect water rendering.

**Performance remains unverified:** final recorded framebuffer **1440×842**, window focus **false**, Dynamic FPS **enabled**. No valid focused FPS/frame times, speedup, maximum-performance or exhaustive visual-equivalence claim. The next performance check is a focused matched terrain, dense forest/fog and river/cloud run with distances, VSync/cap, Dynamic FPS and competing processes recorded. Preserve intended quality while profiling.

### Specification handoff

Completed the five requests from the preserved [previous brief](TASK-previous-brief.md). At release time, the 59-setting inventory was reconciled with source; it is now retained in [the detailed 1.6.7 snapshot](SHADER-SPEC-1.6.7.md), while [TASK.md](TASK.md) and [SPEC-BASELINE.md](SPEC-BASELINE.md) are design/behaviour lists. `SHADER-SPEC.md` remains an older historical reference and the previous brief is unchanged. Future implementation starts only from an explicit request to apply meaningful spec differences; saving a file alone does not trigger work.

### 21 October recheck of the archived brief — no shader changes required

The user requested the five-item archived brief again because it was believed paused/undone. Re-read the current instructions, complete target, pending queue, archived brief, implementation and evidence before editing. **All five features are already implemented and remain intact in 1.6.7.** The archived brief's historical progress is not current state. No shader code or release archive was changed and no new version was manufactured.

- Fresh ZIP integrity/source-byte check passes for all **243 entries**, including **235 packaged runtime assets**. Release and installed SHA-256 both remain `a273a3591d126f1406c9413f7e46684c095e98413998d393375925dce27f56eb`. Every recorded source hash from completed technical testing still matches current source, so those tests apply to the unchanged code; **the 768-link/GPU suites were not rerun or claimed as new runs**.
- Settings definitions, menu/preset/language source and old preference hash still match the completed audit: **53 retained / 59 total**, seven preferred defaults preserved. Re-inspected actual face/sun/cirrus/rain-film code and preserved real Main comparison sheets for each changed feature. Verified all **37 original report capture hashes**. These are earlier actual game captures reviewed again, **not newly captured scenes**.
- Fresh read-only probe of the existing Main client confirms a real `IrisRenderingPipeline`, **Stratus-1.6.7.zip**, all seven preferred defaults, both face controls at 1, sun values 4.50/2.00/1.50, cirrus style/amount/altitude/density 0/0.65/360/1, and all four parsed profiles including Reference. The latest pack-load event also names 1.6.7. [Fresh integrity evidence](../stratus-recheck-167/recheck.json), [fresh runtime state](../stratus-recheck-167/runtime-state.txt).
- The same probe reports **focus=0**, **1440×842**, **Dynamic FPS enabled**. The current desktop app inventory still exposes no Minecraft/Java target to focus. No focused FPS result was collected; no game settings, camera, world or mods were changed by the read-only probe. It schedules one read, without starting a polling driver or redefining classes.
- Updated [CHANGES.md](CHANGES.md) to mark the five already completed feature requests and retain the genuinely unfinished focused performance check. Reconciled [TASK.md](TASK.md) by making the approved preferred-default/Reference policy explicit without copying setting values or weakening verification requirements. Other newer target wording and all historical snapshots/briefs are preserved.

Remaining practical step: obtain a focused matched Main terrain/forest/river benchmark with the recorded controls above. Until then, focused FPS, speed gains and maximum performance remain unverified; existing broader scene-coverage limits are unchanged.

### 21 October follow-up — archived brief and next-pass order

Independently re-read the current target, incremental queue, archived brief, five implementation paths and prior evidence. Rechecked every one of the 243 released archive entries against editable source, archive integrity and the installed archive SHA-256; all match the 1.6.7 hash above. No missing archived shader implementation was found. No source change, duplicate release, settings change or new live visual/performance result was made in this follow-up.

Confirmed the existing Java process is still present (PID 84250). The desktop tool rejected Minecraft by app name and timed out accessing the Dock. Automatic approval review rejected attaching the guarded temporary Java probe because explicit authorisation of process injection was missing. The probe was **not executed**. Asked for that approval and for Minecraft focus; answers remain pending. Background or historic FPS is not substituted for a focused sample. [Follow-up state](../stratus-finish-167/status.json).

The user authorised finishing the archived work first, then implementing the four newer requests now in `CHANGES.md`. Their intended changes have not yet been implemented. Prepared [expert-source research and implementation considerations](../stratus-finish-167/RESEARCH.md) while the benchmark prerequisites remain pending. The current long-term `TASK.md`, legacy snapshots, source, release and original preference files were preserved; the incremental queue explicitly retains the unfinished benchmark and all four requests.

## 20 October 2026 — Stratus 1.6.6

Status: Three requested changes implemented; technical checks, packaging and installation passed. **Main loading/visual acceptance, confirmation against the reported foliage scene, visual equivalence and focused performance remain pending.**

### At a glance

- Blended vanilla and realistic face shading; added a polished square vanilla sun; addressed one reproduced cause of dark foliage dots in fog.
- Built and installed **Stratus 1.6.6**. All 53 settings, their allowed values and the four presets remain available.
- Technical checks passed. **Main still selects 1.6.5**; the new build has not been visually checked in Minecraft or benchmarked with the game focused.

### Changes and reasons

- **Keep vanilla face shading and mix in realistic light.** `core/diffuse.glsl` now uses 65% vanilla axis weights plus 35% realistic sky/ground/solar response at full skylight. Exposure still gates that contribution. Existing strength/blend controls, world-space orientation, rain/night/cave behaviour and contrast bounds remain. The mix is before the existing contrast control; a saved strength of 2.00 remains supported. The English label is now “Blended face contrast”.
- **Polished blocky vanilla sun.** `core/ceiling.glsl` samples the running game's `minecraft:textures/environment/celestial/sun.png` with explicit texel sampling, HDR warmth and the existing broad haze glow. The round procedural solar core/aureole is removed. Sky and environment reflections share this square sun. `SUN_STYLE=0` is labelled “Polished vanilla sun”; `SUN_STYLE=1` still uses native textured sun/moon rendering. The default moon behaviour is preserved. The actual 1.21.11 texture was used as test input; no Mojang image is bundled. No active Main sun-texture override was found, though future resource packs may change the sampled image.
- **Repair a fog depth-miss mechanism that causes dark foliage dots.** A thin cutout may be absent from all four reduced-resolution depth samples; 1.6.5 returned zero fog in that case. `atmosphere-resolve.frag.glsl` now evaluates rejected pixels at their exact full-resolution depth and smoothly blends by confidence. `completeAtmosphereSegment` in `volume.glsl` shares primary-pass border/status handling. The fallback uses the **same selected full atmosphere quality**, including cloud shading, rather than lowering samples. Valid cached samples and underwater behaviour are preserved in controlled tests. The actual reported Main dots remain to be checked; unrelated texture/mipmap/driver causes have not been ruled out.

Seven runtime assets changed: `core/diffuse.glsl`, `core/ceiling.glsl`, `core/volume.glsl`, `core/atmosphere.frag.glsl`, `core/atmosphere-resolve.frag.glsl`, `shaders.properties`, and `lang/en_us.lang`. The other **228 runtime assets** are byte-identical to the 1.6.5 source. Water, matte moisture and cloud-density implementation remain unchanged. [Source diff](../stratus-refine-166/changes.diff), [change inventory](../stratus-refine-166/source-changes.json).

### Settings and quality preservation

Before final packaging, compared old/new inventories: **all 53 option IDs, defaults and allowed values are identical**; menus, slider lists and all four presets are identical; every language key remains. **All 10 saved Main overrides are valid and copied unchanged** to the new pack settings. Nothing was removed, hidden or narrowed. Tooltips and two displayed labels describe the requested shading/sun changes. There is no settings-file migration; the deliberate `SUN_STYLE=0` visual redesign is the requested square-sun change. [Full option/menu/label comparison](../stratus-refine-166/option-inventory.json).

No resolution, draw distance, effect, control, quality preset or sampling budget was reduced. There is no extra render pass. Full atmosphere integration is restricted to low-confidence depth pixels. This bounds unnecessary work but is **not a measured speed gain**: fallback-heavy foliage views can cost more than 1.6.5. Maximising performance at unchanged intended quality requires a matched live bottleneck measurement; no “100% visually equivalent” or speed claim is made without that evidence.

### Output

- Build/source: **Stratus 1.6.6 candidate**, [editable source](../../outputs/Stratus), [ZIP](../../outputs/Stratus-1.6.6.zip), **243 files / 7,770,845 bytes**.
- SHA-256: `96378ece4c83993306de014a3423eb93a16d54b15813e218a52c75ffc8d5a555`.
- Installed alongside 1.6.5 at `/Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)/shaderpacks/Stratus-1.6.6.zip`; installed bytes match. Prior preferences copied only if the new settings file was absent. [Receipt](../../outputs/Stratus-1.6.6-install.json).
- **Main still selects 1.6.5.** Its log confirms `Using shaderpack: Stratus-1.6.5.zip`; this supersedes the earlier 1.6.5 entry's at-delivery “not selected” state. [Baseline runtime evidence](../stratus-refine-166/baseline-runtime.txt). No world, mod or resource-pack changes; existing game left open.

### Completed checks for 1.6.6

- **768 native OpenGL compile/link pairs, eight variants, zero failures** across defaults, vanilla mode, four presets, option extrema and all dimensions. [Compile log](../stratus-refine-166/compile.log). Native compatibility shims are not live Iris loading proof.
- **27 GPU relationships pass**, zero API errors: **4 candidate sun renders, 11 candidate fog cases and 216 candidate face samples**. Separate references: 1 baseline sun render, 11 baseline fog cases and 72 baseline/pure-vanilla face samples. Every sampled sun RGB/alpha texel matches the current vanilla image plus documented HDR tint. The face mix matches 65/35; direction/rain/night/caves/camera/bypasses/other dimensions checked. [Assertions](../stratus-refine-166/gpu-checks.json), [raw data](../stratus-refine-166/gpu.json).
- The controlled missed-depth case reproduces 1.6.5's dark RGB `(0.010, 0.015, 0.010)` and produces fogged RGB approximately `(0.170, 0.189, 0.209)` after repair. Matched-depth, near foreground and underwater results remain unchanged; confidence transition and chunk border checks pass. This validates the mechanism, not yet the user's actual scene.
- **10 water-resolve GPU regressions pass**, zero failures/errors. [Water evidence](../stratus-refine-166/water-regression.json).
- **53 reachable controls labelled; all 235 runtime assets match source in the ZIP; archive integrity and installed bytes verified.** Cast shadows remain off. [Audit](../stratus-refine-166/source-audit.json).

### Visual observations and performance

**Actual 1.6.6 in-game observations: none; pending.** Native desktop inventory still does not expose the running Java/Minecraft window, so the candidate could not be selected or driven for matching captures. Confirmed 1.6.5 loading is baseline evidence only. No competing world session was launched.

Inspected two labelled **offline native-GLSL preview sheets**: [sun comparison](../stratus-refine-166/offline-sun-preview.jpg) shows the old round core and new square texture; [fog reproduction](../stratus-refine-166/offline-fog-preview.jpg) shows dark depth rejection versus corrected scattering. These are **not Minecraft screenshots**. Real sky composition, bloom, motion, the original leaf scene, appearance in different weather and visual equivalence remain pending.

**Performance: not measured.** No focused FPS/frame times, maximum-performance or speedup claim. Keep quality fixed when profiling. The added full-quality fallback is the main new cost to assess in dense forest/fog; cache-matched pixels keep the existing reconstruction path.

### Next checks

1. Select **Stratus-1.6.6.zip** in Main/Iris, verify its name and custom-texture/shader loading in `latest.log`.
2. Compare matched normal-world faces and sun at noon/sunset/rain/night, caves/local lights, native sun mode and controls. Check the square sun through clouds and in water reflection.
3. Return to the actual distant-leaf dot scene, move slowly, compare tiny leaves/sky holes/fences/chunk edges, and recheck underwater/glass/particles/cloud traversal.
4. Benchmark focused matched terrain, dense forest/fog and river/cloud views with resolution, distances, VSync/cap, Dynamic FPS and competing processes recorded. Optimise only measured bottlenecks without reducing intended quality; verify resulting visual equivalence.

Follow [IN-GAME-TEST.txt](../../outputs/Stratus/IN-GAME-TEST.txt). [Current shader specification](SHADER-SPEC.md). Runtime texture binding follows the [Iris custom-texture documentation](https://shaders.properties/current/reference/buffers/custom_textures/).

## 20 October 2026 — Stratus 1.6.5

Status: Implementation, native/GPU checks, packaging and installation complete. Actual Main loading, visual acceptance and focused FPS remain pending.

### At a glance

- Made high clouds independent of lower clouds, restored diffuse face contrast, matched the current vanilla cloud footprint and simplified cloud detail.
- Built and installed **Stratus 1.6.5** with a 12-block default cloud thickness; prior thickness choices remain available.
- Technical checks passed. Live visual acceptance and focused FPS were still pending at delivery; later Main evidence confirmed 1.6.5 loading, as recorded in the 1.6.6 entry above.

### Changes and reasons

1. **High clouds cover lower-cloud gaps.** `ceiling.glsl` now gives the upper layer an independent continuous, stretched wispy field. It no longer shares the lower island mask or its coverage/scale/distortion. The layer retains its own amount and altitude controls. It is a finite-altitude veil with the existing horizon fade, rather than a spherical shell.
2. **Restore realistic diffuse face contrast.** `diffuse.glsl` combines sky hemisphere/ground response with world-space solar orientation. Sky exposure gates it, rain softens solar contrast, and night disables the direct solar term. Contrast is bounded for readability at saved 2.0 values. Zero face strength/blend bypasses it. This is broad diffuse lighting without cast shadows; matte moisture, local lighting and emission handling remain.
3. **Use current vanilla cloud shapes.** The lower layer fetches each occupied alpha cell from `minecraft:textures/environment/clouds.png` through an Iris `customTexture.vanillaClouds` sampler. Explicit integer wrapping preserves the map's connected shapes and holes. The test input came from the installed Minecraft 1.21.11 client JAR; no active Main resource-pack cloud override was found. Resource-pack replacements will be respected at runtime. No Minecraft/Story Mode texture is bundled in the shader ZIP.
4. **Simplify cloud detail.** Fine 3D billows, erosion and pores are removed from cloud density. Connected extrusions use broad density gradients, gentle vertical relief and the existing self-shadow/height lighting. Ray integration splits at texture-cell boundaries to reduce missed cells at grazing angles. This is a Story Mode-inspired simplification, not a certified match to an unseen reference pack.
5. **Correct proportions and explain option migrations.** Default cloud thickness changes from 96 to 12 blocks because the old thickness made current vanilla's 12-block cells into tall columns in an offline render. A 4-block option is added for vanilla slab proportions, and every prior thickness choice remains. Default span 240 maps to 12-block cells. `CLOUD_AMOUNT` now scales opacity of the fixed footprint; `CLOUD_DETAIL` controls broad gradients; `CLOUD_DISTORTION` changes vertical relief only. Other source defaults, preset values and pass resolutions are unchanged. Updated English tooltips describe the actual behaviour.

Only five runtime source assets changed: `shaders/core/ceiling.glsl`, `core/diffuse.glsl`, `core/options.glsl`, `shaders.properties`, and `lang/en_us.lang`. All other 230 shader/config/data assets, including water, moisture and mist implementations, are byte-identical to the saved 1.6.4 baseline. Versioned README/validation/test metadata and the packaging destination were also updated.

### Output and installation

- Build: **Stratus 1.6.5**, candidate awaiting live acceptance.
- Editable source: [outputs/Stratus](../../outputs/Stratus).
- ZIP: [Stratus-1.6.5.zip](../../outputs/Stratus-1.6.5.zip), 243 files, 7,769,903 bytes.
- SHA-256: `d6d005f670a90d2246b3c3e43208d5a5862a70f8ba79a8670aa4724ad8153809`.
- Installed alongside 1.6.4 in `/Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)/shaderpacks/Stratus-1.6.5.zip`. Installed bytes match the ZIP. Existing 1.6.4 preferences were copied to the new `.zip.txt` only if absent; prior settings were not changed.
- [Install receipt](../../outputs/Stratus-1.6.5-install.json). **Selected pack remains Stratus-1.6.4.zip; 1.6.5 is not confirmed loaded.** No competing world session was launched. Main's worlds, mods and resource packs were not changed.
- [Source changes](../stratus-clouds-165/changes.diff) and complete [source manifest](../../outputs/Stratus/SOURCE-MANIFEST.json).

### Completed technical checks

- **768 native OpenGL compile/link pairs, zero failures**, across eight variants (defaults, vanilla sky, four quality presets, option minimum/maximum) and all three dimensions. [Preparation](../stratus-clouds-165/prepare.log), [compile log](../stratus-clouds-165/compile.log). Compatibility shims are not an Iris runtime test.
- **17 actual cloud GLSL renders and 216 face samples; 32 independent checks pass**, zero OpenGL errors. Includes all **65,536 vanilla cloud texture cells**, exact occupied-cell/hole correspondence, lower-layer disable, independent upper coverage, simple detail settings, sun reversal, rain, night, sealed caves, equivalent camera rotation, zero-strength bypasses and Nether/End behaviour. [Assertions](../stratus-clouds-165/gpu-checks.json), [raw GPU results](../stratus-clouds-165/gpu.json).
- **10 water-resolve GPU regressions pass**, zero failures/errors: underwater segment clipping, above-water receivers, sky, glass, additive particles and vertical exits. [Evidence](../stratus-clouds-165/water-regression.json). This does not replace live water regression review.
- **53 reachable controls have English labels**, cast shadows remain disabled, all four presets remain available, **235 runtime assets in the archive match source**, ZIP integrity passed. [Audit](../stratus-clouds-165/source-audit.json).

### Visual observations and performance

**Actual in-game observations for 1.6.5: none; pending.** Main was observed running a normal Java client with `shaderPack=Stratus-1.6.4.zip` in Iris configuration. The desktop tool's app inventory does not expose its Minecraft/Java window, so the candidate could not be selected or safely driven for matching captures. Historical 1.6.4 screenshots and unrelated existing log errors are not evidence that this candidate passed or failed.

Five **offline GLSL previews** were rendered and inspected: below/inside/above the cloud slab, sunset and night. An initial 96-block-thick preview exposed tall columns; after reducing the source default, the new render shows low connected slabs and broad gradients. Sunset and night change their lighting. [Offline preview sheet](../stratus-clouds-165/offline-cloud-preview.jpg). These are labelled offline renders, **not Minecraft screenshots**; actual terrain composition, horizon motion, cloud/resource binding and the user's visual preference remain unverified.

**Performance: not measured.** Removing fine volume noise reduces work per density evaluation, while cell-boundary traversal can increase step count (1024-segment cap). No speedup, 60-FPS claim or inference from compile time. A focused matched benchmark must record Main's actual options, camera, time/weather, resolution, render/simulation distances, VSync/cap and Dynamic FPS state.

### Remaining issues and next step

1. In the running Main instance, select **Stratus-1.6.5.zip** in Iris; confirm the loaded name and absence of shader/custom-texture errors in `latest.log`.
2. Review a normal-world terrain scene and the cloud layer below/inside/above, with motion at different pitches, noon/sunset/night/rain and all presets. With `CLOUD_AMOUNT=0`, high clouds must remain; `CIRRUS_AMOUNT=0` must remove them. Check vanilla/off modes and the new thickness preference.
3. Inspect sun-facing/back-facing terrain, camera rotation, caves/local lights and the zero-strength controls. Check waterline, submerged geometry and glass/particles for nearby regressions.
4. Take focused matched performance samples. Small cloud spans and grazing rays need special attention: integration has a finite range, an interior bound and a 1024-segment cap; very distant tiny silhouettes can still alias.

The vanilla **horizontal footprint** is exact at the density-cell level. Height, scale options, lighting and animation phase intentionally remain Stratus behaviour; it does not reproduce the entire vanilla renderer. See the [shader specification](SHADER-SPEC.md) and [in-game test steps](../../outputs/Stratus/IN-GAME-TEST.txt).

Implementation reference: [Iris custom-texture documentation](https://shaders.properties/current/reference/buffers/custom_textures/) describes runtime game/resource-pack texture binding; the [official 1.21.6 notes](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-6) document the cloud-texture update. The actual test texture is from the locally installed 1.21.11 client.

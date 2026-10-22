from pathlib import Path
import json,hashlib
w=Path('work/stratus-refine-1610');d=Path('work/Custom instructions');t=d/'TASK.md';c=d/'CHANGES.md';log=d/'CHANGE-LOG.md'
sha=lambda x:hashlib.sha256(x).hexdigest()
current_t=t.read_text();current_c=c.read_text();current_l=log.read_text()
for name,text in [('TASK.md',current_t),('CHANGES.md',current_c),('CHANGE-LOG.md',current_l)]: (w/('pre-reconcile-'+name)).write_text(text)
assert current_t==(w/'frozen-TASK.md').read_text(),'TASK changed: merge the newer target before reconciling'
assert 'optimise performance for referance preset to around 60 FPS while keeping essential viausals, eg. resulution' in current_c
assert '### Staged from TASK.md — RUN BOTH dfc0d10a' in current_c
assert json.loads(Path('outputs/Stratus-1.6.10-install.json').read_text())['loaded']
new_t=current_t.replace('versioned release `outputs/Stratus-1.6.9.zip`','versioned release `outputs/Stratus-1.6.10.zip`')
old='- Default policy = preserve the recorded preferred Main choices as source defaults, while keeping Reference separately selectable; preserve original saved preferences and use shader source for exact current values.'
new='- Default policy = keep source defaults in shader code and preserve unrelated latest tuning. For a new release, the change-aware installer carries only unrelated saved overrides and resets change-related keys to approved release/preset defaults; preserve every old settings file and never overwrite an existing new-version file. Visual defaults apply to all presets, performance defaults use appropriate chosen presets, and combined visual/performance defaults use Reference unless explicitly approved otherwise. The approved 1.6.10 migration resets the 1.6.9 colour, film and native-water-texture keys in all four presets; quality assignments remain unchanged. Manual ZIP copying does not run this migration.'
assert old in new_t;new_t=new_t.replace(old,new)
new_t=new_t.replace('- Face-lighting design = at full sky exposure,','- Enhanced face-lighting design = at full sky exposure,')
new_t=new_t.replace('Aim for the requested approximately 60 FPS without lowering resolution or quality;', 'Retain projected-ray interval endpoint reuse and invariant dot products, zero-weight mist foreground skips and zero-contribution mist sunlight skips. Aim for the requested approximately 60 FPS on Reference without lowering resolution or quality;')
start=new_t.index('- Current verification limits = ');end=new_t.index('\n',start)
new_t=new_t[:start]+'- Current verification limits = 1.6.10 has 768 native compile/link pairs, matched tracer/atmosphere GPU checks, ten underwater cases, nine installer integration checks, archive/source/install equivalence, actual Main release loading and finite water/material/night/sun/menu/cloud review. All 62 controls and four quality profiles remain; eight unrelated Main overrides migrated and the related film override reset as approved. No accepted focused full-Reference FPS sample was available: the game was unfocused/AFK limited and the Mac locked. The 60 FPS target stays pending. Cloud captures cover below/above, layer-height grazing, small span, native mode and a finite time pair; occupied-cloud interior, clearer independent cirrus/sunset and exact distant-leaf fog views remain unverified. Exact historical water-pole context and exhaustive preset/mod/moving-camera coverage also remain unverified. Original game state/weather/temporary blocks were restored and test helpers stopped; see the 1.6.10 change log and release receipt.'+new_t[end:]
# Keep genuine unfinished items, narrow verification gaps, and move completed work.
start=current_c.index('## Pending changes\n');end=current_c.index('## Completed changes\n')
pending='''## Pending changes

- optimise performance for referance preset to around 60 FPS while keeping essential viausals, eg. resulution

Performance progress for **1.6.10**: projected-tracer interval reuse and invisible mist-work skips implemented without reducing resolution, quality, range, controls or sampling budgets. Matched GPU output checks pass; unfocused river pass diagnostics suggest lower tracing cost but do not establish gameplay speed. No valid focused full-Reference comparison or achieved 60 FPS claim. The Mac was locked and Minecraft reported unfocused/Dynamic FPS target1 with LONG_AFK/cap15. Keep this request pending. [Current evidence and next test](../stratus-refine-1610/performance-summary.json).

Historical 1.6.9 focused samples were 57.7→56.2 FPS river and 59.1→60.1 forest using the earlier saved quality choices; they do not certify the new full-Reference target. [Historical summary](../stratus-refine-169/performance-summary.json).

### Remaining verification from TASK.md — RUN BOTH dfc0d10a

- [ ] Cloud/foliage verification only — obtain an actual occupied-cloud interior view, clearer independent high-cirrus and sunset framing, and the relevant exact-depth distant-foliage fog fallback scene. Below/above, layer-height grazing, small-span, native and finite motion-pair captures were reviewed in 1.6.10; the layer-height camera was in a footprint hole and cirrus was too subtle for firm acceptance. Preserve the implemented cloud/fog code and controls; stage concrete defects only if reproduced. [Labelled captures](../../outputs/Stratus-1.6.10-visual-checks/index.html).
- [ ] Original-issue verification only — recover/review the originally reported downward-water pole and distant-leaf camera/context. The finite pitch90/shoreline regressions and unchanged pole-filter source do not certify those exact historical views.

'''
completed='''
### Stratus 1.6.10 — 22 October 2026

- [x] Selective settings migration: carry unrelated latest overrides only, reset approved related keys, preserve every old file and existing new-version preferences. Approved 1.6.9 colour/film/water-texture visual defaults apply explicitly in all four presets; future mixed visual/performance defaults belong to Reference unless approved otherwise. Actual Main migration preserved eight unrelated overrides and reset the related film override; nine integration checks pass.
- [x] Existing `REFERENCE` preset now reads **Reference (Recommended)** in Iris. All 62 IDs/defaults/allowed values/menu access and the original six quality assignments per preset remain.
- [x] Finite water review in Main: river/shallow/deep/waterline, waterfall/background water, submerged wood, glass, visible particles and shoreline/screen-edge reflections. Ten current-source underwater GPU regressions also pass. This does not close the exact historical pole issue.
- [x] Finite clear/rain material, sealed cave/local-lamp/night and polished/native sun review, preserving the working 1.6.9 design. Limited/rejected capture attempts are labelled separately.

[Stratus 1.6.10 ZIP](../../outputs/Stratus-1.6.10.zip), [change log and exact evidence](CHANGE-LOG.md#22-october-2026--stratus-1610), [actual captures](../../outputs/Stratus-1.6.10-visual-checks/index.html), [install/load receipt](../../outputs/Stratus-1.6.10-install.json). Installed, selected and loaded in Main; original camera/HUD/pause/flight, weather/daylight and temporary blocks restored. Performance and the remaining verification gaps stay above.

'''
new_c=current_c[:start]+pending+current_c[end:];new_c=new_c.replace('## Completed changes\n','## Completed changes\n'+completed,1)
entry='''## 22 October 2026 — Stratus 1.6.10

### At a glance

- Added a change-aware installer and explicit visual defaults in all four presets. Main retained eight unrelated overrides and reset the approved related film override. **Reference (Recommended)** now appears in Iris; all 62 controls and original quality assignments remain.
- Built **[Stratus 1.6.10](../../outputs/Stratus-1.6.10.zip)**, installed, selected and loaded in Main. [Receipt](../../outputs/Stratus-1.6.10-install.json), [41 labelled actual captures](../../outputs/Stratus-1.6.10-visual-checks/index.html). Original client state, weather/daylight and four temporary blocks restored; all test helpers stopped.
- Passed **768 native pairs**, matched tracer checks over **344,064 pixels per variant**, atmosphere over **131,072 pixels**, **ten underwater cases** and **nine installer integration checks**. Finite water/material/night/sun/menu/cloud views reviewed. **Focused Reference FPS/60 FPS and remaining cloud/original-issue acceptance stay pending.**

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

No valid focused full-Reference sample was available. Minecraft reported1440×842, render12/simulation8, Dynamic FPS UNFOCUSED/target1 and vanilla LONG_AFK/cap15; the desktop tool later reported a locked Mac. Saved VSync=true/maxFPS70/inactivity=afk and Dynamic FPS configuration remain byte-identical. Pending user focus/AppleScript/unlock requests were not treated as approval. No quality cuts were used to satisfy the target. The performance request remains pending.

### Actual Main visual review

Final released ZIP river, underwater air exit and root/Materials pages were captured and inspected. Full Reference QA uses byte-identical235 runtime assets. Finite additional views include submerged wood, transparent glass, visible end-rod particles, waterfall with background pool, clear/rain porous and non-porous fixtures, sealed cave/local light/day/night, polished/native sun, shoreline edge and pitch90 river. Source and synthetic probes supplement these finite views; they are not exhaustive visual acceptance. The first particle capture lacked emitted rods and was superseded by a visible retry. A cave camera was rejected because flow moved it; the corrected view was captured. The shelter wall close-up is insufficient for shelter acceptance.

Cloud review covers below/above, layer-height grazing, small span64, native mode and a finite time pair. The layer-height camera looked through a footprint hole, not occupied cloud. The above-cloud terrain was partly unloaded, so only cloud appearance was accepted. Independent cirrus/sunset captures were too subtle/poorly framed for firm acceptance; these clearer views, occupied-cloud interior and relevant distant-foliage fog scene remain pending. Exact historical pole/leaf cameras were not recovered. The finite downward view does not certify the original pole issue.

Fixed-time baseline/candidate river captures show small reflected-foliage changes even on repeated same-pack captures; **no pixel-equivalence claim** is made from screenshots. The separate native probes provide finite component comparisons within stated tolerances. [Static comparison](../stratus-refine-1610/static-visual-comparison.json), [labelled visual report and per-capture pack/camera manifest](../../outputs/Stratus-1.6.10-visual-checks/index.html).

### Build, restoration and reconciliation

ZIP245 entries/235 runtime assets,7,778,435 bytes, SHA256 `42063ab8b3a24153f6a08c13e87f4d521d1452bee020a00063ce8a8bb5260b3f`. Archive integrity, every source byte and manifest hash pass; immutable full-Reference QA runtime equals released source. Installed ZIP hash matches. [Package checks](../stratus-refine-1610/package-checks.json), [live runtime](../stratus-refine-1610/runtime-v3-Optional_Stratus-1.6.10.zip_.txt), [receipt](../../outputs/Stratus-1.6.10-install.json).

Original camera restored within0.00005 block with identical orientation modulo360; HUD/pause/flight and original menu restored. Original daylight6000, rain0, weather/thunder flags/timers and all four temporary glass blocks restored and verified as their exact original water[level=0] states. Initial restoration hit an unavailable mapped setter before changing blocks; guarded recovery restored and verified exact states, with failure evidence retained. All temporary driver/activity/fixture helpers stopped; profiler original bytecode restored. [Restoration checks](../stratus-refine-1610/restoration-checks.json).

Reconciled TASK only for approved completed migration policy, current release/reference wording and actual verification limits. Moved completed migration, label and finite water/material requests out of CHANGES Pending into Completed. Retained performance, incomplete cloud/foliage acceptance and exact historical issues. [Reconciliation evidence](../stratus-refine-1610/reconciliation.json). No claim that the entire long-term target is finished.

'''
assert '## 22 October 2026 — Stratus 1.6.10' not in current_l
new_l=current_l.replace('# Stratus change and output log\n','# Stratus change and output log\n\n'+entry,1)
# Recheck immediately before each write to preserve any edit arriving mid-reconciliation.
for path,before,after in [(t,current_t,new_t),(c,current_c,new_c),(log,current_l,new_l)]:
 assert path.read_text()==before,f'Concurrent edit: {path}'
 path.write_text(after)
report={'request_id':'dfc0d10a-85ec-429d-ab34-b70c4ce76c83','release':'1.6.10','TASK_frozen_matched_before_reconcile':True,'CHANGES_newer_Reference_target_preserved':True,'completed_moved_out_of_pending':['Selective settings migration and approved all-preset visual defaults','Reference Recommended label','Finite water matrix','Finite material/cave/night/sun matrix'],'remaining_pending':['Approximately60 FPS full Reference active-game performance','Occupied-cloud interior, clearer independent cirrus/sunset, exact distant-foliage fog acceptance','Exact historical water-pole and distant-leaf scene acceptance'],'no_intended_target_weakened_to_excuse_incomplete_code':True,'hashes_after':{p.name:sha(p.read_bytes()) for p in [t,c,log]}}
(w/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

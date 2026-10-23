from pathlib import Path
import json
w=Path('work/stratus-refine-1611');p=Path('outputs/Stratus');load=lambda n:json.loads((w/n).read_text())
rows=[json.loads(line) for line in (w/'chunk-readiness.jsonl').read_text().splitlines()];gates={f.stem:json.loads(f.read_text()) for f in (w/'readiness').glob('*.json')};assert all(g['stable_ms']>=5000 and g['state']['ready'] for g in gates.values());gate={'scope':'Actual normal-world loaded view disk and Sodium queues before visual captures; FPS explicitly deferred.','required_view_disk_columns':441,'render_distance':12,'stable_window_minimum_ms':5000,'observed_not_ready_count':sum(not x['state']['ready'] for x in rows),'observed_max_pending_uploads':max(x['state']['pending_uploads'] for x in rows),'observed_max_pending_tasks':max(x['state']['pending_task_lists'] for x in rows),'completed_gates':gates,'future_BENCH_guard':'Fresh successful gate required at sample start. During sampling poll queues/counts/camera and focus/size; reject nonsteady samples. Actual FPS integration remains deferred/unverified.'};(w/'chunk-gate-checks.json').write_text(json.dumps(gate,indent=2)+'\n')
perf={'version':'1.6.11','status':'Deferred by explicit user instruction: skip for now; user will request later.','new_FPS_samples':0,'target_approximately60FPS_verified':False,'quality_baseline':'User explicitly approved latest saved Main visual and quality choices as Reference. Reference now uses water1/atmosphere1/cloud2/mist3/sky-only0/refraction1. High retains full/detailed settings.','preset_rebase_is_not_shader_code_speedup':True,'new_render_algorithm_optimisation':False,'chunk_gate_implemented_and_exercised_without_FPS':True,'gate_evidence':'work/stratus-refine-1611/chunk-gate-checks.json','next_test':'Only when user requests FPS: same approved Reference settings/camera/resolution; READY gate until all441 view-disk columns present, workers/jobs/uploads/task queues empty, counts stable>=5seconds. Focused active game; record Dynamic FPS/AFK state. Loading-phase results must be labelled separately.','previous1_6_10_full_Reference':'Old full-detail Reference river19.6→20.2/forest17.8→18.1FPS used a different quality baseline; do not compare as an optimisation speedup.'};(w/'performance-summary.json').write_text(json.dumps(perf,indent=2)+'\n')
checks={'version':'1.6.11','date':'2026-10-22','request_id':'d5f466f4-5927-4054-a65f-6a32e48779c1','status':'Approved preset rebase, later-edit-safe migration and actual chunk readiness gate. Native/GPU/Iris/finite visual checks; FPS explicitly deferred. Final release load is recorded in external install receipt.','native':{'program_pairs':768,'variants':8,'dimensions':3,'failures':0,'scope':'Native macOS compatibility-shim compile/link; separate from actual Iris load'},'options':load('option-audit.json'),'Iris_profile_interpretation':load('iris-profile-checks.json'),'installer':load('migration-checks.json'),'underwater':load('water-checks.json'),'chunk_readiness':gate,'performance':perf,'occupied_cloud_evidence':load('cloud-interior-camera.json'),'live':{'profile':'Modrinth Main / Minecraft (1)','world':'Stratus Terrain Lab normal world','Minecraft':'1.21.11','Iris':'1.10.8','Sodium':'0.8.14','hardware':'Apple M1 / macOS / OpenGL4.1','framebuffer':[1440,842],'review':'Matched62-option river/underwater views, existing submerged fixtures, confirmed occupied cloud and clearer independent cirrus/day/sunset isolations. Unloaded first attempts are rejected and superseded by gated retries. Final release and menu review recorded separately in receipt/report.','report':'outputs/Stratus-1.6.11-visual-checks/index.html'},'limits':['No FPS sampling or60FPS verification: explicit user deferral','The approved Reference quality rebase is not a rendering-algorithm speedup','Exact historical pole/distant-leaf contexts and relevant leaf-fog acceptance remain pending','Finite visual checks do not certify every preset/mod/motion/weather combination','All original controls/ranges are retained; selecting a preset intentionally applies its common56 visual defaults plus six quality choices']};(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS1.6.11 — YOUR REFERENCE PRESET AND CHUNK-READY QA
22 October2026 / Minecraft Java1.21.11 / Iris1.10.8 / Sodium0.8.14
Apple M1 / macOS / OpenGL4.1. Original MIT source.

APPROVED PRESET CHANGE
Reference(Recommended) and the source defaults now use the captured latest Main
visual AND quality choices, explicitly approved by the user. Its quality is
half-resolution water/atmosphere, cloud sampling2, mist3, sky-only reflections
and refraction1. This supersedes the old full-detail Reference definition.
High retains full effect resolution, detailed scenery reflections/refraction
and cloud sampling3. All those quality choices remain manually selectable.
Fast/Balanced use lighter quality choices; no component exceeds Reference.
Every preset explicitly shares the same56 visual settings from Reference.
All62 IDs, allowed values, labels/tooltips and menu paths remain available.
Selecting a preset deliberately applies these visual and quality defaults.

CAPTURED MAIN TUNING
Visual values include sky ambient1, film amount0.65, water visibility2.2,
extinction0.9, turbidity3, ripple height0.55/size0.40/rate1, water texture1.
Remaining source visual values are retained and explicit in every profile.
See RELEASE-POLICY.json and CHECKS.json for the complete machine-readable state.

MIGRATION AND NEWER EDITS
The installer resets only the related changed-default/quality keys to the
approved captured Reference values. It carries unrelated overrides and preserves
later manual old-version edits that differ from that capture, including removal
of an override to return to an older source default. Existing new-version
preferences always win. Old archives/preferences are never overwritten.
Run python3 install.py --profile "/path/to/profile" --dry-run, then repeat without
--dry-run. Use --previous-settings when a QA pack is selected. Select the new
ZIP in Iris afterwards. Installing, selecting and loading are separate stages.
Manual ZIP copying does not perform this migration.

VERIFICATION
768 native compile/link pairs/eight variants/zero failures. Iris interpreted
all four62-option profiles and each matched after applying its declared values.
Ten underwater resolve cases at current Reference optics and ten installer
integration checks passed. Actual Main views compare matched Reference tuning,
water/underwater/fixtures, occupied clouds and independent cirrus/day/sunset.
See the labelled report and external Stratus-1.6.11-install.json for exact scope.

CHUNK READINESS AND PERFORMANCE
The QA driver checks all441 columns in the render12 view disk, Sodium build
jobs/workers/upload/task queues and stable counts for at least5seconds before
allowing a steady-state check. Live traces show it blocked while uploads were
pending. Future FPS sampling also requires focus and valid active-game limits.
FPS WAS EXPLICITLY DEFERRED BY THE USER. No new FPS samples or60FPS claim.
The approved lower-cost Reference baseline is not a code-optimisation speedup.
Existing1.6.10 rendering algorithms are retained in this release. Performance,
exact original pole/leaf scenes and remaining leaf-fog acceptance stay pending.
''')
(p/'VALIDATION.txt').write_text('''STRATUS1.6.11 — VALIDATION
768 native compatibility-shim program pairs /8 variants /3 dimensions /0failures.
This checks syntax/linking separately from actual Iris runtime proof.
Ten current-default underwater resolve cases pass with0failures/API errors:
air exits, shallow/deep receivers, glass, additive particles and vertical exits.
Ten temporary-profile installer checks pass, including later related edits,
manual removal of an old override, unrelated preferences, existing new-version
settings, atomic creation and existing/concurrent archive conflicts.

All62 IDs/ranges/menu paths are retained. Four presets explicitly share56visual
values; six quality settings are ordered Fast<=Balanced<=Reference<=High.
Iris parsed62assignments/profile and matched all four applied profile maps.
Source defaults now match approved Reference, including current Main quality.
The old full-detail Reference definition was deliberately superseded by user.

Actual Main captures: matched baseline/candidate Reference tuning, river,
underwater and existing fixtures; camera inside a confirmed occupied active
cloud cell; independent cirrus with lower clouds disabled, day/sunset on/off.
Initial unloaded isolation attempts are rejected; gated retries are retained.
No pixel-equivalence or exhaustive scene/preset/mod certification is claimed.
Final archive/source/installed byte proof and loaded pipeline are recorded in
external outputs/Stratus-1.6.11-install.json and the versioned visual report.

Chunk readiness is actual data, not an arbitrary wait: all441 view-disk columns
loaded, queues/workers/uploads empty and counts stable>=5seconds. Traces show
not-ready periods and later successful gates. Future benchmark sampling requires
a fresh gate and monitors renewed chunk/camera/focus/size changes. FPS integration
and60FPS acceptance remain deferred by the user's explicit request. No FPS was
sampled this pass. Old1.6.10full-quality results are a different quality baseline.

Current rendering algorithms, old pole filter, resource-pack sun/cloud sources,
all higher quality choices, old settings and unrelated mods/worlds are preserved.
Exact historical pole/leaf context and relevant leaf-fog review remain pending.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS1.6.11 — LIVE CHECKS / NEXT PERFORMANCE RUN
Select the new ZIP after running the change-aware installer. Reference now
represents the explicitly approved Main visual AND quality baseline. High keeps
full-resolution detailed optics; Fast/Balanced are lighter. Every control remains.
Confirm Reference(Recommended) in Iris and the expected film/water defaults.
A later preserved manual override can correctly make the active profile Custom.

Completed technical/live checks are listed in VALIDATION.txt and the external
visual report. Initial unloaded frames are rejected and labelled separately.
The active cloud texture was read only into private work evidence; no Minecraft
texture is bundled with the shader. Existing source uses active resource assets.

FPS TESTING IS DEFERRED: do not start sampling until the user requests it again.
For that future run: confirm actual profile/pack/options/framebuffer/render and
simulation distances/weather/time/camera. READY must wait for all view-distance
columns plus empty Sodium jobs/workers/uploads/task queues and stable counts
>=5seconds. A fresh successful gate is required at BENCH start. Record focus,
Dynamic FPS and vanilla AFK limiter continuously. Label chunk-loading samples
separately; never use them as steady-state results. Compare at matched quality;
the preset rebase is not a rendering-algorithm speedup. Keep60FPS pending until
actual evidence supports it. Stop all temporary helpers and restore client/world
state afterwards. Do not substitute old full-detail Reference benchmarks.
''')
print('Prepared1.6.11 release documentation with explicit FPS deferral and approved preset semantics.')

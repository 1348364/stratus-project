from pathlib import Path
import json,hashlib
w=Path('work/stratus-refine-1611');d=Path('work/Custom instructions');files={n:(d/n).read_text() for n in ['TASK.md','CHANGES.md','CHANGE-LOG.md','COMPLETED-CHANGES.md']}
for n,s in files.items():(w/('pre-reconcile-'+n)).write_text(s)
assert files['TASK.md']==(w/'frozen-TASK.md').read_text(),'Newer TASK edits require a preserving merge'
assert json.loads(Path('outputs/Stratus-1.6.11-install.json').read_text())['loaded']
s=files['TASK.md'].replace('versioned release `outputs/Stratus-1.6.10.zip`','versioned release `outputs/Stratus-1.6.11.zip`')
old='- Default policy = ';start=s.index(old);end=s.index('\n',start);s=s[:start]+'''- Default policy = keep exact defaults/choices in shader source. Reference and source defaults use the explicitly approved captured Main visual and quality tuning. All presets explicitly share its 56 visual defaults; six performance settings are ordered Fast ≤ Balanced ≤ Reference ≤ High, with all higher/manual choices retained. New releases carry unrelated latest overrides and reset related keys to approved release defaults; preserve old files and existing new-version settings. Later manual old-version edits differing from the captured approved baseline also win, including returning to an older source default. The 1.6.11 preset rebase was explicitly approved to include quality, superseding the old full-detail Reference definition. Manual ZIP copying does not perform migration.'''+s[end:]
s=s.replace('- Balanced preset = half-resolution water and atmosphere with moderate scenery tracing.','- Balanced preset = half-resolution water and atmosphere with lighter cloud/mist/refraction sampling than Reference and the same approved sky-only reflection mode; keep all other reflection choices available.')
s=s.replace('- "Reference (Recommended)" preset = full effect resolution, detailed reflections and stronger cloud sampling.','- "Reference (Recommended)" preset = the explicitly approved captured Main visual and quality baseline, currently balanced-resolution water/atmosphere/refraction, sky-only reflections and stronger cloud/mist sampling than Balanced. Exact values live in source. Do not silently lower this approved baseline further for performance.')
s=s.replace('- High preset = reference effect resolution with further cloud sampling.','- High preset = full effect resolution, detailed scenery reflections/refraction and higher cloud sampling, above the approved Reference baseline. All levels remain manually selectable.')
needle='- Performance validation = ';start=s.index(needle);end=s.index('\n',start);s=s[:end]+'''\n- Chunk readiness = before steady-state FPS, require all columns in the current view-distance disk loaded, no queued mesh jobs/busy workers/pending uploads/task lists, and stable loaded/section counts for at least five seconds. Require a fresh successful gate at sampling start and reject renewed loading/camera/focus/size changes. Label any optional chunk-loading FPS separately from steady-state results. A fixed wait or frame counter alone is insufficient.'''+s[end:]
start=s.index('- Current verification limits = ');end=s.index('\n',start);s=s[:start]+'''- Current verification limits = 1.6.11 has 768 native compile/link pairs, ten current-default underwater GPU cases, ten migration checks, all four 62-option profiles parsed/matched by Iris, archive/source/install equivalence, actual Main release loading with all 62 values equal to approved Reference, and finite river/underwater/fixture/menu review. The live readiness barrier blocked pending uploads and waited for all 441 render12 columns plus at least five seconds of quiescence. A camera inside an occupied active cloud cell and clearer lower-cloud-disabled cirrus/day/sunset on/off captures were reviewed, with unloaded initial attempts rejected. No FPS was sampled: the user explicitly deferred it until a later request. The approximately60FPS target on the newly approved Reference, actual FPS gate-integration check, relevant distant-leaf fallback and exact historical pole/leaf contexts remain pending. Earlier full-detail Reference FPS does not certify the new baseline or a code speedup. Current rendering algorithms and every control/range remain; source defaults/presets changed by explicit approval. Client view/HUD/pause/flight and original daylight1000/weather/timers were restored, test helpers stopped and QA copies removed; see the1.6.11 receipt/change log.'''+s[end:]
new_task=s
# Edit only identified completed/current-pass lines; preserve unknown newer additions.
s=files['CHANGES.md'];original=[line for line in (w/'frozen-CHANGES.md').read_text().splitlines() if line.startswith('- Make sure that referance')];assert len(original)==1 and original[0] in s;s=s.replace(original[0]+'\n','',1)
perf_line=[line for line in s.splitlines() if line.startswith('- optimise performance for referance')][0]
progress='''

Current **1.6.11** progress: Reference/source defaults now use the explicitly approved captured Main visual **and quality** tuning; every preset shares 56 visual defaults with six ordered quality choices. The live readiness barrier waits for all view-distance columns, empty queues/workers/uploads and stable counts for ≥5 seconds. FPS sampling and the approximately60FPS target remain **unverified and deferred**: the user said “skip for now, i will request this later.” Do not start FPS tests until requested again. [Release/evidence](CHANGE-LOG.md#22-october-2026--stratus-1611), [readiness evidence](../stratus-refine-1611/chunk-gate-checks.json).
''';s=s.replace(perf_line,perf_line+progress,1)
s=s.replace('Performance progress for **1.6.10**:','Historical full-detail Reference progress for **1.6.10**:',1)
cloud_line=[line for line in s.splitlines() if line.startswith('- [ ] Cloud/foliage verification only')];assert len(cloud_line)==1
s=s.replace(cloud_line[0],'- [ ] Verification only — review the relevant exact-depth distant-foliage fog fallback in its intended scene. Occupied-cloud interior and clearer independent cirrus/day/sunset comparisons were completed in 1.6.11; preserve the implemented cloud/fog code and controls. Stage concrete defects only if reproduced. [Verified finite cloud views](../../outputs/Stratus-1.6.11-visual-checks/index.html).',1)
s=s.replace('### Staged clarification — STAGE AND RUN d5f466f4 (22 October 2026)','### Next performance verification — deferred by the user',1)
lines=[]
for line in s.splitlines():
 if line.startswith('- [ ] Adopt the latest saved Main visual **and quality** choices'):continue
 if line.startswith('- [ ] Require actual chunk readiness before steady-state FPS sampling;'):
  line='- [ ] On the next user-requested FPS run, verify the implemented readiness guard in actual sampling: require a fresh successful gate, reject renewed loading/camera/focus/size changes and keep any optional loading-phase samples separate. The barrier itself was live-checked before captures; FPS integration is deferred.'
 if line.startswith('The frozen TASK delta repeats completed1.6.10'):continue
 if line.startswith('FPS deferral for request d5f466f4:'):continue
 lines.append(line)
new_changes='\n'.join(lines).rstrip()+'\n';assert '[x]' not in new_changes and '## Completed changes' not in new_changes
archive_entry='''### Stratus 1.6.11 — 22 October 2026

- [x] Adopted the captured latest Main visual **and quality** tuning as Reference/source defaults, by explicit user choice. All four presets share 56 visual defaults; six quality settings are ordered below/at/above Reference. All 62 IDs, allowed values and menu paths remain; High retains full detailed optics. Actual Iris reports Reference with zero overrides and all62 values match the approved capture.
- [x] Extended selective migration to preserve later related manual edits and removal of an old override, alongside unrelated tuning and existing new-version settings. Ten temporary-profile checks pass; old Main settings remain intact.
- [x] Completed the occupied-cloud interior and clearer independent cirrus/day/sunset portions of the prior verification request. The active cloud texture confirms an occupied alpha255 cell; accepted on/off views were chunk-gated. Unloaded initial attempts are labelled rejected/superseded. The distant-foliage and original pole/leaf checks remain pending in CHANGES.md.

[Stratus1.6.11 ZIP](../../outputs/Stratus-1.6.11.zip), [change log and evidence](CHANGE-LOG.md#22-october-2026--stratus-1611), [actual captures](../../outputs/Stratus-1.6.11-visual-checks/index.html), [install/load receipt](../../outputs/Stratus-1.6.11-install.json). Native768 pairs, ten underwater cases and four62-option Iris profile checks passed. The readiness barrier was live-checked without FPS; actual FPS integration and60FPS acceptance are explicitly deferred by the user. No new rendering-algorithm speedup is claimed.

'''
archive=files['COMPLETED-CHANGES.md'];assert '## Completed changes\n' in archive;new_archive=archive.replace('## Completed changes\n','## Completed changes\n\n'+archive_entry,1)
log_entry='''## 22 October 2026 — Stratus 1.6.11

### At a glance

- Reference/source defaults now use the user's explicitly approved Main visual **and quality** tuning. All four presets share56 visual settings with six ordered quality choices. All62 controls/ranges/menu access remain; High retains full detailed optics. The installer preserves later manual edits.
- Built **[Stratus1.6.11](../../outputs/Stratus-1.6.11.zip)**, installed, selected and loaded in Main. Iris reports **REFERENCE / zero overrides**; all62 runtime values match the captured Main baseline. [Receipt](../../outputs/Stratus-1.6.11-install.json), [18 labelled actual captures](../../outputs/Stratus-1.6.11-visual-checks/index.html).
- Passed768 native pairs, ten underwater cases, ten migration checks and actual Iris interpretation/matching for all four62-option profiles. The readiness barrier blocked while work was pending and waited for stable loaded chunks. Occupied-cloud and clearer independent cirrus/day/sunset views passed finite review. **FPS/60FPS and remaining leaf/historical acceptance stay pending by explicit user deferral.**

### Frozen request and approved scope

Stratus Studio `stage_run` **d5f466f4-5927-4054-a65f-6a32e48779c1**. Current TASK/CHANGES matched their frozen snapshots at start. The nonempty TASK diff only repeats completed1.6.10 reference/migration/optimisation/evidence reconciliation, so no duplicate source work was invented. Existing pending requests supplied the new preset and chunk-readiness work. [Staging record](../stratus-refine-1611/staging.json).

The preset request conflicted with TASK's old full-resolution detailed-Reference definition. The user explicitly chose **“Adopt my current visual and quality choices as Reference”**. This deliberate baseline change supersedes that definition. It is not an equivalent-quality code optimisation and must not be compared with old full-detail Reference as a speedup. The user later said **“skip for now, i will request this later”** for FPS; no FPS samples were taken.

Main preferences changed during the initial reads. Preserved both snapshots and captured the latest saved tuning for the approved baseline; later related manual edits are protected during migration. No newer project-document edits were overwritten. [Initial settings snapshot](../stratus-refine-1611/Main-initial-tuning-snapshot.txt), [approved captured settings](../stratus-refine-1611/Main-before-Stratus-1.6.10.zip.txt).

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

'''
new_log=files['CHANGE-LOG.md'].replace('# Stratus change and output log\n','# Stratus change and output log\n\n'+log_entry,1)
outputs={'TASK.md':new_task,'CHANGES.md':new_changes,'CHANGE-LOG.md':new_log,'COMPLETED-CHANGES.md':new_archive}
for name,text in outputs.items():
 assert (d/name).read_text()==files[name],'Concurrent edit: preserve '+name
 (d/name).write_text(text)
report={'request_id':'d5f466f4-5927-4054-a65f-6a32e48779c1','release':'1.6.11','initial_frozen_current_documents_match':True,'TASK_delta_already_completed1_6_10_not_duplicated':True,'explicit_user_approval_supersedes_old_Reference_definition':True,'later_Main_tuning_snapshots_preserved':True,'newer_manual_override_protection_implemented_and_tested':True,'completed_moved_to_separate_archive':['Approved Main Reference preset/source defaults and ordered shared-style presets','Later manual edit safe migration','Occupied-cloud and clearer cirrus/day/sunset verification portions'],'pending':['Approximately60FPS on new approved Reference; explicitly deferred by user','Actual FPS integration of fresh/stable chunk readiness and renewed-activity rejection','Relevant distant-leaf fog acceptance','Original historical pole/leaf contexts'],'CHANGES_pending_only':True,'new_FPS_samples':0,'hashes_after':{n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in outputs}}
(w/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

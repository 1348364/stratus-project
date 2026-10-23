from pathlib import Path
import json,hashlib,re
w=Path(__file__).parent;d=Path('work/Custom instructions');batch=d/'IN-PROGRESS/7a6a15fb-dcb6-4313-94d3-7a32fb13dd79';checks=json.loads((w/'final-audit.json').read_text());assert checks['release_loaded'] and checks['state_restored'] and checks['all_captures_reviewed']
conflicts=[]
p=d/'TASK.md';s=p.read_text();initial=(w/'initial-TASK.md').read_text()
replacements={
 '- Water look = clear, depth-aware, environment-responsive water with convincing reflections, refraction, ripples, shoreline transitions and underwater visibility, plus a restrained adjustable native animated water-texture tint.':'- Water look = clear, depth-aware, environment-responsive water with convincing reflections, refraction, ripples, shoreline transitions and underwater visibility, plus a clearly visible adjustable native animated water-texture/biome tint across the whole visible surface, including distant reflective water.',
 '- Current reference = editable source `outputs/Stratus/` and versioned release `outputs/Stratus-1.6.11.zip`; check live state before assuming a newer task uses this build. The older water-pole test archive remains preserved separately.':'- Current reference = editable source `outputs/Stratus/` and versioned release `outputs/Stratus-1.6.12.zip`; check live state before assuming a newer task uses this build. The older water-pole test archive remains preserved separately.',
 '- Optics = angle-dependent dielectric Fresnel reflection, refraction, ripple normals, depth-dependent absorption/scattering, biome-aware tint, turbidity and clarity; visible geometry stays vanilla. The optional native still/flow texture uses the active animated atlas sample, modulates transmitted water only and leaves opacity/reflection quality unchanged; zero strength restores the clear surface.':'- Optics = angle-dependent dielectric Fresnel reflection, refraction, ripple normals, depth-dependent absorption/scattering, biome-aware tint, turbidity and clarity; visible geometry stays vanilla. The optional native still/flow atlas pattern and biome colour multiplicatively tint the composed water surface after reflection/transmission mixing, including distant and reflection-dominated water. Preserve native atlas filtering, natural atmospheric fade, sharp reflection detail and opacity; no arbitrary nearby-only cutoff or tint on dry banks/air. Zero strength disables this added surface treatment. Underwater exit/segment attenuation remains independent and unchanged.'}
old=next(l for l in initial.splitlines() if l.startswith('- Current verification limits ='))
replacements[old]='- Current verification limits = 1.6.12 passed768 native compile/link pairs,192 targeted surface GPU samples,ten underwater cases,ten selective-migration checks and actual Iris interpretation/matching of all four62-value profiles. Matched Main zero/half/default=max and1.6.11 baseline views plus close/grazing/downward/underwater, all-preset, existing water-fixture/glass/particle and waterline views were reviewed with actual loaded-chunk gates. The just-below-surface waterline view has a rectangular sky/treetop tint band on both1.6.11 and1.6.12; it remains unresolved and pending, not a clean acceptance result. Source defaults/choices and preset quality assignments are unchanged. Final packaged release/source/install bytes and actual Reference loading are recorded in the1.6.12 receipt/report. This is finite current-world coverage, not exhaustive mod/resource-pack/weather/motion certification. Prior1.6.11 occupied-cloud/cirrus checks remain historical evidence; cloud/fog algorithms are unchanged. No FPS was sampled: the approximately60FPS target, actual FPS gate integration, relevant distant-leaf fallback and exact historical pole/leaf contexts remain pending. Client camera/HUD/pause/flight and original daylight/weather state were restored, helpers stopped and temporary QA variants removed; see CHANGE-LOG.md.'
for a,b in replacements.items():
 if a in s:s=s.replace(a,b,1)
 elif b not in s:conflicts.append('TASK paragraph changed during run; preserved: '+a[:85])
p.write_text(s)
p=batch/'CHANGES.md';s=p.read_text();old=(w/'initial-batch-CHANGES.md').read_text();start=old.index('- [ ] **Vanilla tint');end=old.index('- optimise performance',start);water=old[start:end]
remaining_water='''- [ ] **Remaining waterline acceptance for the whole-surface water change** — the native tint/coverage portion is implemented and finitely verified in1.6.12; this request is not fully closed. A rectangular sky/treetop tint band with the eye just below the surface remains, reproduced at the identical camera on both1.6.11 and1.6.12. Retain the coherent-waterline target; diagnose the missing/near-clipped exit-depth path before attempting a repair, then recheck the transition and above-water tint/underwater/glass/particle regressions. The near-plane explanation is a hypothesis, not a confirmed cause. Repro: Terrain Lab feet164.5,61.24,40.5 / yaw0 / pitch0, approved Reference. [Evidence and scope](../../../stratus-refine-1612/waterline-issue.json), [matched captures](../../../../outputs/Stratus-1.6.12-visual-checks/index.html), [release log](../../CHANGE-LOG.md#23-october-2026--stratus-1612).

'''
if water in s:s=s.replace(water,remaining_water,1)
else:conflicts.append('Active water brief changed during run; newer pending text preserved.')
s=s.replace('Current **1.6.11** progress:','Last performance-related **1.6.11** progress:')
s=s.replace('(CHANGE-LOG.md#','(../../CHANGE-LOG.md#').replace('(../stratus-refine-','(../../../stratus-refine-').replace('(../../outputs/','(../../../../outputs/')
p.write_text(s)
release='23 October 2026 — Stratus 1.6.12'
entry=f'''## {release}

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

Release SHA256: `{checks['sha256']}`; {checks['entries']}entries / {checks['runtime_assets']}runtime assets. [Final audit](../stratus-refine-1612/final-audit.json). Remaining performance/FPS and intended historical leaf/pole checks stay pending in the active batch; its path is authoritative for this request.

'''
p=d/'CHANGE-LOG.md';s=p.read_text();anchor='# Stratus change and output log\n\n';assert anchor in s
if '## '+release not in s:s=s.replace(anchor,anchor+entry,1)
p.write_text(s)
p=d/'COMPLETED-CHANGES.md';s=p.read_text();anchor='## Completed changes\n\n';assert anchor in s
addition='''### Stratus 1.6.12 — 23 October 2026

- [x] Completed the whole-surface tint portion: native animated water texture/biome tint visibly covers the whole water surface, including distant and reflection-dominated views; zero disables the added treatment. Reflections/refraction, shallow-bed clarity, water paths and every control/range/preset quality choice remain. Passed technical/installer/Iris checks and finite matched Main river/grazing/downward/underwater/preset/fixture/waterline review. The pre-existing below-surface rectangular tint band remains unresolved; the original request’s remaining waterline acceptance is kept pending in its active batch. FPS and the original unknown pole/leaf contexts also remain pending.

[Release](../../outputs/Stratus-1.6.12.zip) · [Change log and limits](CHANGE-LOG.md#23-october-2026--stratus-1612) · [Actual visual comparisons](../../outputs/Stratus-1.6.12-visual-checks/index.html) · [Install/load receipt](../../outputs/Stratus-1.6.12-install.json).

'''
if '### Stratus 1.6.12' not in s:s=s.replace(anchor,anchor+addition,1)
p.write_text(s)
(w/'reconciliation.json').write_text(json.dumps({'batch':str(batch),'completed':'whole-surface water tint','pending':'existing waterline acceptance, performance/FPS by deferral and intended historical foliage/pole contexts','conflicts':conflicts,'shared_next_queue_edited':False,'documents':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [d/'TASK.md',d/'CHANGE-LOG.md',d/'COMPLETED-CHANGES.md',batch/'CHANGES.md']}},indent=2)+'\n')
print('Reconciled verified water request; retained active-batch unfinished work. Conflicts:',conflicts)

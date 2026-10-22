from pathlib import Path
import json,hashlib,html,shutil
w=Path(__file__).parent;docs=Path('work/Custom instructions')
receipt=json.loads(Path('outputs/Stratus-1.6.8-install.json').read_text());assert receipt['release_loaded']
assert (w/'driver-stopped.txt').exists()
historical={n:hashlib.sha256((docs/n).read_bytes()).hexdigest() for n in ['TASK-previous-brief.md','SHADER-SPEC-1.6.7.md','SHADER-SPEC.md','SPEC-BASELINE.md']}
original=(docs/'TASK.md').read_text();task=original
changes={
'versioned release `outputs/Stratus-1.6.7.zip`':'versioned release `outputs/Stratus-1.6.8.zip`',
'- Daylight = mostly vanilla block-face contrast, gently enhanced by realistic sun/sky/ground light; preserve caves and local light.':'- Daylight = mostly vanilla block-face contrast, gently enhanced by realistic sun/sky/ground light; preserve caves and local light. Turning the main realistic-lighting mode off restores game vertex face/AO shading and lightmap colour/brightness, with artistic brightness and colour effects bypassed.',
'- Wet materials = absorbent surfaces can darken and develop a subtle rain sheen; dry and non-absorbing surfaces stay matte.':'- Wet materials = absorbent surfaces can darken and develop subtle adjustable sheen in clear weather or rain. Preserve a rain-only choice, exposure/material gating and a true dry setting; non-absorbing surfaces stay matte.',
'- Face-lighting controls = retain the separate component controls, overall face contrast and blend controls; setting either overall control to zero bypasses the effect. Keep ambient occlusion and separately adjustable ground warmth.':'- Face-lighting controls = retain the separate component controls, overall face contrast and blend controls; setting either overall control to zero bypasses the components in enhanced mode. Keep ambient occlusion and separately adjustable ground warmth. A separate main realistic-lighting switch selects the complete vanilla lighting path without erasing saved component settings.',
'- Caves = retain mapped local block light and emission, with controlled brightness and warmth.':'- Caves = retain mapped local block light and emission, with controlled brightness and warmth in enhanced mode. Vanilla lighting uses the original game lightmap rather than Stratus ambient/lamp multipliers or invented emission boosts.',
'- Rain sheen = view-dependent but restrained on exposed absorbent surfaces; non-absorbing metal, clear materials and dry surfaces remain matte.':'- Wet sheen = view-dependent but restrained on exposed absorbent surfaces, with explicit all-weather and rain-only conditions. Surface dampness and sheen strength remain independently adjustable; zero dampness is dry. Non-absorbing metal, glazed materials and sealed caves remain nonglossy.',
'- Wet-sheen migration = preserve saved-setting meaning for sheltered retention while also allowing it to scale the rain-only absorbent film; approximate sky/solar highlights, no scenery trace or extra pass.':'- Wet-sheen migration = preserve saved-setting meaning for sheltered retention and film strength; a separate weather-source choice enables clear-weather film or the previous rain-only response. Approximate sky/solar highlights, no scenery trace or extra pass. The vanilla lighting path bypasses material recolouring/film to preserve vanilla surface colour.',
'- Colour controls = retain exposure, white balance, saturation, ambient brightness, bloom and lighting controls instead of hard-coding one look.':'- Colour controls = retain exposure, white balance, saturation, ambient brightness, bloom and lighting controls instead of hard-coding one look. Vanilla lighting bypasses artistic exposure, white balance, saturation, highlight shoulder, bloom and ground warmth while retaining their saved values. Stratus water, clouds and atmosphere remain independently active.',
'- Menu = navigable two-column Water, Lighting, Atmosphere, Materials, Post and Performance categories with relevant submenus and English labels on every reachable control.':'- Menu = navigable two-column Water, Lighting, Atmosphere, Materials, camera/colour and Performance categories. Use smaller face/ambient/block-light, lower/high-cloud, cloud-shape, colour and bloom groups, concise labels, useful spacing and English tooltips on every reachable control.',
'- Optimisation = target measured bottlenecks; avoid redundant passes, texture reads and ray steps, and skip invisible-pixel work, while preserving full selected quality and all intended visuals.':'- Optimisation = target measured bottlenecks; avoid redundant passes, texture reads and ray steps, and skip invisible-pixel work, while preserving full selected quality and all intended visuals. Skip cloud-field evaluation only beyond its guaranteed zero-density envelope, hoist invariant mist lighting without changing sampling, and skip unused bloom passes in vanilla lighting. Keep whole-game improvement and appearance claims pending until matched focused measurements support them.',
'- Current verification limits = focused FPS, exhaustive scene/preset/mod coverage and the originally reported distant-leaf scene remain unverified for 1.6.7; no full-equivalence or maximum-speed claim follows from finite checks.':'- Current verification limits = 1.6.8 has native/GPU and finite actual Main lighting/material/menu/river review, with preserved current saved settings. Focused 1.6.7/1.6.8 FPS was explicitly deferred by the user to the morning of 22 October 2026. Exhaustive scene/preset/night/mod coverage and the original distant-leaf scene remain unverified. Isolated atmosphere GPU timings do not establish whole-game speedup or universal 99% visual equivalence.'}
for before,after in changes.items():
 assert task.count(before)==1,before
 task=task.replace(before,after)
assert (docs/'TASK.md').read_text()==original,'User changed target during reconciliation'
(w/'reconciliation-before-TASK.md').write_text(original);(docs/'TASK.md').write_text(task)

p=docs/'CHANGES.md';original=p.read_text();queue=original
old="- [ ] Finish the archived 1.6.7 brief's focused matched FPS/frame-time verification before implementing the four requests below. The 243-entry release/source/installed integrity recheck passed. Current benchmark access is waiting for explicit approval of temporary Java test-code attachment and Minecraft window focus; normal desktop selection failed. No new performance result is claimed. [Current check and blockers](../stratus-finish-167/status.json)."
new="- [ ] Finish the archived 1.6.7 brief's focused matched FPS/frame-time verification. Minecraft testing, including the temporary Java test route, is authorised. The user explicitly asked to skip focused testing until the morning of **22 October 2026** and continue implementation. Keep this pending; no background sample counts as a valid result. [Current status](../stratus-finish-167/status.json)."
assert queue.count(old)==1;queue=queue.replace(old,new)
finished=[
'- When the realistic shading is turned off, all shading needs to look vanilla including face shading, colour, brightness, ambiant brightness, etc',
'- Allow wet sheem without being in weather conditions, so all time',
'- Clean up shader options pages, following the guidelines from other popular shaders']
for row in finished:
 assert queue.count(row)==1,row
 queue=queue.replace(row+'\n','')
old='- Optimise performance searching and using exsisting expert sources, while keeping 99% of visuals'
new='- [ ] Optimise performance using existing expert sources while keeping 99% of visuals. **Partial:** 1.6.8 implements empty-cloud bounds checks, invariant mist lighting and the vanilla-mode unused-bloom bypass; all quality budgets and controls remain. Four-view isolated GPU checks measured approximately 4–6% lower atmosphere draw duration with very small tested image differences. **Still pending:** matched focused gameplay FPS/frame times and broader visual review; the finite microbenchmark does not certify universal 99% equivalence. [Measurements and limits](../stratus-refine-168/performance-summary.json).'
assert queue.count(old)==1;queue=queue.replace(old,new)
done='''### Stratus 1.6.8 — 21–22 October 2026

- [x] Added a main Realistic lighting switch: Off restores the game vertex face/AO and lightmap colour/brightness, bypassing artistic brightness/colour and material recolouring. Independent face component controls remain available.
- [x] Added selectable All weather / Rain only sheen, retaining strength/dampness controls and absorbent-material/exposure gating. Main clear-weather comparisons completed.
- [x] Reorganised the existing settings into smaller two-column effect groups, guided by Iris documentation and Complementary's category/submenu organisation. All 59 prior settings/defaults/ranges and four presets remain; 61 controls total.

Built, installed, selected and actually loaded [Stratus 1.6.8](../../outputs/Stratus-1.6.8.zip). Current saved Main values were preserved and carried over; the camera, HUD/pause state and flight flag were restored and the temporary driver stopped. [Change log and verification](CHANGE-LOG.md), [actual Minecraft captures](../../outputs/Stratus-1.6.8-visual-checks/index.html), [install receipt](../../outputs/Stratus-1.6.8-install.json).

'''
queue=queue.replace('## Completed changes\n\n','## Completed changes\n\n'+done,1)
queue=queue.replace('All five are already present in the current **1.6.7** source, released ZIP and installed pack. No missing shader code was found and no duplicate build was made.','At the archived-brief recheck, all five were already present in **1.6.7** source, released ZIP and installed pack; no missing code or duplicate build was needed for that brief. The subsequent approved 1.6.8 changes preserve that completed work and document their deliberate new lighting/film modes.')
assert p.read_text()==original,'User changed queue during reconciliation'
(w/'reconciliation-before-CHANGES.md').write_text(original);p.write_text(queue)

report=Path('outputs/Stratus-1.6.8-visual-checks');(report/'screenshots').mkdir(parents=True,exist_ok=True)
rows=[]
for shot in sorted((w/'screenshots').glob('*.png')):
 status='Reviewed actual Main QA comparison'
 if shot.name=='s168-final-river.png':status='Rejected acceptance frame: insufficient visible terrain after teleport; superseded by loaded overview/release captures'
 elif 'restored-position' in shot.name:status='Camera restoration evidence; not visual acceptance'
 elif shot.name.startswith('s168-release-'):status='Final released 1.6.8 ZIP loaded in Main; reviewed capture'
 elif 'game-vanilla-reference' in shot.name:status='Minecraft with shaders disabled; lighting reference, custom sky/water intentionally differ'
 elif 'final-' in shot.name:status='Final runtime shader code / reviewed Main capture'
 elif 'baseline' in shot.name:status='1.6.7 baseline with matched latest Main option values'
 shutil.copy2(shot,report/'screenshots'/shot.name)
 rows.append({'file':shot.name,'status':status,'sha256':hashlib.sha256(shot.read_bytes()).hexdigest()})
(report/'captures.json').write_text(json.dumps(rows,indent=2)+'\n')
figures='\n'.join('<figure><figcaption>'+html.escape(r['file'])+'<small>'+html.escape(r['status'])+'</small></figcaption><a href="screenshots/'+r['file']+'"><img loading="lazy" src="screenshots/'+r['file']+'" alt="'+html.escape(r['file'])+'"></a></figure>' for r in rows)
(report/'index.html').write_text('''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.6.8 — actual Main verification</title><style>body{font:16px/1.5 system-ui;margin:32px auto;padding:0 20px;max-width:1480px;background:#141b23;color:#edf3f8}a{color:#93d3ff}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:22px}figure{margin:0;background:#202c38;padding:12px;border-radius:8px}figcaption{overflow-wrap:anywhere;margin-bottom:10px}small{display:block;color:#bdcddc;font-size:13px}img{display:block;width:100%;height:auto}aside{border-left:3px solid #80b9e6;padding:0 16px;margin:24px 0}</style></head><body><h1>Stratus 1.6.8 — actual Minecraft checks</h1><p>21–22 October 2026 · Modrinth Main · normal Stratus Terrain Lab · Minecraft 1.21.11 / Iris 1.10.8 / Apple M1 · 1440 × 842 framebuffer.</p><p>These original game captures show clear-weather film sources/strength, vanilla lighting versus a shaders-disabled game reference, the new settings groups, river and underwater views. Final release loading is confirmed separately in the <a href="../Stratus-1.6.8-install.json">install receipt</a>. Click any image for the original pixels.</p><aside>Focused FPS was deferred by the user to the morning of 22 October. The separate 128 × 128 atmosphere GPU microbenchmark is not gameplay FPS or universal 99% image-equivalence proof. Animation continues during comparisons. One early river frame lacks sufficient terrain and is explicitly rejected; restoration frames are state evidence. Broader night/preset/mod/motion checks and the historical foliage scene remain pending.</aside><p><a href="../../work/Custom%20instructions/CHANGE-LOG.md">Detailed change log</a> · <a href="../../work/stratus-refine-168/performance-summary.json">Isolated GPU measurements</a> · <a href="captures.json">Capture hashes and classifications</a></p><main>'''+figures+'</main></body></html>')
assert all(hashlib.sha256((docs/n).read_bytes()).hexdigest()==digest for n,digest in historical.items())
(w/'reconciliation.json').write_text(json.dumps({'target_reconciled_with_source_release_and_evidence':True,'pending_focused_checks_retained':True,'newer_unrelated_edits_preserved':True,'historical_files_unchanged_sha256':historical,'original_game_captures':len(rows)},indent=2)+'\n')
print('Reconciled target and pending queue; historical documents untouched; gallery has',len(rows),'original captures.')

from pathlib import Path
import hashlib,json,re,shutil,html,zipfile
w=Path('work/stratus-check');g=Path('work/minecraft-smoke');p=Path('outputs/Stratus');r=Path('outputs/Stratus-1.4.0-visual-checks');r.mkdir(exist_ok=True)
v=json.loads((w/'validation-1.4.0.json').read_text());target=json.loads((w/'target-140.json').read_text())
for name,digest in v['source_hashes'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
with zipfile.ZipFile(g/'shaderpacks/Stratus-1.4.0.zip') as z:
 for name,digest in v['source_hashes'].items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
log=(w/'minecraft-140-release.log').read_text(errors='replace');assert (g/'qa-complete.txt').read_text().strip()=='v140-final-source-complete'
errors=[line for line in log.splitlines() if re.search(r'ShaderCompileException|Failed to load the shaderpack|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException|\[STRATUS_QA\] ERROR',line,re.I)];assert not errors,errors
for level in range(16):assert f'MATERIAL Block{{minecraft:water}}[level={level}] = {4100 if level==0 else 4103}' in log,level
assert 'Using shaderpack: Stratus-1.4.0.zip' in log
final=['final-reflections','final-waterfall','final-underwater','final-refraction','final-damp-corners','final-cloud-under','final-cloud-above','final-entities','final-nether','final-end','vanilla-sun-clouds','vanilla-clouds','vanilla-moon','clean-water','clean-landscape','clean-clouds','left-open']
settings=['options-'+x for x in ['root','water','reflections','waves','lighting','clouds','sun','fog','materials','post','performance']]
features=['reflections-off','refraction-off','swamp','warm-ocean','frozen-ocean','river','rain-runoff','cave-water','cave-lit','damp-off','damp-grazing','damp-rain','clouds-below','clouds-inside','high-clouds','high-quality-clouds','cloud-water-order','breaking-particles','projectiles','bloom-fireflies','shallow-underwater']
# Each listed frame was inspected directly or in contact sheets; failures/ice-contaminated
# captures and old sun/waterfall images were replaced or excluded.
inspected=final+settings+features
captures={}
for name in inspected:
 f=g/'screenshots'/('v140-'+name+'.png');assert f.exists(),name
 shutil.copy2(f,r/f.name);captures[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
prior_metrics={}
for n in ['balanced-water','balanced-landscape','balanced-clouds','water-confirm','water-final']:
 prior_metrics[n]=json.loads((g/'benchmarks'/('v140-'+n+'.json')).read_text())
metrics={n:json.loads((g/'benchmarks'/('v140-'+n+'.json')).read_text()) for n in ['clean-water','clean-landscape','clean-clouds']}
context=json.loads((w/'release-performance-context.json').read_text())
assert len(context['clients_after_shutdown'])==1 and context['clients_after_shutdown'][0]['type']=='test'
target['other_minecraft_instances_prior_samples']=1;target['other_minecraft_instances']=0
checks={k:x for k,x in v.items() if k!='source_hashes'}
checks.update(source_hashes=v['source_hashes'],actual_iris_load=True,in_game_visual_test=True,shader_errors=0,minecraft='1.21.11',iris='1.10.8',sodium='0.8.14',gpu='Apple M1',opengl='4.1',target=target,
 inspection={'passed':True,'capture_count':len(inspected),'final_runtime_and_menu_views':len(final)+len(settings),'inspected':inspected,'capture_sha256':captures,'scope':'Feature captures across this iteration, followed by final runtime/menu checks. Water views and biome/control/cave captures were repeated after the final tangent-plane refraction and continuous displacement bound. Final underwater/reflection views also test higher SSR hit precision. Cloud/material/particle libraries are unchanged since their feature captures. Finite visual coverage, not all possible worlds/mod combinations.'},
 runtime={'water_levels_verified':16,'water_source_id':4100,'water_flow_id':4103,'active_shader':'Stratus-1.4.0.zip','left_open':True,'world':'StratusCheck (isolated copy)','final_camera':[104.5,104,90.5],'mode':'spectator','original_world_untouched':True,'source_files_identical_to_test_zip':215},
 performance={'measurements':metrics,'method':'Minecraft render-head to render-head monotonic wall intervals, including stalls','preset':'Balanced','framebuffer':[1708,960],'render_chunks':12,'simulation_chunks':8,'vsync':True,'frame_cap':70,'normal_minecraft_also_open':False,'prior_concurrent_measurements':prior_metrics,'context':context,'discarded_samples':['release-water','release-landscape','release-clouds'],'discard_reason':'Player movement and game-mode commands during the samples; not controlled fixed views.','native_compile_finished_before_initial_samples':True,'limits':['Three 20-second single-instance samples after Main exited; finite coverage, including frame stalls.','Five earlier concurrent-load samples retained separately for context. Three player-interrupted samples discarded.','Camera positions/angles recorded before/after each sample. Final source tested.','The final landscape run contains ~67.8ms intervals consistent with Dynamic FPS background limiting; foreground status was not verified throughout. Earlier single-instance landscape was50.4fps before the water-only precision change.','A locked 60 fps target is not verified.']})
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(r/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
(w/'inspection-1.4.0.json').write_text(json.dumps(checks['inspection'],indent=2)+'\n')
perf='\n'.join(f"{name}: {a['average_fps']:.1f} fps average, {a['one_percent_low_fps']:.1f} fps 1% low" for name,a in metrics.items())
text=f'''STRATUS 1.4.0 — WATER-FIRST RELEASE CHECKS
17 October 2026

744 native macOS OpenGL compile/link checks, zero failures: 93 program pairs
across three dimensions and eight variants (four profiles, defaults, option
extremes, vanilla sky). Offline compatibility shims are distinct from actual Iris.
29 GPU-evaluated optical invariants passed: dielectric Fresnel, Snell refraction,
underwater TIR, Beer-Lambert composition, depth absorption, cave/block-light
response, moisture retention/drainage/porosity, cloud depth/direction clipping,
face shading and dark entities. OpenGL probe errors: zero.
43 options remain reachable through the reorganised category/subcategory menu.
215 shader/config files match the actual tested ZIP and source manifest.

Actual Minecraft1.21.11 / Iris1.10.8 / Sodium0.8.14 / AppleM1 OpenGL4.1:
{len(inspected)} inspected feature/runtime/menu captures across this iteration, including
{len(final)+len(settings)} final focused runtime/menu views. Zero shader errors in the final runtime.
All sixteen water levels verified in Iris: source0=4100, flowing1..15=4103.
Fixed during visual QA: incomplete cloud ray coverage/horizon discontinuity,
fixed water reflection boost, crude UV-only refraction, falling-water over-
absorption, unmatched comma-separated fluid states on this Iris version,
blue sky cutouts through water, the vanilla sun's black additive background,
folded floor refraction at grazing angles, and underwater hit-precision banding.
Refraction now intersects the
receiver tangent plane and bounds screen displacement continuously.
Ice-contaminated biome tank captures were discarded; biome tests repeated with
random ticks disabled, then the tick rate restored to3. Water controls, biome
colours, rain, cave optics, sides/underwater, damp corners/ores, clouds from
below/inside/above, vanilla sun/moon/clouds, particles, projectiles, fireflies,
bloom, entities, all dimensions and options were inspected. Library and final
regression scope is recorded in CHECKS.json; this is finite coverage.

All optimisation mods present in Main were reproduced: Sodium, Lithium,
FerriteCore, Entity Culling, Dynamic FPS and Sodium Extra; Fabric API dependency.
Iris and the isolated helper complete the test stack. Main/test JAR hashes match.
Main video settings matched: 12 render, 8 simulation, VSync on, cap70, 1708x960.
Main was gracefully closed with user approval. The final single-instance samples
use only the test Minecraft client, after 8 seconds of scene warmup:
{perf}
Native compiler work had finished before these samples. Camera position and
rotation were checked before/after each run; observations are in CHECKS.json. Five earlier concurrent-load
samples remain in CHECKS.json; three player-interrupted samples were discarded.
The final landscape sample contains ~67.8ms intervals consistent with Dynamic
FPS background limiting; foreground status was not verified throughout. An
earlier single-instance landscape sample was50.4fps before the water-only hit-
precision change. Both are retained in CHECKS.json. A locked60fps is not verified. Screen-space reflection/refraction and sky-cache parallax
limitations remain documented in README.txt.

The isolated client remains OPEN on Stratus1.4.0 at the reflection lake, in
spectator mode with HUD visible. Main's selected shader and original world were
not changed by this task. Release ZIP and editable sources are provided.
'''
(p/'VALIDATION.txt').write_text(text);(p/'IN-GAME-TEST.txt').write_text(text)
rows=''.join(f'<tr><td>{html.escape(n)}</td><td>{x["average_fps"]:.1f}</td><td>{x["one_percent_low_fps"]:.1f}</td><td>{x["p95_frame_ms"]:.1f}</td></tr>' for n,x in metrics.items())
def group(n):
 if n.startswith('options'):return 'Settings'
 if 'water' in n or any(x in n for x in ['reflec','refrac','swamp','ocean','river','cave','runoff']):return 'Water'
 if 'cloud' in n or 'moon' in n:return 'Sky'
 if 'damp' in n:return 'Materials'
 return 'Regression'
cards=''.join(f'<figure data-kind="{group(n)}"><a href="v140-{n}.png"><img loading="lazy" src="v140-{n}.png" alt="{html.escape(n)}"></a><figcaption>{html.escape(n.replace("-"," "))}</figcaption></figure>' for n in inspected)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.4.0 — water-first checks</title><style>
:root{color-scheme:dark}body{margin:0;background:#0e1720;color:#edf4f8;font:16px/1.65 system-ui}main{max-width:1250px;margin:auto;padding:30px 24px}h1{font-size:42px;margin:0}h2{margin-top:38px}p{max-width:1000px;color:#bdcbd6}a{color:#92d6f6}.badge{display:inline-block;background:#173746;padding:5px 12px;border-radius:15px;margin:5px}.hero{width:100%;border-radius:12px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}figure{margin:0;background:#172530;border-radius:10px;overflow:hidden}figure img{width:100%;display:block}figcaption{padding:10px 14px}table{border-collapse:collapse;max-width:850px;width:100%}th,td{padding:8px 16px;text-align:left;border-bottom:1px solid #34444f}button{background:#203643;color:#eaf6ff;border:1px solid #4a697c;padding:9px 15px;border-radius:7px;margin:0 7px 10px 0;cursor:pointer}button[aria-pressed=true]{background:#326f86}.note{border-left:3px solid #d2ad72;padding-left:16px}details{margin:14px 0}pre{white-space:pre-wrap} @media(max-width:750px){.grid{grid-template-columns:1fr}h1{font-size:31px}}
</style><main><h1>Stratus 1.4.0</h1><p>Water-first optics, retained dampness and a reorganised shader menu. Original editable Iris GLSL for Minecraft Java 1.21.11 on macOS.</p>
<div><span class="badge">744 native passes</span><span class="badge">29 GPU optical checks</span><span class="badge">43 reachable settings</span><span class="badge">0 final shader errors</span></div>
<a href="v140-final-reflections.png"><img class="hero" src="v140-final-reflections.png" alt="Water reflections in the actual Minecraft test client"></a>
<h2>What changed</h2><p>Snell-law refraction at water IOR 1.333, dielectric Fresnel and underwater total internal reflection. A shared cloud environment supports reflected and transmitted sky, while clipped screen-space rays resolve visible terrain and entities. Biome tint, sediment, rain runoff, local skylight, cave shelter and lamps influence water. Flowing sheets use bounded thickness, avoiding deep-lake absorption against the sky.</p>
<p>Moisture favours visible concave corners and upward porous faces; walls drain. No random dampness noise. Defaults: vanilla shading mix <b>1.00</b>, water clarity <b>1.70</b>, saturation <b>1.00</b>. Cloud integration covers the full intersected volume with a continuous horizon limit. Actual vanilla fancy clouds and textured sun/moon are independent options.</p>
<p>Scientific basis: <a href="https://pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission">PBRT: Snell and Fresnel</a>, <a href="https://www.usgs.gov/water-science-school/science/turbidity-and-water">USGS: turbidity and runoff</a>, <a href="https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/">Lagarde: wet surfaces</a>. Biome sediment rules are visual heuristics, not measurements or a fluid simulation.</p>
<h2>Performance at current settings</h2><p>Apple M1, 1708×960, 12 render / 8 simulation chunks, VSync, cap70, Balanced. Copied Sodium, Lithium, FerriteCore, Entity Culling, Dynamic FPS, Sodium Extra and Fabric API, with matching Main JAR hashes.</p><p class="note">Main was closed with approval; only the test client ran for these three single-instance 20-second samples. These finite wall-time samples include stalls; camera observations are in results.json. The final landscape run includes intervals consistent with the Dynamic FPS background limit; its foreground status is uncertain. An earlier single-instance landscape run was 50.4 fps before the water-only precision change. A locked 60 fps result is unverified. Earlier concurrent runs and discarded player-interrupted samples are recorded in results.json.</p><table><thead><tr><th>Sample</th><th>Average fps</th><th>1% low fps</th><th>95th frame ms</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h2>Inspected in-game captures</h2><p>Click any unmodified Minecraft ScreenshotRecorder frame for full resolution. The gallery includes feature checks across the iteration and focused final runtime/menu checks. Water control, biome and cave captures were repeated after the final refraction correction. Cloud, material and particle feature captures retain the tested libraries; final sky and general regression views provide additional coverage. The failed ice, black-quad and blue-sky-cutout captures were replaced or excluded.</p>
<div id="filters">'''+''.join(f'<button type="button" data-filter="{n}" aria-pressed="{str(n=="All").lower()}">{n}</button>' for n in ['All','Water','Sky','Materials','Settings','Regression'])+'''</div><div class="grid">'''+cards+'''</div>
<details><summary>Scope and remaining approximations</summary><p>Screen-space optics cannot reconstruct hidden/off-screen geometry. The directional sky cache uses the camera origin, so nearby low-cloud parallax is approximate. Vanilla sun textures and cloud meshes render in the view, but their exact off-screen shapes are not reconstructed by the fallback cache. Refraction uses one opaque depth layer and bounds displacement to available screen coverage; flowing-sheet thickness and cavity retention are geometric approximations. No displaced waves, full fluid simulation or cast shadow maps. Finite tests cannot cover every world and resource/mod combination.</p></details>
<p><a href="results.json">Full checks, source/capture hashes and timings</a> · The test client is left open at the reflection lake on Stratus 1.4.0. The original world and Main shader selection were preserved.</p></main><script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('figure').forEach(f=>f.hidden=b.dataset.filter!=='All'&&f.dataset.kind!==b.dataset.filter)}));</script></html>'''
(r/'index.html').write_text(page)
print('Report:',r/'index.html','|',len(inspected),'inspected frames,',len(final)+len(settings),'runtime/menu views')

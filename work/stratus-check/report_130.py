"""Generate the report from inspected final-source Minecraft captures and timings."""
from pathlib import Path
import hashlib,html,json,re,shutil,zipfile
pack=Path('outputs/Stratus');work=Path('work/stratus-check');game=Path('work/minecraft-smoke');report=Path('outputs/Stratus-1.3.0-visual-checks')
evidence=json.loads((work/'validation-1.3.0.json').read_text());inspection=json.loads((work/'inspection-1.3.0.json').read_text());exit_record=json.loads((work/'exit-1.3.0.json').read_text())
names=(work/'shots-1.3.0.txt').read_text().splitlines();assert len(names)==50 and inspection['inspected']==names and inspection['passed']
assert (game/'qa-complete.txt').read_text().strip()=='r130-complete'
assert exit_record['exit_code']==143
log=(work/'minecraft-1.3.0.log').read_text(errors='replace');marker='Using shaderpack: Stratus-1.3.0-candidate-v2.zip';assert marker in log;runtime=log[log.index(marker):]
benchmark_log=(work/'minecraft-1.3.0-benchmark.log').read_text(errors='replace')
assert 'Using shaderpack: Stratus-1.3.0.zip' in benchmark_log
runtime+='\n'+benchmark_log
patterns=r'ShaderCompileException|Failed to load the shaderpack|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException'
errors=[line for line in runtime.splitlines() if re.search(patterns,line,re.I)];assert not errors,errors
assert 'BUFFER 0 RGBA8' in runtime
for i in range(1,8):assert f'BUFFER {i} RGBA16F' in runtime
for d in ['minecraft:the_nether','minecraft:the_end']:assert d in runtime
for n,digest in evidence['source_hashes'].items():assert hashlib.sha256((pack/n).read_bytes()).hexdigest()==digest,n
report.mkdir(exist_ok=True);shots={}
for name in names:
 source=game/'screenshots'/f'g130-{name}.png';assert f'SCREENSHOT g130-{name} ' in runtime,name
 shutil.copy2(source,report/source.name);shots[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
perf_tags=['fresh130-balanced-landscape','fresh130-balanced-water','fresh130-balanced-clouds','fresh130-fast-water','fresh130-fast-clouds']
performance={tag:json.loads((game/'benchmarks'/f'{tag}.json').read_text()) for tag in perf_tags}
baseline={tag:json.loads((game/'benchmarks'/f'{tag}.json').read_text()) for tag in ['fresh120-landscape','fresh120-water','fresh120-clouds']}
for row in performance.values():assert row['sampled_seconds']>19 and row['frames']>100
for tag in ['balanced-landscape','balanced-water','balanced-clouds','fast-water','fast-clouds']:
 p=game/'screenshots'/f'q130-{tag}.png';assert p.exists();shutil.copy2(p,report/p.name)
limits=['Finite scenarios, not an exhaustive block/mod/world guarantee','Isolated Iris/Sodium/test-helper client; normal-profile mod stack not reproduced','Normal Minecraft client also running; shared GPU/CPU and thermal contention','Native UI inventory reported the Mac locked during measurement; active-play timing may differ','20-second wall-interval samples, not isolated GPU timings; stutters affect lows','No guarantee of locked 60 fps or native Retina resolution performance','Mist follows height, 3D density and depth/skylight, not a simulated terrain humidity field','Approximate cloud scattering and prefiltered reflection sky; half-resolution thin-edge detail loss','Screen-space water cannot recover hidden geometry; approximate partial transparency and bounded waterfall thickness','Class-based estimated roughness and porosity, no measured PBR maps or cast-shadow maps']
checks={k:v for k,v in evidence.items() if k!='source_hashes'}
checks.update(actual_iris_compilation=True,in_game_visual_test=True,runtime={'minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','gpu':'Apple M1','opengl':'4.1','dimensions':['Overworld','Nether','End'],'shader_errors':len(errors),'source_files_match_delivery':len(evidence['source_hashes']),'screenshots_sha256':shots,'main_suite_preset':'Reference, with named comparison options; Fast/High cloud views','settings':(work/'final-settings-1.3.0.txt').read_text(),'inspection':inspection,'process_exit':exit_record,'limits':limits},performance={'framebuffer':[1708,960],'logical_window':[854,480],'render_distance_chunks':8,'simulation_distance_chunks':5,'vsync':False,'fps_cap':260,'warmup_seconds':'45 initial, 25 after pack switch, 15 after relocation; fresh client after visual QA','time':3000,'weather':'clear','normal_client_concurrently_running':True,'mac_locked_reported_during_measurement':True,'method':'MinecraftClient render-head to render-head monotonic wall intervals; no external GPU probe/compiler during final samples','fresh_final_source':performance,'after_extended_reload_qa':{p.stem:json.loads(p.read_text()) for p in (game/'benchmarks').glob('final130-*.json')},'previous_1_2_0_high':baseline,'excluded_experiments':['Initial water/pool-rim and sealed roof views were discarded, rebuilt as an open pool and remeasured','Earlier 1.3 draft timings excluded from final-source claims']})
(pack/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(report/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
perf_lines='\n'.join(f"{tag}: {row['average_fps']:.1f} fps average, {row['one_percent_low_fps']:.1f} fps 1% low" for tag,row in performance.items())
validation=f'''STRATUS 1.3.0 - VERIFIED VALIDATION
17 October 2026

NATIVE GPU: PASS
Apple M1 OpenGL 4.1: 630 compile/link pairs, zero failures. 90 programs routed
across three dimensions, seven variants (default, Fast, Balanced, Reference,
High, numeric minimum/maximum). Offline compatibility shims, separate from Iris.
39 controls/menu entries verified. AO default and maximum remain 1.00.

FOCUSED GPU: PASS
34 cases execute delivered GLSL: denser water, consistent split paths, six
unique cube-face irradiances, warmer daytime ground without night colour shift,
non-glowing entities in darkness, emissive interiors, billboard stability,
XYZ cloud density, upper wisps, depth clipping, structured mist with a clear
foreground and covered-space suppression, warm daytime-only sun.
Both actual quarter-resolution bloom passes execute a separate HDR impulse test:
default radius 3.00 spreads farther than 0.50. OpenGL errors: zero.

ACTUAL IRIS AND VISUAL QA: PASS
Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Java 21 on Apple M1.
50 final-source captures inspected, plus five final-source benchmark views. Tested
normal/underside block faces, warmth comparison, daylight/dark/lit entities,
bloom on/off/radius, fireflies, water body/clarity/refraction/sides/underwater,
water viewed through clouds, projectiles/destruction/smoke, rain/transparency,
lowland fog, ground-level morning/noon sun, sunset, main/upper cloud volumes,
quality profiles, held items, blindness, Nether/lava/End and return.
Shader errors: zero. All {len(evidence['source_hashes'])} shader/configuration files match the tested ZIP.
Water/cloud ordering was exercised at cloud altitude 128/thickness 40, camera
Y184, so both cloud and pool fit the 8-chunk test view; default main layer is192.
The lower-cloud comparison avoids mistaking clipped distant chunks for a shader
failure. Nether was recaptured after its loading screen cleared. The original world and normal-client selection were not edited.

PERFORMANCE (ACTUAL FRAME INTERVALS)
1708x960 framebuffer, 8 render chunks / 5 simulation chunks, VSync off, cap 260.
Normal client was also running. Samples 20 seconds after 15-45 seconds warmup in a fresh client.
{perf_lines}

The approximately 60 fps target was not fully reached in this setup. Averages
and low-percentile stutters differ. The Mac was reported locked during testing. Shared
hardware, world complexity, mods, thermal state, render distance and resolution
can change results. This is not a locked 60 fps or native Retina claim.

See CHECKS.json and the visual report for raw results, limits and observations.
Raw Minecraft screenshot PNGs are unretouched. Test process stopped (SIGTERM143).
'''
(pack/'VALIDATION.txt').write_text(validation)
(pack/'IN-GAME-TEST.txt').write_text(validation)
rows=''.join(f'<tr><td>{html.escape(tag.removeprefix("fresh130-"))}</td><td>{r["average_fps"]:.1f}</td><td>{r["one_percent_low_fps"]:.1f}</td><td>{r["p95_frame_ms"]:.1f}</td></tr>' for tag,r in performance.items())
before=''.join(f'<tr><td>{tag.removeprefix("fresh120-")}</td><td>{r["average_fps"]:.1f}</td><td>{r["one_percent_low_fps"]:.1f}</td></tr>' for tag,r in baseline.items())
cards=''.join(f'<figure><a href="g130-{name}.png" target="_blank"><img loading="lazy" src="g130-{name}.png" alt="{html.escape(name)}"></a><figcaption>{html.escape(name.replace("-"," "))}</figcaption></figure>' for name in names)
notes=''.join(f'<li>{html.escape(v)}</li>' for v in inspection['observations'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.3.0 — Minecraft checks</title><style>body{margin:0;background:#111820;color:#e4edf4;font:16px/1.55 system-ui}main{max-width:1280px;margin:auto;padding:40px 24px}h1{font-size:42px;margin:0}p{max-width:950px;color:#b9c9d6}a{color:#93d6ef}small{color:#a1b6c5}.badges{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}.badges span{background:#203c3b;border:1px solid #3c6863;border-radius:20px;padding:6px 14px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:20px}figure{margin:0;background:#1b2631;border-radius:10px;overflow:hidden}img{width:100%;display:block}figcaption{padding:10px 14px;color:#c3d3df;text-transform:capitalize}select{background:#223543;color:white;border:1px solid #5c788a;border-radius:7px;padding:10px;font:inherit;margin:8px 0 16px}.compare{max-width:1000px;margin:28px 0 40px}table{border-collapse:collapse;margin:20px 0;width:100%;max-width:900px}th,td{border-bottom:1px solid #3b4e5e;padding:10px;text-align:left}.notes{border-left:3px solid #75b9cb;padding-left:18px}li{margin:8px 0}</style><main><small>ACTUAL MINECRAFT CAPTURES · 17 OCTOBER 2026</small><h1>Stratus 1.3.0</h1><p>Denser refracting water, visible warm sun, vanilla/natural face lighting, warmer ground, structured lowland mist, rounded clouds and upper wisps. Half-resolution reflection and atmosphere passes preserve the look at lower cost.</p><div class="badges"><span>50 inspected scenes</span><span>0 shader errors</span><span>630 native checks</span><span>34 GPU cases + bloom radius</span></div><p><a href="../Stratus-1.3.0.zip">Installable shader ZIP</a> · <a href="results.json">Raw results and limitations</a></p><h2>Performance</h2><p>Apple M1, 1708×960 actual framebuffer, eight render chunks, five simulation chunks. VSync off, cap 260; 20-second samples after 15–45 seconds warmup in a fresh client. The earlier extended reload session showed additional stalls; its results are retained in the raw data. The user's other Minecraft client was also running, and the native UI inventory reported the Mac locked. Active-play performance can differ. These wall-time samples include stalls; no external GPU tests ran during the final measurements. Around 60 fps is a target, not a locked-frame-rate guarantee.</p><table><thead><tr><th>1.3.0 preset / view</th><th>Average fps</th><th>1% low fps</th><th>95th frame ms</th></tr></thead><tbody>'''+rows+'''</tbody></table><details><summary>Previous 1.2.0 High, same views and test setup</summary><table><thead><tr><th>View</th><th>Average fps</th><th>1% low fps</th></tr></thead><tbody>'''+before+'''</tbody></table><p>Early pool-rim/sealed-roof attempts were excluded and replaced by a verified open-water view. Earlier draft timings are not used for final-source claims.</p></details><h2>Inspected results</h2><ul>'''+notes+'''</ul><h2>Compare a requested effect</h2><div class="compare"><select id="comparison"><option value="bloom-default">Bloom — default radius 3</option><option value="bloom-off">Bloom — off</option><option value="bloom-small-radius">Bloom — radius 0.5</option><option value="warm-ground">Ground — warm</option><option value="ground-warmth-off">Ground — warmth off</option><option value="refraction-close">Water — refraction on</option><option value="refraction-off-close">Water — refraction off</option><option value="water-below-clouds">Lake through foreground clouds</option><option value="water-clouds-off">Same lake — clouds off</option></select><img id="comparison-image" src="g130-bloom-default.png" alt="Effect comparison"></div><h2>Visual coverage</h2><p>Click a frame for its unmodified Minecraft PNG. Main suite uses Reference sampling and named comparisons. Balanced/Fast benchmark views also use the final source. Water/cloud occlusion uses cloud altitude 128/thickness 40 and camera Y184 to keep the pool inside the eight-chunk test view; other cloud views use the default Y192 layer and Y360 upper wisps.</p><div class="grid">'''+cards+'''</div><h2>Practical limits</h2><ul>'''+''.join(f'<li>{html.escape(x)}</li>' for x in limits)+'''</ul><h2>Research</h2><p><a href="https://shaders.properties/current/reference/programs/composite/">Iris pass order</a> · <a href="https://advances.realtimerendering.com/s2015/">Horizon volumetric-cloud presentation</a> · <a href="https://google.github.io/filament/main/filament.html">Filament lighting</a></p><p><small>Editable GLSL: outputs/Stratus/. Helper remains exclusively in the workspace test instance. Original world untouched.</small></p></main><script>document.getElementById('comparison').onchange=function(){document.getElementById('comparison-image').src='g130-'+this.value+'.png'};</script></html>'''
(report/'index.html').write_text(page)
print('Recorded final visual coverage, exact source identities and measured performance.')

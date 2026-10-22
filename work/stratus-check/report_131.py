"""Record the optimization tested against the user's current video settings."""
from pathlib import Path
import json,hashlib,shutil,re,html
work=Path('work/stratus-check');game=Path('work/minecraft-smoke');pack=Path('outputs/Stratus');report=Path('outputs/Stratus-1.3.1-visual-checks')
v=json.loads((work/'validation-1.3.1.json').read_text());inspection=json.loads((work/'inspection-1.3.1.json').read_text());target=json.loads((work/'current-settings-target.json').read_text());exit_record=json.loads((work/'exit-1.3.1.json').read_text())
assert inspection['passed'] and exit_record['exit_code']==143
assert (game/'qa-complete.txt').read_text().strip()=='v131-complete'
log=(work/'minecraft-current-settings.log').read_text(errors='replace');marker='Using shaderpack: Stratus-1.3.1.zip';assert marker in log
errors=[s for s in log[log.index(marker):].splitlines() if re.search(r'ShaderCompileException|Failed to load the shaderpack|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException',s,re.I)];assert not errors,errors
for file,digest in v['source_hashes'].items():assert hashlib.sha256((pack/file).read_bytes()).hexdigest()==digest,file
for lib in ['options','frame','ceiling','volume','diffuse','medium','field']:
 p=Path('shaders/core')/(lib+'.glsl');assert (pack/p).read_bytes()==(work/'prior-1.3.0'/p).read_bytes()
metrics={}
for build,prefix in [('1.3.0 initial','settings130-balanced'),('1.3.1','settings131-balanced'),('1.3.0 repeat','settings130-repeat')]:
 metrics[build]={name:json.loads((game/'benchmarks'/f'{prefix}-{name}.json').read_text()) for name in ['landscape','water','clouds']}
report.mkdir(exist_ok=True);images={}
for name in inspection['inspected']:
 p=game/'screenshots'/f'v131-{name}.png';assert p.exists() and f'SCREENSHOT v131-{name} ' in log,name
 shutil.copy2(p,report/p.name);images[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['landscape','water','clouds']:
 p=game/'screenshots'/f's131-balanced-{n}.png';shutil.copy2(p,report/p.name)
checks={k:value for k,value in v.items() if k!='source_hashes'}
checks.update(actual_iris_compilation=True,in_game_visual_test=True,runtime={'shader_errors':0,'minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','gpu':'Apple M1','opengl':'4.1','framebuffer':[1708,960],'source_files_match_tested_zip':len(v['source_hashes']),'inspection':inspection,'captures_sha256':images,'process_exit':exit_record},performance={'target':target,'measurements':metrics,'preset':'Balanced','duration_seconds':20,'warmup_seconds':'15 after relocation, 25 after shader change','method':'Minecraft render-head to render-head monotonic wall intervals; actual frame wall times including stalls','mac_unlocked_confirmed_before_run':True,'bounded_awake_assertion_during_run':True,'normal_profile_settings_unchanged':True,'limits':['Isolated Iris/Sodium client with copied video/Sodium settings; full normal-profile mod stack not reproduced','Three fixed views, finite samples and changing system/thermal load; no guarantee of locked 60 fps','The 1.3.0 repeat is included to show timing variability rather than selecting the fastest result']},inherited_optics_probes={'release':'1.3.0','case_count':34,'library_bytes_match':True,'note':'Actual-GLSL optical libraries and bloom code are unchanged; earlier focused probe evidence remains applicable.'})
(pack/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(report/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
perf='\n'.join(f"{name}: {r['average_fps']:.1f} fps average, {r['one_percent_low_fps']:.1f} fps 1% low" for name,r in metrics['1.3.1'].items())
text=f'''STRATUS 1.3.1 - VERIFIED OPTIMIZATION
17 October 2026

Target: user's current video settings, read from Modrinth Main: 12 render chunks,
8 simulation chunks, VSync on, cap 70, launcher window 854x480 (1708x960 actual).
Mac unlocked; bounded awake assertion during the run. No other Minecraft process
was detected before launch. Normal profile settings and selection were preserved.

630 native compile/link checks: PASS, zero failures. 90 program pairs across
three dimensions and seven variants. Offline compatibility shims, separately
from actual Iris. All 206 shader/config files match the tested archive.

Actual Minecraft 1.21.11 / Iris1.10.8 / Sodium0.8.14, Apple M1 OpenGL4.1:
{len(inspection['inspected'])} optimization-regression views inspected; zero shader errors.
Geometry, entities, water edges/refraction/underwater/interfaces, particles, rain,
bloom, mist, clouds/cirrus, water/cloud order, Fast reflections and Nether/End.
The 1.3.0 optical libraries and bloom sources are byte-identical; its 34 focused
GPU optical cases remain applicable. The previous release's 50-scene report is
retained separately; those are not counted as new 1.3.1 captures.

Changed: cached neighbour radial depth for atmosphere upsampling; skipped water
work on non-water pixels; skipped unused reflection reconstruction in Fast.
Visual controls, shading and cloud/mist/reflection sampling counts are retained.

20-second frame wall-time samples (including stalls), Balanced:
{perf}

Before/after measurements and a repeated 1.3.0 control are in CHECKS.json and the
visual report. Real-time approximations and half-resolution edge limitations
remain documented in README.txt. Full normal-profile mods were not reproduced.
Test process stopped with SIGTERM, exit143. Original world untouched.
'''
(pack/'VALIDATION.txt').write_text(text);(pack/'IN-GAME-TEST.txt').write_text(text)
rows=''.join(f'<tr><td>{label}</td><td>{scene}</td><td>{r["average_fps"]:.1f}</td><td>{r["one_percent_low_fps"]:.1f}</td><td>{r["p95_frame_ms"]:.1f}</td></tr>' for label,views in metrics.items() for scene,r in views.items())
cards=''.join(f'<figure><a href="v131-{n}.png"><img loading="lazy" src="v131-{n}.png" alt="{html.escape(n)}"></a><figcaption>{html.escape(n.replace("-"," "))}</figcaption></figure>' for n in inspection['inspected'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.3.1 — current settings tests</title><style>body{background:#111820;color:#e6eef4;font:16px/1.6 system-ui;margin:0}main{max-width:1250px;margin:auto;padding:32px 24px}h1{font-size:40px;margin:0}p{max-width:950px;color:#bfceda}a{color:#90d2f4}table{border-collapse:collapse;width:100%;max-width:950px}th,td{padding:9px;text-align:left;border-bottom:1px solid #3a4b5c}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:18px;margin-top:20px}figure{margin:0;background:#1c2c3a;border-radius:8px;overflow:hidden}img{width:100%;display:block}figcaption{padding:9px 14px;text-transform:capitalize}small{color:#9fbdcc}</style><main><small>ACTUAL MINECRAFT CHECKS · 17 OCTOBER 2026</small><h1>Stratus 1.3.1</h1><p>Optimized for your saved video settings: 12 render chunks, eight simulation chunks, VSync on and a 70 fps cap. Launcher window 854×480, actual framebuffer 1708×960. The Mac was unlocked and kept awake during testing. No other Minecraft process was detected before launch.</p><p>Cached depth removes repeated reconstruction in the atmosphere pass. Water work is skipped on dry pixels, and Fast skips unused reflection reconstruction. The visible effects, controls and sampling counts are retained.</p><p><a href="../Stratus-1.3.1.zip">Download shader ZIP</a> · <a href="results.json">Raw results</a> · <a href="../Stratus-1.3.0-visual-checks/index.html">Previous visual feature checks</a></p><h2>Measured performance</h2><p>Balanced preset, 20 seconds per view, 15–25 seconds warmup. These are frame wall times including stalls. The repeated old version shows variability; differences cannot all be attributed to the shader. This isolated test uses the same video/Sodium settings, with Iris/Sodium and a helper, rather than the complete normal-profile mod stack.</p><table><thead><tr><th>Build</th><th>View</th><th>Average fps</th><th>1% low fps</th><th>95th frame ms</th></tr></thead><tbody>'''+rows+'''</tbody></table><h2>Visual regression checks</h2><p>630 native compile/link passes, zero failures. Actual Iris loaded the same source with zero shader errors. Click a frame for its unmodified ScreenshotRecorder PNG.</p><div class="grid">'''+cards+'''</div><p>Finite coverage, not every world/mod condition. Screen-space optics, approximate cloud scattering and height/depth-based mist remain documented in the source README.</p></main></html>'''
(report/'index.html').write_text(page)
print('Recorded',len(images),'visual checks and three-view before/after/control measurements.')

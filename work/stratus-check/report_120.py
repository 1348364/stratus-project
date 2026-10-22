"""Record completed visual inspection and package the exact tested GLSL."""
from pathlib import Path
import hashlib,html,json,re,shutil,zipfile
pack=Path('outputs/Stratus');work=Path('work/stratus-check');game=Path('work/minecraft-smoke');report=Path('outputs/Stratus-1.2.0-visual-checks')
evidence=json.loads((work/'validation-1.2.0.json').read_text())
probe=json.loads((work/'bloom-probe-1.2.0.json').read_text());assert probe['opengl_errors']==0 and probe['larger_radius_spreads_further']
assert (game/'qa-complete.txt').read_text().strip()=='f120-complete'
inspection=json.loads((work/'inspection-1.2.0.json').read_text());names=(work/'shots-1.2.0.txt').read_text().splitlines()
assert inspection['inspected']==names and inspection['passed'] and len(names)==40
exit_record=json.loads((work/'exit-1.2.0.json').read_text());assert exit_record['exit_code']==143
log=(work/'minecraft-1.2.0.log').read_text(errors='replace');marker='Using shaderpack: Stratus-1.2.0-reference.zip';assert marker in log
runtime=log[log.index(marker):]
patterns=r'ShaderCompileException|Failed to load the shaderpack|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException'
errors=[line for line in runtime.splitlines() if re.search(patterns,line,re.I)];assert not errors,errors
for i in range(7):assert f'BUFFER {i} RGBA16F' in runtime
assert 'pipeline for dimension minecraft:the_nether' in runtime or 'minecraft:the_nether' in runtime
assert 'minecraft:the_end' in runtime
for name,digest in evidence['source_hashes'].items():assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
report.mkdir(exist_ok=True);shots={}
for name in names:
 source=game/'screenshots'/f'f120-{name}.png';assert f'SCREENSHOT f120-{name} ' in runtime,name
 shutil.copy2(source,report/source.name);shots[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
checks={k:v for k,v in evidence.items() if k!='source_hashes'}
checks.update(actual_iris_compilation=True,in_game_visual_test=True,bloom_radius_probe=probe)
checks['runtime']={'minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','gpu':'Apple M1','opengl':'4.1','presets':['High sampling throughout main suite','Fast/Reference cloud views'],'dimensions':['Overworld','Nether','End'],'shader_errors':len(errors),'source_files_match_delivery':len(evidence['source_hashes']),'screenshots_sha256':shots,'settings':(work/'settings-1.2.0.txt').read_text(),'inspection':inspection,'process_exit':exit_record,'game_fps_measured':False,'limits':['Finite scenarios, not every possible block/mod/world condition','Normal-profile mod stack was not reproduced','Class-based estimated roughness and porosity; no measured PBR maps','Approximate environment wet film, skylight exposure, cloud scattering and water thickness','No cast-shadow maps or full global illumination','Animated particles, clouds and block-light flicker differ between comparison frames']}
(pack/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(report/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
(pack/'VALIDATION.txt').write_text('''STRATUS 1.2.0 - VERIFIED VALIDATION
17 October 2026

NATIVE GPU: PASS
Apple M1 OpenGL 4.1: 486 compile/link checks, zero failures. 81 program pairs,
three dimension routes, six variants (default, Fast, Reference, High, numeric
minimum/maximum). Uses compatibility-to-core shims, separately from real Iris.
All expanded inputs match the current source. 34 controls/menu entries verified.
AO default and maximum remain 1.00; water clarity maximum is now 4.00.

FOCUSED GPU OPTICS/LIGHTING: PASS
21 cases execute the actual GLSL libraries. Verified non-uniform RGB wet
absorption, lower absorption for smooth surfaces, view-dependent wet sheen,
zero moisture on covered blocks/entities, entity normal lighting and zero
self-emission in darkness, separate emissive interiors, billboard stability,
water path consistency and higher clarity, XYZ cloud density and cloud sunlight
attenuation, near-geometry cloud occlusion, daytime-only solar core.
OpenGL errors: 0. A separate HDR impulse test executes both actual bloom passes:
the 1.50 radius spreads farther than 0.50, with OpenGL errors 0.

ACTUAL IRIS AND VISUAL QA: PASS
Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Java 21 on Apple M1.
40 final-source captures inspected: blocks/undersides, wet/dry/film comparisons,
entities in daylight/darkness/lantern light, bloom on/off/radius, fireflies,
water clarity/top/side/underwater/interface, projectiles, destruction/smoke
particles, rain/transparency, mist, sun at several times, cloud volume and
parallax, quality presets, held items, blindness, Nether, lava immersion and End.
Shader errors: 0. All 182 delivered shader/config files match the tested ZIP.

Visual testing prompted a below-horizon sky/fog colour correction and less
uniform cloud coverage. Breaking particles were recaptured before their short
lifetime elapsed. Lava was recaptured in Creative, rather than Spectator mode.
Unmodified ScreenshotRecorder PNGs are in Stratus-1.2.0-visual-checks/.
No screenshots were generated or retouched to simulate test results.

LIMITS
These are finite checks, not an exhaustive visual or mod-compatibility guarantee.
The isolated instance uses Iris, Sodium and a test-only helper, not every mod in
the normal client. No FPS benchmark. Physical and screen-space approximations
are documented in README.txt. See CHECKS.json for raw results and provenance.
''')
(pack/'IN-GAME-TEST.txt').write_text('''STRATUS 1.2.0 - ACTUAL MINECRAFT TEST
17 October 2026

PASS: 40 final-source visual captures, zero shader errors.
Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1 OpenGL 4.1.
High sampling with the user's ambient brightness, AO and water settings formed
the main suite. Fast/Reference clouds and maximum water clarity were also viewed.
Overworld, Nether, End, lava immersion, daylight/night/weather, block materials,
entities, particles, transparency, water interfaces, fog, clouds, solar visibility,
bloom, held items and blindness were exercised. Raw screenshots and observations
are in Stratus-1.2.0-visual-checks/ and CHECKS.json.

The helper executes commands and captures via Minecraft's own APIs in a separate
workspace gameDir and copied world. It is not shipped in the shader or installed
in the normal profile. Original world unchanged. Test process stopped: SIGTERM,
exit 143. All 182 shader/configuration files match the tested archive exactly.
The existing firefly compatibility resource pack was enabled during this run.

No full normal-profile mod-stack or FPS claim. Class-based material properties,
approximate wet environment reflections and cloud scattering, and screen-space
water limits are documented in README.txt. Forty scenes are finite coverage.
''')
research=[('Wet material research','https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/'),('Filament lighting reference','https://google.github.io/filament/main/filament.html'),('Nubis cloud presentation','https://advances.realtimerendering.com/s2017/')]
cards=''.join(f'<figure><a href="f120-{name}.png" target="_blank"><img loading="lazy" src="f120-{name}.png" alt="{html.escape(name)}"></a><figcaption>{html.escape(name.replace("-"," "))}</figcaption></figure>' for name in names)
links=' · '.join(f'<a href="{url}">{title}</a>' for title,url in research)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.2.0 — Minecraft visual checks</title><style>body{margin:0;background:#111820;color:#e4edf4;font:16px/1.55 system-ui}main{max-width:1280px;margin:auto;padding:40px 24px}h1{font-size:42px;margin:0}p{max-width:900px;color:#b9c9d6}a{color:#93d6ef}small{color:#a1b6c5}.badges{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}.badges span{background:#203c3b;border:1px solid #3c6863;border-radius:20px;padding:6px 14px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:20px}figure{margin:0;background:#1b2631;border-radius:10px;overflow:hidden}img{width:100%;display:block}figcaption{padding:10px 14px;color:#c3d3df;text-transform:capitalize}select{background:#223543;color:white;border:1px solid #5c788a;border-radius:7px;padding:10px;font:inherit;margin:8px 0 16px}.compare{max-width:1000px;margin:28px 0 40px}.notes{border-left:3px solid #75b9cb;padding-left:18px}code{color:#c7e6ed}</style><main><small>ACTUAL MINECRAFT CAPTURES · 17 OCTOBER 2026</small><h1>Stratus 1.2.0</h1><p>Natural form lighting, wet surface optics, a haze-softened sun, volumetric cloud depth, bloom radius and expanded water clarity. These are test-world captures, not generated previews.</p><div class="badges"><span>40 inspected scenes</span><span>0 shader errors</span><span>486 native compile/link passes</span><span>21 GPU optics cases + bloom radius</span></div><div class="notes"><p>Testing corrected a below-horizon sky/fog mismatch and overly uniform cloud coverage. Entities were checked in daylight, an unlit room and lantern light. The wet-film comparison separates reflective sheen from absorption.</p><p>Finite coverage in an isolated Iris/Sodium client. Roughness/porosity, cloud scattering and wet sky reflection are approximations. No full mod-stack or FPS benchmark. <a href="results.json">Detailed results</a> · <a href="../Stratus-1.2.0.zip">Shader ZIP</a></p></div><h2>Wet surface comparison</h2><div class="compare"><label for="material">Same viewpoint:</label><br><select id="material"><option value="wet-floor">Damp — absorption and water film</option><option value="no-film-floor">Damp — absorption only</option><option value="dry-floor">Dry</option></select><img id="comparison" src="f120-wet-floor.png" alt="Wet surface comparison"></div><h2>Visual coverage</h2><p>Click a frame to inspect the original PNG.</p><div class="grid">'''+cards+'''</div><h2>Research</h2><p>'''+links+'''</p><p><small>Editable source: outputs/Stratus/. Test helper remains exclusively in work/minecraft-smoke/.</small></p></main><script>document.getElementById('material').onchange=function(){document.getElementById('comparison').src='f120-'+this.value+'.png'};</script></html>'''
(report/'index.html').write_text(page)
print('Recorded 40 inspected captures and exact tested-source identity; shader errors:',len(errors))

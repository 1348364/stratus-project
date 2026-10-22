"""Publish evidence only after final runtime and explicit visual inspection."""
from pathlib import Path
import hashlib,html,json,re,shutil,zipfile
w=Path('work/stratus-check');g=Path('work/minecraft-smoke');p=Path('outputs/Stratus')
r=Path('outputs/Stratus-1.5.0-visual-checks');r.mkdir(exist_ok=True)
v=json.loads((w/'validation-1.5.0.json').read_text())
captures=json.loads((w/'captures-150.json').read_text())+json.loads((w/'menus-150.json').read_text())
review=json.loads((w/'inspection-150.json').read_text())
assert review['inspected']==[c['name'] for c in captures]
assert (g/'qa-complete.txt').read_text().strip()=='v150-release-complete'
for name,digest in v['source_hashes'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
with zipfile.ZipFile(g/'shaderpacks/Stratus-1.5.0.zip') as z:
    for name,digest in v['source_hashes'].items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
log=(w/'minecraft-150.log').read_text(errors='replace')
error_pattern=r'ShaderCompileException|Failed to load the shaderpack|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException|\[STRATUS_QA\] ERROR'
errors=[line for line in log.splitlines() if re.search(error_pattern,line,re.I)];assert not errors,errors
for level in range(16):assert f'MATERIAL Block{{minecraft:water}}[level={level}] = {4100 if level==0 else 4103}' in log,level
assert 'ENTITY_SHADOW_ID 4200' in log
assert 'PACK Stratus-1.5.0.zip' in log
assert 'Gamerule random_tick_speed is now set to: 0' in log and 'Gamerule random_tick_speed is now set to: 3' in log
assert 'shaderPack=Stratus-1.5.0.zip' in (g/'config/iris.properties').read_text()
capture_hashes={}
for c in captures:
    name='v150-'+c['name']+'.png';f=g/'screenshots'/name;assert f.is_file(),name
    shutil.copy2(f,r/name);capture_hashes[name]=hashlib.sha256(f.read_bytes()).hexdigest()
checks={k:x for k,x in v.items() if k!='source_hashes'}
checks.update(status='verified within documented finite scope',source_hashes=v['source_hashes'],
    runtime={'actual_iris_load':True,'shader_errors':0,'minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','gpu':'Apple M1','opengl':'4.1','water_levels_verified':16,'water_source_id':4100,'water_flow_id':4103,'entity_shadow_id':4200,'active_shader':'Stratus-1.5.0.zip','left_open':True,'world':'StratusCheck (isolated copy)','final_camera':[156.5,105,43.5],'source_assets_identical_to_test_zip':len(v['source_hashes']),'custom_3d_texture_verified':True,'random_tick_speed_restored':3},
    inspection={'capture_count':len(captures),'captures':captures,'capture_sha256':capture_hashes,'review':review,'scope':'Final 128-cubed data and full-resolution High source. Five initial material screenshots excluded because fixture chunks had not loaded; board rebuilt in loaded/temporarily forced chunks and recaptured. Finite water/sky/material/dimension/menu coverage; no claim to all possible worlds.'},
    quality={'priority':'Visual fidelity per user request; previous60fps target withdrawn','preset':'HIGH','refraction_max_samples':256,'reflection_max_steps':96,'weather_volume':[128,128,128],'sky_cache':[512,256],'reflection_atmosphere_buffer_scale':1.0,'performance_benchmark':False,'60fps_verified':False},
    limits=['Screen-space rays cannot recover hidden or off-screen geometry, or independent transparent depth layers. Disocclusions and screen-edge fallback transitions can remain.','Material absorption classes are artist-tuned block heuristics, not measured porosity or PBR texture maps.','Cloud and fog scattering, weather and biome sediment are approximations. Sky-cache origin introduces cloud parallax approximation.','Shading waves do not displace block geometry. No cast terrain shadow maps or full fluid simulation.','Visual inspection is finite; heavily modified resource packs and every world configuration are not covered.'],
    non_shader_findings=['An obsolete randomTickSpeed command was rejected; correct1.21.11 namespaced random_tick_speed was then used and restored.','Initial material fixture writes failed because chunks were unloaded; replaced by a loaded-chunk fixture and five inspected replacement screenshots.','Offline local test login reports unrelated Realms authentication errors; no claim that the entire log is error-free.'])
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(r/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
text=f'''STRATUS1.5.0 — ACTUAL RUNTIME AND VISUAL CHECKS
18 October2026

744 native macOS OpenGL compile/link checks passed, zero failures:93 program
pairs across eight variants and three dimensions. Offline compatibility shims
are distinct from actual Iris runtime verification.
41 actual GLSL GPU cases passed with zero OpenGL errors: Snell transmission
in both directions, dielectric Fresnel/TIR, Beer-Lambert split/depth consistency,
material absorption ranking/nonabsorbing metals/shelter, broad exposed film,
cloud direction/depth clipping, spatial3D fog/near-clear/cave rejection, face
lighting and dark entities. A synthetic opaque cube/floor test confirms that
the bent ray correctly hits a cube top which the unbent camera ray misses.
50 controls are reachable through the Iris menus and have English labels.
All219 shader/config/data files match the actual tested archive, including
the original128-cubed RGBA8 weather volume. Its3D sampling was also verified
visually in the actual Iris client with a temporary diagnostic view.

Minecraft1.21.11 / Iris1.10.8 / Sodium0.8.14 / Apple M1 OpenGL4.1:
{len(captures)} final-source scene/control/menu captures inspected. Zero shader-specific
errors in this runtime log; unrelated offline Realms authentication errors are
not shader errors. All sixteen source/flowing water levels map correctly;
entity shadow suppression ID4200 is verified in Iris.

Water: submerged3D wood block, logs, crossbeam, steps, slabs, fence gaps and
glass from above, below, grazing and reverse angles; both sides of the waterline;
shore corners; reflection on/off; deep/shallow water; waterfall sides/lip;
dark/lit caves and striped receivers; river/swamp/warm/frozen biome comparisons;
rain/night; elevated water over a lower cloud layer; clarity and exaggerated
distortion controls. Random ticks were disabled during biome tests to prevent
ice, then restored to3. Screen-space disocclusions/fallback limits remain.

Materials: whole-face exposed wet film, separate pore darkening, dry and
absorption-only controls, rain and grazing views. Soil, timber, stone/ore,
polished stone, iron, glazed ceramic and sandstone were compared. Initial
missing-board captures were discarded and replaced after loading the chunks.
Clouds: beneath, inside and above the main volume, above cirrus, density/detail
control, actual vanilla sun/moon/cloud options. Fog: landscape, closer forest
pockets and stronger artistic settings. Nether/End, entities, particles,
projectiles, fireflies/bloom and thirteen actual settings screens inspected.
Detailed observations and unmodified captures are in the visual report.

High prioritises quality:256 transmission samples,96 reflection steps,
full-resolution reflection/atmosphere targets and512x256 sky cache. The user
explicitly withdrew the60fps goal. No new performance claim is made.

The isolated client remains OPEN at the submerged wooden test structure.
All fixtures are in the copied StratusCheck world. Main worlds, mods and
configuration are outside this task's writes; only a new shader ZIP/preferences
will be installed there, with its existing selection preserved. Install record
is provided beside the release archive.

Limits: single-depth screen-space transmission/reflection cannot reconstruct
hidden/off-screen or multiple transparent layers. Material classes, cloud
multiple scattering, fog weather fields and biome sediment are approximations.
Cloud-cache parallax is approximate; waves do not displace block geometry.
No cast terrain shadow maps or fluid simulation. Finite testing cannot prove
every world, camera, mod or resource-pack combination is free of artifacts.
'''
(p/'VALIDATION.txt').write_text(text);(p/'IN-GAME-TEST.txt').write_text(text)
def esc(s):return html.escape(s,quote=True)
cards=''.join(f'<figure data-kind="{esc(c["group"])}"><a href="v150-{esc(c["name"])}.png"><img loading="lazy" src="v150-{esc(c["name"])}.png" alt="{esc(c["name"])}"></a><figcaption><b>{esc(c["name"].replace("-"," "))}</b><p>{esc(c["note"])}</p></figcaption></figure>' for c in captures)
buttons=''.join(f'<button type="button" data-filter="{n}" aria-pressed="{str(n=="All").lower()}">{n}</button>' for n in ['All','Water','Sky','Materials','Atmosphere','Settings','Regression'])
notes=''.join('<li>'+esc(n)+'</li>' for n in review['observations'])
limitations=''.join('<li>'+esc(n)+'</li>' for n in checks['limits'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus1.5.0 — water, materials and volumetric sky</title><style>
:root{color-scheme:dark}body{margin:0;background:#101820;color:#edf3f6;font:16px/1.6 system-ui}main{max-width:1280px;margin:auto;padding:32px 24px}h1{font-size:42px;margin:0}h2{margin-top:34px}p{color:#bfcdd7}a{color:#9bd6ee}.badge{display:inline-block;padding:5px 12px;background:#23404b;border-radius:14px;margin:4px}.hero{width:100%;border-radius:10px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}figure{margin:0;background:#1a2a35;border-radius:10px;overflow:hidden}figure img{width:100%;display:block}figcaption{padding:12px 16px}figcaption p{font-size:14px;margin:4px 0}button{padding:8px 14px;border:1px solid #476171;background:#1a303e;color:#eaf4fa;border-radius:6px;margin:0 7px 9px 0;cursor:pointer}button[aria-pressed=true]{background:#39758b}.note{border-left:3px solid #d0ac6c;padding-left:15px}li{margin:8px 0}@media(max-width:750px){.grid{grid-template-columns:1fr}h1{font-size:30px}}
</style><main><h1>Stratus1.5.0</h1><p>Water-first refraction, material-based wet darkening, broad surface films, rounded3D clouds and nearer volumetric fog. Original editable Iris GLSL, tested on Apple Silicon macOS.</p>
<div><span class="badge">744 compile/link passes</span><span class="badge">41 GPU cases</span><span class="badge">50 reachable controls</span><span class="badge">0 shader errors in runtime</span></div>
<a href="v150-wood-above.png"><img class="hero" src="v150-wood-above.png" alt="Actual Minecraft submerged three-dimensional wooden refraction fixture"></a>
<h2>Water and wet materials</h2><p>Perspective-correct Snell rays use actual opaque scene depth and preserved receiver normals. The wooden test structure exposes corners, steps, thin gaps and different depths. Physical distortion is1.00; stronger settings are deliberately artistic. Fresnel, underwater total internal reflection and shared water extinction apply above and below the surface.</p>
<p>Wet darkening now follows material absorption. Soil and raw timber darken more; polished stone less; metal, glass and glazed ceramics have no pore darkening. Surface-water sheen covers whole exposed faces independently, with no corner-retention or random dampness mask. These block classes are visual heuristics.</p>
<h2>Clouds, fog and controls</h2><p>An original128³ weather texture drives rounded cloud body, finer erosion and spatial fog pockets. Cloud lighting samples sun transmission and ambient occlusion; fog integrates extinction and directional light along the view ray. All previous controls remain, with seven new controls, useful wider ranges and a separate refraction submenu. Vanilla shading mix1.00, water clarity1.70 and saturation1.00 remain the defaults.</p>
<p class="note">Quality takes priority. High uses full-resolution reflection/atmosphere buffers, a512×256 sky cache and up to256 refraction samples. The previous60fps goal was withdrawn; this release makes no frame-rate promise.</p>
<h2>Visual observations</h2><ul>'''+notes+'''</ul>
<h2>Inspected actual game captures</h2><p>Unmodified Minecraft screenshots from the final shader/assets. Click any frame for full resolution. Control packs change only the stated option. Missing-board captures were excluded and replaced after the fixture chunks loaded.</p><div>'''+buttons+'''</div><div class="grid">'''+cards+'''</div>
<h2>Limits and test scope</h2><ul>'''+limitations+'''</ul><p>The isolated client is left open at the submerged wooden structure. Main's existing shader selection and non-shader files are preserved. The coverage includes common water scenarios, three dimensions and thirteen settings views, rather than every possible world.</p>
<p><a href="results.json">Full evidence, source and screenshot hashes</a> · <a href="../Stratus-1.5.0.zip">Installable shader ZIP</a></p>
<details><summary>Scientific and implementation references</summary><p><a href="https://pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission">PBRT: dielectric transmission</a> · <a href="https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/">Lagarde: wet materials and water films</a> · <a href="https://graphics.stanford.edu/~henrik/papers/egwr99/egwr99.pdf">Jensen et al.: wet materials</a> · <a href="https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-horizon-zero-dawn">Guerrilla: volumetric clouds</a> · <a href="https://advances.realtimerendering.com/s2015/">Hillaire: volumetric integration</a> · <a href="https://shaders.properties/current/reference/buffers/custom_textures/">Iris: custom3D textures</a></p><p>Rendering code and procedural volume are original; these sources inform the physical models and rendering concepts.</p></details></main>
<script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('figure').forEach(f=>f.hidden=b.dataset.filter!=='All'&&f.dataset.kind!==b.dataset.filter)}));</script></html>'''
(r/'index.html').write_text(page)
print('Published report:',len(captures),'inspected frames;',len(v['source_hashes']),'tested source/assets.')

"""Record source identity and real-game visual evidence after inspecting captures."""
from pathlib import Path
import hashlib,json,re,shutil,zipfile
root=Path('outputs/Stratus');game=Path('work/minecraft-smoke');work=Path('work/stratus-check')
log=(work/'minecraft-visual-passed.log').read_text()
assert 'Using shaderpack: Stratus-1.0.6.zip' in log
assert 'file/Stratus-Firefly-Compatibility-1.21.11.zip' in log
assert 'final-visual-suite' in (game/'qa-complete.txt').read_text()
assert 'OpenGL Renderer: Apple M1' in log
runtime=log[log.index('Creating pipeline for dimension minecraft:overworld'):]
errors=[line for line in runtime.splitlines() if '/ERROR]' in line or re.search(r'ShaderCompileException|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|ArrayIndexOutOfBoundsException|undeclared identifier',line,re.I)]
assert not errors,errors
for index,fmt in enumerate(['RGBA8','RGBA16F','RGBA8','RGBA16F','RGBA16F']):
 assert f'BUFFER {index} {fmt}' in log
for block in ['stone','iron_ore','deepslate_iron_ore']:
 assert f'MATERIAL Block{{minecraft:{block}}} = 4112' in log
assert 'ENTITY_SHADOW_ID 4200' in log
assert 'Validated 432 program pairs; 0 failures.' in (work/'compile.log').read_text()
source_hashes={}
with zipfile.ZipFile(game/'shaderpacks/Stratus-1.0.6.zip') as z:
 for source in sorted((root/'shaders').rglob('*')):
  if source.is_file() and source.suffix in {".vsh",".fsh",".glsl",".properties",".lang"}:
   name=source.relative_to(root).as_posix(); data=source.read_bytes()
   assert z.read(name)==data,name
   source_hashes[name]=hashlib.sha256(data).hexdigest()
patch=Path('outputs/Stratus-Firefly-Compatibility-1.21.11.zip')
assert patch.read_bytes()==(game/'resourcepacks'/patch.name).read_bytes()
shots=['qa-firefly-day','qa-firefly-night','qa-firefly-animation-1','qa-firefly-animation-2','qa-firefly-animation-3','qa-ore-pairs','qa-entity-shadows','qa-water-glass-slime','qa-rain','qa-underwater','qa-forest-scenery']
inspection=json.loads((work/'visual-inspection.json').read_text())
assert set(inspection['inspected_screenshots'])==set(shots)
assert inspection['reported_defects_resolved']
report=Path('outputs/Stratus-1.0.6-visual-checks');report.mkdir(exist_ok=True)
hashes={}
for name in shots:
 assert f'SCREENSHOT {name} ' in log,name
 path=game/'screenshots'/f'{name}.png';shutil.copy2(path,report/path.name)
 hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
for name in ['before-ore-pairs','before-entity-shadow','vt-before-firefly-day','no-shaders-firefly']:
 path=game/'screenshots'/f'{name}.png';shutil.copy2(path,report/path.name)
exit_record=json.loads((work/'minecraft-visual-exit.json').read_text())
assert exit_record['exit_code']==143
result={'passed':True,'date':'2026-10-16','pack':'Stratus-1.0.6.zip','minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','fabric_loader':'0.19.5','java':21,'gpu':'Apple M1','preset':'Reference','dimension':'Overworld','world':'Isolated client with copied local singleplayer world','shader_errors':0,'source_hashes':source_hashes,'in_game_visual_test':True,'visual_inspection':inspection,'screenshots_sha256':hashes,'resource_pack_test':{'base':'VanillaTweaks_r924703_MC26.3.x.zip','base_formats':[84,97],'game_format':75,'black_bush_reproduced_with_shaders_disabled':True,'compatibility_patch':patch.name,'patch_sha256':hashlib.sha256(patch.read_bytes()).hexdigest(),'patch_contains':'One blockstate override, metadata and readme; no textures'},'test_process_exit':exit_record,'warnings':['Unused shader interface warnings','Offline dummy identity authentication failures before world load','Native gldCopyBufferSubData NEEDS IMPLEMENTATION diagnostic'],'server_tick_lag_warning':"Can't keep up!" in log,'limits':['No FPS benchmark','Held-item visibility was not verified because the HUD was hidden','Reference preset and Overworld visually tested; other presets/dimensions compiled offline only','Vanilla assets and VanillaTweaks plus compatibility patch tested; full normal-profile mod combination not tested','Finite visual scenarios, not a claim of no possible visual defects']}
(work/'minecraft-smoke-result.json').write_text(json.dumps(result,indent=2)+'\n')
(report/'results.json').write_text(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2)+'\n')
(root/'IN-GAME-TEST.txt').write_text('''STRATUS 1.0.6 - ACTUAL MINECRAFT VISUAL QA
16 October 2026

PASS: real Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14, Apple M1,
OpenGL 4.1, Reference preset, copied local Overworld. Shader errors: 0.
All shader/config sources and the resource compatibility ZIP match the tested
files byte for byte. Native offline compile/link: 432 passes, zero failures.

Visually inspected actual Minecraft screenshots of stone/deepslate ore rows,
cow/slime/dropped-item shadows, firefly bushes by day and night across several
animation frames, shallow water, glass, translucent slime, rain, underwater,
and surrounding forest scenery.

Ore host stone now shares its dampness class with neighboring stone/deepslate.
Vanilla entity shadow discs are suppressed while the game option stays enabled.
The black firefly model also reproduced with shaders DISABLED. The supplied
VanillaTweaks build targets formats 84-97, while this game uses format 75.
A separate format-75 compatibility resource pack selects the vanilla firefly
model; it was enabled above VanillaTweaks during the final visual test.
No textures are copied or replaced by that patch.

Actual before/after PNGs and results.json are in the adjacent
Stratus-1.0.6-visual-checks folder. Screenshots were saved by Minecraft's own
ScreenshotRecorder API; no generated or retouched images are used as evidence.
The test-only Fabric helper runs solely in the isolated workspace gameDir.
It is not shipped with or installed into the normal profile. The test process
was stopped with SIGTERM (exit 143); the original world was never modified.

Limits: no FPS benchmark, held-item visibility test, full normal-profile mod stack test, exhaustive world
condition test, or in-game checks of other presets/dimensions. Unused shader
interface warnings, offline identity authentication failures, and the native
gldCopyBufferSubData diagnostic remain distinct from shader errors.
''')
print('Verified final source identity and',len(shots),'inspected in-game screenshots; shader errors:',len(errors))

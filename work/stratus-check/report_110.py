"""Finalize delivery only after inspecting the actual release screenshots."""
from pathlib import Path
import json,hashlib,re,shutil,zipfile
work=Path('work/stratus-check');pack=Path('outputs/Stratus');game=Path('work/minecraft-smoke')
evidence=json.loads((work/'validation-1.1.0.json').read_text())
log=(work/'minecraft-1.1.0-final.log').read_text();marker='Using shaderpack: Stratus-1.1.0-verified5.zip'
assert marker in log and 'v110-release-suite' in (game/'qa-complete.txt').read_text()
runtime=log[log.rindex(marker):]
errors=[line for line in runtime.splitlines() if '/ERROR]' in line or re.search('ShaderCompileException|Failed to create shader|Shader compilation failed|Invalid framebuffer|OpenGL Error|GL_INVALID|undeclared identifier|ArrayIndexOutOfBoundsException',line,re.I)]
assert not errors,errors
for i in range(7):assert f'BUFFER {i} RGBA16F' in runtime
assert 'file/Stratus-Firefly-Compatibility-1.21.11.zip' in log
names=['clouds-below','clouds-inside','clouds-above','sky-light','overview','water-sides','water-top','underwater','underwater-interface','materials','thrown-items','block-breaking-particles','smoke-particles','bloom-night','rain-glass-slime','held-item']
inspection=json.loads((work/'inspection-1.1.0.json').read_text())
assert inspection['inspected']==names and inspection['reported_features_implemented']
report=Path('outputs/Stratus-1.1.0-visual-checks');report.mkdir(exist_ok=True)
shots={}
for name in names:
 tag='release110-'+name
 assert f'SCREENSHOT {tag} ' in runtime,tag
 source=game/'screenshots'/(tag+'.png');shutil.copy2(source,report/source.name)
 shots[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
for name in ['bloom-on','bloom-off','materials-on','damp-off','face-off','ao-off']:
 source=game/'screenshots'/('final110-'+name+'.png');shutil.copy2(source,report/source.name)
for source in ['vt-before-firefly-day','no-shaders-firefly']:
 shutil.copy2(game/'screenshots'/(source+'.png'),report/(source+'.png'))
# The compared material/bloom functions were unchanged by the later sky refinement.
with zipfile.ZipFile(game/'shaderpacks/Stratus-1.1.0-bloom-off.zip') as old:
 for name in ['diffuse.glsl','medium.glsl','bloom-horizontal.frag.glsl','bloom-vertical.frag.glsl','output.frag.glsl']:
  assert old.read('shaders/core/'+name)==(pack/'shaders/core'/name).read_bytes(),name
exit_record=json.loads((work/'exit-1.1.0.json').read_text());assert exit_record['exit_code']==143
for name,digest in evidence['source_hashes'].items():assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
checks={k:v for k,v in evidence.items() if k!='source_hashes'}
checks['actual_iris_compilation']=True;checks['in_game_visual_test']=True
checks['runtime']={'minecraft':'1.21.11','iris':'1.10.8','sodium':'0.8.14','java':21,'gpu':'Apple M1','opengl':'4.1','preset':'Reference','dimension':'Overworld','tested_zip':'Stratus-1.1.0-verified5.zip','source_files_match_delivery':len(evidence['source_hashes']),'shader_errors':len(errors),'screenshots_sha256':shots,'inspection':inspection,'process_exit':exit_record,'control_comparisons':json.loads((work/'visual-control-comparisons.json').read_text()),'comparison_note':'Control pairs use the final material/bloom functions. The distant sky was refined subsequently and final release scenes were recaptured. Animated particles and lightmap flicker can differ between captures.','warnings':['Unused shader-interface linker warnings','Offline dummy-identity authentication failures before world load','Native gldCopyBufferSubData diagnostic'],'server_tick_lag_warning':"Can't keep up!" in runtime,'game_fps_measured':False,'limits':['Overworld and Reference visually tested; other dimensions/presets passed offline compilation only','Full normal-profile mod stack was not reproduced','Waterfall thickness is estimated; screen-space reflections cannot see hidden geometry','Sky-exposure wetness uses the game lightmap rather than rain ray tracing','Finite visual scenarios; no assertion that every possible visual defect is absent']}
(pack/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(report/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
(pack/'VALIDATION.txt').write_text('''STRATUS 1.1.0 - VERIFIED VALIDATION
16 October 2026

NATIVE GPU: PASS
Apple M1, OpenGL 4.1. 81 program pairs across three dimension routes and six
configurations (defaults, Fast, Reference, High, numeric minima/maxima):
486 compile/link checks, zero failures. Includes compatibility-to-core shims;
this offline harness is separate from the actual Iris integration test.
All expanded test sources match the delivered GLSL. 31 controls and language
entries verified. Quality profiles change sampling options only. No external
shader includes, shadow programs, compute shaders, SSBOs or image load/store.

FOCUSED GPU PROBES: PASS
13 cases executed the actual delivered GLSL libraries. Outdoor dampness was
identical at widely separated world positions and across block material IDs
and face directions. Covered blocks and entities retained the input colour.
Shared water attenuation matched split-versus-combined travel distances within
floating-point tolerance. The finite cloud layer had nonzero density below,
inside and above; backward/horizontal rays outside it and nearer occluders
excluded it. Sky light leakage measurably raised radiance toward the broad
light direction. Face shading caused a small bounded change. OpenGL errors: 0.

ACTUAL MINECRAFT VISUAL QA: PASS
Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14, Apple M1, Reference preset,
copied singleplayer Overworld. Final release shader errors: 0. Sixteen actual
Minecraft screenshots were inspected. All 182 shader/configuration sources
match the tested ZIP byte for byte. See IN-GAME-TEST.txt and CHECKS.json.
The installed VanillaTweaks build was tested with the format-75 firefly patch.
No screenshots were generated or retouched for evidence.

Control comparisons separately inspected bloom, dampness, face shading and AO
on/off. Their material/bloom functions match this release. The sky was refined
after those pairs; final release screenshots were recaptured. Animated
particles and lightmap flicker prevent treating every pixel difference as a
controlled numeric measurement.

LIMITS
No FPS benchmark, full normal-profile mod-stack test, or in-game checks of
other dimensions/presets. Screen-space water thickness/reflections and skylight
wetness are approximations, documented in README.txt. Unused linker inputs,
offline authentication failures and the native driver diagnostic are distinct
from shader errors. This is finite visual coverage, not an exhaustive guarantee.
''')
(pack/'IN-GAME-TEST.txt').write_text('''STRATUS 1.1.0 - ACTUAL IN-GAME VISUAL TEST
16 October 2026

PASS: Reference preset, Minecraft 1.21.11, Iris 1.10.8, Sodium 0.8.14,
Java 21, Apple M1 OpenGL 4.1. Final shader errors: 0.

Inspected actual release screenshots:
- AO at 1.00, mixed outdoor block materials, wet ores and restrained face tint.
- Water tops, falling sides, deep underwater and the underwater interface.
- Fixed-height clouds from below, within and above, with the patterned high sky.
- Broad sky light opening and subtle bloom at night.
- Rendered snowball, egg and ender pearl entities with motion.
- Actual block-destruction particles and translucent smoke particles.
- Rain, glass, translucent slime, cow/item shadow regression, firefly cutouts.
- Visible held iron pickaxe with the HUD shown.

Sixteen final captures were saved using Minecraft's ScreenshotRecorder API.
The test-only helper modifies only the separate workspace gameDir and copied
world. It is neither shipped nor installed into the normal profile. The test
Java process was stopped with SIGTERM, exit 143. Original world unchanged.
All 182 shader/configuration files match the tested release ZIP byte for byte.

The VanillaTweaks build supplied by the user targets resource formats 84-97;
Minecraft 1.21.11 uses 75. Its black firefly planes reproduced even with shaders
disabled. The separate compatibility resource pack selects vanilla bush models
and remains enabled above VanillaTweaks during QA. A version-correct
VanillaTweaks build is the preferred long-term replacement.

No FPS benchmark or exhaustive mod/world-condition claim. Other quality presets
and dimensions were compiled offline, not visually exercised in this run.
Screen-space water and skylight exposure limits are described in README.txt.
Actual screenshots and detailed results are in Stratus-1.1.0-visual-checks/.
''')
print('Recorded sixteen inspected release captures; shader errors:',len(errors))

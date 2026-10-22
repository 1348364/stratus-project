from pathlib import Path
import json,re,hashlib,difflib,zipfile
w=Path(__file__).parent;p=Path('outputs/Stratus');base=w/'baseline';shader=p/'shaders'
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text()
gpu=json.loads((w/'gpu-checks.json').read_text());water=json.loads((w/'water-regression.json').read_text());assert gpu['failures']==water['failures']==water['opengl_errors']==0
assert 'UNSUPPORTED' not in (w/'probe-runtime.log').read_text()
oldhash=json.loads((w/'baseline-hashes.json').read_text());changed=[n for n,h in oldhash.items() if n.startswith('shaders/') and hashlib.sha256((p/n).read_bytes()).hexdigest()!=h]
assert len(changed)==7,changed
assert (p/'shaders/core/options.glsl').read_bytes()==(base/'shaders/core/options.glsl').read_bytes()
properties=(shader/'shaders.properties').read_text();oldprops=(base/'shaders/shaders.properties').read_text()
important=lambda s:[l for l in s.splitlines() if l.startswith(('profile.','size.','scale.','screen.','sliders='))]
assert important(properties)==important(oldprops)
with zipfile.ZipFile('outputs/Stratus-1.6.5.zip') as z:
 assert all(z.read(n)==(base/n).read_bytes() for n in z.namelist())
report={
 'version':'1.6.6','date':'2026-10-20','status':'Implemented candidate, technical checks passed; live visual/performance acceptance pending',
 'baseline':{'version':'1.6.5','source_archive_match':True,'Main_loaded_evidence':'work/stratus-refine-166/baseline-runtime.txt'},
 'changes':[
 'Face irradiance retains 65% vanilla weights with 35% realistic world-space light at full skylight; cave/exposure gating and existing strength/blend controls remain.',
 'Default sun samples the current Minecraft 1.21.11 square texture with HDR warmth and existing haze; round procedural core/aureole removed. Native vanilla sun/moon mode remains.',
 'Atmosphere resolve evaluates rejected-depth pixels at exact full-resolution depth using the selected full atmosphere budget, with smooth confidence blending instead of zero fog.'
 ],
 'native':{'program_pairs':768,'variants':8,'failures':0,'scope':'Native macOS OpenGL compatibility shims, not live Iris loading'},
 'gpu':{'candidate_sun_renders':4,'candidate_fog_cases':11,'candidate_face_samples':216,'reference_sun_renders':1,'reference_fog_cases':11,'reference_face_samples':72,'relationship_checks':27,'water_resolve_cases':10,'failures':0,'opengl_errors':0,'scope':'Actual expanded GLSL on native OpenGL, including baseline/reference comparisons; not Minecraft visual acceptance'},
 'source':{'changed_runtime_assets':changed,'unchanged_runtime_assets':235-len(changed),'options_defaults_and_ranges_unchanged':True,'presets_pass_resolutions_controls_unchanged':True,'water_moisture_cloud_density_code_preserved':True},
 'performance':{'measured':False,'FPS_or_speedup_claim':False,'visual_equivalence_claim':False,'quality_preservation':'No resolution, sample, draw-distance, preset or control reduction. Full selected atmosphere quality in selective fallback, no extra pass. Live equivalence and frame cost pending.','risk':'Thin geometry with poor reduced-resolution depth coverage can invoke additional full-quality atmosphere integration; requires matched forest scenes and focused frame-time measurement.'},
 'live':{'intended_profile':'Modrinth Main / Minecraft (1)','observed_pack':'Stratus-1.6.5.zip','candidate_loaded':False,'visual_review':'pending','reported_leaf_dots_eliminated_in_Main':'not yet verified','limitation':'Native desktop inventory cannot select the running Minecraft Java window. Existing game remains open; no competing world session.'},
 'limits':[
 'The depth-miss black-dot mechanism is reproduced and fixed in a controlled GPU test; other foliage/mipmap/driver causes cannot be excluded without the actual scene.',
 'Sun texture uses the 1.21.11 environment/celestial/sun.png resource path; resource-pack replacements can change its appearance. No Mojang texture is redistributed.',
 'The polished sun projection is custom sky rendering, not the native celestial draw; option 1 retains the native renderer.',
 'Existing 1.6.5 cloud range, small-cell horizon aliasing risks and screen-space water limitations remain.'
 ],
 'evidence':{'native':'work/stratus-refine-166/compile.log','gpu':'work/stratus-refine-166/gpu-checks.json','water':'work/stratus-refine-166/water-regression.json','sun_preview':'work/stratus-refine-166/offline-sun-preview.jpg','fog_preview':'work/stratus-refine-166/offline-fog-preview.jpg','runtime_baseline':'work/stratus-refine-166/baseline-runtime.txt'}
}
(p/'CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.6.6 — VANILLA LIGHTING BLEND, SQUARE SUN AND FOG CUTOUT REPAIR
Editable Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
GLSL 330 / OpenGL 4.1. MIT source included. Candidate: live acceptance pending.

CHANGES FROM 1.6.5
Face shading keeps vanilla as its main contribution: 65% fixed axis contrast,
35% realistic sky/ground/solar response at full sky exposure, before existing
strength/blend controls and limits. World-space light, rain and cave gating stay.
The default sun reads Minecraft's blocky texture with HDR warmth and haze,
replacing the round procedural core. Native vanilla sun/moon mode remains.

Tiny leaves can be missed by every lower-resolution fog depth sample. The old
resolve then applied zero fog, leaving dark dots. Rejected pixels now receive
an exact-depth full-quality atmosphere evaluation, smoothly blended according
to confidence. Valid cached samples and underwater behaviour are preserved.
The mechanism is verified offline; the reported Main scene is not yet checked.

PRESERVED
1.6.5 connected vanilla-footprint clouds, independent high veil, all controls,
defaults, allowed values, four quality presets, pass resolutions and budgets.
Matte moisture, water/reflection/refraction/fog clipping, transparency, mist
model and bloom remain. No quality reduction or new render pass. The fallback
can add cost in foliage-heavy views; actual performance remains unmeasured.

INSTALL
Keep Stratus-1.6.6.zip zipped in shaderpacks and select it in Iris. Copy prior
.zip.txt preferences to Stratus-1.6.6.zip.txt only if the new file is absent.
Main was observed loading 1.6.5; 1.6.6 live loading is not yet confirmed.

CHECKS
768 native compile/link pairs, zero failures. Actual candidate GPU renders:
4 sun, 11 fog, 216 face samples, plus 10 water-resolve regressions. 27 focused
relationships pass; baseline/reference renders are counted separately in
CHECKS.json. Sun texels match the installed 1.21.11 texture. Two offline preview
sheets inspected; they are not Minecraft screenshots. See VALIDATION.txt.

LIMITS
Main visual acceptance, the actual reported leaf scene, matched visual
regressions and focused FPS/frame time are pending. No speedup or full visual
equivalence claim. Existing cloud integration and screen-space water limits
remain. Runtime sun/cloud textures respect resource packs and are not bundled.
The new sun resource path targets Minecraft 1.21.11 specifically.
''')
validation='''STRATUS 1.6.6 — CANDIDATE VALIDATION
20 October 2026

COMPLETED FOR THIS BUILD
- 768 native macOS OpenGL compile/link pairs, eight variants, zero failures.
  Defaults, vanilla sky, four quality presets, option extrema, all dimensions.
  Compatibility shims are not Iris transform/runtime emulation.
- Actual GLSL GPU comparisons: 4 candidate sun renders + 1 baseline; 11 candidate
  fog cases + 11 baseline; 216 candidate face samples + 72 baseline/reference.
  27 relationships pass, zero API errors or unresolved probe binding warnings.
- Sun texture RGB/alpha and HDR tint checked at every rendered sample against
  the current 32x32 vanilla asset. Visibility-zero and native-mode checks pass.
- Face mix matches 65% vanilla + 35% previous physical irradiance at default
  strength. Direction, rain/night/caves, camera invariance, other dimensions,
  saved strength 2 and bypass controls checked.
- Reproduced the original rejected-depth unfogged dot. Its corrected RGB adds
  atmospheric scattering; matched depth, near clear foreground and underwater
  remain unchanged in controlled tests. Confidence transition and far border
  checks pass. Does not certify the actual reported Main foliage scene.
- 10 full water-resolve GPU regressions pass, zero failures/errors.
- Seven runtime assets changed. Options/defaults/ranges, menus/presets and pass
  resolutions unchanged. No lower sampling or draw distance; selective fallback
  uses the same full atmosphere quality as the primary pass. No extra pass.
- Offline before/after sun and fog preview sheets visually inspected. These are
  labelled native GLSL renders, not in-game screenshots.
- package.py verifies every packaged byte and ZIP integrity.

PENDING
Load 1.6.6 in Main/Iris and inspect the real distant foliage scene, sun and
terrain under day/sunset/night/rain, motion, caves and other dimensions. Confirm
resource binding and all presets/native sun mode. Recheck water/transparency.
Run matched representative scenes with focused FPS/frame time and Dynamic FPS,
resolution, distances, cap and VSync recorded. No speed or visual-equivalence
claim: a depth-miss fallback adds work in foliage-heavy views.

Main was confirmed loading 1.6.5 in its log. The desktop inventory still cannot
select its Java window, so 1.6.6 loading/review is not claimed. Baseline and all
current evidence are in work/stratus-refine-166 and CHECKS.json. Historical
1.6.5 evidence does not certify these changes.
'''
(p/'VALIDATION.txt').write_text(validation)
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.6 — PENDING LIVE REVIEW / PERFORMANCE

1. Select Stratus-1.6.6.zip in Main/Iris and confirm its loaded name in latest.log
   without shader or custom-texture errors. Preserve prior .zip.txt preferences.
2. Match normal-world camera, time/weather, resolution, render distance and
   shader controls against 1.6.5. Compare both bright/dark block faces, camera
   turns, morning/evening sun, rain and torch-lit caves. Vanilla contrast should
   remain dominant; FACE_BLEND or FACE_SHADING zero must bypass face contrast.
3. View the square sun at noon/sunset through clouds. Check native sun/moon mode,
   SUN_VISIBILITY zero, bloom and water reflection. The default polished sun
   should retain the active Minecraft texture's square silhouette.
4. Return to the actual distant-leaf black-dot scene. Move/turn slowly through
   fog; inspect tiny leaves, sky gaps, fences, near foliage and the chunk edge.
   Compare matched captures and reject unloaded-terrain/camera collision frames.
5. Check waterline, underwater/glass/particles and cloud traversal for regressions.
6. Benchmark matched representative terrain, dense forest/fog and river/cloud
   scenes before/after, focused, with Dynamic FPS state recorded. Include the
   fallback-heavy view. Record frame times/FPS, hardware, resolution, distances,
   VSync/cap and competing processes. Do not reduce samples/resolution/effects
   to claim a speed gain. GPU-only previews are not a gameplay benchmark.

These checks are pending for 1.6.6. Preserve original screenshots and log paths;
update TASK.md, CHANGE-LOG.md and SHADER-SPEC.md with evidence when completed.
''')
f=p/'package.py';s=f.read_text();assert "'Stratus-1.6.5.zip'" in s;f.write_text(s.replace("'Stratus-1.6.5.zip'","'Stratus-1.6.6.zip'"))
d=[]
for name in oldhash:
 f=p/name;b=base/name
 if f.suffix in {'.glsl','.properties','.lang','.py','.txt'} and f.is_file() and f.read_bytes()!=b.read_bytes():d.extend(difflib.unified_diff(b.read_text().splitlines(True),f.read_text().splitlines(True),fromfile='1.6.5/'+name,tofile='1.6.6/'+name))
(w/'changes.diff').write_text(''.join(d))
(w/'source-changes.json').write_text(json.dumps({'changed':changed,'unchanged':235-len(changed),'baseline_archive_matches':True,'quality_configuration_unchanged':True},indent=2)+'\n')
print('Wrote current candidate metadata, test instructions and source evidence.')

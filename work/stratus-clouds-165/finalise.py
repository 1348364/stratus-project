from pathlib import Path
import json,hashlib,re
w=Path(__file__).parent;p=Path('outputs/Stratus')
compile_log=(w/'compile.log').read_text();assert 'Validated 768 program pairs; 0 failures.' in compile_log
checks=json.loads((w/'gpu-checks.json').read_text());water=json.loads((w/'water-regression.json').read_text());assert checks['failures']==water['failures']==water['opengl_errors']==0
base=json.loads((w/'baseline-shaders.json').read_text())
changed=[f for f,h in base.items() if f.startswith('shaders/') and hashlib.sha256((p/f).read_bytes()).hexdigest()!=h]
assert set(changed)=={'shaders/shaders.properties','shaders/core/options.glsl','shaders/core/ceiling.glsl','shaders/core/diffuse.glsl','shaders/lang/en_us.lang'}
report={
 'version':'1.6.5','date':'2026-10-20','status':'Implemented and packaged candidate; Main visual review and foreground FPS pending',
 'changes':[
 'High clouds use an independent continuous wispy veil, including lower-cloud gaps.',
 'Diffuse face shading follows world-space sun direction, sky hemisphere and ground contribution, with rain/exposure gating and bounded contrast.',
 'Physical cloud footprint reads the running Minecraft/resource-pack clouds.png through an Iris custom sampler. Every occupied pixel and hole is retained.',
 'Fine 3D billows/erosion removed in favour of connected extrusions, broad gradients and self-shadowing. Cell-boundary quadrature protects the silhouette.',
 'Default cloud thickness reduced from 96 to 12 blocks; 4-block option added. All prior allowed thicknesses retained.'
 ],
 'native':{'program_pairs':768,'variants':8,'failures':0,'scope':'Native macOS OpenGL compatibility shims; not Iris transformation/loading proof'},
 'gpu':{'cloud_renders':17,'face_samples':216,'water_resolve_cases':10,'relationship_checks':len(checks['checks']),'footprint_cells_compared':65536,'failures':0,'opengl_errors':0,'scope':'Actual expanded cloud/diffuse/water GLSL, offline OpenGL; not Minecraft screenshots or FPS'},
 'source':{'changed_shader_assets':changed,'unchanged_shader_assets':235-len(changed),'all_water_mist_and_moisture_files_unchanged':True},
 'live':{'intended_profile':'Modrinth Main / Minecraft (1)','observed_selected_pack':'Stratus-1.6.4.zip','candidate_loaded':False,'candidate_visual_review':'pending','reason':'Existing normal Java client is running, but native desktop inventory cannot select its window. Main was left running; no competing world session launched.'},
 'performance':{'measured':False,'claim':'No FPS or speedup claim. Lower noise cost and more cell-boundary steps are a trade-off requiring a focused matched benchmark.'},
 'limits':[
 'Resource packs can change the cloud texture; no Mojang or Story Mode texture is redistributed.',
 'Exact vanilla horizontal map topology, not an exact reproduction of vanilla height, tick phase, draw range or lighting. Set thickness 4 for vanilla slab proportions.',
 'CLOUD_AMOUNT now scales opacity of the fixed vanilla footprint; CLOUD_DETAIL controls broad gradients; CLOUD_DISTORTION affects only vertical relief.',
 'Lower integration has a 1024-segment safety cap; small span values and grazing rays need live temporal/performance review. Integration remains bounded to 7000 blocks and has the existing smooth interior distance bound.',
 'High cloud veil still uses a finite-altitude slab and horizon fade; it is independent of lower coverage, not a full spherical cloud shell.',
 'Face lighting is a broad diffuse approximation, not cast shadows. Existing AO and separate ground warmth remain.',
 'Story Mode-inspired simplicity is an interpretation; no exact reference pack or in-game style match has been certified.'
 ],
 'evidence':{'compile':'work/stratus-clouds-165/compile.log','gpu':'work/stratus-clouds-165/gpu-checks.json','water':'work/stratus-clouds-165/water-regression.json','offline_preview':'work/stratus-clouds-165/offline-cloud-preview.jpg','source_diff':'work/stratus-clouds-165/changes.diff'}
}
(p/'CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
validation='''STRATUS 1.6.5 — CANDIDATE VALIDATION
20 October 2026

COMPLETED
- 768 native macOS OpenGL compile/link pairs, eight variants, zero failures:
  defaults, vanilla sky, Fast/Balanced/Reference/High, option extremes and all
  three dimensions. Compatibility shims do not reproduce every Iris transform.
- 17 actual cloud-shader GPU renders and 216 diffuse-face samples; 32 independent
  relationships pass, including all 65,536 current vanilla footprint cells,
  holes, upper-layer independence, sun reversal, rain, night, caves, contrast
  bypass, camera invariance and other-dimension behaviour. Zero GPU API errors.
- 10 actual water-resolve regression cases pass: submerged-segment clipping,
  air receivers, sky after exit, glass, additive particles and vertical exits.
- Five offline cloud previews inspected below/inside/above and at sunset/night.
  These are native GLSL previews, NOT Minecraft screenshots or visual acceptance.
- Only five shader/config/lang assets changed. All water, moisture, mist,
  entry-point wrappers, pass resolutions and quality preset values are unchanged.
- package.py verifies archive integrity and packaged bytes against source.

PENDING
- Load this candidate in Modrinth Main and verify Iris custom-texture binding.
- Inspect actual terrain/face lighting, cloud silhouette/gradients and motion,
  horizon aliasing, inside/outside transitions, rain/night and vanilla/off modes.
- Check the new default 12-block thickness against the user's visual preference.
- Measure focused FPS with matched options/camera/weather/render distance,
  resolution, VSync/cap and Dynamic FPS state. No speedup or FPS claim.

Main was observed running Stratus-1.6.4.zip. The desktop inventory cannot select
its Java window. No candidate live loading/review is claimed. Source checks and
an archive existing on disk do not prove it loaded. Full evidence and known
limits are in CHECKS.json and work/Custom instructions/CHANGE-LOG.md.
'''
(p/'VALIDATION.txt').write_text(validation)
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.5 — PENDING MAIN REVIEW

1. Copy Stratus-1.6.5.zip into Main/shaderpacks if it is not already present.
   Keep it zipped. Copy the previous .zip.txt preferences to the new name only
   if the new file does not already exist. Existing values should be preserved.
2. Select Stratus-1.6.5.zip in Iris and confirm that name in latest.log without
   shader compilation or custom-texture loading errors.
3. In the normal Stratus Terrain Lab world, inspect clouds below, within and
   above the layer; turn and move slowly, including at grazing horizon angles.
   Check noon, sunset, night and rain. Disable CLOUD_AMOUNT: high clouds should
   remain visible throughout the sky. CIRRUS_AMOUNT zero should hide them.
4. At default CLOUD_SPAN 240, compare the lower connected footprint/holes with
   current Minecraft clouds. Default thickness is 12; choose 4 for vanilla slab
   proportions. Source density gradients and shading intentionally differ.
5. Inspect stone/dirt/wood faces under morning/evening sun, camera rotation,
   rain and cave torchlight. Check FACE_SHADING and FACE_BLEND zero bypasses.
   Confirm matte surfaces and waterline/glass/particles remain coherent.
6. Capture matching settings/cameras before comparing releases. Check all four
   presets and vanilla cloud/sun modes. Store original screenshots and log paths.
7. Benchmark only while focused and record Dynamic FPS, hardware, resolution,
   render/simulation distances, cap and VSync. Background samples are invalid.

These steps have not been completed for 1.6.5. Historical 1.6.4 live evidence
must not be used to certify this candidate. See VALIDATION.txt / CHECKS.json.
''')
(p/'README.txt').write_text('''STRATUS 1.6.5 — CONNECTED CLOUDS AND DIFFUSE FACE LIGHTING
Editable Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
Target: GLSL 330 / OpenGL 4.1. MIT source included. Candidate, live review pending.

CHANGES
High clouds form an independent sky-wide wispy veil, including gaps in the
physical clouds. Lower clouds read the running game's current clouds.png,
including resource-pack replacements, through an Iris custom texture. No
Minecraft or Story Mode cloud texture is bundled. The horizontal footprint
preserves its occupied pixels and holes. It is extruded with simple forms,
smooth gradients and self-shadowing instead of detailed 3D pores/billows.

Default thickness is now 12 blocks (previously 96); 4 is available for vanilla
slab proportions. All prior thickness values remain selectable. CLOUD_SPAN 240
maps each texture pixel to 12 blocks. Saved option IDs are retained, but
CLOUD_AMOUNT now scales the fixed footprint's opacity, CLOUD_DETAIL controls
broad gradients and CLOUD_DISTORTION only gentle vertical relief. Changes of
height, scale, tick phase and lighting are deliberate custom behaviour.

Block-face contrast combines diffuse sky/ground response and world-space solar
orientation, softened by rain and gated by sky exposure. It remains diffuse:
solid blocks keep matte moisture absorption. FACE_SHADING/FACE_BLEND zero
bypasses contrast. No cast-shadow pass or glossy wet coat is introduced.
Water optics, clear unbent underwater transmission, fog clipping, transparency,
mist, bloom and all four quality presets are preserved.

INSTALL
Keep Stratus-1.6.5.zip zipped in the instance shaderpacks folder and select it
in Iris. To preserve preferences, copy the previous pack's .zip.txt to
Stratus-1.6.5.zip.txt only if that new file does not already exist. Source defaults
are distinct from saved overrides. Main was last observed using 1.6.4; packaging
or installation alone does not prove this candidate loaded.

CHECKS
768 native compile/link pairs; 17 cloud GPU renders; 216 face samples; 32
relationship checks; all 65,536 vanilla footprint cells; 10 water regressions
passed. Five offline previews inspected. These are technical checks, not live
Minecraft visual acceptance or FPS measurements. Actual Main review and focused
performance checks remain pending. See VALIDATION.txt, IN-GAME-TEST.txt and
CHECKS.json. Run package.py to rebuild this versioned archive.

LIMITS
Screen-space water limitations and nearest visible water exit remain. Cloud
integration is finite (7000 blocks, smooth interior bound, 1024 lower-cell step
cap); grazing rays/small spans need live motion and performance review. The
upper layer is a finite-altitude veil with horizon fade. It is not a spherical
shell. Diffuse face lighting is an approximation without cast shadows. Exact
Story Mode reference matching and a speedup are not claimed.
''')
pkg=p/'package.py';s=pkg.read_text();assert "'Stratus-1.6.4.zip'" in s;s=s.replace("'Stratus-1.6.4.zip'","'Stratus-1.6.5.zip'");pkg.write_text(s)
print('Wrote version 1.6.5 metadata with completed technical and pending live checks.')

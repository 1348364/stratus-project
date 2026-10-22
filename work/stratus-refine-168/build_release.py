from pathlib import Path
import json, difflib, shutil, hashlib
w=Path(__file__).parent;p=Path('outputs/Stratus')
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text()
gpu=json.loads((w/'gpu-checks.json').read_text());assert gpu['failures']==0
water=json.loads((w/'water-regression.json').read_text());assert water['failures']==water['opengl_errors']==0
perf=json.loads((w/'performance-summary.json').read_text());assert perf['opengl_errors']==0
inventory=json.loads((w/'option-audit.json').read_text())
changed=[];diff=[]
for f in sorted((w/'baseline/shaders').rglob('*')):
 if not f.is_file() or f.name.startswith('.'):continue
 rel=f.relative_to(w/'baseline');new=p/rel
 if f.read_bytes()!=new.read_bytes():
  changed.append(rel.as_posix());diff.extend(difflib.unified_diff(f.read_text().splitlines(True),new.read_text().splitlines(True),fromfile='1.6.7/'+rel.as_posix(),tofile='1.6.8/'+rel.as_posix()))
(w/'changes.diff').write_text(''.join(diff));(w/'source-changes.json').write_text(json.dumps({'changed_runtime_assets':changed},indent=2)+'\n')
checks={'version':'1.6.8','date':'2026-10-21','status':'New lighting mode, all-weather wet film and settings layout implemented; targeted atmosphere optimisations tested. Focused gameplay performance deferred at user request.',
 'controls':inventory,'native':{'program_pairs':768,'variants':8,'failures':0,'scope':'OpenGL compatibility-shim compile/link; separate from live Iris'},
 'GPU':gpu,'water':{'cases':len(water['cases']),'failures':0,'API_errors':0},'performance':perf,
 'live':{'profile':'Modrinth Main / Minecraft (1)','world':'Stratus Terrain Lab (normal)','route':'User-authorised guarded temporary Java API driver; no game class redefinition, mod installation or competing client','captures':'outputs/Stratus-1.6.8-visual-checks/index.html','reviewed':['Baseline/rain-only/all-weather/off in clear weather','Vanilla lighting against game shaders-disabled reference','Lighting, face, materials, clouds, cirrus, camera and performance pages'],'final_release_receipt':'outputs/Stratus-1.6.8-install.json'},
 'settings_policy':'All 59 existing defaults/ranges and four presets unchanged. Copy latest Main saved values only if new version settings file is absent; keep original preference bytes.',
 'limits':['Focused FPS/frame-time testing explicitly deferred by user until tomorrow morning. No whole-game speedup claim.','Vanilla mode restores game lighting/colour; Stratus water, sky/clouds and atmosphere remain, so the entire frame is not a vanilla-game image.','All-weather film remains absorbent-material and exposure gated; sealed caves/nonporous surfaces are not made glossy.','Finite checks do not prove universal 99-percent visual equivalence, all scene/preset/night/mod coverage, or solve historical foliage/water edge limitations.']}
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.6.8 — VANILLA LIGHTING, ALL-WEATHER SHEEN AND CLEARER SETTINGS
Minecraft Java 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Apple M1 macOS.
GLSL 330 / OpenGL 4.1. Original MIT source; resource textures are not bundled.

NEW CONTROLS
Lighting > Realistic lighting: Off restores Minecraft vertex face lighting/AO
and the game lightmap's colour/brightness. It bypasses Stratus ambient/lamp
boosts, ground warmth, material recolouring, bloom and camera grading. Water,
clouds and atmosphere remain Stratus effects. On retains the previous enhanced
lighting and every saved tuning value. The existing realistic face COMPONENT
is still an independent multiplier; use the new main switch for a full lighting
bypass. No existing control is silently converted into a different setting.

Materials > Wet sheen conditions: All weather (new default) allows an exposed
absorbent surface to show film without rain. Rain only reproduces 1.6.7's film.
Wet sheen strength, dampness and material/exposure gating still apply; zero
strength disables film. Vanilla lighting bypasses material recolouring/film.
Non-absorbing metal/glazed surfaces and sealed caves stay nonglossy.

SETTINGS
All 59 previous controls/defaults/ranges retained; 61 total. Four quality preset
definitions, including Reference, remain unchanged. The six main categories
remain, with smaller face/ambient/block-light, lower/high-cloud, shape, camera
and bloom groups. Preserved original option IDs, slider choices and tooltips.
Main's newer saved values are copied for the release without replacing source
defaults or overwriting an existing new-version settings file.

PERFORMANCE AND VALIDATION
Native compile/link: 768 pairs / eight variants, zero failures.
Actual GLSL: 795 component samples, 12 output samples, 20 relationship checks,
10 water cases and 65,536 matched atmosphere pixels pass.
Atmosphere skips field work outside mathematically empty cloud slabs and
hoists ray/uniform-invariant mist lighting while preserving multiplication
order, sample counts, effect resolutions and traversal limits. Vanilla mode
skips its two unused bloom passes. No quality setting was reduced.
Four-view 128x128 Apple M1 GPU microbenchmarks showed 4-6% lower atmosphere draw
time in the longer isolated comparison. This is NOT gameplay FPS or a general
speedup guarantee. Focused matched gameplay testing was deferred by the user
until tomorrow morning. Universal 99% visual equivalence is not certified.

ACTUAL MINECRAFT
Controlled Main captures compare new modes, a shaders-disabled vanilla
reference, materials and menus. Final released-ZIP loading and current settings
are recorded separately in outputs/Stratus-1.6.8-install.json and the change log.
See VALIDATION.txt, CHECKS.json, IN-GAME-TEST.txt and the visual report.

INSTALL
Keep Stratus-1.6.8.zip zipped in shaderpacks and select it in Iris. Preserve old
releases and preference files. Copy the latest saved values only when the new
.zip.txt does not already exist. Do not overwrite newer user settings.

LIMITS
Film, porosity and atmosphere are approximations. Existing screen-space water
miss/edge limits, finite cloud range and foliage-fallback costs remain. Finite
visual coverage is not exhaustive night/preset/mod or motion certification.
''')
(p/'VALIDATION.txt').write_text('''STRATUS 1.6.8 — VALIDATION / 21 OCTOBER 2026

768 native macOS OpenGL compile/link pairs / eight variants: zero failures.
Native compatibility shims are separate from actual Iris loading proof.
795 actual GLSL component samples, 12 actual output samples, 20 relationships,
10 water-resolve cases and 65,536 matched full-atmosphere pixels pass.
59 old controls/defaults/ranges retained, 61 total, all reachable and labelled;
all four preset definitions and old slider membership remain unchanged.

Actual Main API captures compare baseline, Rain only, All weather and sheen Off
in clear weather; the new vanilla mode against shaders-disabled Minecraft;
enhanced lighting; and the new settings pages. Final-code river/underwater and
menu captures are preserved in the project evidence. Final released-ZIP state
is documented in the external install receipt and change log.

PERFORMANCE LIMIT
Four matched 128x128 full-atmosphere GPU microbenchmarks, using rotated variant
order, 32 draws per query and five measured rounds after warm-up, showed about
4-6% lower draw time. Initial shorter batches were mixed; all raw experiments
are retained. Max tested atmosphere RGB difference is below 0.018 of an 8-bit
sRGB code value; alpha error below 0.0001. These finite tests do not establish
universal 99% appearance equivalence or a whole-game FPS improvement.
The user explicitly deferred focused Minecraft FPS/frame times until tomorrow
morning. No valid gameplay performance result is claimed. No sample, draw
distance, effect resolution, quality preset or intended feature was reduced.

FULL LIMITS
Vanilla mode restores original material lighting and colour while keeping
Stratus water/cloud/atmosphere effects. All-weather sheen remains limited to
exposed absorbent materials. Existing reflection/volume/fog approximations and
incomplete original-leaf, all-night, all-preset and mod coverage remain.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.8 — LIVE CHECKS AND FOLLOW-UP

Completed: matched clear-weather film sources/strength; vanilla lighting versus
Minecraft shaders disabled; enhanced lighting; settings groups; finite water
and atmosphere views. See project work/stratus-refine-168 and visual report.

Controls: Lighting > Realistic lighting for the complete lighting bypass;
Materials > Wet sheen conditions for All weather / Rain only. The realistic
face component slider remains a component control, not the main mode switch.

Pending by user request until tomorrow morning: focused FPS/frame-time samples
for 1.6.7 and matched 1.6.8 terrain, forest/fog and river/cloud scenes. Record
Dynamic FPS, framebuffer, distances, VSync/cap, current saved shader options
and competing instances. Do not infer game speed from native microbenchmarks.
Also broaden cave/night, presets, motion, underwater/glass/particle edges and
the original distant-leaf artifact as relevant; keep finite evidence separate
from exhaustive visual claims. Preserve all quality levels during profiling.
''')
package=p/'package.py';s=package.read_text();assert "'Stratus-1.6.7.zip'" in s;s=s.replace("'Stratus-1.6.7.zip'","'Stratus-1.6.8.zip'");package.write_text(s)
print('Prepared 1.6.8 documentation and packaging; gameplay FPS explicitly pending.')

from pathlib import Path
import json,hashlib,re,difflib,html,shutil
w=Path(__file__).parent;p=Path('outputs/Stratus');assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text()
gpu=json.loads((w/'gpu-checks.json').read_text());assert gpu['failures']==0
snap=json.loads((w/'settings-snapshot.json').read_text());inventory=json.loads((w/'option-inventory.json').read_text())
# Only comments differ between the final source and the fully rendered v2 QA build.
import zipfile
with zipfile.ZipFile(w/'packs/Stratus-1.6.7-QA-v2.zip') as z:
 def tokens(s):return re.findall(r'\w+|[^\s]',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
 differences=[]
 for n in z.namelist():
  if not n.startswith('shaders/'):continue
  current=(p/n).read_bytes();old=z.read(n)
  if current!=old:
   assert (p/n).suffix in {'.glsl','.fsh','.vsh'} and tokens(current.decode())==tokens(old.decode()),n
   differences.append(n)
(w/'runtime-equivalence.json').write_text(json.dumps({'runtime_build':'Stratus-1.6.7-QA-v2.zip','final_source_shader_count':235,'all_tokens_identical':True,'comment_only_differences':differences},indent=2)+'\n')
# Preserve all original screenshots; copy a gallery to the delivered evidence directory.
report=Path('outputs/Stratus-1.6.7-visual-checks');(report/'screenshots').mkdir(parents=True,exist_ok=True)
rows=[]
for shot in sorted((w/'screenshots').glob('*.png')):
 shutil.copy2(shot,report/'screenshots'/shot.name)
 status='Actual Main capture; comparison/supporting evidence'
 if shot.name in {'baseline-current-view.png','s167-v2-menu-sun.png','s167-v2-menu-materials.png'}:status='Not acceptance evidence: paused menu or stale menu frame; retained original'
 elif 'baseline' in shot.name:status='1.6.6 baseline'
 elif shot.name.startswith('s167-v2-') or shot.name.startswith('s167-confirmed-'):status='Final shader-code comparison / reviewed Main capture'
 elif 'cirrus' in shot.name:status='Supporting high-cloud isolation comparison; unchanged cirrus code'
 else:status='Preliminary sun/default experiment; final v2 comparisons supersede it'
 rows.append({'file':shot.name,'status':status,'sha256':hashlib.sha256(shot.read_bytes()).hexdigest()})
(report/'captures.json').write_text(json.dumps(rows,indent=2)+'\n')
body=''.join('<figure><figcaption>'+html.escape(r['file'])+'<br><small>'+html.escape(r['status'])+'</small></figcaption><a href="screenshots/'+r['file']+'"><img loading="lazy" src="screenshots/'+r['file']+'"></a></figure>' for r in rows)
(report/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Stratus 1.6.7 actual Main checks</title><style>body{background:#131a21;color:#e9eff4;font:16px system-ui;max-width:1500px;margin:30px auto;padding:20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:20px}figure{margin:0;background:#202c37;padding:12px}img{width:100%}small{color:#abc0d1}a{color:#90cff5}</style><h1>Stratus 1.6.7 — actual Minecraft Main captures</h1><p>21 October 2026. Minecraft 1.21.11 / Iris 1.10.8 / Apple M1. Normal Stratus Terrain Lab world. These are actual Minecraft framebuffer captures, not generated concepts or offline GLSL previews. Shader pipeline and camera positions were checked before capture.</p><p>Reviewed: stronger local sun halo versus native mode; visible high cirrus versus off and 1.6.6; independent face controls; rainy wet-sheen off/default/maximum and nonporous metal; clear materials; river/underwater; settings menus. Animation continues, so rain/cloud frames are not pixel-exact. Some early menu captures lagged one frame; corrected captures are labelled confirmed. Focused performance, exhaustive temporal/mod compatibility and night/sheltered-wet fixtures remain unverified.</p><p>Immutable v2 QA shader tokens match final source (two comment-only differences). Final release loading/captures are recorded in the install receipt and change log.</p><main>'''+body+'</main>')
changed=[];diff=[]
for old in (w/'baseline/shaders').rglob('*'):
 if not old.is_file():continue
 rel=old.relative_to(w/'baseline');new=p/rel
 if old.read_bytes()!=new.read_bytes():
  changed.append(str(rel));diff.extend(difflib.unified_diff(old.read_text().splitlines(True),new.read_text().splitlines(True),fromfile='1.6.6/'+str(rel),tofile='1.6.7/'+str(rel)))
(w/'changes.diff').write_text(''.join(diff));(w/'source-changes.json').write_text(json.dumps({'changed_runtime_assets':changed,'unchanged_runtime_assets':235-len(changed)},indent=2)+'\n')
check={
 'version':'1.6.7','date':'2026-10-21','status':'Implemented; native/GPU checks and actual Main comparisons completed. Focused performance unverified.',
 'settings':{'before':'work/stratus-refine-167/settings-snapshot.json','applied_preferred_defaults':snap['source_defaults_to_change'],'preserved_options':53,'total_options':59,'new_controls':inventory['added_controls'],'Reference_profile_preserved':True,'old_saved_file_preserved':True},
 'changes':['Captured Main 1.6.6 effective defaults and applied its seven overrides as new source defaults.','Added sun-local halo strength/radius and core-brightness controls without changing global bloom.','Added independent vanilla/realistic face-component multipliers; both 1 reproduce the previous combination.','Increased cirrus optical contrast/density and added independent cirrus-density control.','Added rain-gated, view-dependent film/highlights on exposed absorbent materials while retaining sheltered matte retention.'],
 'native':{'pairs':768,'variants':8,'failures':0,'scope':'Native OpenGL compatibility-shim compile/link; not a substitute for Iris loading'},
 'GPU':{'samples':539,'candidate_samples':490,'baseline_samples':49,'relationship_checks':21,'water_resolve_cases':10,'failures':0,'API_errors':0},
 'live':{'profile':'Main / Minecraft (1)','world':'Stratus Terrain Lab (normal world)','runtime_test_archive':'Stratus-1.6.7-QA-v2.zip','final_tokens_match_runtime':True,'pipeline_verified':True,'captures':'outputs/Stratus-1.6.7-visual-checks/index.html','reviewed':['Sun versus vanilla/halo off','Cirrus only/off and baseline','Face components separately disabled','Wet off/default/maximum in rain; nonporous metal; clear material','Sunset atmosphere (sun partly cloud-occluded)','River and underwater','Corrected Lighting/Sun/Materials menus and Cloud menu'],'final_release_loading_receipt':'outputs/Stratus-1.6.7-install.json'},
 'performance':{'focused_measurement':False,'speedup_claim':False,'resolution_or_samples_reduced':False,'notes':'Main was initially unfocused; no valid focused FPS result. Preferred quality defaults match saved Main settings; all four quality presets remain unchanged. No extra render pass or scenery trace; dry/nonporous film work bypassed. No maximised-performance or full visual-equivalence claim.'},
 'limits':['Wet film is an environment/solar approximation, not ray-traced coating or simulated rain accumulation; existing absorption classes are heuristic.','Bright high clouds form a broad veil rather than dense cumulonimbus; finite slab/horizon limits remain.','Rain/cloud animation means visual comparisons are controlled but not pixel-identical.','Full night/sheltered-wet and exhaustive preset/motion/mod visual coverage are not claimed.','Existing screen-space water and depth-miss fallback costs remain; actual dense-forest focused profiling still needed.']}
(p/'CHECKS.json').write_text(json.dumps(check,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.6.7 — PREFERRED DEFAULTS, SUN CONTROLS, CIRRUS AND RAIN SHEEN
Minecraft Java 1.21.11 / Iris 1.10.8 on Apple Silicon macOS.
GLSL 330 / OpenGL 4.1. Editable MIT source included.

PREFERRED DEFAULTS
Captured Main's selected 1.6.6 settings before editing and applied seven values:
CLOUD_LAYERS 1; GROUND_WARMTH 0.00; MIST_DETAIL 2; REFLECTION_MODE 2;
WATER_EXTINCTION 3.00; WATER_RENDER_QUALITY 2; WATER_TURBIDITY 6.00.
All other existing defaults and allowed values remain. Reference is still a
selectable preset, not a replacement for these preferred defaults.

NEW CONTROLS AND BEHAVIOUR
59 controls: all 53 previous settings retained plus six new controls.
VANILLA_FACE_CONTRAST and REALISTIC_FACE_CONTRAST independently multiply the
legacy 65/35 components. Both 1.00 reproduce the previous combination; zero
removes only that component. FACE_SHADING / FACE_BLEND remain combined masters.
SUN_CORE_BRIGHTNESS (4.50), SUN_HALO_STRENGTH (2.00), SUN_HALO_RADIUS (1.50)
tune polished mode's square core and sun-local falloff. Global bloom is unchanged;
vanilla mode is retained. Set core 2.80 / halo 0 for the former sun contribution.
CIRRUS_DENSITY (1.00) controls the now brighter, more visible independent high
veil. Its amount/altitude controls and lower cloud shapes remain available.
WET_SHEEN retains saved values and sheltered absorption, and now adds a thin,
view-dependent rain film/highlights on exposed absorbent materials. Clear/dry,
sealed and non-absorbing surfaces do not receive a uniform glossy coat.

VERIFICATION
768 native links, 539 targeted GPU samples (490 candidate / 49 baseline),
21 relationships and 10 water regressions pass. Actual Main comparisons inspect
the sun, high clouds, both face components, wet strengths/material gating,
clear materials, sunset atmosphere, river/underwater and settings menus.
Final shader tokens match the runtime-tested immutable v2 QA build; final ZIP
selection is recorded separately in the install receipt / change log.
Focused FPS is unverified. No speedup or exhaustive visual-equivalence claim.
No pass, resolution, sample or distance reduction. All four presets remain.

INSTALL
Keep Stratus-1.6.7.zip zipped in shaderpacks and select it in Iris. Copy prior
.zip.txt preferences only if the new file does not exist. Preferred existing
values now also work with no settings file. Preserve the old 1.6.6 preferences.
See VALIDATION.txt, CHECKS.json, IN-GAME-TEST.txt and the project change log.

LIMITS
Rain film and porosity are visual approximations; no detailed scenery reflection
or water accumulation is simulated on solids. Existing screen-space water,
finite cloud range and far-cell limits remain. High cirrus is a broad veil.
Night/sheltered-wet, exhaustive preset/motion/mod checks and focused profiling
remain pending. Runtime sun/cloud textures respect resource packs; not bundled.
''')
(p/'VALIDATION.txt').write_text('''STRATUS 1.6.7 — VALIDATION / 21 OCTOBER 2026

COMPLETED
768 native macOS OpenGL compile/link pairs, eight variants, zero failures.
Actual GLSL GPU probes: 490 candidate and 49 baseline samples; 21 independent
relationships pass, zero API errors. Includes exact legacy face combination,
independent controls, dry/nonporous/cave wet gating, grazing film strength and
2.8125x upper optical density with lower-layer independence. Ten full water-
resolve regressions pass under the newly preferred 3.00/6.00 defaults.
53 previous control IDs/ranges retained; 59 total reachable/labelled controls.
Seven saved values applied to defaults, old preference bytes preserved. Four
preset definitions, including Reference, unchanged. Exact inventories recorded.

ACTUAL MAIN VISUAL REVIEW
Minecraft 1.21.11 / Iris 1.10.8 / normal Stratus Terrain Lab. A guarded project-
local API driver captured the existing client; no mods installed or world copy
opened. Pipeline and camera checked. Reviewed sun/vanilla/halo, cirrus only/off,
face component off combinations, rain wet strengths and metal, clear material,
sunset atmosphere, river/underwater and menu controls. Full original captures
and preliminary/rejected-frame labels are in the visual report. Corrected menu
captures include a render wait; two early stale menu frames are not passes.
Final source tokens match the immutable QA-v2 build; only two comments differ.
Final release loading/normal selection is documented in the external install
receipt, rather than inferred from source or archive creation.

PENDING / LIMITS
Focused FPS and matched frame times remain unverified; no speedup, maximum-
performance or exhaustive equivalence claim. No quality reduction or extra
render pass; preferred quality defaults match the user's saved settings.
No exhaustive night/sheltered-wet, all-preset motion or mod visual certification.
Rain/porosity/film and upper clouds are approximations. Existing cloud range,
screen-space water limitations and selective fog-fallback costs remain.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.7 — COMPLETED AND FOLLOW-UP CHECKS

Actual Main comparisons were captured for preferred settings, polished/native
sun, cirrus only/off, independent face components, rain wet strengths, nonporous
metal and clear materials, sunset atmosphere, river/underwater and settings menus.
See outputs/Stratus-1.6.7-visual-checks and work/stratus-refine-167.

Follow up with a focused matched benchmark: normal-world terrain, dense forest/
fog and river/cloud views. Record Dynamic FPS state, resolution, distances,
VSync/cap, competing instances and exact settings. Do not lower quality to claim
a speedup. Background/unfocused FPS is not an accepted gameplay measurement.
Additional useful visual checks: night and sheltered damp materials, prolonged
cloud motion/height transitions, all quality presets and different resource packs.
Reference remains selectable; it does not replace the preferred source defaults.
Preserve original screenshots and distinguish additional observations from the
finite set already reviewed. See CHECKS.json for controls and known limits.
''')
f=p/'package.py';s=f.read_text();assert "'Stratus-1.6.6.zip'" in s;f.write_text(s.replace("'Stratus-1.6.6.zip'","'Stratus-1.6.7.zip'"));print('Prepared release metadata and actual-Main gallery.')

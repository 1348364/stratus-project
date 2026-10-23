from pathlib import Path
import json,hashlib
w=Path(__file__).parent;p=Path('outputs/Stratus');v='1.7.0-rc1';load=lambda n:json.loads((w/n).read_text())
limits=['Just-below-surface rectangular sky/treetop tint band remains visible in native mode, as on the previous baseline. No waterline acceptance or fix claimed.', 'Remaining live wet-film side/underside, shelter/rain and transparent glass/ice/slime/honey controls-off comparisons skipped at user request after Mac locked.', 'Native underwater biome, status-effect, night-vision, mod and resource-pack compatibility not fully verified. Native mode retains Stratus straight-through underwater exit rather than vanilla back-face surface overlay, so it is not pixel-identical vanilla.', 'Only nearest visible transparent interface; bounded screen-space refraction, missing scenery uses sky fallback, overlapping solids/particles and water-behind-glass require final live acceptance.', 'No FPS samples. Performance and the approximately60FPS target remain deferred.', 'Candidate archive is packaged only. Temporary QA equivalents loaded; final candidate archive not installed/selected/reviewed. Stable1.6.12 restored.']
checks={'version':v,'batch':'43b4c0ad-c217-4a82-8534-29d34345f150','status':'Release candidate; incomplete live acceptance. All four requests remain pending.','native_pairs':768,'native_failures':0,'native_matrix_log':'work/stratus-refine-1613/compile-final.log','wet_GPU':load('wet-checks.json'),'transparent_GPU':load('glass-checks.json'),'legacy_underwater_GPU':load('legacy-water-final-checks.json'),'native_underwater_GPU':load('native-water-final-checks.json'),'controls':load('control-checks.json'),'migration':load('migration-checks.json'),'Iris_profiles':{k:{a:v[a] for a in ['option_count','matches_after_applying_full_profile']} for k,v in load('iris-profile-checks.json').items()},'FPS_samples':0,'limits':limits,'release_installed':False,'release_loaded':False,'source_equivalent_QA_loaded':True}
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.7.0-rc1 — NATIVE WATER AND TRANSPARENT OPTICS CANDIDATE

A standalone original Iris shader pack, MIT licensed. This is a development
candidate with incomplete live acceptance, not the completed1.7 water milestone.
The stable previous1.6.12 archive and saved preferences are preserved.

Changes:
- Water style: Vanilla default in every preset, or the retained Stratus physical
  colour/extinction mode. Native mode samples the active animated water atlas,
  vertex biome colour, native lightmap and game environmental underwater fog.
  Full-resolution native surface detail survives reduced-resolution optics.
- Stronger exposed film on top, side and underside faces, retaining shelter,
  roughness, drainage, weather choices and independent true-zero controls.
- Original nearest-interface thin-solid optics for mapped glass/panes, ice,
  slime and honey; independent reflection/refraction strengths. Related material
  render-path and visual acceptance is still pending.
-65 reachable options; all previous62 IDs/defaults/ranges and preset quality
  assignments preserved. No new fullscreen pass; one additional metadata buffer.

Install manually by copying the versioned ZIP into shaderpacks and selecting it
in Iris. Manual copying does not migrate settings. install.py --profile PATH
--previous-settings OLD.zip.txt performs selective migration without selecting
or loading the candidate. --dry-run previews the result. Old preferences and
existing new-version files always win over replacement. Related WATER_TEXTURE
uses approved defaults unless changed manually after the captured baseline;
new controls use source defaults unless a prior explicit manual value exists.
All unrelated current overrides carry forward.

Water controls remain accessible in both modes. Visibility, extinction,
turbidity and the biome override govern Stratus mode; native mode follows the
actual game colour/fog instead. WATER_TEXTURE scales the native alpha layer in
Vanilla mode, and retains whole-surface patterned tint in Stratus mode.

Transparent optics use flat block face normals and bounded screen-space
sampling, not water waves or full-volume ray tracing. Off-screen/hidden scenery
cannot be reconstructed. Multiple overlapping transparent layers and particles
have limited nearest-interface information. Both new optics controls at zero
bypass the effect. No third-party shader implementation was copied.

IMPORTANT LIMITS: known rectangular waterline band remains. Wet-face and glass
live acceptance, biome/status/resource-pack fog coverage and final ZIP loading
remain pending after the user skipped further live checks. Native underwater
mode keeps the prior straight-through exit: it deliberately omits vanilla's
back-face texture overlay, and enabled Stratus optics/atmosphere also differ.
No FPS was measured; no speedup or60FPS claim. See VALIDATION.txt,
IN-GAME-TEST.txt and CHECKS.json for exact evidence boundaries.
''')
(p/'VALIDATION.txt').write_text('''STRATUS 1.7.0-rc1 — CANDIDATE VALIDATION

Native Apple M1 OpenGL4.1 / GLSL330 compatibility-shim compilation:
768 program pairs,0 failures, on final shader source. This is not Iris runtime
transformation or visual proof. Includes all dimensions, four preset choices
and extrema. Warnings are retained in work/stratus-refine-1613/compile-final.log.

Targeted actual GLSL GPU probes:
-96 wet-film samples: all six face normals, weather, shelter and zero controls.
-24,576 transparent-optics pixel samples: metadata/foreground guards, separate
  reflection/refraction and both-zero identity;814 interior pixels changed for
  each independently enabled effect.
-Ten physical-mode and ten native-mode full-resolution underwater composition
  cases: actual submerged distances, nearest exits, glass and additive paths.
All reported0 failures and0 OpenGL errors. Controlled GPU inputs are not live
Minecraft glass, particle or fog-status acceptance.

Control audit:65 reachable options, all previous62 defaults/allowed ranges and
all original four quality assignments preserved. English tooltips present.
Iris parsed all four65-value profiles and matched them when fully applied;
this is a read-only parser/matcher check, not four new live preset captures.
Thirteen installer policy checks passed in temporary profiles, including
preserving later manual/unknown controls and refusing archive replacement.

Live QA equivalents loaded on Minecraft1.21.11, Iris1.10.8, Sodium0.8.14,
Main / Stratus Terrain Lab. Final v3 river surface/far/underwater/waterline
views and shaders-off comparisons reviewed. Native texture sharpness was
corrected after v2 softness. v1's Iris scalar vec4 clear parsing failure was
fixed by explicit four-component clear. Shader-only v3 variants use final
candidate shader bytes with controlled options. Exact final release ZIP has
not been installed, selected or loaded; it is a packaged candidate only.

Remaining visual checks were skipped by user after the Mac locked. The native
waterline capture still has a rectangular sky/treetop band; no clean waterline
acceptance. Additional biome/status/resource-pack, wet faces and transparent
solid layering/zero controls remain pending. FPS remains explicitly deferred.
Candidate packaging uses byte-equivalent source manifest and ZIP integrity
checks. No asset/licence from Minecraft or Sildur is redistributed.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.7.0-rc1 — FINITE LIVE EVIDENCE AND REMAINING CHECKS

Actual Main normal-world captures at1440x842, render distance12, clear/time1000.
Labels and individual cameras/loaded pack/readiness gates are in the report:
outputs/Stratus-1.7.0-rc1-visual-checks/index.html and manifest.json.
Animated textures, particles and clouds advance between captures. Unfocused
visual captures are not FPS results. No FPS samples were taken.

Reviewed: shaders-off vanilla river and underwater, native isolated river,
Reference candidate river/far-bank/underwater and just-below-waterline views;
legacy Stratus mode river was reviewed on v2. v3 preserves the legacy source
and passes the updated physical resolve GPU cases. Above-water native water
colour/texture are close to vanilla, with extra Stratus optics retained when
enabled. Underwater foreground geometry is coherent at the finite tested
camera, but the exit overlay differs from vanilla by the retained straight-
through design. The waterline band is visible and remains unresolved.

After user said skip to unlocking for further live checks, the remaining
visual route was cancelled. Original1.6.12 selection and original player/HUD/
pause/flight/daylight/weather state are restored by guarded test helpers;
restoration evidence is recorded separately in the project, not assumed from
this file. No temporary fixture blocks were placed in this batch.

Before stable acceptance: resume the named batch, verify existing state, then
inspect final ZIP and all new wet-film face/weather/zero conditions; compare
glass/stained/tinted/panes, ice/slime/honey with optics off/on, underwater/glass/
water/particles, cave fallbacks and scenery mode; compare a real water biome
and fog/status changes to shaders-off; inspect menus and finite motion. Resolve
the waterline defect before claiming the roadmap1.7 milestone passed.
FPS stays deferred until explicitly requested. Retain unrelated queued work.
''')
(w/'pending-verification.json').write_text(json.dumps(limits,indent=2)+'\n')
print('Candidate docs prepared with explicit pending acceptance.')

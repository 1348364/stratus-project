from pathlib import Path
import json
w=Path(__file__).parent;p=Path('outputs/Stratus');load=lambda n:json.loads((w/n).read_text());v='1.7.0-rc2'
limits=['Focused Minecraft FPS comparison skipped at user request after locked-Mac prerequisite. No global speedup or60FPS claim; sustained approximately25FPS report still pending.','Progressive unfinished-frame presentation cannot be implemented by a shader pack. No renderer/mod or swapchain changes made.','Known rectangular waterline band and earlier unverified cloud/fog/transparent-solid coverage remain in their earlier batches; no clean1.7 milestone claim.','Finite current-world/fixture coverage only; exact original cave camera not recovered. Original user screenshot and controlled stepped-water reproduction both informed the repair.','Native underwater surface texture is restored, with native atlas/light and slider coverage. Submerged-only fog keeps air beyond the interface clearer than shaders-off vanilla; not pixel-identical vanilla rendering.','Foliage/cutout material4113 stays matte as a whole, avoiding interior leaf-plane sheen. This is a material exclusion, not full voxel-based occlusion or cast shadows.','Remaining local-fixture frames are reviewed as finite visual evidence; several five-second stable FPS-style gates could not settle while unfocused. Scheduling waits are not chunk-readiness or FPS proof.']
checks={'version':v,'batch':'1af89474-f56a-4419-bc73-7f12d4950cfa','native_pairs':768,'native_failures':0,'native_matrix_log':'work/stratus-170-rc2/compile-final-v3.log','raster_GPU':load('raster-final-checks.json'),'wet_GPU':load('wet-checks.json'),'native_dark_cache_before_expected_failure':load('dark-native-before.json'),'native_dark_cache_after':load('dark-native-after.json'),'native_underwater_GPU':load('native-water-final-v3.json'),'physical_underwater_GPU':load('legacy-water-final-v3.json'),'controls':load('control-checks.json'),'migration':load('migration-checks.json'),'atmosphere_single_pass':load('atmos-performance.json'),'FPS_samples':0,'performance_acceptance':'Pending; focused comparison skipped by user. Native pass timings do not establish gameplay performance.','live_evidence':'See versioned gallery and external install/load receipt. Source-equivalent QA checks are separate from final ZIP loading.','limits':limits}
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(w/'limitations.json').write_text(json.dumps(limits,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.7.0-rc2 — MATERIAL, ENTITY AND NATIVE WATER REPAIRS

Original Iris shader pack, MIT licensed. Release candidate; the full1.7 water
milestone and sustained gameplay performance have not passed acceptance.

Changes from rc1:
- Preserve valid dark native water colours instead of substituting a bright
  biome tint. This fixes the reproduced pale cave-water step faces/edge bands.
- Vanilla water mode now includes the active animated underside texture, tied
  to WATER_TEXTURE, with zero and intermediate strengths. Stratus physical mode
  retains its clear underwater interface. Fog still stops at the true water exit.
- Ordinary entities regain vanilla-style two-light face shading in vanilla
  lighting mode, with their actual lightmap, texture and model normals. The
  existing enhanced lighting path and emissive/spidereyes passes remain.
- Leaf/plant cutout surfaces stay matte; their interior planes do not receive
  film. Exposed solid film remains, with a substantially lower solar lobe gain.
- Missing-background water transmission respects local sky exposure. An exact
  zero-contribution underwater atmosphere resolve skips redundant depth/taps.

All65 controls, defaults/ranges and preset quality assignments are retained.
No added pass, reduced resolution, removed quality choice or forced preset.
Related WATER_TEXTURE uses approved defaults where appropriate; later manual
choices and every unrelated override carry forward. Old and existing new-
version settings/archives are never overwritten. Use install.py --profile PATH
--previous-settings OLD.zip.txt, or --dry-run to inspect migration. Manual ZIP
copying does not migrate settings; installation does not imply selection/load.

Deliverable archives belong in the intended Minecraft shaderpacks folder and
remain installed after QA cleanup. Exact final installation/loading evidence is
in the external versioned receipt. Preserve older deliverables/preferences.

LIMITS: no focused FPS sample or general speedup claim. Requested progressive
partial-frame display is owned by Minecraft's renderer, beyond a shader pack.
Submerged-only fog intentionally differs from vanilla's distance fog for air
beyond an exit. Foliage exclusion covers the whole cutout material, not only
neighbour-facing leaf planes. Known waterline defect and earlier pending checks
remain explicit; this is not exhaustive weather/mod/resource-pack certification.
See VALIDATION.txt, IN-GAME-TEST.txt, CHECKS.json and the project change log.
''')
(p/'VALIDATION.txt').write_text('''STRATUS 1.7.0-rc2 — TECHNICAL EVIDENCE

Final source:768 native Apple M1 OpenGL4.1 compatibility-shim program pairs,
0 failures (compile-final-v3.log). All dimensions/presets/extrema; this is not
Iris transformation or visual proof. Exact warnings/logs retained in project.

Targeted actual GLSL GPU checks:
-13 raster/entity cases: opaque/cutout/emissive film masks, native underside
  full/half/zero and physical-mode coverage/transmission, six directional faces.
-96 wet-film weather/shelter/zero/face samples,0 failures/API errors.
-Ten native and ten physical full-resolution underwater composition cases,
  including glass/additive/exit inputs,0 failures/API errors.
-Three dark/native-cache cases: prior source reproduced bright substitution
  on valid dark, valid black and absent-cache inputs. Final source passes all
  three to within1e-8 maximum error; valid black stays valid and missing alpha
  skips the native layer. The prior failures are intentional reproduction proof.
-Single-pass submerged atmosphere timing uses native GL_TIME_ELAPSED at512².
  Output is identical with the zero-contribution bypass. All timing batches are
  recorded, with warm-up variance. This is not Minecraft FPS or proof that the
  user's sustained25FPS problem is solved.

Control audit:65 controls, every old default/range/menu path, all four original
preset assignments and all620 material tokens preserved; tooltips updated.
Thirteen temporary-profile installer checks pass. Source/ZIP integrity and
installed-byte comparison use existing package/install tools. Final selection,
load and effective options are recorded externally in the versioned receipt.

No FPS sample accepted. Performance remains pending after user skipped the
locked-Mac focus prerequisite. Research used primary Sodium/Khronos/GLFW
sources; existing culling configuration was inspected and preserved. No new
mod, presentation/frame skipping, cast-shadow pass or quality reduction added.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.7.0-rc2 — FINITE LIVE CHECKS

Main / Stratus Terrain Lab, Minecraft1.21.11, Iris1.10.8, Sodium0.8.14,
Apple M1/macOS,1440x842, render distance12, time1000/clear. Variant names and
per-capture cameras/reviews are in the saved versioned gallery manifest.
Animations and particles advance between frames. Unfocused visual evidence
is not gameplay FPS; no benchmark commands or accepted FPS samples.

Compare native underside texture at zero/half/full with shaders-off and rc1;
matched stepped-water cave views reproduce pale faces/edges on the prior
source and remove them with dark-native validity handling; inspect matte leaf
cutouts and exposed solid film; compare ordinary entity face shading with
shaders-off. Supplemental indoor/entity/glass views are recorded in the
report only when actually captured/reviewed. Exact original screenshot cave
camera is not known; do not label the controlled fixture as the same location.

Initial water/fixture captures passed full loaded-column/mesh gates. Some
five-second FPS-style gates could not settle while background mesh uploads
continued. Remaining already-loaded local-fixture views use camera/pipeline
assertions plus inspection of the actual changed geometry, with this narrower
scope labelled in the manifest. Waits only schedule capture; no FPS gate claim.
Unloaded/clipped views must be rejected or their acceptance kept pending.

The user skipped focused FPS when asked to unlock. Native fog/status/resource-
pack extremes, prior transparent-solid/cloud acceptance and the known
waterline band remain outside accepted completion. No general60FPS/speedup
claim. Restore original session state, all temporary fixture blocks/sheep and
world weather/daylight, then stop helpers and remove only unchanged temporary
QA copies; keep deliverable candidates installed. Actual restoration proof
belongs in the external restoration receipt, not an assumption from this file.
''')
print('Release candidate documents prepared; limits kept explicit.')

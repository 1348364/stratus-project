from pathlib import Path
import json,hashlib,re
w=Path(__file__).parent;pack=Path('outputs/Stratus')
checks={'version':'1.6.9','date':'2026-10-22','status':'Shader implementation with finite technical and Main visual checks. Focused performance is recorded separately; 60 FPS is not guaranteed.','request_id':'0d847664-366f-4d24-a8eb-e198c604b09c','staging':json.loads((w/'staging.json').read_text()),'controls':json.loads((w/'option-audit.json').read_text()),'native':{'program_pairs':768,'variants':8,'failures':0,'scope':'Native macOS OpenGL compatibility-shim compile/link, separate from Iris'},'GPU':json.loads((w/'gpu-checks.json').read_text()),'water':json.loads((w/'water-regression.json').read_text()),'live':{'profile':'Modrinth Main / Minecraft (1)','world':'Stratus Terrain Lab (normal world)','Minecraft':'1.21.11','Iris':'1.10.8','Sodium':'0.8.14','hardware':'Apple M1 / macOS / OpenGL 4.1','review':'Actual framebuffer captures: vanilla block reference, porous/nonporous film, native-water texture off/strong, river, underwater, waterline and materials/water menus. Final release load is recorded in install receipt.','report':'outputs/Stratus-1.6.9-visual-checks/index.html'},'performance':{'status':'See work/stratus-refine-169/performance-summary.json for completed focused comparisons. No quality cuts; no general 60 FPS guarantee.','structural_changes':['Do not run unused scenery-reflection composite when REFLECTION_MODE=0; its consumers are already compile-time disabled.','Reject underwater and non-water pixels before interface-metadata fetches in lake compose.'],'preserved':'All source quality choices, profile definitions, buffer resolutions, traversal caps and sampling budgets preserved.'},'limits':['Finite scene coverage is not all-weather/night/preset/mod certification.','White blocks may reflect a darker sky at grazing angles; that is optional film reflection, not absorption darkening.','The carried-forward water-pole filter is preserved byte-for-byte; this pass does not independently certify the original reported view.','WET_DARKENING is an explicitly retired compatibility control, not an active effect.']}
(pack/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(pack/'README.txt').write_text('''STRATUS 1.6.9 — VANILLA COLOUR, SURFACE FILM AND WATER TEXTURE
22 October 2026 / Minecraft Java 1.21.11 / Iris 1.10.8 / Sodium 0.8.14
Apple M1, macOS, GLSL 330 / OpenGL 4.1. Original MIT source.

CHANGES
Vanilla lighting is now the source default. It preserves Minecraft texture,
vertex face/AO and lightmap colour without artistic grading. Existing saved
Realistic lighting = On still loads the enhanced path and its tuning controls.
Stratus water, atmosphere and independently adjustable wet film remain active.

Removed absorption darkening and sheltered retained dampness. A thin exposed
film reflects sky/sun on porous and non-porous blocks, including metal/glazed
materials. All-weather and rain-only conditions remain. Sealed caves stay dry;
zero film amount or sheen is a true bypass. Film may reflect a darker sky on a
white block at grazing angles; diffuse albedo itself is not darkened.

Water > Vanilla water texture adds a restrained animated native still/flow
pattern to transmitted water. Uses the active atlas/resource pack, not a
bundled Mojang image. Strength zero restores the clear surface. It adds no
texture lookup, does not change opacity and leaves reflected scenery intact.

CONTROLS AND MIGRATION
62 controls: all 61 previous IDs, ranges and menu access remain, plus the new
water-texture slider. Four preset definitions and every quality choice remain.
SURFACE_DAMPNESS keeps its ID/values and now labels Surface film amount; its
absorption/retention behaviour was explicitly removed. WET_DARKENING retains
saved values and menu access as Retired darkening, an intentional no-op. This
is documented rather than silently converting it into another effect.
Existing REALISTIC_LIGHTING=1 overrides are honoured; only the new source
default changes to 0. All other prior numerical defaults are unchanged.

PERFORMANCE
Skip the unused scenery-reflection pass in sky-only reflection mode and avoid
unneeded water-interface metadata work. No resolution, sample budget, render
distance, quality preset or intended visual feature was reduced. Isolated or
unfocused numbers do not establish gameplay FPS. See the project evidence log
and performance-summary.json for focused samples and remaining target limits.

VERIFICATION
768 native compile/link pairs, 795 component samples, 12 output samples and
10 underwater resolve cases passed. Actual Main captures cover terrain colour,
film/non-porous materials, texture strength, river/underwater/waterline and menus.
Final release loading is recorded separately in Stratus-1.6.9-install.json.
See VALIDATION.txt, CHECKS.json and the versioned visual report in outputs/.

INSTALL
Keep Stratus-1.6.9.zip zipped in Main's shaderpacks folder and select it in Iris.
Preserve old releases/settings. Copy latest saved values only if the new
.zip.txt does not already exist; never overwrite newer user tuning.

LIMITS
Screen-space misses, finite cloud range, foliage-fallback costs and approximate
film/atmosphere remain. The pre-existing water-pole filter is carried forward;
the exact originally reported downward view is not independently certified.
Finite checks do not certify all night/weather/preset/mod combinations or 60 FPS.
''')
(pack/'VALIDATION.txt').write_text('''STRATUS 1.6.9 — VALIDATION / 22 OCTOBER 2026

Native macOS OpenGL compatibility-shim compile/link: 768 pairs, 8 variants,
3 dimensions, zero failures. Separate from actual Iris runtime proof.
Actual GLSL probes: 795 component and 12 output samples, 11 relationship
checks, zero failures/API errors. Includes absorption-independent film,
non-porous response, cave/dry/rain-only bypass, vanilla colour transfer and
artistic-control bypass. Ten full-resolution underwater resolve regressions
passed, including air exits, deep receivers, glass, particles and vertical exits.

All 61 prior control IDs/ranges/menu access remain; 62 total and four unchanged
quality preset definitions. Deliberate source default change: vanilla lighting.
Explicit behaviour removal: absorption/retention; WET_DARKENING is retired.
See CHECKS.json and the external option audit for exact scope.

Actual Main normal-world captures compare dry blocks with shaders-disabled
Minecraft, film on porous and non-porous fixtures, water texture off/strong,
river, underwater/waterline and settings pages. One initial unloaded-fixture
capture is rejected and preserved as evidence, not counted as visual acceptance.
Final release load/source/archive equivalence is recorded in the install receipt.

PERFORMANCE
Focused samples use the actual Minecraft frame-end duration ring with window
focus and framebuffer checks. Dynamic FPS remains enabled. Exact conditions,
raw frame samples and the final summary live in work/stratus-refine-169.
Background samples are invalid and carry no FPS claim. Quality, resolution
choices, sample budgets, range and profiles were not reduced for this release.
No universal appearance equivalence or general 60 FPS guarantee is claimed.

Coverage remains finite. The pre-existing pole-filter code is unchanged;
original reported-view acceptance, exhaustive cave/night/weather/preset/mod
and moving camera coverage require further targeted review as relevant.
''')
(pack/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.9 — LIVE CHECKS AND FOLLOW-UP

Select Stratus-1.6.9.zip in Main. Water texture strength is under Water.
Wet sheen conditions, Surface film amount and Wet sheen strength are under
Materials; Retired darkening explains saved-setting compatibility. Lighting >
Realistic lighting selects vanilla (new default) or preserved enhanced lighting.

Completed finite review: vanilla block palette against shaders-disabled game,
absorption removed, porous/non-porous film, native-water texture off/strong,
river, underwater, waterline, Materials and Water menus. See versioned visual
report and CHANGE-LOG.md for accepted versus rejected capture labels.

Focused FPS evidence is separate from visual acceptance. Preserve 1440x842,
render distance 12, VSync/cap, actual saved shader options, time/weather and
fixed cameras when repeating the recorded comparisons; record focus and Dynamic
FPS. Do not infer game speed from native compilation or background captures.
Keep all quality levels available. Any unmet 60 FPS target stays in CHANGES.md.

Broaden night/rain/shelter, all presets, motion, transparent edges and the exact
original water-pole/distant-leaf views when those scenes are available. Preserve
older ZIPs and current saved settings. Never call finite checks exhaustive.
''')
p=pack/'package.py';s=p.read_text().replace('Stratus-1.6.9-water-pole-test.zip','Stratus-1.6.9.zip');p.write_text(s)
print('Prepared release documentation with actual technical scope and explicit performance boundary.')

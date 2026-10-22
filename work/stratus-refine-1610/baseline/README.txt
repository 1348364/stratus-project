STRATUS 1.6.9 — VANILLA COLOUR, SURFACE FILM AND WATER TEXTURE
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

FOCUSED ACTIVE-GAME RESULTS
1440x842, render distance12, unchanged quality and saved options, Dynamic FPS
enabled, vanilla limiter held at NONE/cap70 by temporary activity resets:
river baseline57.6906 / new56.1894 FPS; forest baseline59.1302 / new60.0723 FPS.
Each sample30 seconds, zero focus-loss polls. River p95 frame24.6077ms; forest
p95 20.7933ms in the new build. No general speedup or sustained60 FPS claim.
The performance request stays pending. Initial AFK/unfocused runs are excluded.

STRATUS 1.6.9 WATER-POLE TEST — CANDIDATE, NOT VISUALLY ACCEPTED
Minecraft Java 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Apple M1 macOS.
GLSL 330 / OpenGL 4.1. Original MIT source; resource textures are not bundled.

WATER-REFLECTION CANDIDATE
Smooth the undefined longitude at the vertical poles of the sky-reflection
cache. This targets four bright wedges in the user's 22 October screenshot
while retaining the existing water fog, reflection, refraction and controls.
Native compile/link passed; the candidate has not yet passed an in-game
before/after visual check. All remaining notes below describe the preserved
1.6.8 baseline and are not new claims for this candidate.

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
Keep Stratus-1.6.9-water-pole-test.zip zipped in shaderpacks and select it in Iris for testing. Preserve old
releases and preference files. Copy the latest saved values only when the new
.zip.txt does not already exist. Do not overwrite newer user settings.

LIMITS
Film, porosity and atmosphere are approximations. Existing screen-space water
miss/edge limits, finite cloud range and foliage-fallback costs remain. Finite
visual coverage is not exhaustive night/preset/mod or motion certification.

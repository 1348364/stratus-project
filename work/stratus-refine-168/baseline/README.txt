STRATUS 1.6.7 — PREFERRED DEFAULTS, SUN CONTROLS, CIRRUS AND RAIN SHEEN
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

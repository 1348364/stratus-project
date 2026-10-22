STRATUS 1.4.0 — ORIGINAL IRIS SHADER PACK
Minecraft Java 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / macOS OpenGL 4.1
Original editable GLSL. Independent Stratus implementation; no Willow shader code.

INSTALL
Put Stratus-1.4.0.zip in your Minecraft instance's shaderpacks folder.
Video Settings > Shader Packs > Stratus-1.4.0.zip > Apply.
Shader Pack Settings opens the reorganised category menu.
The .zip.txt file contains preferences, not shader code; source defaults are built in.
An existing personal override can override factory defaults: Reset restores the
new defaults (vanilla shading mix 1.00, water clarity 1.70, saturation 1.00).

WATER-FIRST OPTICS
Air/water IOR 1.333, Snell-law refraction, exact unpolarised dielectric Fresnel,
and the underwater critical angle/total internal reflection. Normal incidence
reflects about 2.04%, increasing toward grazing angles. Refraction intersects the local opaque tangent plane, then validates the hit
against the screen-depth field. Foreground, off-screen and changed-receiver hits
use a smooth confidence fallback. Displacement is continuously bounded to available
screen coverage; grazing floors do not use an unstable Z-slice iteration.
Beer-Lambert RGB absorption plus suspended-particle scattering uses the same
path model for still-water tops, sides and underwater. Flowing water is identified
from block state and uses a finite sheet/slab thickness: sky behind a waterfall
is not treated as dozens of blocks of deep lake water.
A small directional environment map integrates the same cloud volume as the sky.
Clipped screen-space reflection rays use samples across the visible interval;
blocks and opaque entities are eligible. Seven hit refinements (eight on High)
reduce underwater depth-quantisation stripes. Premultiplied, depth/normal-guided
upsampling separates reflection confidence from colour. The cache covers sky
outside the current view and sky transmitted through thin flowing sheets, so
waterfalls do not cut blue holes through the overcast sky. Submerged reflection paths also absorb light.

ENVIRONMENT
Vanilla vertex water tint provides spatial biome boundaries. Smoothed camera-biome
properties provide sediment/humidity and underwater colour fallback. Swamps are
more organic/turbid; rivers collect rain runoff; warm/cold ocean tints differ.
Local skylight and block light distinguish sheltered/cave water from outdoor
water; cave surfaces are calmer and reject outdoor rain runoff. Water clarity
and sediment controls remain adjustable. This is a rendering model: biome rules
are heuristics, not measured chemistry, a fluid simulation or real sediment data.

DAMP SURFACES
Visible raised terrain neighbours identify corners/depressions that retain water.
Upward porous ground retains more; exposed vertical faces drain. Rain adds films;
biome humidity affects drying tendency. Pore absorption, changed roughness,
Fresnel sky sheen and broad sun highlights give a wet material response.
There is no random dampness noise. Ores and matching stone use the same class.
Entities, particles and held items stay outside terrain dampness.

CLOUDS / SKY
Rounded 3D density with broad connected overcast and finer lobe erosion, two
altitude layers, sun transmission samples and forward-scattering highlights.
The marcher covers its complete intersected volume; no stride cap truncation.
Near samples concentrate around the camera and share a continuous horizon limit,
including flying below/inside/above clouds. All integrations respect scene depth.
Atmosphere > Clouds > Cloud style selects Stratus, real vanilla fancy clouds,
or off. Atmosphere > Sun and moon selects the original Minecraft textured sun/
moon or the soft Stratus sun. The options are independent.

OPTIONS
Water: visibility, biome response, sediment, absorption; Reflections; Waves/refraction.
Lighting and shadows: ambient, vanilla AO, face lighting/mix, warm ground, lamps.
Atmosphere: Clouds; Sun and moon; Fog.
Materials: retained dampness, sheen. Colour and bloom: saturation, white balance,
bloom strength/radius. Performance: cloud/mist/reflection sampling.
All previous controls remain accessible. Fast/Balanced/Reference/High profiles
change sampling; use Balanced first on Apple Silicon.

LIMITS
Screen-space optics cannot recover hidden/off-screen geometry. The sky cache
uses the camera origin, so very low nearby clouds have approximate reflection
parallax. Vanilla cloud meshes and vanilla sun textures are drawn in the view;
the off-screen sky fallback does not reconstruct those exact mesh/texture shapes.
Depth refraction uses a single opaque layer, not multiple glass/water interfaces.
Very thin edges may use undistorted fallback. Geometry remains vanilla Minecraft;
there are no displaced waves, full water-volume boundaries or cast shadow maps.
Cavity dampness is view-dependent geometry estimation, not persistent water storage;
occluded cavities cannot contribute. No PBR resource maps are required.
Fixed exposure and neutral saturation do not force unlit vanilla brightness.

SOURCES / SCIENTIFIC BASIS
PBRT4, Specular Reflection and Transmission (Snell, Fresnel, refractive indices):
https://pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission
USGS, Turbidity and Water (particles, runoff, scattering):
https://www.usgs.gov/water-science-school/science/turbidity-and-water
S. Lagarde, Physically Based Wet Surfaces (pores, roughness, films):
https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/
Iris documentation (uniforms, options, vanilla sky/cloud flags):
https://shaders.properties/current/
Photon's public option categories were consulted only as menu-structure reference:
https://github.com/sixthsurge/photon/blob/main/shaders/shaders.properties
No Photon rendering code is included.

BUILD / VERIFICATION
Edit shaders/core/*.glsl and run python3 package.py from this directory or by path.
The ZIP contains source, these notes, checks and a source checksum manifest.
See VALIDATION.txt / CHECKS.json and the separate 1.4.0 visual report for actual
compiler, in-game image inspections, mod-copy hashes and finite FPS measurements.
Offline compiler checks alone do not demonstrate Minecraft/Iris visual correctness.

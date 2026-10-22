STRATUS 1.1.1 - ORIGINAL IRIS SHADER PACK
Minecraft Java 1.21.11 / Iris / Apple Silicon macOS OpenGL 4.1.
Fully editable GLSL source is included. No earlier shader pack is imported.

CURRENT REVISION
- Ambient occlusion defaults to 1.00 and the menu reaches 1.00.
- Shared water absorption/tint and ripples for tops, sides and underwater.
- Finite world-height volumetric clouds; fly below, through and above the layer.
- Broad restrained daylight glow through the sky and clouds.
- Subtle separable bright-pixel bloom, adjustable to zero.
- Forward HDR geometry lighting, including block particles and thrown items.
- Every outdoor terrain/block-entity material receives matte dampness.
- No procedural dampness noise. Outdoor coverage uses skylight.
- Vanilla-style face contrast: bright tops, darker sides and darkest undersides.

INSTALL
Place Stratus-1.1.1.zip, still compressed, in shaderpacks and select it in Iris.
For live editing, use this directory with shaders/ directly inside it.
Fast, Reference and High alter cloud/mist/reflection sampling quality only.
All aesthetic controls have the same defaults across profiles.

WATER
Water uses shared extinction and body colour from every viewing direction.
Sided waterfall thickness is bounded because screen-space data cannot recover
an unseen exit interface. Overlapping translucent layers use approximate
composition. Reflections use visible scene data and procedural sky.
No material gloss or environmental reflections are applied to solid blocks.

CLOUDS AND LIGHT
The layer defaults to centre Y=192, thickness 40 blocks. Cloud altitude and
thickness are adjustable. It has world-space density and camera parallax, not
just a texture on the sky. Lighting is an approximation of broad scattering;
there is no simulated weather system or full physical multiple scattering.
The distant patterned overcast sky is retained above this finite cloud layer.
Bloom defaults to 0.06 and only spreads bright HDR pixels. Fixed exposure stays.
Face shading defaults to 1.00. Display-colour weights are top 1.00, north/south
0.80, east/west 0.60 and bottom 0.50. Non-axis-aligned normals blend smoothly.
It is fixed in world space and adds no cast-shadow pass or face colour tint.
The shader applies this once; Iris oldLighting remains disabled.
Reference: https://shaders.properties/current/reference/shadersproperties/features/#oldlighting

DAMPNESS
All static blocks, translucent blocks and block entities use the same smooth
outdoor wetting response, including unlisted/modded blocks. Entities and held
items are not blocks and stay dry. Water has its own optical model. Emissive
interiors retain their light. Skylight is used as an exposure approximation;
it is not a rain-occlusion ray trace. No world-position dampness noise remains.

VANILLA TWEAKS
The supplied VanillaTweaks_r924703_MC26.3.x.zip targets resource formats 84-97;
Minecraft 1.21.11 uses format 75. Its custom firefly bushes render black even
with shaders disabled. Use a VanillaTweaks build intended for 1.21.11, or enable
Stratus-Firefly-Compatibility-1.21.11.zip ABOVE VanillaTweaks in Resource Packs.
That separate resource pack selects vanilla firefly models; no textures copied.

SOURCE
core/raster: forward geometry lighting into HDR colour, plus water metadata.
core/resolve: opaque scene, sky and world-height clouds; preserve SSR scene.
core/lake + medium: common water surfaces, reflections and underwater medium.
core/ceiling: finite cloud volume and broad sky illumination.
core/diffuse: uniform outdoor dampness and vanilla-style face shading.
core/bloom-horizontal + bloom-vertical: half-resolution separable bloom.
core/output: fixed exposure, bloom contribution and display conversion.
Properties contain menus, quality profiles, material IDs and render blending.
No compute shaders, SSBOs, image load/store or external texture assets.

TEST STATUS
See IN-GAME-TEST.txt, VALIDATION.txt and CHECKS.json for current verified results.
REBUILD: python3 package.py. Python is not required to use the pack.

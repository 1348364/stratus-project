STRATUS 1.2.0 - ORIGINAL IRIS SHADER PACK
Minecraft Java 1.21.11 / Iris / Apple Silicon macOS OpenGL 4.1.
Editable original GLSL source included. No earlier shader pack is imported.

THIS REVISION
- Natural form shading: integrated sky/ground hemispheres and cosine sun light.
  Blocks, entities and held items share this lighting. Particle quads retain
  lightmap shading rather than inheriting a solid object's face normal.
- Wet materials: pore absorption/saturation, reduced roughness, a thin Fresnel
  sky film and GGX/Smith sun highlights. There is no procedural dampness noise.
  Outdoors exposure is shared; stone and embedded ores share one material class.
- Bloom has a separate, resolution-stable radius and a soft highlight threshold.
- A haze-softened solar core and aureole reveal the sun through overcast.
- Clouds use volumetric XYZ density, height profiles, density-based sunlight
  attenuation and forward scattering. Fly below, inside and above the layer.
- Water clarity can now reach 4.00; its default remains 0.90. Tops, sides and
  underwater still share the same absorption and colour model.
- AO remains at default/max 1.00; foreground clarity and distant mist are retained.

INSTALL
Put Stratus-1.2.0.zip in shaderpacks and select it in Iris.
For live editing, use this directory with shaders/ directly inside it.
Fast, Reference and High alter cloud/mist/reflection sampling quality only.

CONTROLS
Surface dampness controls pore filling and wet film coverage outdoors, including
clear weather. Wet surface sheen scales the reflective film independently.
Natural form shading controls broad diffuse shape; default 1.00. Iris oldLighting
is disabled to avoid applying the game's face multipliers a second time.
Bloom defaults to strength 0.06, radius 1.50. Radius scales with image height.
Sun visibility defaults to 0.65, alongside the existing broad Sky leak control.
Cloud centre defaults to Y=192, thickness 56 blocks; both are adjustable.

MATERIAL AND LIGHT LIMITS
Porosity and roughness are plausible class estimates, not measured material
maps. Unknown/modded blocks and block entities use a generic rough dielectric.
Smooth glass/metals absorb less; fabric retains a broad rough response. Dynamic
entities/held items stay dry. Bright emissive interiors retain their emission.
Sky exposure uses the game's lightmap; it is not an exact rain-occlusion test.
The sky film is an approximate environment reflection, not reflected local scene
geometry. Directional lighting has no cast-shadow map or full GI solution.
Indoor point-light direction is unavailable; the shader retains broad indoor
fill and the game's local lightmap. No spatial dampness noise or puddles added.

WATER AND CLOUD LIMITS
Free-standing waterfall thickness is estimated; screen-space data cannot reveal
an unseen exit interface. SSR cannot show geometry outside the visible scene.
Cloud lighting approximates single scattering plus an ambient multiple-scattering
floor. Noise is computed in GLSL, with no external textures or compute shaders.
Cloud reflections use fewer integration samples to keep their cost bounded.

RESEARCH BASIS (original implementation, real-time approximations)
Wet absorption, roughness and layered water optics:
https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/
Diffuse/specular separation, microfacet GGX/Smith/Fresnel and clear coats:
https://google.github.io/filament/main/filament.html
Volumetric cloud density and lighting concepts:
https://advances.realtimerendering.com/s2017/ (Nubis, Andrew Schneider)
Iris vanilla orientation multiplier and AO behaviour:
https://shaders.properties/current/reference/shadersproperties/features/

VANILLA TWEAKS
The previously supplied 26.3 resource pack targets formats newer than 1.21.11.
Use its 1.21.11 build or the separate Stratus firefly compatibility resource pack
above it. The compatibility resource pack is not part of this shader ZIP.

VALIDATION
See IN-GAME-TEST.txt, VALIDATION.txt and CHECKS.json for the current results and
coverage limits. Rebuild with python3 package.py; Python is not needed to play.

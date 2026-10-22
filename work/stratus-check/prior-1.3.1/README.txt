STRATUS 1.3.1 - ORIGINAL IRIS SHADER PACK
Minecraft Java 1.21.11 / Iris / Apple Silicon macOS OpenGL 4.1.
Original editable GLSL source included. No Willow source is imported.

THIS REVISION
- Less transparent water, a stronger body colour and real moving refraction.
- Emissive-aware bloom with visible radius; ordinary white entities and blocks
  are excluded from the low threshold used for lights.
- Warmer sunlight and an aureole visible through the clouds from ground level.
- Warmer exposed ground during daylight; indoor and night colour stays stable.
- Hybrid face shading combines vanilla top/side/bottom weights with continuous
  sky, ground and directional-light response, including entities/held items.
- Rounded, tetrahedral gradient-noise cloud density and a detailed upper layer.
- World-anchored 3D lowland mist: height-dependent pools and irregular billows,
  clipped to visible terrain and suppressed by indoor skylight exposure.
- Clouds/fog are composited after water. Looking down from above clouds no
  longer draws a distant lake over the foreground cloud layer.

PERFORMANCE DESIGN
1.3.1 caches neighbour depth for atmosphere reconstruction, skips water work on
non-water pixels and removes unused reflection reconstruction in Fast.
The visible effects and sampling counts are retained.
Atmosphere and screen-space water reflections integrate at half resolution,
with depth-aware reconstruction and shared animated water normals.
Bloom uses quarter-resolution buffers and fused Gaussian taps. Water reflections
use 16/28 trace samples instead of 22/46, and broad sky/cloud approximations
replace repeated reflection ray marches. Rough wet sky reflection is prefiltered.
Frame-time measurements, hardware, dimensions, render distance and limitations
are recorded in CHECKS.json and the visual report after validation finishes.
The target is approximately 60 fps, not a hardware-independent guarantee.

CONTROLS
Water clarity: lower is less transparent. New default 0.35; range 0.20-4.00.
Water distortion bends the transmitted scene using animated ripple normals.
Bloom strength defaults to 0.18 and radius to 3.00. Radius scales with image height.
Vanilla shading mix defaults to 0.50; natural form shading remains adjustable.
Sun-warmed ground defaults to 0.45. Sun visibility defaults to 0.85.
Main clouds default to centre Y=192, thickness 72; upper wisps default to Y=360.
AO default/max stays 1.00. Existing ambient and dampness controls are retained.

INSTALL
Place Stratus-1.3.1.zip in shaderpacks, select it in Iris and apply.
Editable source is this directory with shaders/ directly inside it.
Fast/Balanced/Reference/High change cloud/mist/reflection sampling counts.
Balanced keeps terrain reflections and both cloud layers with fewer integration
samples. It is the default; Reference and High provide denser sampling.

LIMITS
The mist follows world-height density and visible depth, not a simulated terrain
humidity field. It favours low ground and avoids a uniform foreground veil;
hidden terrain and full weather fluid dynamics are unavailable to this pack.
Cloud scattering, shadow probes and upper wisps are real-time approximations.
Depth-aware half-resolution reconstruction can lose very thin detail at edges.
Screen-space refraction/reflection cannot recover hidden geometry. Free-standing
waterfall thickness is bounded. Behind-water cloud segments use fewer samples.
Partially transparent layers use approximate composition.
Wet materials use estimated porosity/roughness, not measured PBR maps. The sky
film is an approximate environment reflection. No dampness noise is introduced.
Dynamic entities/held items stay dry, and only true emission receives boosted
light bloom. There are no cast-shadow maps or full global illumination.

SOURCE
raster: forward HDR surfaces, lightmap, material/sky/emission metadata.
resolve: raw opaque scene/sky and reflection source.
water-reflection: half-resolution bounded screen-space reflection tracing.
lake: water normals, depth absorption, refraction and reflection reconstruction.
atmosphere + volume: half-resolution 3D clouds and lowland mist after water.
atmosphere-resolve: depth-aware upsampling and foreground cloud composition.
bloom-horizontal/vertical: masked highlight extraction and separable spread.
output: stable fixed exposure and display conversion.
No compute shaders, SSBOs, external images or shader dependencies.

RESEARCH
Iris render-pass ordering and buffer sizing:
https://shaders.properties/current/reference/programs/composite/
Volumetric clouds and half-resolution reconstruction concepts:
https://advances.realtimerendering.com/s2015/
Lighting and wet-surface optics:
https://google.github.io/filament/main/filament.html
https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/

VALIDATION
Read IN-GAME-TEST.txt, VALIDATION.txt and CHECKS.json for the exact status.
Rebuild with python3 package.py. Python is not required to use the shader.

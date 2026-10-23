WILLOW MIST 2.0
Original Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
Created from the supplied overcast lake/valley images and visual brief.

THE LOOK
A continuous grey-blue cloud ceiling, diffuse light, layered pale valley mist,
natural foreground colours, subdued ambient occlusion, matte solid blocks,
blue depth-dependent water and rippled reflections of visible scenery.
Lantern interiors remain warm and detailed. There is no bloom or shadow pass.
The four supplied images are the design target, not screenshots of this pack.

INSTALL
1. Use Minecraft Java with a compatible Iris/Sodium installation.
   The inspected installation contains Iris 1.10.8 and Sodium 0.8.14 for 1.21.11.
2. Open Options > Video Settings > Shader Packs > Open Shader Pack Folder.
3. Copy Willow-Mist-2.0.zip into that folder, leaving it compressed.
4. Refresh if needed, select the pack and apply it.
5. Open Shader Pack Settings. Reference is the default quality configuration.

You can alternatively copy the editable Willow-Mist folder into shaderpacks.
The shaders/ directory must be directly inside the pack folder, or at the root
of its ZIP. This deliverable has not been installed or selected automatically.

PRESETS
Fast: one cloud-detail layer, one mist sample, procedural sky water reflections.
      Missing tree/terrain reflections are a deliberate reference compromise.
Reference (default): two cloud-detail layers, three mist samples, 24 reflection
      ray steps plus four refinement steps where an intersection is found.
High: three cloud-detail layers, five mist samples, 48 reflection ray steps
      plus six refinement steps at an intersection.

The domain-warp cloud sheet is present in every preset. Presets change sampling
budgets, retaining all artistic defaults: colour, exposure, AO, water strength,
cloud coverage, mist density and movement. All keep solids matte and cast
shadows disabled. No game frame-rate claim has been made.

CONTROLS
Light and colour: ambient brightness, independent AO, colour temperature,
  saturation, block-light brightness and warmth.
Overcast sky: coverage, band scale, irregularity, shading, speed and samples.
Layered valley mist: density, layer altitude, height falloff, clear foreground
  distance and integration samples.
Water: reflection strength/quality/distance, shallow clarity, depth absorption,
  ripple strength/frequency/speed.

The lower mist layer defaults to world Y=72, with another broad layer above it.
If your valley is much higher, raise Mist layer altitude to suit the terrain.
Setting ambient occlusion lower changes contact shading, not exposure.

Rain is not forced by the shader. The overcast look works with clear Minecraft
weather; actual rain/snow still follows the world's weather. The shader does
not change weather, time, terrain, textures or any world data.

WHAT CHANGED FROM WILLOW LITE
- Replaced the warm daylight grade and bloom with neutral foreground colour,
  fixed exposure, a mild highlight shoulder and concentrated lantern interiors.
- Added a world-anchored, warped overcast sky shared by direct views and water.
- Replaced simple distance haze with height-dependent, spatially varied mist.
- Added water-only screen-space terrain reflections and sky fallback, an opaque
  scene snapshot, depth absorption and shallow visibility.
- Added independent weak vanilla AO, gentler diffuse face orientation shading,
  three sampling presets and explicit Nether/End routes.
- Retained Iris-compatible automatic alpha testing and line fallback.

EDIT THE SOURCE
shaders/lib/settings.glsl    25 controls and their permitted values.
shaders/lib/sky.glsl         Cloud ceiling and atmospheric colours.
shaders/lib/fog.glsl         Layered mist, exposure gate and environment fog.
shaders/lib/lighting.glsl    Diffuse lightmap lighting and face shading.
shaders/lib/water.glsl       Ripples, transmission, absorption, Fresnel balance.
shaders/lib/reflection.glsl  Short screen-space rays, refinement and fallback.
shaders/lib/geometry.*       Shared block/entity/translucent shading.
shaders/lib/deferred.fsh     Procedural sky and opaque scene snapshot.
shaders/lib/final.fsh        Linear-to-display output with fixed exposure.
shaders/shaders.properties  Menus and sampling presets.
shaders/block.properties    Water/emissive material classification.
shaders/world-1, world1      Explicit Nether and End program routes.

All shader code is editable GLSL. There are no external code dependencies or
custom texture assets. Minecraft's active textures, biome tints, models and
geometry remain in use. The optional ZIP builder uses only Python's standard
library: run `python3 build.py` from this folder after editing.

KNOWN LIMITS
Screen-space reflections can only use scenery that is visible to the camera.
Off-screen, occluded, overly distant or uncertain hits fade to the same sky
used overhead. This avoids a black miss, but cannot reproduce an off-screen
tree. Reflection detail can change as visibility changes. There is no temporal
history or planar scene rendering. Lanterns and held items are masked out.

The waterfall keeps ordinary animated Minecraft water sides; the custom
reflective surface applies only to top-facing water viewed from air. Glass,
ice, slime, honey and solids never enter the custom water branch.

Mist uses a few analytic density samples and per-surface skylight, not a full
volumetric simulation. Enclosed cave surfaces with no skylight suppress outdoor
mist; cave entrances and modded lighting still need in-game checks. Set the
layer altitude for terrain far above the default sea-level valley.

Sunset, night, caves, underwater and other dimensions use restrained defaults
extrapolated from the daytime reference. Nether and End retain their engine
fog colours and do not use the overcast cloud ceiling or valley mist.

Actual Iris loading, settings-menu behaviour, in-game appearance and game
performance have not been verified. See VALIDATION.txt for the precise tests.
No dedicated integration with Distant Horizons, Voxy, or PBR resource packs
is provided. Screenshots of the supplied generated terrain cannot establish
an exact visual match in a different Minecraft world.

SUGGESTED IN-GAME ACCEPTANCE CHECK
Use a local test world with a lake, spruce trees, shore, matte wood platform,
lantern and glass. Compare daytime clear weather against the supplied images.
Check clouds, mist distribution, contact shading, colours and water separately.
Then check sunset, night, cave interiors, underwater, rain/snow and both other
dimensions. Move the camera near water and screen edges, look through glass,
break a block, and check an entity's damage tint. Measure FPS at a known render
distance and resolution before making a performance comparison.

OFFICIAL INTERFACE REFERENCES
https://shaders.properties/current/reference/programs/gbuffers/
https://shaders.properties/current/reference/programs/deferred/
https://shaders.properties/current/reference/buffers/depthtex/
https://shaders.properties/current/reference/constants/ambientocclusionlevel/
https://shaders.properties/current/reference/shadersproperties/features/
https://shaders.properties/current/reference/miscellaneous/macos/

License: MIT. Complete original shader implementation, building on the original
Willow Lite structure, without importing another shader pack.

STRATUS 1.0.6
Standalone Iris shader pack created from the attached images and visual brief.
Target: Minecraft Java 1.21.11, Iris, Apple Silicon macOS / OpenGL 4.1.

ORIGIN
All shader implementation files in this pack were authored anew for the supplied
visual specification. It has its own deferred renderer, attachment layout,
procedural ceiling, analytic mist integrals and water composition pass.
It does not depend on, import or modify an earlier shader pack. The only shader
includes are files under this pack's shaders/core/ directory. Standard Iris
interfaces, GLSL syntax and established mathematical functions remain necessary.

VERSION 1.0.6 - ENTITY SHADOWS, ORES AND CUTOUTS
Suppresses the vanilla circular shadow through Iris entity-shadow identification.
All vanilla ore variants, raw ore blocks and infested stone now share the
mineral dampness class. Plant stems no longer use timber absorption.
Opaque terrain explicitly rejects transparent texels. Dedicated late particle
and translucent entity/block-entity programs blend into HDR colour and preserve
water metadata.

FIREFLY BUSH RESOURCE-PACK COMPATIBILITY
The supplied VanillaTweaks_r924703_MC26.3.x.zip targets game formats 84-97;
Minecraft 1.21.11 uses format 75. Its bush models produced black planes even
with shaders disabled. The separate Stratus-Firefly-Compatibility-1.21.11.zip
resource pack overrides only the firefly-bush blockstate to select the vanilla
model. Enable it ABOVE VanillaTweaks in Options > Resource Packs. It contains
no copied Minecraft textures. The shader ZIP belongs in shaderpacks; this
small compatibility ZIP belongs in resourcepacks. A compatible VanillaTweaks
build for 1.21.11 is another way to address the incompatible resource pack.

VERSION 1.0.5 - CLEAR FOREGROUND AND BRIGHTER AMBIENT LIGHT
Outdoor mist now starts beyond 80 blocks and blends gradually into the
background. Ordinary engine fog no longer adds a second full haze layer on
top of Stratus mist. Distant valley layers and the render-distance fade remain.
Diffuse ambient brightness defaults to 1.40, with a wider range up to 2.00.
Corner AO is reset to the original Stratus default 0.30.

VERSION 1.0.4 - STRONGER VISIBLE DAMPNESS
Rebalanced the dampness after 1.0.3 was too subtle, especially on side faces.
Default strength is now 1.00, with a wider 0.00-2.00 range. Soil, wood and stone
have stronger diffuse absorption with broad stable variation. Side faces retain
80 percent of top-face damp coverage. Exponential absorption preserves texture
contrast without clipping darker pixels. All surfaces remain matte.

VERSION 1.0.3 - DAMP DIFFUSE MATERIALS
Added the missing reference dampness: outdoor soil, stone and wood absorb more
diffuse light; foliage receives a lighter adjustment. Vanilla texture patterns
and colour ratios remain intact. All solids remain matte. Broad static variation
is world-anchored, and skylight suppresses the effect in enclosed caves.
Surface dampness defaults to 1.00 in every preset, including clear weather.
Set it to zero in Diffuse surfaces to disable it. Rain adds a small smooth increase.
Snow, glass, emitters, entities, held items and unclassified materials have no
damp mask. Nether and End omit this Overworld surface treatment.

VERSION 1.0.2 FIX
Declared RGBA8 and RGBA16F in the shader source. The test harness no longer
supplies those constants. Both the original missing-declaration failure and
the repaired source have been checked, preserving symbolic Iris format names.

VERSION 1.0.1 FIX
Expanded the three Iris clear-colour constructors to four explicit components.
This fixes the confirmed Index 1 out of bounds for length 1 pack-load error.
The installed Iris parser regression now passes.

REFERENCE APPEARANCE
- Soft grey-blue overcast ceiling with broad irregular, undulating bands.
- Pale horizontal valley mist, clear nearby objects and fading distant terrain.
- Diffuse light, independently reduced vanilla AO and matte solid surfaces.
- Damp matte soil, wood and stone; neutral wood and natural vegetation colours.
- Medium blue water, shallow visibility, small ripples and scenery reflections.
- Compact amber lantern interiors retaining their texture detail.
- Fixed exposure. No shadow pass, bloom, sunbeams, lens effects or material gloss.

The supplied images are design targets. They are not captures from this pack.
Minecraft textures, block geometry, models and biome colours stay in use; this
pack does not reproduce generated texture irregularities or reconstruct terrain.

INSTALLATION
1. Run Minecraft Java with compatible Iris and Sodium.
2. Open Options > Video Settings > Shader Packs > Open Shader Pack Folder.
3. Place Stratus-1.0.6.zip in that folder, keeping the ZIP compressed.
4. Refresh the list if needed, select Stratus-1.0.6.zip and apply it.
5. Reference is the default preset in Shader Pack Settings.

For live editing, copy this Stratus folder to shaderpacks instead of the ZIP.
The shaders/ folder must be directly inside the pack directory. The delivered
archive has also been tested in an isolated Minecraft installation. Select it
in your normal profile to use it there.

PRESETS
Fast: simplest broad cloud detail, simple mist patches, procedural sky reflection.
      Missing reflected trees and terrain are an explicit reference compromise.
Reference: two cloud-detail levels, more mist variation, 22 scenery reflection
      samples plus five refinement steps at a candidate intersection.
High: three cloud-detail levels, finer mist variation, 46 scenery reflection
      samples plus six refinement steps.

Quality presets only change CLOUD_LAYERS, MIST_DETAIL and REFLECTION_MODE.
They preserve the same colours, AO, density, water controls and movement rates.
All keep solid blocks matte and cast shadows disabled. FPS is unmeasured.

CONTROLS
Diffuse surfaces: sky ambient brightness, independent corner AO, white balance,
saturation, surface dampness, local lamp brightness and warmth.
Overcast ceiling: coverage, band size, irregularity, internal shade and drift.
Layered mist: density, principal layer Y, thickness and clear foreground distance.
Lake: reflection strength/quality/range, water clarity and absorption, ripple
strength, spacing and speed.

The principal mist layer defaults to world Y=70 with another layer above it.
Raise Lower mist altitude for valleys well above sea level. Reducing corner AO
does not change exposure. Cloud and ripple speed can each be set to zero.
The ceiling looks overcast even during clear game weather. Actual rain and snow
follow the world's weather; the pack does not change weather or world state.

SOURCE GUIDE
shaders/core/options.glsl          Defaults and 26 user controls.
shaders/core/frame.glsl            Iris frame interfaces and colour conversion.
shaders/core/field.glsl            Smooth integer-hash procedural field.
shaders/core/ceiling.glsl          Warped, softly shaded overcast bands.
shaders/core/air.glsl              Closed-form height and layered mist integrals.
shaders/core/diffuse.glsl          Matte illumination and emissive interiors.
shaders/core/raster.vert.glsl      Mesh attributes for terrain and entities.
shaders/core/raster.frag.glsl      Material capture and late translucency.
shaders/core/resolve.frag.glsl     Deferred light/fog resolution and sky.
shaders/core/trace.glsl            Perspective-correct screen-space ray stepping.
shaders/core/lake.frag.glsl         Independent water composition after translucency.
shaders/core/output.frag.glsl      Stable display output and highlight shoulder.
shaders/shaders.properties         Menus, presets and attachment blending.
shaders/block.properties           Water/emissive material classification.
shaders/world-1 and world1         Nether and End routes using the same renderer.

RENDERING LAYOUT
Before deferred:
  colortex0: texture colour and vertex/biome tint, RGBA8.
  colortex1: oriented normal and material class, RGBA16F.
  colortex2: vanilla lightmap sample and sky exposure, RGBA8.
Deferred:
  Resolve matte lighting, fog and sky into colortex3 (RGBA16F).
  Preserve opaque radiance and reflectability in colortex4 (RGBA16F).
  Reset colortex0 and colortex1 for late water attributes using buffer flipping.
After deferred:
  Translucency blends into colortex3. Water alone records colour/normal/depth.
  Composite builds water absorption and reflections into a flipped colortex3.
  Final converts this linear image to the display with fixed exposure.

There are no compute shaders, SSBOs, image load/store, shadow programs, external
texture assets or dependencies on another shader pack. The line program uses
Iris's standard compatibility fallback. Iris supplies per-draw alpha tests.

LIMITS AND UNTESTED CONDITIONS
Screen-space reflections only see visible scene data. Uncertain, off-screen and
overly distant hits fade to the procedural sky. There is no temporal history,
off-screen scene reconstruction or planar reflected-world rendering. Lanterns,
other classified emissive blocks and the held item are excluded from reflections.

When glass is nearer than the recorded water surface, the shader conservatively
retains ordinary translucent composition. Custom water reflections can therefore
be absent through that glass. This preserves its foreground tint and shape.
Basic glass, a translucent slime and shallow water were inspected in the
1.0.6 visual test. Complex overlapping transparency remains a limitation.

Custom water reflections apply to top-facing water viewed from air. Waterfall
sides retain ordinary Minecraft texture animation and geometry. Glass, stone,
wood, vegetation and other solid blocks do not receive environmental reflections.

Mist uses analytic height integrals with broad procedural variation, not a full
volumetric simulation. Per-surface skylight suppresses valley mist on unexposed
cave surfaces. Cave entrances and unusual lighting mods remain unverified.

Sunset, night, underwater, caves and other dimensions were not shown in the
daytime references. Their settings are restrained extrapolations. Nether and End
use game fog colours and omit the overcast ceiling and valley mist.

Version 1.0.6 was visually tested in a real Minecraft Overworld on Apple M1,
including all three reported defects, day/night bushes, water, glass, slime,
rain and underwater views. No shader errors were logged in the final test.
Exact reference-scene matching, held-item visibility, settings-menu checks and
FPS measurements remain unverified. See IN-GAME-TEST.txt and CHECKS.json.

REBUILD
Run `python3 package.py` from this folder. Only Python's standard library is
needed. This creates ../Stratus-1.0.6.zip and refreshes SOURCE-MANIFEST.json.
Python is not needed to use the shader.

IN-GAME CHECKLIST
In a local test world compare a spruce lake, shore, wood deck and lantern with
the supplied reference at similar camera angle and daylight. Check cloud bands,
mist altitude, foreground colour, AO and water separately. Then test a cave,
night, sunset, underwater, glass, rain/snow and both other dimensions. Move along
shorelines and screen edges to evaluate reflection transitions. Check entity
damage tint, held items and block-breaking overlays. Record resolution, render
distance and other rendering mods before measuring performance.

Official Iris interfaces:
https://shaders.properties/current/reference/programs/deferred/
https://shaders.properties/current/reference/constants/rendertargets/
https://shaders.properties/current/reference/shadersproperties/rendering/
https://shaders.properties/current/reference/buffers/depthtex/

Licence: MIT. See LICENSE.txt.

# Stratus 1.6.7 detailed rebuild snapshot — reference only

This is the archived detailed 1.6.7 rebuild reference, including historical source defaults and evidence. The editable target for future design and behaviour changes is `TASK.md`.

For current work, use `TASK.md` as the complete target and `CHANGES.md` for pending incremental requests. This archived file is not a change queue.

Snapshot status: reconciled with **Stratus 1.6.7** on 21 October 2026. The five requests in `TASK-previous-brief.md` were implemented, technically checked, packaged, installed and loaded in Main, with finite actual Minecraft visual comparisons completed. Focused FPS and exhaustive scene coverage remain pending. See `CHANGE-LOG.md` for evidence and limits.

## Purpose and visual direction

Stratus is an original Minecraft Java shader pack for Iris. It keeps Minecraft's block shapes and vanilla texture detail while adding softer, physically motivated lighting, expressive clouds and atmosphere, and particularly strong water optics. The intended look is natural and visually impressive without making terrain glossy or changing the game into a different art style. Water clarity, reflections, refraction, depth colour, turbidity, wetness and environment response are high priorities. Visual quality must be balanced against actual performance on the user's hardware.

## Current reference build and compatibility

- Reference source: `outputs/Stratus/` (editable pack); shader programs and shared code are under `outputs/Stratus/shaders/`.
- Current release: `outputs/Stratus-1.6.7.zip` (243 files; 235 runtime assets; 7,771,716 bytes). SHA-256 `a273a3591d126f1406c9413f7e46684c095e98413998d393375925dce27f56eb`. Packaged bytes match editable source and the installed archive.
- Verified native and current Main runtime: Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1 macOS, GLSL 330 / OpenGL 4.1. This is finite compatibility evidence for the existing profile, not exhaustive mod certification.
- Licence: `outputs/Stratus/LICENSE.txt` (MIT). Carry the licence and attribution into a rebuild.
- Intended runtime review: Modrinth `Main`, normal world / Stratus Terrain Lab for natural terrain and river scenes. Confirm the live profile, loaded ZIP and settings before judging a new build.
- `outputs/Stratus/README.txt`, `VALIDATION.txt`, `CHECKS.json`, `IN-GAME-TEST.txt`, `SOURCE-MANIFEST.json` and `outputs/Stratus-1.6.7-install.json` provide release evidence and inventory. Main selects and has actually loaded 1.6.7, confirmed by the live Iris log and parsed current-pack API. Installation or configuration alone is not loading proof.

## Rendering architecture

The Iris entry programs in `shaders/` are small wrappers around the shared GLSL in `shaders/core/`. `world-1/` and `world1/` provide Nether and End variants. A rebuild may reorganise passes, but must preserve the effects and correct transparency/depth ordering.

| Stage | Current entry point | Main shared code / role |
| --- | --- | --- |
| Geometry and translucent raster | `gbuffers_*.fsh` | `raster.frag.glsl`, `raster.vert.glsl`, `diffuse.glsl`, `moisture.glsl`; block/entity/water/particle/hand output and material response. |
| Initial scene resolve | `deferred.fsh` | `resolve.frag.glsl`; combines raster data for later effects. |
| Environment | `deferred1.fsh` | `environment.frag.glsl`, `environment.glsl`; sky and environmental lighting. |
| Reflection | `composite.fsh` | `water-reflection.frag.glsl`, `scene-trace.glsl`; above-water scenery/sky reflection. |
| Water surface/composition | `composite1.fsh`, `composite2.fsh` | `lake.frag.glsl`, `water-resolve.frag.glsl`, `medium.glsl`, `water-path.glsl`, `water-interface.glsl`, `refraction.glsl`; water optics, depth and transparency. |
| Atmosphere | `composite3.fsh`, `composite4.fsh` | `atmosphere.frag.glsl`, `atmosphere-resolve.frag.glsl`, `volume.glsl`, `weather-volume.glsl`; clouds and mist. |
| Post processing | `composite5.fsh`, `composite6.fsh`, `final.fsh` | Bloom passes and `output.frag.glsl`; final colour output. |

`ceiling.glsl` binds `uniform sampler2D vanillaClouds` via `customTexture.vanillaClouds=minecraft:textures/environment/clouds.png`. It uses integer texel alpha fetches with explicit periodic wrapping, respecting the active game/resource-pack map without redistributing that texture. `weatherNoise` remains available for mist; cloud density no longer uses fine 3D weather noise.

The atmosphere resolve reconstructs cached fog with depth weights. If total depth confidence is below 0.12, non-underwater pixels use an exact-depth `completeAtmosphereSegment(..., true)` evaluation with the same selected full quality; `smoothstep(0.02, 0.12, confidence)` blends back to the cache. The shared helper in `volume.glsl` includes border fog and status effects for both paths. This repairs the zero-fog fallback that can leave distant thin cutouts dark. It adds selective work, not an extra pass or quality reduction. Actual reported foliage and performance remain pending.

`shaders/shaders.properties` defines Iris rendering behaviour, pass blending/buffer resolution, menus and quality presets. `shaders/core/options.glsl` defines available values and source defaults. `shaders/lang/en_us.lang` contains user-facing labels. These three must stay in sync when controls change.

## Visual and functional requirements

### Terrain, lighting and materials

- Preserve vanilla texture detail and block geometry. At full sky exposure, retain the 65% vanilla / 35% realistic sky/ground/sun-facing blend as a reproducible setting. `VANILLA_FACE_CONTRAST` and `REALISTIC_FACE_CONTRAST` independently adjust its components. `FACE_SHADING` and `FACE_BLEND` remain available as overall contrast controls; either zero bypasses the effect. Existing AO and separate `GROUND_WARMTH` remain. Both component controls default to 1.00 and reproduce the former 65/35 combination; zero removes only that component. This is broad diffuse lighting without cast-shadow visibility. Caves retain local mapped light and emission handling.
- `SUN_STYLE=0` draws a polished blocky sun using the active Minecraft `textures/environment/celestial/sun.png` through `customTexture.vanillaSun`. Keep the square silhouette, HDR warmth and a halo local to the sun. `SUN_CORE_BRIGHTNESS`, `SUN_HALO_STRENGTH` and `SUN_HALO_RADIUS` separately tune the polished mode without brightening unrelated objects. `SUN_VISIBILITY` controls the textured core. `SUN_STYLE=1` retains native textured sun/moon rendering. Respect resource-pack replacements; do not redistribute Mojang textures. Main comparisons verified the runtime binding, square core and stronger local glow; core/halo/radius defaults are 4.50/2.00/1.50. Global bloom is unchanged. Core 2.80 and halo 0 retain the earlier sun contribution.
- Local block light has controllable level and warmth; bloom remains restrained and should not make ordinary white blocks or entities glow.
- Moisture changes porous surfaces through absorption, drainage, shelter, humidity and rain. `WET_SHEEN` must produce an adjustable, visible but restrained wet highlight on suitable wet materials while preserving the existing moisture absorption and saved value compatibility. Dry and non-absorbing materials must not become uniformly glossy. Actual Main off/default/maximum rain comparisons show a subtle grazing sheen; clear materials and tested nonporous metal remain matte. Deliberate semantic extension: saved `WET_SHEEN` values still control sheltered retention and now also scale a rain-only exposed absorbent film. The film uses approximate sky reflection and solar highlights, without scenery tracing or a new pass. Porosity is heuristic and rain response is instantaneous rather than accumulated.
- Preserve controls for exposure, white balance, saturation, bloom, ambient brightness and lighting rather than hard-coding one look.

### Water

- Water uses angle-dependent dielectric Fresnel reflection, refraction, ripples/normals, depth-dependent absorption/scattering, environment-aware tint and turbidity, and clarity controls. The visible water geometry remains vanilla.
- Above-water reflections support sky fallback and screen-space scenery tracing. Hidden or off-screen geometry may be unavailable; fade misses to sky without severe edge artifacts. Fast preset explicitly uses sky-only reflection.
- Above-water refraction distortion is adjustable. In the 1.6.4 baseline, underwater transmission is straight-through without a Snell window or reflection overlay. A rebuild may improve this only with explicit visual verification.
- Underwater attenuation applies only to the actual submerged ray segment and ends at the nearest visible water exit. Do not tint the air, distant trees or banks above the water surface as though submerged.
- Keep waterline, shallow/deep river, shore, waterfall, submerged three-dimensional geometry, glass and particle edges coherent. Transparent blocks and falling water should not introduce inverted patches or opaque rectangles.
- Main user controls include `WATER_VISIBILITY` (source default 1.70), `WATER_EXTINCTION` (3.00), `WATER_TURBIDITY` (6.00), `BIOME_WATER` (1), `REFLECT_LEVEL` (1.00), `REFLECTION_MODE` (2), `REFLECT_RANGE` (120), `WATER_DISTORTION` (1.00), `RIPPLE_HEIGHT` (0.80), `RIPPLE_SIZE` (1.00), `RIPPLE_RATE` (0.45), and reflection/refraction/render quality. Saved Main overrides can differ from source defaults.

### Clouds, sky and mist

- The Stratus cloud mode uses the running game's current cloud footprint as the basis for connected physical cloud forms, with adjustable altitude, thickness, coverage, density, shade depth, movement and sampling. Existing `CLOUD_STYLE` modes are Stratus volumetric (0), vanilla fancy (1) and off (2).
- High cirrus is an independent, sky-wide wispy layer controlled by `CIRRUS_AMOUNT`, `CIRRUS_ALTITUDE` and `CIRRUS_DENSITY`. It must remain visible with lower clouds disabled, subject to its own zero/off controls, and retain a natural horizon fade. Main isolation captures show the brighter broad high veil with lower clouds disabled; zero removes it. Optical density is 0.045 times `CIRRUS_DENSITY` (default 1.00), increased from 0.016; daylight colour is brighter. Existing amount 0.65 and altitude 360 blocks are unchanged. This remains a wispy broad veil with finite slab/range limits, rather than dense storm clouds.
- Physical clouds now extrude the current vanilla/resource-pack alpha footprint. Each occupied cell and hole is retained; default span 240 gives 12-block cells. There is no horizontal noise warp, porous erosion or detailed billow field. Gentle vertical relief, broad density gradients and self-shadow/height lighting provide the simple Story Mode-inspired treatment. Exact horizontal topology was verified against every pixel of the installed 1.21.11 map. Height, tick phase, lighting and range intentionally differ from vanilla; exact Story Mode style and exhaustive live motion/height coverage remain unverified. Lower-cloud forms were inspected in the normal-world sky and river captures; their shape code is unchanged in 1.6.7.
- Mist is layered and spatially varied, with a clear foreground distance and restrained cave behaviour. Weather and time should change appearance coherently.
- Key current editable-source defaults include `CLOUD_AMOUNT` 0.68, `CLOUD_ALTITUDE` 256 blocks, `CLOUD_THICKNESS` 12 blocks, `CLOUD_SPAN` 240, `CLOUD_LAYERS` 1, `CIRRUS_AMOUNT` 0.65, `CIRRUS_ALTITUDE` 360 blocks, `MIST_AMOUNT` 0.85 and `MIST_CLEAR` 24 blocks. The complete inventory below is the editable target; compare it with the actual source during implementation.
- Cloud integration uses continuous midpoint quadrature, splitting lower-layer steps at exact vanilla texture-cell boundaries. The upper layer keeps uniform steps. There is no temporal jitter or extra pass. Lower traversal has a 1024-segment safety cap. The range remains bounded to 7000 blocks, smoothly approaching max(512, 4*CLOUD_SPAN) inside the layer (960 blocks at default span). Distant interior structure uses the background; small spans/grazing rays may hit the cap or alias and need live review.
- Option migrations: `CLOUD_AMOUNT` scales opacity of the fixed lower footprint instead of changing its shape; `CLOUD_DETAIL` controls broad gradient strength; `CLOUD_DISTORTION` affects gentle vertical relief only. Existing identifiers and all prior allowed values remain. The 12-block thickness default avoids tall columns seen in an initial offline render; saved explicit thickness overrides continue to apply.

## Controls and presets

Keep a navigable two-column shader settings menu with Water, Lighting, Atmosphere, Materials, Post and Performance categories, and relevant submenus. Keep user-visible English labels for every reachable control. Carry forward every practical setting, its allowed values, presets and saved-setting compatibility across releases, so the user can keep fine tuning. Do not hide, narrow or silently repurpose controls for performance or convenience. If an effect is rebuilt, preserve its useful control or provide an equivalent; document any unavoidable migration and preserve saved option identifiers when semantics are compatible. Compare option inventories before packaging each version.

| Preset | Current intended trade-off |
| --- | --- |
| Fast | Lowest effect resolution; sky-only reflections; reduced cloud/mist/refraction sampling. |
| Balanced | Half-resolution water and atmosphere with moderate scenery tracing. |
| Reference | Full effect resolution, detailed reflection and stronger cloud sampling. |
| High | Further cloud sampling at reference effect resolution. |

Current preset overrides, from `shaders/shaders.properties`:

| Preset | `WATER_RENDER_QUALITY` | `CLOUD_LAYERS` | `MIST_DETAIL` | `ATMOSPHERE_QUALITY` | `REFLECTION_MODE` | `REFRACTION_QUALITY` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fast | 0 | 1 | 1 | 0 | 0 | 0 |
| Balanced | 1 | 1 | 2 | 1 | 1 | 0 |
| Reference | 2 | 2 | 3 | 2 | 2 | 2 |
| High | 2 | 3 | 3 | 2 | 2 | 2 |

All current presets disable cast shadows. Dry and non-absorbing solids remain matte; exposed absorbent materials can show adjustable rain film. Vanilla cloud and sun modes remain independently selectable. Do not assume changing preset preserves the same visual controls or FPS; compare with the actual saved settings.

### Editable variable and value inventory

Each line gives the control identifier, current editable-source default and all currently allowed menu values. This inventory matches the completed 1.6.7 `outputs/Stratus/shaders/core/options.glsl` on 21 October 2026: all 53 previous controls retained and six added, for 59 total. The seven preferred Main values are now source defaults; all four preset definitions, including Reference, remain unchanged and selectable. Parsed Main state reports Custom with zero options changed by the user. Values in Main's `.zip.txt` can override these defaults. Keep this list aligned with `options.glsl`, `shaders.properties` and `lang/en_us.lang` when implementing a spec edit.

```text
SKY_AMBIENT = 1.40 [0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00 2.50 3.00 4.00]
EXPOSURE = 0.20 [-3.00 -2.00 -1.50 -1.00 -0.50 0.00 0.20 0.50 0.75 1.00 1.50 2.00 3.00]
ambientOcclusionLevel = 1.00 [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
WHITE_BALANCE = 0.00 [-0.24 -0.16 -0.08 -0.04 0.00 0.04 0.08 0.16 0.24]
SURFACE_SATURATION = 1.00 [0.00 0.25 0.50 0.75 0.85 0.93 1.00 1.07 1.15 1.30 1.50 1.75 2.00]
SURFACE_DAMPNESS = 1.00 [0.00 0.15 0.35 0.65 1.00 1.35 1.70 2.00 2.50 3.00]
CLOUD_AMOUNT = 0.68 [0.00 0.35 0.60 0.68 0.75 0.90 1.00]
CLOUD_ALTITUDE = 256.0 [64.0 96.0 128.0 160.0 192.0 224.0 256.0 320.0 384.0 512.0 640.0 768.0]
CLOUD_THICKNESS = 12.0 [4.0 12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
SKY_LEAK = 0.35 [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
CLOUD_SPAN = 240.0 [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
CLOUD_DISTORTION = 0.85 [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
CLOUD_RELIEF = 0.75 [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
CLOUD_DRIFT = 0.25 [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
CLOUD_LAYERS = 1 [1 2 3]
MIST_AMOUNT = 0.85 [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
MIST_Y = 70.0 [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
MIST_THICKNESS = 18.0 [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
MIST_CLEAR = 24.0 [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
MIST_DETAIL = 2 [1 2 3]
REFLECT_LEVEL = 1.00 [0.00 0.40 0.60 0.85 1.00]
REFLECTION_MODE = 2 [0 1 2]
REFLECT_RANGE = 120.0 [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
WATER_VISIBILITY = 1.70 [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
WATER_EXTINCTION = 3.00 [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
RIPPLE_HEIGHT = 0.80 [0.00 0.15 0.30 0.55 0.80 1.00 1.30 1.70 2.20 3.00]
RIPPLE_SIZE = 1.00 [0.25 0.40 0.65 0.80 1.00 1.25 1.50 2.00 3.00 4.00]
RIPPLE_RATE = 0.45 [0.00 0.10 0.20 0.45 0.70 1.00 1.50 2.00 3.00]
FACE_SHADING = 1.00 [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00 1.25 1.50 2.00]
WET_DARKENING = 1.00 [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00 2.50]
WET_SHEEN = 0.85 [0.00 0.15 0.35 0.65 0.85 1.00 1.35 1.70 2.00]
BLOOM_STRENGTH = 0.18 [0.00 0.03 0.06 0.12 0.18 0.25 0.35 0.50 0.75 1.00]
BLOOM_RADIUS = 3.00 [0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00 8.00 12.00]
SUN_VISIBILITY = 0.85 [0.00 0.25 0.45 0.65 0.85 1.00 1.50 2.00 3.00]
LAMP_LEVEL = 1.00 [0.20 0.40 0.70 0.85 1.00 1.15 1.30 1.60 2.00 3.00]
LAMP_HEAT = 0.25 [0.00 0.15 0.25 0.40 0.60 0.80 1.00 1.50]
VANILLA_FACE_CONTRAST = 1.00 [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
REALISTIC_FACE_CONTRAST = 1.00 [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
SUN_CORE_BRIGHTNESS = 4.50 [0.50 1.00 1.50 2.00 2.80 3.50 4.50 6.00 8.00]
SUN_HALO_STRENGTH = 2.00 [0.00 0.15 0.35 0.65 0.85 1.00 1.20 1.50 2.00 3.00]
SUN_HALO_RADIUS = 1.50 [0.35 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
CIRRUS_DENSITY = 1.00 [0.00 0.25 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
FACE_BLEND = 1.00 [0.00 0.25 0.50 0.75 1.00]
GROUND_WARMTH = 0.00 [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
WATER_DISTORTION = 1.00 [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
CIRRUS_AMOUNT = 0.65 [0.00 0.35 0.65 0.85 1.00]
CIRRUS_ALTITUDE = 360.0 [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
CLOUD_STYLE = 0 [0 1 2]
SUN_STYLE = 0 [0 1]
WATER_TURBIDITY = 6.00 [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
BIOME_WATER = 1 [0 1]
REFRACTION_QUALITY = 0 [0 1 2]
ATMOSPHERE_QUALITY = 1 [0 1 2]
WATER_RENDER_QUALITY = 2 [0 1 2]
CLOUD_DENSITY = 1.00 [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
CLOUD_DETAIL = 1.00 [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
MIST_SCALE = 96.0 [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
MIST_BREAKUP = 0.85 [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
MIST_LIGHT = 0.65 [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
```

## Packaging and installation contract

- `outputs/Stratus/package.py` collects shader programs, shared code, properties, language files, data/metadata and documentation into a standalone ZIP. It writes `SOURCE-MANIFEST.json`, verifies ZIP integrity and compares packaged bytes with source before replacing the destination.
- `outputs/Stratus/generate_volume.py` is included with the source; preserve generated-volume inputs/metadata when rebuilding.
- A new release needs its own versioned ZIP and matching package metadata. Do not overwrite an older release or the user's newer saved `.zip.txt` options.
- Install the ZIP in the intended instance's `shaderpacks`, select it in Iris, verify the loaded name in the game/log, then test. Packaging, installation and loading are separate proof points.
- Preserve the Main profile's unrelated mods, resource packs, worlds and settings. Use project-local temporary test files when possible.

## Verification and acceptance

- Run the available native compile/link and GPU checks, then verify ZIP integrity/source equivalence. Record exactly what ran and its result; earlier results do not certify a new build.
- Review the actual changed scenes in Minecraft. For water: river, surface, waterline, deep/shallow sections, submerged wood, glass, waterfall and particles. For clouds: below/inside/above layer, several camera pitches and heights, motion, day/sunset and vanilla mode. For lighting: different block faces, materials, rain, caves and local lights.
- Match options, resolution, render distance, weather, time and camera for comparisons; check that the intended ZIP is active. Reject frames with unloaded terrain or a camera intersecting blocks.
- Measure performance only with the game focused and Dynamic FPS/background throttling recorded. The 1.6.4 foreground FPS was **not verified**; do not claim 60 FPS or a speedup from that release's records.
- Keep technical tests, package/install state, actual visual findings and FPS as separate entries in `CHANGE-LOG.md`. Provide screenshot/log paths and state any pending checks.

## Known limitations and verification status

- Screen-space reflections/refraction cannot recover every hidden or off-screen surface.
- Underwater fog in 1.6.4 uses the nearest visible exit and a clear-sky fallback for missing exits.
- Moisture is a visual approximation, not physically measured porosity or sediment.
- The 1.6.6 baseline added the vanilla-dominant blend, square sun and exact-depth fog fallback. Release 1.6.7 adds preferred defaults, local sun controls, independent face controls, visible high cirrus and restrained rain film. Its own 768 native links, 539 GPU samples / 21 relationships and 10 water-resolve cases pass; it does not rely on earlier release tests.
- The controlled depth-rejection mechanism is repaired; the actual reported distant-leaf scene could also contain texture/mipmap/driver artifacts and is not yet certified fixed.
- Main actually loaded 1.6.7 and finite visual comparisons are recorded in `outputs/Stratus-1.6.7-visual-checks/index.html`. The recorded framebuffer is 1440×842, focus is false, and Dynamic FPS is enabled. No valid focused FPS/frame time, maximum-speed or exhaustive visual-equivalence claim is implied. Full night/sheltered-wet, all-preset motion and exhaustive mod coverage remain pending.
- Performance/quality: full settings, presets, resolutions and sample budgets remain; the fallback deliberately uses full selected quality. Dense foliage/fog may increase integration cost. Profile matched representative scenes before optimising, preserve 100% of intended features/quality, and label unchanged visuals or speed gains unverified until measured/reviewed.
- The 1.6.7 inventory audit confirms 59 reachable and labelled controls, unchanged prior allowed values, menu access, slider lists and all four presets. The original 1.6.6 saved settings bytes are preserved. Keep these controls and saved-value compatibility across future releases; document deliberate behaviour extensions such as the rain-film use of `WET_SHEEN`.
- Check the actual scenes relevant to a spec edit and perform matched performance review without reducing intended quality. Use the current release's `IN-GAME-TEST.txt` for specific checks.

## Completed implementation and evidence — 21 October 2026

- Implemented all five requests from the archived brief; built, installed, selected and actually loaded **1.6.7** in normal Modrinth Main / Stratus Terrain Lab. [Release and detailed evidence](CHANGE-LOG.md), [install receipt](../../outputs/Stratus-1.6.7-install.json), [visual report](../../outputs/Stratus-1.6.7-visual-checks/index.html).
- Snapshotted Main's seven saved overrides before editing and adopted them as source defaults; the old preference file remains byte-identical. Reference remains available. [Snapshot](../stratus-refine-167/settings-snapshot.json), [option audit](../stratus-refine-167/option-inventory.json), [actual runtime settings](../stratus-refine-167/final-runtime-state.txt).
- Passed 768 native compile/link pairs, 539 targeted GPU samples / 21 relationships and 10 water-resolve regressions. Actual Main comparisons cover polished/native sun, cirrus-only/off, independent face components, rain strengths/material gating, clear materials, river/underwater and settings menus. Original captures include labelled preliminary and rejected frames.
- Restored player camera and HUD/pause/menu state, stopped the temporary test driver and removed unchanged test packs/settings from Main. The released ZIP remains selected. Focused performance and the remaining coverage limits above are explicitly pending.
- Reconciled this specification and its baseline only after completed implementation; no newer user delta was present. The historical `SHADER-SPEC.md` and archived brief remain untouched. Future work starts only from an explicit request to apply meaningful edits.

## Rebuild handoff rule

Use this file as the visual, functional and settings target, then consult `outputs/Stratus/shaders/core/options.glsl`, `shaders.properties`, `lang/en_us.lang`, the shader source, release manifest and validation records for implementation details. This file inventories user-facing settings and important rendering parameters; it does not list every local GLSL temporary variable. If rebuilding cleanly, reimplement deliberately rather than copying old shaders blindly. Preserve saved option names where useful and record deliberate deviations in `CHANGE-LOG.md`.

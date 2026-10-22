# Stratus shader rebuild specification

Status: Updated for Stratus 1.6.6 on 20 October 2026. Native/GPU checks, packaging and installation passed; Main loading, actual visual acceptance, reported foliage-dot confirmation and focused performance remain pending. No measured speedup or full visual-equivalence claim. See `CHANGE-LOG.md` for evidence.

## Purpose and visual direction

Stratus is an original Minecraft Java shader pack for Iris. It keeps Minecraft's block shapes and vanilla texture detail while adding softer, physically motivated lighting, expressive clouds and atmosphere, and particularly strong water optics. The intended look is natural and visually impressive without making terrain glossy or changing the game into a different art style. Water clarity, reflections, refraction, depth colour, turbidity, wetness and environment response are high priorities. Visual quality must be balanced against actual performance on the user's hardware.

## Current reference build and compatibility

- Reference source: `outputs/Stratus/` (editable pack); shader programs and shared code are under `outputs/Stratus/shaders/`.
- Current packaged candidate: `outputs/Stratus-1.6.6.zip` (243 files; 235 runtime assets). SHA-256 `96378ece4c83993306de014a3423eb93a16d54b15813e218a52c75ffc8d5a555`. Prior 1.6.5/1.6.4 archives remain preserved.
- Target carried forward from 1.6.4; native checks run for 1.6.6, current live compatibility pending: Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1 macOS, GLSL 330 / OpenGL 4.1.
- Licence: `outputs/Stratus/LICENSE.txt` (MIT). Carry the licence and attribution into a rebuild.
- Intended runtime review: Modrinth `Main`, normal world / Stratus Terrain Lab for natural terrain and river scenes. Confirm the live profile, loaded ZIP and settings before judging a new build.
- `outputs/Stratus/README.txt`, `VALIDATION.txt`, `CHECKS.json`, `IN-GAME-TEST.txt`, `SOURCE-MANIFEST.json` and `outputs/Stratus-1.6.6-install.json` provide current candidate evidence and inventory. The ZIP is installed in Main beside 1.6.5 with copied preferences; Main still selects 1.6.5 (confirmed in the runtime log). Installation is not loading proof.

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

- Preserve vanilla texture detail and block geometry. At full sky exposure, `formIrradiance` mixes 65% vanilla axis weights with 35% realistic sky/ground/sun-facing response, before the existing contrast control. Exposure gates the realistic share; fixed vanilla weights remain the sheltered/other-dimension baseline. `FACE_SHADING` default 1.00 and `FACE_BLEND` default 1.00 multiply contrast, bounded to 0.18–1.18; either zero bypasses it. Existing AO and separate `GROUND_WARMTH` default 0.45 remain. This is broad diffuse lighting without cast-shadow visibility. Caves retain local mapped light and emission handling.
- `SUN_STYLE=0` now draws a polished blocky sun using the current Minecraft 1.21.11 `textures/environment/celestial/sun.png` through `customTexture.vanillaSun`. `polishedVanillaSun` projects and fetches exact texels, adds HDR warmth, and shares the existing broad haze glow with the reflection environment. There is no round procedural core/aureole. `SUN_VISIBILITY` controls the textured core. Native celestial draws stay disabled in this mode, preserving the existing default moon behaviour. `SUN_STYLE=1` retains native textured sun/moon rendering without a duplicate procedural disk. Resource-pack replacements are respected; no Mojang texture is redistributed. Native binding/orientation/composition in Main are pending live verification.
- Local block light has controllable level and warmth; bloom remains restrained and should not make ordinary white blocks or entities glow.
- Moisture changes porous surfaces through absorption, drainage, shelter, humidity and rain. Solid blocks remain matte: no sky-reflecting wet film or glossy solid-block sheen. `WET_SHEEN` is a legacy saved option identifier now used for sheltered matte moisture retention.
- Preserve controls for exposure, white balance, saturation, bloom, ambient brightness and lighting rather than hard-coding one look.

### Water

- Water uses angle-dependent dielectric Fresnel reflection, refraction, ripples/normals, depth-dependent absorption/scattering, environment-aware tint and turbidity, and clarity controls. The visible water geometry remains vanilla.
- Above-water reflections support sky fallback and screen-space scenery tracing. Hidden or off-screen geometry may be unavailable; fade misses to sky without severe edge artifacts. Fast preset explicitly uses sky-only reflection.
- Above-water refraction distortion is adjustable. In the 1.6.4 baseline, underwater transmission is straight-through without a Snell window or reflection overlay. A rebuild may improve this only with explicit visual verification.
- Underwater attenuation applies only to the actual submerged ray segment and ends at the nearest visible water exit. Do not tint the air, distant trees or banks above the water surface as though submerged.
- Keep waterline, shallow/deep river, shore, waterfall, submerged three-dimensional geometry, glass and particle edges coherent. Transparent blocks and falling water should not introduce inverted patches or opaque rectangles.
- Main user controls include `WATER_VISIBILITY` (source default 1.70), `WATER_EXTINCTION` (0.90), `WATER_TURBIDITY` (1.00), `BIOME_WATER` (1), `REFLECT_LEVEL` (1.00), `REFLECTION_MODE` (1), `REFLECT_RANGE` (120), `WATER_DISTORTION` (1.00), `RIPPLE_HEIGHT` (0.80), `RIPPLE_SIZE` (1.00), `RIPPLE_RATE` (0.45), and reflection/refraction/render quality. Saved Main overrides can differ from source defaults.

### Clouds, sky and mist

- The Stratus cloud mode uses the running game's current cloud footprint as the basis for connected physical cloud forms, with adjustable altitude, thickness, coverage, density, shade depth, movement and sampling. Existing `CLOUD_STYLE` modes are Stratus volumetric (0), vanilla fancy (1) and off (2).
- High cirrus is an implemented independent, continuous wispy layer controlled by `CIRRUS_AMOUNT` and `CIRRUS_ALTITUDE`. It no longer shares the lower footprint/coverage/scale/distortion. GPU tests show positive density throughout a 24 km sample and identical upper density when the lower layer is disabled or its settings change. It is a finite-altitude 28-block veil with horizon fade, not a spherical shell. Actual sky composition is pending live review.
- Physical clouds now extrude the current vanilla/resource-pack alpha footprint. Each occupied cell and hole is retained; default span 240 gives 12-block cells. There is no horizontal noise warp, porous erosion or detailed billow field. Gentle vertical relief, broad density gradients and self-shadow/height lighting provide the simple Story Mode-inspired treatment. Exact horizontal topology was verified against every pixel of the installed 1.21.11 map. Height, tick phase, lighting and range intentionally differ from vanilla; exact Story Mode style and live appearance remain unverified.
- Mist is layered and spatially varied, with a clear foreground distance and restrained cave behaviour. Weather and time should change appearance coherently.
- Core source defaults include `CLOUD_AMOUNT` 0.68, `CLOUD_ALTITUDE` 256 blocks, `CLOUD_THICKNESS` 12 blocks (changed from 96; 4 is now also selectable), `CLOUD_SPAN` 240, `CLOUD_LAYERS` 3, `CIRRUS_AMOUNT` 0.65, `CIRRUS_ALTITUDE` 360 blocks, `MIST_AMOUNT` 0.85 and `MIST_CLEAR` 24 blocks. Read `options.glsl` for every other default and allowed value.
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

The exact profile values are in `shaders/shaders.properties`. All current presets disable cast shadows and keep solids matte. Vanilla cloud and sun modes remain independently selectable. Do not assume changing preset preserves the same visual controls or FPS; compare with the actual saved settings.

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

## Known limitations and unfinished work

- Screen-space reflections/refraction cannot recover every hidden or off-screen surface.
- Underwater fog in 1.6.4 uses the nearest visible exit and a clear-sky fallback for missing exits.
- Moisture is a visual approximation, not physically measured porosity or sediment.
- 1.6.6 adds the vanilla-dominant lighting blend, polished square sun and exact-depth fog fallback. Completed evidence: 768 native links; 27 GPU relationships across 4 candidate sun renders, 11 fog cases and 216 face samples; 10 water regressions; 53 labelled controls; ZIP/source and installed-byte match. Baseline/reference renders are counted separately. Two inspected offline previews are not Minecraft screenshots.
- The controlled depth-rejection mechanism is repaired; the actual reported distant-leaf scene could also contain texture/mipmap/driver artifacts and is not yet certified fixed.
- Main was confirmed loading 1.6.5. 1.6.6 and copied preferences are installed, but the desktop tool cannot select its normal Java window for live comparison. No focused FPS/frame time, maximum-speed or full visual-equivalence claim.
- Performance/quality: full settings, presets, resolutions and sample budgets remain; the fallback deliberately uses full selected quality. Dense foliage/fog may increase integration cost. Profile matched representative scenes before optimising, preserve 100% of intended features/quality, and label unchanged visuals or speed gains unverified until measured/reviewed.
- All 53 option IDs/defaults/allowed values, menus/sliders/presets and language keys match 1.6.5; 10 saved Main overrides remain valid. “Blended face contrast” and “Polished vanilla sun” labels explain the requested redesign. No settings-file migration. Inventory evidence: `work/stratus-refine-166/option-inventory.json`.
- Next: select 1.6.6 in Iris, verify runtime binding, compare the original foliage scene, terrain/sun/weather/motion/native modes and water/transparency; then benchmark focused matched forest, terrain and river/cloud views. Follow `outputs/Stratus/IN-GAME-TEST.txt`.

## Rebuild handoff rule

Use this file as the visual and functional target, then use `outputs/Stratus/shaders/core/options.glsl`, `shaders.properties`, `lang/en_us.lang`, the shader source, release manifest and validation records for exact behaviour. If rebuilding cleanly, reimplement deliberately rather than copying old shaders blindly. Keep the option names and defaults that users may have saved where compatibility is useful. Record every deliberate deviation and the reason in `CHANGE-LOG.md`.

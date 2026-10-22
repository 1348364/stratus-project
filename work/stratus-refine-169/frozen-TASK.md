# Stratus — editable shader specification

This is the complete, long-term target for Stratus: its intended look, behaviour, construction and checks—not an instruction to rebuild everything on every pass. Put the specific work you want done next in [CHANGES.md](CHANGES.md), then tell the coding chat **“Apply the pending changes.”** Saving either file alone does not start work. In-game option defaults live in shader source. The detailed 1.6.7 snapshot and historical settings inventory remain in [SHADER-SPEC-1.6.7.md](SHADER-SPEC-1.6.7.md).

## Quick edit — major design choices

- Overall look = recognisably vanilla Minecraft: original block geometry and texture detail, with natural lighting, expressive atmosphere and visually impressive water; avoid a uniformly glossy or photorealistic terrain makeover.
- Water look = clear, depth-aware, environment-responsive water with convincing reflections, refraction, ripples, shoreline transitions and underwater visibility.
- Reflection approach = scenery where visible, sky fallback where geometry is missing, with no harsh screen-edge artefacts.
- Underwater rule = only the genuinely submerged portion of a view ray gets water tint or fog; banks, air and distant trees above water stay untinted.
- Lower clouds = connected, Minecraft-footprint-based physical clouds with simple vertical shape, broad shading and gentle movement.
- High clouds = separate, bright, wispy cirrus that remains visible even when lower clouds are disabled.
- Mist = layered and varied, with a clear foreground, restrained caves and coherent weather/time changes.
- Daylight = mostly vanilla block-face contrast, gently enhanced by realistic sun/sky/ground light; preserve caves and local light. Turning the main realistic-lighting mode off restores game vertex face/AO shading and lightmap colour/brightness, with artistic brightness and colour effects bypassed.
- Sun = a polished square Minecraft sun with warm HDR core and a local halo; native textured mode remains available.
- Wet materials = absorbent surfaces can darken and develop subtle adjustable sheen in clear weather or rain. Preserve a rain-only choice, exposure/material gating and a true dry setting; non-absorbing surfaces stay matte.
- Performance = make the implementation as efficient as measurement allows without removing controls or sacrificing any intended visual feature or quality level.
- Compatibility = keep existing user-facing options, presets, menus, labels and saved-setting behaviour across versions.

## Full shader specification

### Identity and reference

- Project = Stratus, an original Minecraft Java shader pack for Iris.
- Current reference = editable source `outputs/Stratus/` and versioned release `outputs/Stratus-1.6.8.zip`; check live state before assuming a newer task uses this build.
- Verified reference runtime = Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1/macOS and GLSL 330/OpenGL 4.1; this is not blanket certification for other setups.
- Licence = MIT; keep licence and attribution in a clean rebuild.
- Intended live review = Modrinth Main and a normal-world terrain/river scene; confirm actual profile, loaded ZIP and options before judging a build.
- Source of in-game option defaults/choices = `outputs/Stratus/shaders/core/options.glsl`; do not copy a settings inventory into this file.
- Default policy = preserve the recorded preferred Main choices as source defaults, while keeping Reference separately selectable; preserve original saved preferences and use shader source for exact current values.

### Terrain, lighting, sun and materials

- Face-lighting design = at full sky exposure, preserve the reproducible 65% vanilla / 35% realistic sky/ground/sun-facing blend; its two components remain independently adjustable.
- Face-lighting controls = retain the separate component controls, overall face contrast and blend controls; setting either overall control to zero bypasses the components in enhanced mode. Keep ambient occlusion and separately adjustable ground warmth. A separate main realistic-lighting switch selects the complete vanilla lighting path without erasing saved component settings.
- Shadows = all current presets have cast shadows disabled; broad directional diffuse lighting must not imply cast-shadow visibility.
- Caves = retain mapped local block light and emission, with controlled brightness and warmth in enhanced mode. Vanilla lighting uses the original game lightmap rather than Stratus ambient/lamp multipliers or invented emission boosts.
- Bloom = restrained; ordinary white blocks and entities must not appear to glow.
- Polished sun texture = sample the active game's/resource pack's square sun through `customTexture.vanillaSun`; keep its silhouette, warm HDR core and a halo local to the sun.
- Sun controls = keep separate core, halo-strength, halo-radius and core-visibility adjustments; do not brighten unrelated objects or alter global bloom as a substitute.
- Native celestial mode = retain native textured sun/moon rendering without a duplicate procedural sun; never redistribute Mojang textures.
- Moisture sources = absorption, drainage, shelter, humidity and rain; porosity is an approximation rather than physically measured material data.
- Wet sheen = view-dependent but restrained on exposed absorbent surfaces, with explicit all-weather and rain-only conditions. Surface dampness and sheen strength remain independently adjustable; zero dampness is dry. Non-absorbing metal, glazed materials and sealed caves remain nonglossy.
- Wet-sheen migration = preserve saved-setting meaning for sheltered retention and film strength; a separate weather-source choice enables clear-weather film or the previous rain-only response. Approximate sky/solar highlights, no scenery trace or extra pass. The vanilla lighting path bypasses material recolouring/film to preserve vanilla surface colour.
- Colour controls = retain exposure, white balance, saturation, ambient brightness, bloom and lighting controls instead of hard-coding one look. Vanilla lighting bypasses artistic exposure, white balance, saturation, highlight shoulder, bloom and ground warmth while retaining their saved values. Stratus water, clouds and atmosphere remain independently active.

### Water

- Optics = angle-dependent dielectric Fresnel reflection, refraction, ripple normals, depth-dependent absorption/scattering, biome-aware tint, turbidity and clarity; visible geometry stays vanilla.
- Above-water reflections = support screen-space scenery plus sky; hidden or off-screen geometry is unavailable, so blend misses to sky without severe edge artefacts.
- Fast reflection mode = sky-only; higher modes keep scenery tracing where available.
- Refraction = distortion above water is adjustable; the present underwater baseline transmits straight through without a Snell window or reflection overlay. Any redesign requires explicit in-game verification.
- Underwater medium = attenuate only the actual submerged ray segment and stop at the nearest visible water exit; missing exits can use clear-sky fallback.
- Water edge cases = keep waterline, shallow/deep river, shore, waterfall, submerged 3D geometry, glass, particles and other transparency coherent.
- Water failure cases = no inverted patches, opaque rectangles, or air/distant banks tinted as if submerged.

### Lower clouds, cirrus and mist

- Vanilla-cloud source = use the running game's/resource-pack cloud alpha footprint via `customTexture.vanillaClouds`; preserve occupied cells and holes with periodic integer texel sampling.
- Lower-cloud topology = extrude the exact horizontal vanilla footprint; no horizontal noise warp, porous erosion or detailed billow field. Height, light, range and tick phase may differ from vanilla.
- Lower-cloud appearance = gentle vertical relief, broad density gradients, self-shadow and height lighting; connected simple forms rather than noisy storm-cloud detail.
- Cloud-control meanings = amount affects opacity without reshaping the footprint; detail affects broad gradients; distortion affects gentle vertical relief only. Existing identifiers and selectable choices remain compatible.
- Cloud integration = continuous midpoint quadrature; split lower-layer traversal at exact vanilla texture-cell boundaries, keep upper-layer steps uniform, and add no temporal jitter or extra pass.
- Cloud safety/range = retain a 1024-segment lower traversal cap and 7000-block outer range; inside the layer, range approaches `max(512, 4*CLOUD_SPAN)`. Check small spans and grazing rays for aliasing/cap effects.
- Cirrus = independent sky-wide wispy veil with natural horizon fade; its own zero/off controls remove it even if lower clouds remain.
- Cirrus density model = optical density `0.045 × CIRRUS_DENSITY`, brighter daylight colour and finite slab/range; not dense storm clouds.
- Mist = spatially varied layers with a clear foreground and restrained cave treatment; preserve weather/time response.
- Thin-cutout fog fallback = below 0.12 cached depth confidence, use full-quality exact-depth atmosphere evaluation and blend back with `smoothstep(0.02, 0.12, confidence)`; include border fog/status effects, never a zero-fog fallback.
- Resource textures = respect current texture-pack replacements and do not bundle Minecraft's cloud or sun images.

### Controls, presets and rendering

- Menu = navigable two-column Water, Lighting, Atmosphere, Materials, camera/colour and Performance categories. Use smaller face/ambient/block-light, lower/high-cloud, cloud-shape, colour and bloom groups, concise labels, useful spacing and English tooltips on every reachable control.
- Control preservation = carry forward every practical shader option, allowed value, preset, menu path and saved-setting identifier; do not hide, narrow or silently repurpose a control for performance.
- Fast preset = lowest effect resolution, sky-only reflections and reduced cloud/mist/refraction sampling.
- Balanced preset = half-resolution water and atmosphere with moderate scenery tracing.
- Reference preset = full effect resolution, detailed reflections and stronger cloud sampling.
- High preset = reference effect resolution with further cloud sampling.
- Preset relationship = all current presets disable cast shadows; switching presets may affect both image quality and FPS, so compare actual saved settings rather than assume equivalence.
- Iris architecture = entry wrappers in `shaders/`, shared GLSL in `shaders/core/`, with Nether and End variants.
- Pass order = geometry/translucency → scene resolve → environment → reflection → water composition → atmosphere → bloom/final colour; preserve transparency and depth ordering if reorganised.
- Settings implementation = synchronise `options.glsl`, `shaders.properties` and `lang/en_us.lang` when controls change.
- Optimisation = target measured bottlenecks; avoid redundant passes, texture reads and ray steps, and skip invisible-pixel work, while preserving full selected quality and all intended visuals. Skip cloud-field evaluation only beyond its guaranteed zero-density envelope, hoist invariant mist lighting without changing sampling, and skip unused bloom passes in vanilla lighting. Keep whole-game improvement and appearance claims pending until matched focused measurements support them.

### Packaging, testing and evidence

- Packaging = build a new versioned standalone ZIP with `outputs/Stratus/package.py`, source manifest, archive integrity and source-byte equivalence; preserve generated-volume inputs and metadata.
- Existing releases/settings = do not overwrite older release archives or a newer saved `.zip.txt` options file; preserve unrelated mods, worlds, resource packs and instance settings.
- Installation = install in the intended instance, select in Iris and verify the active loaded pack in game/log; packaged, installed, selected and loaded are distinct states.
- Technical validation = run native compile/link, targeted GPU checks and ZIP/source validation for the changed build; prior-release passes do not certify new code.
- Visual validation = inspect actual changed scenes in Minecraft with matched options, resolution, render distance, weather, time and camera; reject unloaded terrain or camera-inside-block frames.
- Water scenes = river, surface, waterline, shallow/deep sections, submerged wood, glass, waterfall and particles.
- Cloud scenes = below/inside/above layer, multiple camera pitches/heights, motion, day/sunset and vanilla mode.
- Lighting scenes = block faces, materials, rain, caves, local lamps and the polished/native sun comparison.
- Performance validation = focused-game FPS/frame time with hardware, settings and Dynamic FPS/background throttling recorded; do not claim speedup from unmatched scenes or background-throttled results.
- Evidence log = start each release entry in `CHANGE-LOG.md` with a short summary, then record changed files, build, technical checks, installed/loaded state, in-game visuals, performance and pending checks separately.
- Current verification limits = 1.6.8 has native/GPU and finite actual Main lighting/material/menu/river review, with preserved current saved settings. Focused 1.6.7/1.6.8 FPS was explicitly deferred by the user to the morning of 22 October 2026. Exhaustive scene/preset/night/mod coverage and the original distant-leaf scene remain unverified. Isolated atmosphere GPU timings do not establish whole-game speedup or universal 99% visual equivalence.
- Rebuild rule = use this entire list as the absolute target for a clean rebuild; consult source and the archived detailed 1.6.7 spec for implementation facts, preserve compatible saved option names and document deliberate deviations.
- Change scope = for an ordinary coding pass, work only on pending requests in `CHANGES.md`; preserve every other requirement in this file.
- After-change reconciliation = after each completed change, compare this target with actual source, options, presets, release and checks; refine stale or unclear wording and incorporate completed, approved design changes without overwriting newer user edits.
- Pending-work rule = if intended behaviour is not implemented or verified, keep it visible in `CHANGES.md` and the evidence log. Never weaken this target merely to make incomplete code appear compliant.

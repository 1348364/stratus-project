STRATUS 1.6.4 — MATTE MOISTURE AND SMOOTHER CLOUD TRAVERSAL
Original Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
Target: GLSL 330 / OpenGL 4.1. Complete editable source and MIT license included.

Solid blocks retain vanilla texture detail and matte diffuse shading. Porosity,
face drainage, partial shelter, humidity and rain vary moisture absorption.
The previous sky-reflecting wet film and sun highlight are removed. Nonabsorbing
metal/glazed classes do not acquire porous-material absorption.

MIGRATION: WET_SHEEN remains a compatible saved identifier, now labeled
Sheltered moisture retention. Its value controls extra matte absorption on
porous partially sheltered faces. It cannot enable glossy solid-block reflections.
Existing option values, including water extinction 3.00 and turbidity 6.00 in
the tested profile, were preserved. Defaults and saved overrides are distinct.

Clouds use continuous integration without the old power-of-two spacing jumps.
Inside the cloud volume a smooth distance bound gives nearby cloud structure
more useful samples instead of resolving it as distant horizontal sheets.
The noise field stays in world space; no temporal jitter or extra pass is added.

Above-water water optics remain. Underwater transmission stays unbent, without
a Snell window or reflection overlay. Water fog ends at the nearest visible
exit and does not accumulate over the air beyond it. Glass and particle edges
remain at full resolution. All presets disable cast shadows and keep solids matte.

INSTALL
Put Stratus-1.6.4.zip in the instance shaderpacks folder, keep it zipped, and
select it in Iris. To retain preferences, copy the previous pack's .zip.txt
options beside it using the new Stratus-1.6.4.zip.txt name. In Main this has
already been done by the delivery script; do not overwrite newer preferences.

PRESETS
Fast: lowest effect resolutions, sky-only water reflections; missing terrain
reflection is an explicit reference compromise.
Balanced: half-resolution water/atmosphere and modest scenery tracing.
Reference: full effect resolution, detailed reflections and two cloud sample levels.
High: additional cloud sampling with the same artistic direction.
Vanilla cloud and sun modes remain available independently of quality presets.

VERIFICATION AND LIMITS
768 native compile/link pairs and 122 focused candidate GPU renders passed.
Actual Main visual checks are documented in VALIDATION.txt and CHECKS.json.
Foreground FPS is unverified; no 60-FPS or speedup claim. Water screen-space
limits and nearest-exit behavior remain. Moisture is a visual approximation.
Inside clouds, the integration range approaches max(512, 4*CLOUD_SPAN), or 960
blocks at default span, with distant interior structure approximated by the
background. Low sampling can still soften fine detail. See validation for scope.

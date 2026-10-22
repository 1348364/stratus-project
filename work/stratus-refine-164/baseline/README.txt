STRATUS 1.6.3 — WATER FOG STOPS AT THE SURFACE
Original Iris shader pack for Minecraft Java 1.21.11.

Underwater fog now covers the water segment of the camera ray. An invisible
water-exit depth ends that segment at the surface; objects in air beyond the
exit no longer accumulate water fog over their full distance from the camera.
The interface stays visually transparent, with no Snell window or underwater
reflection overlay. Submerged terrain retains depth-dependent absorption.
Glass and particles use separate foreground/background water distances.
Above-water optics are unchanged. The existing exit-depth attachment is reused;
there is no extra rendering pass or world-data capture.

Validation: 768 native OpenGL compile/link pairs passed across eight variants.
Thirteen focused GPU cases exercised the full-resolution resolve and the
invisible raster capture:
near/far objects beyond the exit, submerged receivers, sky, glass, additive
particles, and vertical exits. All passed with no OpenGL errors.
Main visual verification completed in Stratus Terrain Lab (Creative, normal
world). Matched river-waterline and upward views show restored detail in
above-water objects, with no circular interface patch. A close submerged wood
beam and deeper river view retain water absorption. Above-water river checked.
Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14 / Apple M1 OpenGL 4.1.
The saved water extinction 3.00 and turbidity 6.00 were preserved.

INSTALL: put Stratus-1.6.3.zip in the instance shaderpacks folder, keep it
zipped, and select it in Iris. Editable GLSL and validation are included.
Target: macOS OpenGL 4.1 / GLSL 330. No new clean FPS measurement was made.

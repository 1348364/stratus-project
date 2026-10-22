STRATUS 1.6.12 — WHOLE-SURFACE VANILLA WATER TINT
23 October 2026 / Minecraft Java 1.21.11 / Iris 1.10.8 / Sodium 0.8.14
Apple M1 / macOS / OpenGL 4.1. Original MIT source.

Native animated still/flow luminance and biome colour now modulate the composed
water surface, including reflective and distant water. No distance cutoff,
extra texture reads, blur, render pass or opacity change. The surface tint is
multiplicative: it does not add light or flatten reflected detail.
WATER_TEXTURE retains its full range and ID: zero gives clear optics; all four
presets keep the approved 1.00 default. Every prior control, choice, menu,
preset quality and unrelated visual default is preserved.

Reference retains the approved Main visual AND quality tuning from 1.6.11;
High retains full-resolution effects and detailed scenery optics. This release
makes no performance improvement or approximately60FPS claim. FPS is deferred.

Build: python3 package.py. Install with python3 install.py --profile "/path/to/profile"
Use --dry-run first. Only WATER_TEXTURE is related to this release. Unrelated
latest overrides and later manual water choices are carried; existing new-version
preferences always win. Older archives/preferences are never overwritten.
See CHECKS.json, VALIDATION.txt and the external install/load/visual evidence.

KNOWN PENDING WATERLINE CHECK
At feet164.5,61.24,40.5/yaw0/pitch0 in Terrain Lab, a rectangular sky/treetop
tint band appears just below the surface. It is reproduced at matched settings
on1.6.11 and1.6.12, so it predates this surface-tint change. It remains unresolved
and pending; do not describe all waterline views as clean. See the external
waterline baseline captures and work/stratus-refine-1612/waterline-issue.json.

STRATUS 1.6.6 — VANILLA LIGHTING BLEND, SQUARE SUN AND FOG CUTOUT REPAIR
Editable Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
GLSL 330 / OpenGL 4.1. MIT source included. Candidate: live acceptance pending.

CHANGES FROM 1.6.5
Face shading keeps vanilla as its main contribution: 65% fixed axis contrast,
35% realistic sky/ground/solar response at full sky exposure, before existing
strength/blend controls and limits. World-space light, rain and cave gating stay.
The default sun reads Minecraft's blocky texture with HDR warmth and haze,
replacing the round procedural core. Native vanilla sun/moon mode remains.

Tiny leaves can be missed by every lower-resolution fog depth sample. The old
resolve then applied zero fog, leaving dark dots. Rejected pixels now receive
an exact-depth full-quality atmosphere evaluation, smoothly blended according
to confidence. Valid cached samples and underwater behaviour are preserved.
The mechanism is verified offline; the reported Main scene is not yet checked.

PRESERVED
1.6.5 connected vanilla-footprint clouds, independent high veil, all controls,
defaults, allowed values, four quality presets, pass resolutions and budgets.
Matte moisture, water/reflection/refraction/fog clipping, transparency, mist
model and bloom remain. No quality reduction or new render pass. The fallback
can add cost in foliage-heavy views; actual performance remains unmeasured.

INSTALL
Keep Stratus-1.6.6.zip zipped in shaderpacks and select it in Iris. Copy prior
.zip.txt preferences to Stratus-1.6.6.zip.txt only if the new file is absent.
Main was observed loading 1.6.5; 1.6.6 live loading is not yet confirmed.

CHECKS
768 native compile/link pairs, zero failures. Actual candidate GPU renders:
4 sun, 11 fog, 216 face samples, plus 10 water-resolve regressions. 27 focused
relationships pass; baseline/reference renders are counted separately in
CHECKS.json. Sun texels match the installed 1.21.11 texture. Two offline preview
sheets inspected; they are not Minecraft screenshots. See VALIDATION.txt.

LIMITS
Main visual acceptance, the actual reported leaf scene, matched visual
regressions and focused FPS/frame time are pending. No speedup or full visual
equivalence claim. Existing cloud integration and screen-space water limits
remain. Runtime sun/cloud textures respect resource packs and are not bundled.
The new sun resource path targets Minecraft 1.21.11 specifically.

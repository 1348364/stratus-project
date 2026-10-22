STRATUS 1.6.5 — CONNECTED CLOUDS AND DIFFUSE FACE LIGHTING
Editable Iris shader pack for Minecraft Java 1.21.11 on Apple Silicon macOS.
Target: GLSL 330 / OpenGL 4.1. MIT source included. Candidate, live review pending.

CHANGES
High clouds form an independent sky-wide wispy veil, including gaps in the
physical clouds. Lower clouds read the running game's current clouds.png,
including resource-pack replacements, through an Iris custom texture. No
Minecraft or Story Mode cloud texture is bundled. The horizontal footprint
preserves its occupied pixels and holes. It is extruded with simple forms,
smooth gradients and self-shadowing instead of detailed 3D pores/billows.

Default thickness is now 12 blocks (previously 96); 4 is available for vanilla
slab proportions. All prior thickness values remain selectable. CLOUD_SPAN 240
maps each texture pixel to 12 blocks. Saved option IDs are retained, but
CLOUD_AMOUNT now scales the fixed footprint's opacity, CLOUD_DETAIL controls
broad gradients and CLOUD_DISTORTION only gentle vertical relief. Changes of
height, scale, tick phase and lighting are deliberate custom behaviour.

Block-face contrast combines diffuse sky/ground response and world-space solar
orientation, softened by rain and gated by sky exposure. It remains diffuse:
solid blocks keep matte moisture absorption. FACE_SHADING/FACE_BLEND zero
bypasses contrast. No cast-shadow pass or glossy wet coat is introduced.
Water optics, clear unbent underwater transmission, fog clipping, transparency,
mist, bloom and all four quality presets are preserved.

INSTALL
Keep Stratus-1.6.5.zip zipped in the instance shaderpacks folder and select it
in Iris. To preserve preferences, copy the previous pack's .zip.txt to
Stratus-1.6.5.zip.txt only if that new file does not already exist. Source defaults
are distinct from saved overrides. Main was last observed using 1.6.4; packaging
or installation alone does not prove this candidate loaded.

CHECKS
768 native compile/link pairs; 17 cloud GPU renders; 216 face samples; 32
relationship checks; all 65,536 vanilla footprint cells; 10 water regressions
passed. Five offline previews inspected. These are technical checks, not live
Minecraft visual acceptance or FPS measurements. Actual Main review and focused
performance checks remain pending. See VALIDATION.txt, IN-GAME-TEST.txt and
CHECKS.json. Run package.py to rebuild this versioned archive.

LIMITS
Screen-space water limitations and nearest visible water exit remain. Cloud
integration is finite (7000 blocks, smooth interior bound, 1024 lower-cell step
cap); grazing rays/small spans need live motion and performance review. The
upper layer is a finite-altitude veil with horizon fade. It is not a spherical
shell. Diffuse face lighting is an approximation without cast shadows. Exact
Story Mode reference matching and a speedup are not claimed.

STRATUS1.5.0 — ORIGINAL IRIS SHADER PACK
Minecraft Java1.21.11 / Iris1.10.8 / Sodium0.8.14 / Apple Silicon macOS OpenGL4.1.

This revision separates material absorption from exposed-surface wet sheen,
replaces single-face UV-warp refraction with perspective-correct scene tracing,
and reworks clouds/fog with original periodic3D volume data. Reference quality
is the default, as requested; the previous60fps target is no longer a constraint.

WATER
Snell refraction uses air IOR1 / water1.333 in both directions, with physical
Fresnel and underwater total internal reflection. Distortion1.00 is physical;
values above1.00 deliberately exaggerate it. The transmission ray samples scene
depth and actual receiver normals to preserve block corners and gaps. High
quality permits256screen samples with precise hit validation. High also uses
full-resolution scenery reflections/atmosphere and a512x256cloud sky cache. Beer-Lambert
absorption, scattering, biome tint/sediment, cave lighting, rain response, flowing
sheets and underwater path accounting remain shared with the prior release.

MATERIALS
Absorbent soil, raw timber, stone/ores, masonry and cloth darken according to
material absorption. Smooth/glazed ceramics, glass and metal have no pore
darkening. Polished stone is less absorbent. These block classes are heuristics,
not measured material science or resource-pack PBR maps. Water-film reflections
cover exposed faces independently of absorption; no depth-neighbour corner mask
or random dampness noise. Surface dampness is the master control; Material
absorption darkening and Wet surface sheen are separate controls.

CLOUDS / FOG
Rounded multilayer cloud volumes, fine3D erosion, multiple sun-transmission
samples and approximate multiple scattering. No compulsory flat density floor.
The original128-cubed RGBA volume is included, with its procedural generator.
Fog integrates drifting3D pockets, internal extinction and directional sunlight.
Default foreground clear range24blocks brings local pockets closer while
preserving the immediate foreground. Valley altitude and pocket size/variation
are independent settings. Dense fog/clouds remain geometry-depth clipped.
Actual vanilla cloud and sun/moon options remain available.

OPTIONS
Expanded ranges expose subtle through deliberately exaggerated looks. All
previous options remain; new refraction quality, cloud density/detail and fog
shape/light controls add more specific tuning. Factory defaults preserve
vanilla shading mix1.00, water clarity1.70 and saturation1.00.

INSTALL
Put Stratus-1.5.0.zip in the instance shaderpacks folder, select it in Iris and
Apply. Source defaults use high water/cloud quality; lower sampling profiles
remain available. A personal sidecar can override factory values. The .zip.txt
file contains preferences, not shader code. Main world/mod/settings files must
not be changed by shader installation.

BUILD
python3 package.py creates the installable ZIP, including editable GLSL and
all data. generate_volume.py rebuilds the original volume data (requires NumPy).
The shader itself does not require Python, compute shaders, SSBOs or images.

LIMITS
Screen-space rays cannot reconstruct hidden/off-screen geometry or multiple
independent transparent layers. Flowing-sheet thickness, biome sediment,
material absorption and multiply-scattered light are rendering approximations.
Water waves change shading normals, not block geometry. Cloud-cache parallax
is approximate. No cast terrain shadow map or full fluid simulation is included.
See VALIDATION.txt and CHECKS.json for actual test scope and remaining findings.

RESEARCH
PBRT4: dielectric Fresnel, Snell refraction and total internal reflection:
https://pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission
Lagarde: separate porous wet darkening and surface-water films:
https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/
Jensen, Legakis, Dorsey: Rendering of Wet Materials:
https://graphics.stanford.edu/~henrik/papers/egwr99/egwr99.pdf
Guerrilla: volumetric cloud modeling and lighting concepts:
https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-horizon-zero-dawn
Hillaire: volumetric lighting / participating-media integration:
https://advances.realtimerendering.com/s2015/
Iris: raw3D custom texture binding:
https://shaders.properties/current/reference/buffers/custom_textures/
No rendering code, texture or asset from another shader pack is included.

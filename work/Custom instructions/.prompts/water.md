# Water workflow

Apply this workflow only to the water changes requested in TASK.md.

1. Locate the current water, transparency, fog and compositing passes. Trace colour/depth inputs and coordinate spaces before editing.
2. Reproduce the reported issue and identify whether it involves reflection, refraction, attenuation, transparency, normals or pass ordering.
3. Implement a focused correction. Preserve unrelated optics and expose new controls only when useful.
4. Check relevant scenes: shallow/deep water, shore, waterfall, waterline, upward underwater view and submerged three-dimensional geometry. Include stained glass or other transparent blocks when the change affects their compositing.
5. Look for halos, inverted surfaces, depth discontinuities, off-screen reflection artifacts and excessive distortion. Keep separate defects separately tracked.
6. Run available compile/package checks and inspect the actual scene in the intended Minecraft profile. Record matched settings and performance when relevant.

Describe remaining screen-space limitations plainly. Generated images cannot establish that a shader fix works.

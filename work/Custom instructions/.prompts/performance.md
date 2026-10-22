# Performance workflow

1. Confirm the actual selected build, profile, hardware, resolution, render distance, shader settings and test scene.
2. Establish a repeatable baseline with Minecraft focused. Record background throttling/Dynamic FPS and competing game instances before drawing conclusions.
3. Identify a bottleneck using available profiling or controlled comparisons. Form a specific hypothesis before changing samples, resolution or algorithms.
4. Make focused improvements to the measured bottleneck while preserving the full intended appearance and useful controls. Do not silently lower resolution, sampling, draw distance or effect quality. If a trade-off is unavoidable, present it for the user's choice rather than claiming equivalent visuals.
5. Repeat the same scene and settings after the change. Report measured FPS or frame time with collection conditions; label estimates as estimates.
6. Inspect affected visuals for regressions. If focused in-game measurement is unavailable, mark performance unverified and provide a reproducible next check.

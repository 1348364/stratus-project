# Preparation for the authorised next pass

21 October 2026. No shader source or release changed during this preparation.

## Performance

- [Apple: Optimizing GPU performance](https://developer.apple.com/documentation/xcode/optimizing-gpu-performance): identify expensive passes and shader work from measurements, then repeat the workload after a change. Its Metal debugger instructions are not a claim that the existing OpenGL Minecraft process can use that profiler.
- [Apple: Tuning Your OpenGL ES App](https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/Performance/Performance.html): establish scenario-dependent performance before optimising. This is retired iOS/OpenGL ES guidance; apply the measurement principle, not unsupported platform-specific tooling, to macOS OpenGL.
- [NVIDIA: Advanced API Performance — Shaders](https://developer.nvidia.com/blog/advanced-api-performance-shaders/): branch/texture scheduling trade-offs depend on the workload. NVIDIA recommendations do not prove a speed gain on Apple M1. Search excerpt retrieved; direct page fetch timed out.

Candidate hypothesis from source inspection: `volumetricMist` repeats sun direction/colour/daylight and atmosphere calculations that depend only on uniforms or the ray within a sampling loop. Hoisting identical expressions may remove redundant work without changing quality or step counts, but the compiler may already do this. Measure rather than assume a gain. Preserve atmosphere confidence fallback, cloud traversal, all sample budgets and water paths.

## Shader settings menus

- [Iris: shaders.properties overview](https://shaders.properties/current/reference/shadersproperties/overview/): explicit screen/subscreen membership, slider lists, profiles and language tooltips are supported mechanisms for organising settings.
- [Complementary Reimagined: current shaders.properties](https://raw.githubusercontent.com/ComplementaryDevelopment/ComplementaryReimagined/main/shaders/shaders.properties): observed categories, nested effect submenus, spacing, and separate performance/camera/material pages. Use these organisation principles; do not copy shader implementation or assets.

Proposed Stratus structure: retain existing six main categories, group face/ambient/local lighting, split lower/high cloud controls, move advanced shape parameters into a clear subgroup, keep quality choices together, and give every retained option a discoverable route. Existing option IDs, value lists, presets and saved values remain.

## Behaviour preparation

- Fully vanilla lighting needs more than turning off the realistic face term: the current vanilla term remains multiplied by 0.65 outdoors; lightmap/ambient/lamp multipliers and final exposure/white balance/saturation/shoulder also alter the result. Verify a vanilla reference at matched camera, gamma, time and weather before claiming equivalence. Preserve the independent controls and avoid silently changing the default enhanced look.
- All-weather sheen needs an explicit controllable film source independent of current rain, while preserving the existing weather-driven behaviour and material gating. Keep non-absorbing surfaces nonglossy; clarify labelling rather than pretending porosity is physically measured.

Implementation follows completion of the archived verification as requested. Focused measurement and live API access remain dependent on the pending user answers.

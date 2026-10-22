# Stratus — changes for the next coding pass

Put only the changes you want worked on now under **Pending changes**. `TASK.md` is the complete shader target and remains in force for everything else. A saved file does not start work; tell the coding chat **“Apply the pending changes.”** After implementation and verification, move completed requests to [COMPLETED-CHANGES.md](COMPLETED-CHANGES.md) with the release/evidence reference. If none remain pending, leave **“No pending changes.”** Partial or unverified work stays pending. Studio run actions save the submitted brief as a separate `IN-PROGRESS/<request-id>/CHANGES.md` batch and clear this pending section for your next requests. The coder works on that saved batch; queued work is not completed work.

## Pending changes


- [ ] **Vanilla tint across the entire visible water surface** — make the native animated vanilla/resource-pack water appearance clearly noticeable across nearby, middle-distance and distant visible water, including reflection-dominated views. The current nearby-only/subtle appearance is insufficient. Use the active still/flow texture and biome water colour; preserve natural distance filtering and atmospheric fade without an arbitrary nearby-only cutoff or a uniform colour overlay on the scene. “Entire surface” describes coverage, not identical brightness or texture contrast at every distance.

  Preserve the `WATER_TEXTURE` control, full choice range, menu access and saved-setting compatibility; zero disables this added surface treatment. Keep reflections recognisable and sharp, refraction, depth/clarity, ripple normals, transparency, shoreline/waterfall behaviour and correct submerged-ray attenuation. Apply the intended changed visual default consistently across presets while preserving their approved quality choices and unrelated tuning. This request deliberately broadens TASK.md’s current “modulates transmitted water only” rule where necessary to make the tint visible over the whole surface; reconcile that wording after implementation and verification rather than treating it as a reason to leave reflective/distant water unaffected. It does not authorise tinting above-water banks, trees, glass or the whole screen.

  **Acceptance for the later implementation pass:** compare matched in-game `WATER_TEXTURE` zero/default/maximum views across near/middle/far river or open water, looking down and at grazing/reflection-dominated angles. Confirm the changed default visibly affects the full visible water surface, native animation/biome colour and resource-pack replacements remain respected, and distance filtering avoids shimmer or abrupt bands. Check all presets and shallow/deep water, waterline, waterfall and underwater/transparency regressions; run relevant source/compile/GPU/package and option-compatibility checks and record actual visual evidence. Keep missing checks pending. FPS remains deferred until the user requests it again; do not start it as part of this item.


- optimise performance for referance preset to around 60 FPS while keeping essential viausals, eg. resulution. performance checks has to wait for all chuncks loaded first for a smoother check, other rendering situations can be implmented too like FPS while chuncks loading. 

Current **1.6.11** progress: Reference/source defaults now use the explicitly approved captured Main visual **and quality** tuning; every preset shares 56 visual defaults with six ordered quality choices. The live readiness barrier waits for all view-distance columns, empty queues/workers/uploads and stable counts for ≥5 seconds. FPS sampling and the approximately60FPS target remain **unverified and deferred**: the user said “skip for now, i will request this later.” Do not start FPS tests until requested again. [Release/evidence](CHANGE-LOG.md#22-october-2026--stratus-1611), [readiness evidence](../stratus-refine-1611/chunk-gate-checks.json).


Historical full-detail Reference progress for **1.6.10**: projected-tracer interval reuse and invisible mist-work skips implemented without reducing resolution, quality, range, controls or sample budgets. Matched GPU output checks pass. After the user foregrounded Main, all six30-second full-Reference samples stayed focused at1440×842 with Dynamic FPS FOCUSED and vanilla limiter NONE/cap70. River pooled results were **19.6→20.2 FPS** (two samples/build); forest **17.8→18.1 FPS** (one/build). Small finite gains do not certify general gameplay performance; **the approximately60FPS target remains unmet**. [Current evidence, raw references and next optimisation](../stratus-refine-1610/performance-summary.json).

Historical 1.6.9 focused samples were 57.7→56.2 FPS river and 59.1→60.1 forest using the earlier saved quality choices; they do not certify the new full-Reference target. [Historical summary](../stratus-refine-169/performance-summary.json).

### Remaining verification from TASK.md — RUN BOTH dfc0d10a

- [ ] Verification only — review the relevant exact-depth distant-foliage fog fallback in its intended scene. Occupied-cloud interior and clearer independent cirrus/day/sunset comparisons were completed in 1.6.11; preserve the implemented cloud/fog code and controls. Stage concrete defects only if reproduced. [Verified finite cloud views](../../outputs/Stratus-1.6.11-visual-checks/index.html).
- [ ] Original-issue verification only — recover/review the originally reported downward-water pole and distant-leaf camera/context. The finite pitch90/shoreline regressions and unchanged pole-filter source do not certify those exact historical views.

### Next performance verification — deferred by the user

- [ ] On the next user-requested FPS run, verify the implemented readiness guard in actual sampling: require a fresh successful gate, reject renewed loading/camera/focus/size changes and keep any optional loading-phase samples separate. The barrier itself was live-checked before captures; FPS integration is deferred.

# Stratus — changes for the next coding pass

Put only the changes you want worked on now under **Pending changes**. `TASK.md` is the complete shader target and remains in force for everything else. A saved file does not start work; tell the coding chat **“Apply the pending changes.”** After implementation and verification, move completed requests to [COMPLETED-CHANGES.md](COMPLETED-CHANGES.md) with the release/evidence reference. If none remain pending, leave **“No pending changes.”** Partial or unverified work stays pending.

## Pending changes

- Make sure that referance preset defualt is applied with performance and visual changes from my settings. Other presets will have the performance options = (lower < referance < higher). All preset visuals will pan towards referance preset. 

- optimise performance for referance preset to around 60 FPS while keeping essential viausals, eg. resulution. performance checks has to wait for all chuncks loaded first for a smoother check, other rendering situations can be implmented too like FPS while chuncks loading. 

Performance progress for **1.6.10**: projected-tracer interval reuse and invisible mist-work skips implemented without reducing resolution, quality, range, controls or sample budgets. Matched GPU output checks pass. After the user foregrounded Main, all six30-second full-Reference samples stayed focused at1440×842 with Dynamic FPS FOCUSED and vanilla limiter NONE/cap70. River pooled results were **19.6→20.2 FPS** (two samples/build); forest **17.8→18.1 FPS** (one/build). Small finite gains do not certify general gameplay performance; **the approximately60FPS target remains unmet**. [Current evidence, raw references and next optimisation](../stratus-refine-1610/performance-summary.json).

Historical 1.6.9 focused samples were 57.7→56.2 FPS river and 59.1→60.1 forest using the earlier saved quality choices; they do not certify the new full-Reference target. [Historical summary](../stratus-refine-169/performance-summary.json).

### Remaining verification from TASK.md — RUN BOTH dfc0d10a

- [ ] Cloud/foliage verification only — obtain an actual occupied-cloud interior view, clearer independent high-cirrus and sunset framing, and the relevant exact-depth distant-foliage fog fallback scene. Below/above, layer-height grazing, small-span, native and finite motion-pair captures were reviewed in 1.6.10; the layer-height camera was in a footprint hole and cirrus was too subtle for firm acceptance. Preserve the implemented cloud/fog code and controls; stage concrete defects only if reproduced. [Labelled captures](../../outputs/Stratus-1.6.10-visual-checks/index.html).
- [ ] Original-issue verification only — recover/review the originally reported downward-water pole and distant-leaf camera/context. The finite pitch90/shoreline regressions and unchanged pole-filter source do not certify those exact historical views.

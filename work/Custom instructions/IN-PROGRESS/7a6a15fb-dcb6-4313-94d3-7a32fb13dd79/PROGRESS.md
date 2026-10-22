# Batch progress

Status: technical checks passed; live visual matrix in progress; not packaged.

## Resume here
- Work/evidence: `work/stratus-refine-1612/`; baseline source preserved there.
- Changed: lake composition, new water-surface helper, WATER_TEXTURE tooltip. Native atlas pattern/biome tint multiply completed water optics, without distance cutoff, added reads or reflection blur. All option values/profiles unchanged.
- Frozen delta repeats verified 1.6.11 reconciliation; no duplicate work staged. Shared CHANGES.md is the next queue and is untouched.
- Next: native compile/link, targeted surface and underwater GPU checks, option/installer audit; package new 1.6.12, load and inspect matched Main scenes if live access works.

## Evidence and remaining work
- Initial fingerprints and snapshot comparison saved in work directory.
- Water appearance acceptance remains unverified. Existing foliage/historical-context requests remain pending.
- FPS remains explicitly deferred; no sampling authorised by this batch.

## Technical/live checkpoint
- Native:768 compile/link pairs, zero failures (`compile.log`). Surface GPU:192 samples, zero failures (`surface-checks.json`). Underwater:10cases, zero errors (`water-checks.json`). Installer:10integration checks (`migration-checks.json`). Options/preset inventories unchanged (`option-audit.json`).
- Existing Main process73612 / Terrain Lab /1.6.11 baseline confirmed by actual Iris runtime report. Current game differs from prior session: new initial camera/weather recorded. Active VanillaTweaks has no water asset replacement. Framebuffer1440×842; unfocused captures are visual evidence only, no FPS.
- Driver version1612 attached; BENCH command explicitly disabled. World/daylight/weather state saved for restoration. First camera-flight transition rejected; retry with flight set before camera passed actual loaded441-column gate.
- Reviewed baseline/zero/half/max river views. Tint visible on distant reflective water; same geometry/camera, no source distance cutoff. Close/grazing/downward/underwater/all-preset captures queued. No fixture blocks touched.
- Before final stop: install/select/review released ZIP, return original camera/HUD/pause/flight, restore exact weather/daylight via restore-world-time marker, stop driver and verify markers; remove only own temporary Main QA variants after equivalence checks.

- Additional review: close and grazing on/off pairs show full visible water coverage, preserved reflections/shallow bed and dry banks. Straight-down90° and underwater exit/particles reviewed. Fast/Balanced finite views reviewed. Actual Iris parsed and matched all four62-value profiles. Remaining Reference/High and existing fixtures/waterline captures queued. Report draft: `outputs/Stratus-1.6.12-visual-checks/index.html`; review notes distinguish inspected and pending images.

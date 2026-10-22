# Batch progress

Status: implementation candidate; verification in progress. No release packaged or accepted yet.

## Resume here

- Source: outputs/Stratus. Three added options (65 total): WATER_STYLE, TRANSPARENT_REFLECTIONS, TRANSPARENT_REFRACTION. Previous 62 controls/ranges and quality assignments retained. Native water default in all presets; selectable physical Stratus mode. Original thin-interface transparent optics and six-face exposed wet film implemented.
- Baseline/evidence: work/stratus-refine-1613/baseline, initial-fingerprints.json and initial-* documents. Shared next CHANGES.md untouched; TASK unchanged so far. Frozen delta required no duplicate staging.
- Passed earlier native 768 shader pairs, 96 wet-film GPU samples, 10 legacy/10 native underwater resolve cases and 24,576 guarded transparent-optics GPU samples. Final source refinements invalidate the previous compile/resolve run; final matrix now running. Wet and transparent helper code unchanged since their passing probes.
- QA v1 failed Iris scalar vec4 clear parsing; explicit four-component clear fixed. v2 loaded and actual river/native-vs-vanilla, legacy and underwater screenshots saved. Native atlas layer moved to full resolution in v3 after noticing texture softness; no final visual acceptance yet.
- Current unique v3 packs installed byte-verified (QA-v3-install-equivalence.json); river captures queued. Existing guarded Visual1613Driver/WorldTime1613 still active in same Minecraft PID73612, Main, normal Stratus Terrain Lab. Refreshed live state confirms previous test camera164.5,60,40.5, clear/time1000, HUD hidden/pause off; no newer user camera edits detected.
- Original player/HUD/pause/flight in visual-original-client-state.txt; original weather/time in original-world-state.txt. No temporary fixture blocks placed by this batch yet. Restore these, select final validated release (or original1.6.12 if incomplete), stop helpers and remove only owned unchanged temporary QA files before ending.
- Remaining: final source compile/resolve probes; live final water/biome/fog, wet-face and transparent-solid off/on coverage; profiles/menu/options/migration checks; release metadata/version choice per roadmap; package/install/live final release; restoration; TASK/change-log/archive reconciliation. Keep any unverified compatibility/request portions pending.
- FPS remains explicitly deferred. No focused sampling, speedup or 60FPS claim. Do not consume shared next CHANGES.md or later queued batches.

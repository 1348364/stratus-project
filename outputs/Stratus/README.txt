STRATUS1.6.11 — YOUR REFERENCE PRESET AND CHUNK-READY QA
22 October2026 / Minecraft Java1.21.11 / Iris1.10.8 / Sodium0.8.14
Apple M1 / macOS / OpenGL4.1. Original MIT source.

APPROVED PRESET CHANGE
Reference(Recommended) and the source defaults now use the captured latest Main
visual AND quality choices, explicitly approved by the user. Its quality is
half-resolution water/atmosphere, cloud sampling2, mist3, sky-only reflections
and refraction1. This supersedes the old full-detail Reference definition.
High retains full effect resolution, detailed scenery reflections/refraction
and cloud sampling3. All those quality choices remain manually selectable.
Fast/Balanced use lighter quality choices; no component exceeds Reference.
Every preset explicitly shares the same56 visual settings from Reference.
All62 IDs, allowed values, labels/tooltips and menu paths remain available.
Selecting a preset deliberately applies these visual and quality defaults.

CAPTURED MAIN TUNING
Visual values include sky ambient1, film amount0.65, water visibility2.2,
extinction0.9, turbidity3, ripple height0.55/size0.40/rate1, water texture1.
Remaining source visual values are retained and explicit in every profile.
See RELEASE-POLICY.json and CHECKS.json for the complete machine-readable state.

MIGRATION AND NEWER EDITS
The installer resets only the related changed-default/quality keys to the
approved captured Reference values. It carries unrelated overrides and preserves
later manual old-version edits that differ from that capture, including removal
of an override to return to an older source default. Existing new-version
preferences always win. Old archives/preferences are never overwritten.
Run python3 install.py --profile "/path/to/profile" --dry-run, then repeat without
--dry-run. Use --previous-settings when a QA pack is selected. Select the new
ZIP in Iris afterwards. Installing, selecting and loading are separate stages.
Manual ZIP copying does not perform this migration.

VERIFICATION
768 native compile/link pairs/eight variants/zero failures. Iris interpreted
all four62-option profiles and each matched after applying its declared values.
Ten underwater resolve cases at current Reference optics and ten installer
integration checks passed. Actual Main views compare matched Reference tuning,
water/underwater/fixtures, occupied clouds and independent cirrus/day/sunset.
See the labelled report and external Stratus-1.6.11-install.json for exact scope.

CHUNK READINESS AND PERFORMANCE
The QA driver checks all441 columns in the render12 view disk, Sodium build
jobs/workers/upload/task queues and stable counts for at least5seconds before
allowing a steady-state check. Live traces show it blocked while uploads were
pending. Future FPS sampling also requires focus and valid active-game limits.
FPS WAS EXPLICITLY DEFERRED BY THE USER. No new FPS samples or60FPS claim.
The approved lower-cost Reference baseline is not a code-optimisation speedup.
Existing1.6.10 rendering algorithms are retained in this release. Performance,
exact original pole/leaf scenes and remaining leaf-fog acceptance stay pending.

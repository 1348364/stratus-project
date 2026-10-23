STRATUS 1.6.10 — SETTINGS MIGRATION AND MEASURED-WORK OPTIMISATION
22 October 2026 / Minecraft Java1.21.11 / Iris1.10.8 / Sodium0.8.14
Apple M1, macOS, GLSL330 / OpenGL4.1. Original MIT source.

CHANGES
Preserve the 1.6.9 vanilla colour, independent surface film and native animated
water texture. Reference is now labelled Reference (Recommended); its ID and
full effect resolution/quality remain unchanged. All 62 controls, choices and
menus remain. Every preset explicitly uses the approved colour/film/water-texture
visual defaults. Existing quality assignments remain exactly as before.

The scenery tracer reuses projected interval endpoints and invariant dot
products. Mist skips density work only for its zero-weight clear foreground,
and skips sunlight density samples only when sunlight/scattering contributes
zero. No effect, sample budget, range, resolution or quality selection is cut.
The slower plane-cache experiment was rejected and is not included.

SETTINGS MIGRATION
Use install.py to carry only unrelated latest overrides to a new release.
RELEASE-POLICY.json lists the nine related colour/film/water-texture keys reset
to intended defaults for this release. This reset was explicitly user-approved.
Original old settings remain untouched. Existing new-version settings always
win; the installer never overwrites them or a conflicting archive. Selecting a
preset deliberately applies its explicit visual defaults and original quality.
Future visual defaults apply to all presets; combined visual/performance
changes default to Reference unless explicitly approved otherwise. Performance
implementation changes in this release apply to all presets without quality cuts.

INSTALL
Keep the ZIP zipped. From the editable source folder run:
python3 install.py --profile "/path/to/Modrinth/profile" --dry-run
python3 install.py --profile "/path/to/Modrinth/profile"
Then select Stratus-1.6.10.zip in Iris. Use --archive for a ZIP elsewhere and
--previous-settings for an explicit old .zip.txt path. This matters if a test
pack is currently selected. Installing is separate from selecting/loading.
Manual ZIP copying does not run the selective-settings migration.

VERIFICATION
768 native compile/link pairs / zero failures. Actual GLSL matched tracer
checks: 344,064 pixels per variant, three qualities, zero hit mismatches.
Atmosphere: 131,072 matched pixels across day/night, max linear error <0.0001.
Ten underwater resolve cases and nine installer integration checks passed.
Finite actual Main captures cover water, materials, night and cloud views;
see the labelled visual report and install receipt for exact accepted scope.

FOCUSED FULL-REFERENCE RESULTS AND LIMITS
1440x842 / render12 / simulation8 / same six Reference quality selections,
weather clear / time6000 / fixed matched cameras / saved VSync true / cap70.
Dynamic FPS FOCUSED; vanilla limiter NONE/cap70 confirmed every5seconds.
River, two30-second samples per build: baseline19.6154 / new20.1645 FPS.
Forest, one30-second sample per build: baseline17.7699 / new18.0673 FPS.
All six samples had zero focus-loss polls. Small finite gains (~2.8% river,
~1.7% forest) are not a general gameplay guarantee. Reference60FPS remains
unmet and pending. Earlier~56FPS samples used different saved quality choices.
No native GPU probe/profiler ran concurrently. Temporary activity resets left
saved options unchanged and were stopped; original client state was restored.
Screen-space misses, finite cloud range and approximate film/atmosphere remain.
Occupied-cloud interior, clearer independent cirrus/sunset, exact historical
pole/leaf views and exhaustive scene/preset/mod/motion coverage remain pending.
See VALIDATION.txt, CHECKS.json and Stratus-1.6.10-performance.json in outputs/.

from pathlib import Path
import json
w=Path('work/stratus-refine-1610');p=Path('outputs/Stratus')
def read(n):return json.loads((w/n).read_text())
performance={'status':'Pending: focused active-game Reference comparison unavailable; no whole-game speedup or 60 FPS claim.', 'target_preset':'REFERENCE', 'quality_reduction':False,'framebuffer':[1440,842],'render_distance_chunks':12,'simulation_distance_chunks':8,'saved_vsync':True,'saved_max_fps':70,'saved_inactivity_fps_limit':'afk','DynamicFPS_enabled':True,'observed_focus':False,'observed_DynamicFPS_state':'UNFOCUSED','observed_vanilla_limiter':'LONG_AFK / cap15','scope':'Main river GPU pass diagnostics are unfocused and do not establish gameplay FPS. Native probes are isolated microbenchmarks.', 'reflection_pass_diagnostic_ms':{'baseline':24.274,'candidate':22.457},'diagnostic_limit':'Different short diagnostic sessions; not an accepted matched focused benchmark. Plane-cache and no-reflection-fog experiments were rejected and are excluded from release source.','actual_samples':'No accepted focused sample for 1.6.10 yet. Mac locked / game unfocused; retain request in CHANGES.md.'}
(w/'performance-summary.json').write_text(json.dumps(performance,indent=2)+'\n')
checks={'version':'1.6.10','date':'2026-10-22','request_id':'dfc0d10a-85ec-429d-ab34-b70c4ce76c83','status':'Finite source/native GPU and Main QA checks; installed/loaded release proof is recorded separately in outputs/Stratus-1.6.10-install.json. Performance target remains pending.','baseline':'Released Stratus1.6.9, byte-equivalent runtime snapshot','native':{'program_pairs':768,'variants':8,'failures':0,'scope':'Native macOS OpenGL compatibility-shim compile/link; separate from Iris runtime'},'controls':read('option-audit.json'),'migration':read('migration-checks.json'),'trace':read('interval-checks.json'),'atmosphere':read('mist-checks.json'),'water':read('water-checks.json'),'performance':performance,'live':{'profile':'Modrinth Main / Minecraft (1)','world':'Stratus Terrain Lab normal world','Minecraft':'1.21.11','Iris':'1.10.8','Sodium':'0.8.14','hardware':'Apple M1 / macOS / OpenGL4.1','scope':'Actual framebuffer captures from immutable QA packs using final runtime code. Baseline, isolation variants and rejected frames are labelled separately in the visual report. Release loading and final preferences require the external install receipt.','report':'outputs/Stratus-1.6.10-visual-checks/index.html'},'preserved':['All 62 source option IDs/defaults/allowed values and menu paths','Original six quality assignments in each of four profiles','Full chosen framebuffer/effect resolutions, sample budgets, traversal caps and ranges','Existing pole filter and all unrelated runtime source','Older archives/preferences and existing new-version settings'], 'limits':['No accepted focused Reference FPS sample and no verified 60 FPS result','Finite checks do not certify all scenes, presets, mods or movement','Exact historical downward-water pole and distant-leaf contexts remain unverified','Repeated same-pack reflected foliage varies; screenshots do not establish pixel equivalence','The plane-cache and no-reflection-fog diagnostic experiments are not release source']}
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(p/'README.txt').write_text('''STRATUS 1.6.10 — SETTINGS MIGRATION AND MEASURED-WORK OPTIMISATION
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

PERFORMANCE AND LIMITS
The 60 FPS Reference request remains pending. Unfocused GPU pass diagnostics
and isolated timings do not establish gameplay FPS or a whole-game speedup.
No accepted focused 1.6.10 comparison is claimed. Preserve focus, resolution,
quality, weather/time and both Dynamic FPS and Minecraft AFK state for retests.
Screen-space misses, finite cloud range, approximate film/atmosphere and finite
scene coverage remain. The old pole filter is unchanged; exact historical pole
and distant-leaf views remain unverified. See VALIDATION.txt and CHECKS.json.
''')
(p/'VALIDATION.txt').write_text('''STRATUS 1.6.10 — VALIDATION / 22 OCTOBER 2026

Native compatibility-shim compile/link: 768 program pairs, eight variants,
three dimensions, zero failures. This is separate from actual Iris loading.
Actual projected-tracer GLSL: seven synthetic scenes at three quality levels,
344,064 pixels per variant, zero hit mismatches, zero errors over0.001 and
zero OpenGL errors. Same interval budgets, ranges and occlusion logic remain.
Actual full atmosphere GLSL: eight day/night/height/range cases,131,072 matched
pixels, max linear RGBA error0.0000621081 (<0.0001), zero OpenGL errors.
Ten current-source underwater resolve cases pass, including air exits, glass,
additive particles and vertical exits. Nine temporary-profile installer checks
pass, including concurrent conflicting archive refusal and no overwrites.

All62 prior IDs/defaults/ranges/menu access and four profiles retained.
Nine visual defaults explicitly apply in each profile; original six quality
assignments remain unchanged. Reference label updated; identifier retained.
Related saved overrides reset only via the approved migration policy. Existing
new-version preferences and all old versions remain untouched.

Actual Main QA uses final runtime source in immutable named test packs. Normal
river, underwater, waterline and controlled fixture/cloud/material scenes were
captured; accepted, limited and rejected frames are labelled in the report.
Repeated captures show reflected-foliage variation even on the same baseline;
no screenshot pixel-equivalence claim is made. Native matched probes establish
finite component equivalence within the tolerances above, not universal visuals.
Final release archive/source/installed equivalence and loaded pack are recorded
separately in outputs/Stratus-1.6.10-install.json.

Performance remains pending: no accepted focused full Reference FPS comparison.
The Mac/game was unavailable for focus. Dynamic FPS reported UNFOCUSED while
Minecraft reported LONG_AFK/cap15. Such observations cannot certify shader FPS.
GPU pass diagnostics guide optimisation only. No quality reductions were used.
Exact historical pole/leaf scenes, exhaustive presets/mods and moving-camera
coverage remain pending as described in the project queue and change log.
''')
(p/'IN-GAME-TEST.txt').write_text('''STRATUS 1.6.10 — LIVE CHECKS AND FOLLOW-UP

Run install.py with the latest actual previous release settings, then select
Stratus-1.6.10.zip. Confirm active Iris pipeline and log before judging it.
The installer preserves unrelated tuning; testing Reference should not erase
your normal saved quality preferences. Reference (Recommended) retains its ID.
Materials: film amount, sheen conditions/strength, retired darkening. Water:
vanilla texture strength. Lighting: vanilla/enhanced switch and retained tuning.

Review actual river/reflections, shallow/deep water, waterline, underwater air
exits, glass, submerged wood, particles and waterfall. Review clouds below,
within and above the layer, small spans/grazing rays, cirrus alone, motion,
sunset and native mode. Review clear/rain film, cave/local lamps/night and
native/polished sun. Reject unloaded terrain and inside-block captures. The
versioned visual report records finite checks and any remaining gaps.

To complete performance acceptance: unlock/focus the existing Main window,
use full Reference at1440x842/render12/simulation8 and matched fixed cameras,
weather clear/time6000. Record focus continuously, Dynamic FPS state and the
Minecraft inactivity limiter. Temporary activity resets may hold NONE/cap70
without modifying saved settings; stop the helper afterwards. Compare30-second
baseline/candidate samples with no concurrent native GPU test/profiler. A locked,
background-throttled or AFK-limited window is invalid even if a counter appears.
Keep the approximately60 FPS target pending until actual evidence supports it.

Restore original camera/HUD/pause/flight, weather/daytime/timers and temporary
fixture blocks after testing. Preserve all older ZIPs, preferences, mods and
worlds. Exact historical pole/leaf contexts remain separately unverified.
''')
print('Wrote 1.6.10 release documentation with explicit pending FPS limits.')

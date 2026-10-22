from pathlib import Path
import json
w=Path(__file__).parent;docs=Path('work/Custom instructions');r=json.loads(Path('outputs/Stratus-1.6.9-install.json').read_text());assert r['loaded'];assert (w/'driver-stopped.txt').exists()
entry=f'''## 22 October 2026 — Stratus 1.6.9

### At a glance

- Completed vanilla block colours, film on porous/non-porous blocks, removal of absorption/retained dampness, and a subtle adjustable animated vanilla-water texture. All 61 previous control IDs/ranges/menu access and four presets remain; 62 controls total. Retired darkening is explicitly labelled rather than silently repurposed.
- Built **[Stratus 1.6.9](../../outputs/Stratus-1.6.9.zip)**, installed, selected and actually loaded it in Main. [Release receipt](../../outputs/Stratus-1.6.9-install.json), [actual captures](../../outputs/Stratus-1.6.9-visual-checks/index.html). Latest Main overrides carried forward; camera/HUD/pause/flight restored and both temporary helpers stopped.
- Passed 768 native pairs, 795 component/12 output samples, 11 GPU relationships and ten underwater regressions, plus finite actual Main material/colour/water/menu review. Focused active-game tests at 1440×842: river **57.7 → 56.2 FPS**, forest **59.1 → 60.1 FPS**. No general speedup or sustained 60 FPS claim; **performance remains pending**.

### Staging and preserved work

User-authorised Stratus Studio `stage_run` **0d847664-366f-4d24-a8eb-e198c604b09c** had a zero-byte frozen specification delta. Current `TASK.md` and `CHANGES.md` matched the queued snapshots; no target/source gap was invented as extra work. Implemented the four visual requests from the existing five-item queue and partially addressed the performance request. [Staging evidence](../stratus-refine-169/staging.json), [reconciliation](../stratus-refine-169/reconciliation.json).

Editable source was already the newer **1.6.9-water-pole-test** candidate, not 1.6.8. Its `environment.glsl` filter and test ZIP were preserved byte-for-byte. This pass reviewed finite river/downward/underwater views but does not independently certify the original reported pole view or call that historical issue solved.

### Behaviour and controls

**Vanilla block colours:** `REALISTIC_LIGHTING` source default changes from 1 to 0. The existing vanilla path restores game vertex face/AO/lightmap colour and bypasses artistic exposure, white balance, saturation, bloom and highlight compression. Existing saved `1` values still select enhanced lighting and retain all related controls; no artist setting was erased. Main already selected `0`. Actual matched dry-iron front/top crops differ from shaders-disabled Minecraft by at most one 8-bit RGB code; granite/grass are affected slightly by retained atmosphere, so the whole frame is not claimed vanilla. [Fixture comparison](../stratus-refine-169/vanilla-fixture-comparison.json).

**Film and dampness removal:** removed pore-absorption attenuation and sheltered retained moisture. `wetSurfaceResponse` now evaluates exposed film on porous and non-porous blocks, including metal and glazed materials, under either lighting mode. All-weather/rain-only, exposure, world-face drainage, material roughness and independent amount/strength remain. Zero amount or sheen is an exact dry bypass and sealed caves remain dry. A white surface can reflect a darker sky at grazing angles; that optional view-dependent reflection is separate from the removed diffuse absorption. Actual matched final-code iron/glazed/granite captures were inspected; [finite pixel comparison](../stratus-refine-169/final-film-comparison.json).

`SURFACE_DAMPNESS` keeps its identifier/full range and film scaling, now labelled **Surface film amount**; absorption/retention is deliberately removed. `WET_DARKENING` keeps its ID/range/menu/saved values as **Retired darkening**, an intentional no-op explained by its tooltip. This is the compatibility exception required by the user's explicit effect removal. [Control and preset audit](../stratus-refine-169/option-audit.json).

**Native water texture:** new `WATER_TEXTURE` slider under Water, strength default 0.15, zero/off through 1.00. Reuses the already-fetched active still/flow atlas texel and carries luminance in unused water metadata red. The lake compose modulates transmitted radiance only; reflection, opacity, biome tint, physical water path and refraction stay independent. No extra texture read or Mojang asset distribution. Off/strong actual Main captures show the pattern/tint response; final river/underwater/waterline captures preserve the intended water appearance.

### Performance and validity

Skip `composite` when scenery reflection is disabled (`REFLECTION_MODE=0`): its readers are already compiled out. Move interface normal/depth reads after non-water/underwater rejection in lake compose. No buffer resolution, sample budget, traversal cap, draw distance, preset or user quality selection was lowered. Actual Iris confirms `{{composite=>false, composite5=>false, composite6=>false}}` in the selected vanilla/sky-only mode. These structural skips do not prove a whole-game speedup.

Initial 854×480 unfocused samples were rejected. After the user focused the normal 1440×842 window, static samples stayed near 29 FPS. Inspection of the installed Minecraft code and live limiter identified **SHORT_AFK / cap30** despite focus. A temporary guarded API helper reset Minecraft's activity timestamp and Dynamic FPS activity every five seconds, only while focus=1; no saved setting was changed. The monitor confirmed **NONE / cap70**, Dynamic FPS **FOCUSED**, world time6000, rain0 and fixed cameras. Its original SHORT_AFK→NONE transition and all observations are retained. Both helpers were stopped after testing. [Activity monitor](../stratus-refine-169/activity-monitor.txt), [stopped helper](../stratus-refine-169/activity-stopped.txt).

Valid 30-second active-game samples on Apple M1 / Minecraft1.21.11 / Iris1.10.8 / Sodium0.8.14, framebuffer1440×842, render distance12, simulation distance8, unchanged source/saved quality, saved VSync=true/maxFPS70, Dynamic FPS enabled:

| Scene | Baseline mean FPS | 1.6.9 mean FPS | New median / p95 / p99 frame ms |
| --- | ---: | ---: | --- |
| River, original camera | 57.6906 | 56.1894 | 16.7813 / 24.6077 / 33.6671 |
| Forest/river horizon, repeated after focus loss | 59.1302 | 60.0723 | 16.1523 / 20.7933 / 27.2975 |

Baseline is the preserved water-pole test using current saved Main settings; updated sample uses byte-identical final runtime source in immutable v2 QA. Both include actual selected Fast-related options, new film amount0.15 and texture0.15. Each accepted sample had zero unfocused polls and unchanged framebuffer. The first forest active sample lost focus and its baseline started unfocused; neither is accepted. Earlier focused samples were AFK-capped and are excluded. Dynamic FPS's own `enableVsync` method reported false while the saved game option stayed true; record that runtime distinction when reproducing. No other native GPU workload ran during accepted samples.

The scene-dependent means do not establish a consistent improvement; the river falls short of 60. Performance stays in Pending changes. The next performance pass should profile the normal-world river with activity/focus/quality fixed and repeat matched samples before accepting further shader changes. [Complete benchmark summary and raw-file references](../stratus-refine-169/performance-summary.json).

### Verification and delivery

Seven runtime files changed relative to the preserved candidate: `core/options.glsl`, `core/diffuse.glsl`, `core/moisture.glsl`, `core/raster.frag.glsl`, `core/lake.frag.glsl`, `shaders.properties`, `lang/en_us.lang`. [Source diff](../stratus-refine-169/changes.diff), [change inventory](../stratus-refine-169/source-changes.json). The existing pole filter and all unrelated runtime assets are retained.

- Native Apple M1 OpenGL compatibility-shim compile/link: **768 pairs / eight variants / zero failures**, separate from actual Iris load. [Log](../stratus-refine-169/compile.log).
- Actual GLSL probes: **795 component /12 output samples,11 relationships,zero failures/API errors**. Includes absorption-independent/nonporous film, dry/cave/rain-only bypass, vanilla diffuse and final display transfer. [Checks](../stratus-refine-169/gpu-checks.json).
- Ten actual full-resolution underwater resolve cases pass: submerged/air receivers, clear-sky exits, glass, additive particles and vertical exits. [Results](../stratus-refine-169/water-regression.json).
- Actual Main scenes: dry vanilla reference; porous/nonporous dry/film and grazing views; native-water texture off/strong; river, underwater/waterline; Materials/Water menus and exact released-ZIP captures. One initially unloaded nonporous frame is rejected and preserved. Capture labels distinguish preliminary, final-code, baseline and vanilla frames. Animation continues; no universal pixel-equivalence claim.
- Package **243 entries /235 runtime assets /{r['bytes']:,} bytes**, ZIP CRC/source equivalence and installed hash verified. SHA-256 `{r['sha256']}`. Final runtime source exactly matches the tested v2 QA archive; release metadata is new. Latest current saved Main values are copied only because the new release settings did not exist. Iris may omit an explicit saved value equal to its new default; effective values, not comment timestamps, are compared.
- Restored original camera166.190733,65.928693,32.553558 / yaw108.45755 / pitch38.829258, HUD shown, pause-on-focus-loss true and flying true. Temporary QA archives removed only when their generated content/settings still match; workspace evidence retained. Minecraft remains open on the installed release.

`TASK.md` reconciles the approved completed colour/film/water design and exact limits; four verified requests moved out of Pending changes. No conflict against the frozen snapshots was found. The 60 FPS performance request remains pending. Cave/night/rain/preset/mod/motion coverage, the original distant-leaf scene and exact original pole-view acceptance remain incomplete; finite checks do not certify those cases.

'''
p=docs/'CHANGE-LOG.md';s=p.read_text();assert '## 22 October 2026 — Stratus 1.6.9\n' not in s;p.write_text(s.replace('# Stratus change and output log\n\n','# Stratus change and output log\n\n'+entry,1));print('Recorded completed visual work and explicit pending performance with actual evidence.')

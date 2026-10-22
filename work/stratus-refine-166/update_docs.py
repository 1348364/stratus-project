from pathlib import Path
import json,re
folder=Path('work/Custom instructions');receipt=json.loads(Path('outputs/Stratus-1.6.6-install.json').read_text());sha=receipt['sha256'];size=f"{receipt['bytes']:,}"
entry=f'''## 20 October 2026 — Stratus 1.6.6

Status: Three requested changes implemented; technical checks, packaging and installation passed. **Main loading/visual acceptance, confirmation against the reported foliage scene, visual equivalence and focused performance remain pending.**

### Changes and reasons

- **Keep vanilla face shading and mix in realistic light.** `core/diffuse.glsl` now uses 65% vanilla axis weights plus 35% realistic sky/ground/solar response at full skylight. Exposure still gates that contribution. Existing strength/blend controls, world-space orientation, rain/night/cave behaviour and contrast bounds remain. The mix is before the existing contrast control; a saved strength of 2.00 remains supported. The English label is now “Blended face contrast”.
- **Polished blocky vanilla sun.** `core/ceiling.glsl` samples the running game's `minecraft:textures/environment/celestial/sun.png` with explicit texel sampling, HDR warmth and the existing broad haze glow. The round procedural solar core/aureole is removed. Sky and environment reflections share this square sun. `SUN_STYLE=0` is labelled “Polished vanilla sun”; `SUN_STYLE=1` still uses native textured sun/moon rendering. The default moon behaviour is preserved. The actual 1.21.11 texture was used as test input; no Mojang image is bundled. No active Main sun-texture override was found, though future resource packs may change the sampled image.
- **Repair a fog depth-miss mechanism that causes dark foliage dots.** A thin cutout may be absent from all four reduced-resolution depth samples; 1.6.5 returned zero fog in that case. `atmosphere-resolve.frag.glsl` now evaluates rejected pixels at their exact full-resolution depth and smoothly blends by confidence. `completeAtmosphereSegment` in `volume.glsl` shares primary-pass border/status handling. The fallback uses the **same selected full atmosphere quality**, including cloud shading, rather than lowering samples. Valid cached samples and underwater behaviour are preserved in controlled tests. The actual reported Main dots remain to be checked; unrelated texture/mipmap/driver causes have not been ruled out.

Seven runtime assets changed: `core/diffuse.glsl`, `core/ceiling.glsl`, `core/volume.glsl`, `core/atmosphere.frag.glsl`, `core/atmosphere-resolve.frag.glsl`, `shaders.properties`, and `lang/en_us.lang`. The other **228 runtime assets** are byte-identical to the 1.6.5 source. Water, matte moisture and cloud-density implementation remain unchanged. [Source diff](../stratus-refine-166/changes.diff), [change inventory](../stratus-refine-166/source-changes.json).

### Settings and quality preservation

Before final packaging, compared old/new inventories: **all 53 option IDs, defaults and allowed values are identical**; menus, slider lists and all four presets are identical; every language key remains. **All 10 saved Main overrides are valid and copied unchanged** to the new pack settings. Nothing was removed, hidden or narrowed. Tooltips and two displayed labels describe the requested shading/sun changes. There is no settings-file migration; the deliberate `SUN_STYLE=0` visual redesign is the requested square-sun change. [Full option/menu/label comparison](../stratus-refine-166/option-inventory.json).

No resolution, draw distance, effect, control, quality preset or sampling budget was reduced. There is no extra render pass. Full atmosphere integration is restricted to low-confidence depth pixels. This bounds unnecessary work but is **not a measured speed gain**: fallback-heavy foliage views can cost more than 1.6.5. Maximising performance at unchanged intended quality requires a matched live bottleneck measurement; no “100% visually equivalent” or speed claim is made without that evidence.

### Output

- Build/source: **Stratus 1.6.6 candidate**, [editable source](../../outputs/Stratus), [ZIP](../../outputs/Stratus-1.6.6.zip), **243 files / {size} bytes**.
- SHA-256: `{sha}`.
- Installed alongside 1.6.5 at `/Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)/shaderpacks/Stratus-1.6.6.zip`; installed bytes match. Prior preferences copied only if the new settings file was absent. [Receipt](../../outputs/Stratus-1.6.6-install.json).
- **Main still selects 1.6.5.** Its log confirms `Using shaderpack: Stratus-1.6.5.zip`; this supersedes the earlier 1.6.5 entry's at-delivery “not selected” state. [Baseline runtime evidence](../stratus-refine-166/baseline-runtime.txt). No world, mod or resource-pack changes; existing game left open.

### Completed checks for 1.6.6

- **768 native OpenGL compile/link pairs, eight variants, zero failures** across defaults, vanilla mode, four presets, option extrema and all dimensions. [Compile log](../stratus-refine-166/compile.log). Native compatibility shims are not live Iris loading proof.
- **27 GPU relationships pass**, zero API errors: **4 candidate sun renders, 11 candidate fog cases and 216 candidate face samples**. Separate references: 1 baseline sun render, 11 baseline fog cases and 72 baseline/pure-vanilla face samples. Every sampled sun RGB/alpha texel matches the current vanilla image plus documented HDR tint. The face mix matches 65/35; direction/rain/night/caves/camera/bypasses/other dimensions checked. [Assertions](../stratus-refine-166/gpu-checks.json), [raw data](../stratus-refine-166/gpu.json).
- The controlled missed-depth case reproduces 1.6.5's dark RGB `(0.010, 0.015, 0.010)` and produces fogged RGB approximately `(0.170, 0.189, 0.209)` after repair. Matched-depth, near foreground and underwater results remain unchanged; confidence transition and chunk border checks pass. This validates the mechanism, not yet the user's actual scene.
- **10 water-resolve GPU regressions pass**, zero failures/errors. [Water evidence](../stratus-refine-166/water-regression.json).
- **53 reachable controls labelled; all 235 runtime assets match source in the ZIP; archive integrity and installed bytes verified.** Cast shadows remain off. [Audit](../stratus-refine-166/source-audit.json).

### Visual observations and performance

**Actual 1.6.6 in-game observations: none; pending.** Native desktop inventory still does not expose the running Java/Minecraft window, so the candidate could not be selected or driven for matching captures. Confirmed 1.6.5 loading is baseline evidence only. No competing world session was launched.

Inspected two labelled **offline native-GLSL preview sheets**: [sun comparison](../stratus-refine-166/offline-sun-preview.jpg) shows the old round core and new square texture; [fog reproduction](../stratus-refine-166/offline-fog-preview.jpg) shows dark depth rejection versus corrected scattering. These are **not Minecraft screenshots**. Real sky composition, bloom, motion, the original leaf scene, appearance in different weather and visual equivalence remain pending.

**Performance: not measured.** No focused FPS/frame times, maximum-performance or speedup claim. Keep quality fixed when profiling. The added full-quality fallback is the main new cost to assess in dense forest/fog; cache-matched pixels keep the existing reconstruction path.

### Next checks

1. Select **Stratus-1.6.6.zip** in Main/Iris, verify its name and custom-texture/shader loading in `latest.log`.
2. Compare matched normal-world faces and sun at noon/sunset/rain/night, caves/local lights, native sun mode and controls. Check the square sun through clouds and in water reflection.
3. Return to the actual distant-leaf dot scene, move slowly, compare tiny leaves/sky holes/fences/chunk edges, and recheck underwater/glass/particles/cloud traversal.
4. Benchmark focused matched terrain, dense forest/fog and river/cloud views with resolution, distances, VSync/cap, Dynamic FPS and competing processes recorded. Optimise only measured bottlenecks without reducing intended quality; verify resulting visual equivalence.

Follow [IN-GAME-TEST.txt](../../outputs/Stratus/IN-GAME-TEST.txt). [Current shader specification](SHADER-SPEC.md). Runtime texture binding follows the [Iris custom-texture documentation](https://shaders.properties/current/reference/buffers/custom_textures/).

'''
f=folder/'CHANGE-LOG.md';s=f.read_text();assert s.startswith('# Stratus change and output log\n');s=s.replace('# Stratus change and output log\n\n','# Stratus change and output log\n\n'+entry,1);f.write_text(s)
f=folder/'SHADER-SPEC.md';s=f.read_text()
s=re.sub(r'^Status:.*$', 'Status: Updated for Stratus 1.6.6 on 20 October 2026. Native/GPU checks, packaging and installation passed; Main loading, actual visual acceptance, reported foliage-dot confirmation and focused performance remain pending. No measured speedup or full visual-equivalence claim. See `CHANGE-LOG.md` for evidence.',s,count=1,flags=re.M)
s=re.sub(r'^- Current packaged candidate:.*$',f'- Current packaged candidate: `outputs/Stratus-1.6.6.zip` (243 files; 235 runtime assets). SHA-256 `{sha}`. Prior 1.6.5/1.6.4 archives remain preserved.',s,flags=re.M)
s=s.replace('native checks run for 1.6.5','native checks run for 1.6.6').replace('`outputs/Stratus-1.6.5-install.json`','`outputs/Stratus-1.6.6-install.json`').replace('The ZIP is installed in Main beside 1.6.4 with copied preferences; Main still selects 1.6.4.','The ZIP is installed in Main beside 1.6.5 with copied preferences; Main still selects 1.6.5 (confirmed in the runtime log).')
s=re.sub(r'^- Preserve vanilla texture detail and block geometry\. `formIrradiance`.*$', '- Preserve vanilla texture detail and block geometry. At full sky exposure, `formIrradiance` mixes 65% vanilla axis weights with 35% realistic sky/ground/sun-facing response, before the existing contrast control. Exposure gates the realistic share; fixed vanilla weights remain the sheltered/other-dimension baseline. `FACE_SHADING` default 1.00 and `FACE_BLEND` default 1.00 multiply contrast, bounded to 0.18–1.18; either zero bypasses it. Existing AO and separate `GROUND_WARMTH` default 0.45 remain. This is broad diffuse lighting without cast-shadow visibility. Caves retain local mapped light and emission handling.',s,flags=re.M)
s=s.replace('- Sun and moon have Stratus and vanilla modes. The Stratus sun is softened by haze/overcast; the vanilla option keeps the original textures.', '- `SUN_STYLE=0` now draws a polished blocky sun using the current Minecraft 1.21.11 `textures/environment/celestial/sun.png` through `customTexture.vanillaSun`. `polishedVanillaSun` projects and fetches exact texels, adds HDR warmth, and shares the existing broad haze glow with the reflection environment. There is no round procedural core/aureole. `SUN_VISIBILITY` controls the textured core. Native celestial draws stay disabled in this mode, preserving the existing default moon behaviour. `SUN_STYLE=1` retains native textured sun/moon rendering without a duplicate procedural disk. Resource-pack replacements are respected; no Mojang texture is redistributed. Native binding/orientation/composition in Main are pending live verification.')
needle='`shaders/shaders.properties` defines Iris rendering behaviour'
s=s.replace(needle,'The atmosphere resolve reconstructs cached fog with depth weights. If total depth confidence is below 0.12, non-underwater pixels use an exact-depth `completeAtmosphereSegment(..., true)` evaluation with the same selected full quality; `smoothstep(0.02, 0.12, confidence)` blends back to the cache. The shared helper in `volume.glsl` includes border fog and status effects for both paths. This repairs the zero-fog fallback that can leave distant thin cutouts dark. It adds selective work, not an extra pass or quality reduction. Actual reported foliage and performance remain pending.\n\n'+needle)
a=s.index('- The four cloud/lighting changes are implemented in 1.6.5.');b=s.index('\n## Rebuild handoff rule',a)
s=s[:a]+'''- 1.6.6 adds the vanilla-dominant lighting blend, polished square sun and exact-depth fog fallback. Completed evidence: 768 native links; 27 GPU relationships across 4 candidate sun renders, 11 fog cases and 216 face samples; 10 water regressions; 53 labelled controls; ZIP/source and installed-byte match. Baseline/reference renders are counted separately. Two inspected offline previews are not Minecraft screenshots.
- The controlled depth-rejection mechanism is repaired; the actual reported distant-leaf scene could also contain texture/mipmap/driver artifacts and is not yet certified fixed.
- Main was confirmed loading 1.6.5. 1.6.6 and copied preferences are installed, but the desktop tool cannot select its normal Java window for live comparison. No focused FPS/frame time, maximum-speed or full visual-equivalence claim.
- Performance/quality: full settings, presets, resolutions and sample budgets remain; the fallback deliberately uses full selected quality. Dense foliage/fog may increase integration cost. Profile matched representative scenes before optimising, preserve 100% of intended features/quality, and label unchanged visuals or speed gains unverified until measured/reviewed.
- All 53 option IDs/defaults/allowed values, menus/sliders/presets and language keys match 1.6.5; 10 saved Main overrides remain valid. “Blended face contrast” and “Polished vanilla sun” labels explain the requested redesign. No settings-file migration. Inventory evidence: `work/stratus-refine-166/option-inventory.json`.
- Next: select 1.6.6 in Iris, verify runtime binding, compare the original foliage scene, terrain/sun/weather/motion/native modes and water/transparency; then benchmark focused matched forest, terrain and river/cloud views. Follow `outputs/Stratus/IN-GAME-TEST.txt`.
''' +s[b:]
f.write_text(s)
f=folder/'TASK.md';s=f.read_text();s=re.sub(r'^Status:.*$', 'Status: Implemented as Stratus 1.6.6; technical checks, packaging and installation passed. Main loading/visual acceptance, original foliage-scene confirmation and focused performance remain pending.',s,count=1,flags=re.M)
a=s.index('## Progress and evidence');s=s[:a]+'''## Progress and evidence

- Changes: All three requested changes implemented: 65% vanilla / 35% realistic face mix at full skylight; current Minecraft square sun texture with HDR warmth/haze; exact-depth full-quality fog fallback for rejected thin cutouts. [Change log](CHANGE-LOG.md), [source diff](../stratus-refine-166/changes.diff).
- Output: [Stratus-1.6.6.zip](../../outputs/Stratus-1.6.6.zip), installed alongside 1.6.5 with unchanged copied preferences. [Install receipt](../../outputs/Stratus-1.6.6-install.json). Main is confirmed using 1.6.5; 1.6.6 loading is pending.
- Technical checks: 768 native compile/link pairs, zero failures; 27 GPU relationships across 4 candidate sun renders, 11 fog cases, 216 face samples and separate baseline/reference comparisons; 10 water-resolve regressions pass. [Compile](../stratus-refine-166/compile.log), [GPU](../stratus-refine-166/gpu-checks.json), [water](../stratus-refine-166/water-regression.json).
- Settings: Before final packaging, verified all 53 option IDs/defaults/allowed values, menus, sliders, presets and language keys retained; 10 saved Main overrides valid. Only requested-effect labels/tooltips changed. [Inventory](../stratus-refine-166/option-inventory.json). All 235 runtime assets match packaged source; [audit](../stratus-refine-166/source-audit.json).
- In-game visual review: Pending. Desktop inventory cannot select the running normal Java window. Offline [sun](../stratus-refine-166/offline-sun-preview.jpg) and [fog](../stratus-refine-166/offline-fog-preview.jpg) comparisons were inspected; they are not Minecraft screenshots. The black-dot depth-miss mechanism is reproduced/repaired technically, but the actual reported scene remains unverified.
- Performance and equivalence: Pending. No measured speedup, FPS or full visual-equivalence claim. No resolution/sampling/distance/effect/control reduction; fallback uses full selected quality and can add cost to dense foliage scenes. Focused matched bottleneck profiling is still required.
- Documentation: [CHANGE-LOG.md](CHANGE-LOG.md) and [SHADER-SPEC.md](SHADER-SPEC.md) updated for 1.6.6, evidence and known limits.
- Remaining issues: Select 1.6.6 in Main, confirm shader/resource loading, inspect the reported distant-foliage scene and terrain/sun/cloud/water/transparency regressions, then measure focused matched representative scenes. Follow [IN-GAME-TEST.txt](../../outputs/Stratus/IN-GAME-TEST.txt).
''';f.write_text(s)
print('Updated current task, appended 1.6.6 change/output entry and revised shader specification; preserved prior history and standing requirements.')

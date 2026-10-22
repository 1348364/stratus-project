from pathlib import Path
import hashlib, json, html, shutil

root = Path(__file__).resolve().parents[2]
docs = root / 'work/Custom instructions'
work = Path(__file__).parent
task = docs / 'TASK.md'
baseline = docs / 'SPEC-BASELINE.md'
expected = 'cb83e2d880001bb6e6d9b93882814e1f2d1e858624d7c3b2195f953cbbbd935c'
original = task.read_bytes()
assert hashlib.sha256(original).hexdigest() == expected, 'New user edits: reconcile separately'
assert baseline.read_bytes() == original, 'Unimplemented spec delta: preserve it'
historical = {n: (docs/n).read_bytes() for n in ['SHADER-SPEC.md', 'TASK-previous-brief.md']}
spec = original.decode()

def replace(old, new):
    global spec
    assert spec.count(old) == 1, old
    spec = spec.replace(old, new)

replace('Snapshot status: built from the 1.6.6 release specification and the current editable source on 21 October 2026. The source is being changed for the prior brief, so newly added controls and the current values below are **draft implementation state**, not a released or visually accepted build. The previous brief is preserved in `TASK-previous-brief.md`. See `CHANGE-LOG.md` for verified release history.',
        'Snapshot status: reconciled with **Stratus 1.6.7** on 21 October 2026. The five requests in `TASK-previous-brief.md` are implemented, technically checked, packaged, installed and loaded in Main, with finite actual Minecraft visual comparisons completed. Focused FPS and exhaustive scene coverage remain pending. This file and `SPEC-BASELINE.md` record the completed target; the prior brief remains preserved verbatim. See `CHANGE-LOG.md` for evidence and limits.')
replace('- Last packaged candidate at this snapshot: `outputs/Stratus-1.6.6.zip` (243 files; 235 runtime assets). SHA-256 `96378ece4c83993306de014a3423eb93a16d54b15813e218a52c75ffc8d5a555`. The editable source may be ahead of this ZIP while the previous brief is in progress.',
        '- Current release: `outputs/Stratus-1.6.7.zip` (243 files; 235 runtime assets; 7,771,716 bytes). SHA-256 `a273a3591d126f1406c9413f7e46684c095e98413998d393375925dce27f56eb`. Packaged bytes match editable source and the installed archive.')
replace('- Target carried forward from 1.6.4; native checks run for 1.6.6, current live compatibility pending: Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1 macOS, GLSL 330 / OpenGL 4.1.',
        '- Verified native and current Main runtime: Minecraft Java 1.21.11, Iris 1.10.8, Sodium 0.8.14, Apple M1 macOS, GLSL 330 / OpenGL 4.1. This is finite compatibility evidence for the existing profile, not exhaustive mod certification.')
replace('- `outputs/Stratus/README.txt`, `VALIDATION.txt`, `CHECKS.json`, `IN-GAME-TEST.txt`, `SOURCE-MANIFEST.json` and `outputs/Stratus-1.6.6-install.json` provide release evidence and inventory. At this snapshot, Main\'s Iris configuration selects 1.6.6; verify actual loading from the live log before judging visuals. Installation or configuration alone is not loading proof.',
        '- `outputs/Stratus/README.txt`, `VALIDATION.txt`, `CHECKS.json`, `IN-GAME-TEST.txt`, `SOURCE-MANIFEST.json` and `outputs/Stratus-1.6.7-install.json` provide release evidence and inventory. Main selects and has actually loaded 1.6.7, confirmed by the live Iris log and parsed current-pack API. Installation or configuration alone is not loading proof.')
replace('This is broad diffuse lighting without cast-shadow visibility.',
        'Both component controls default to 1.00 and reproduce the former 65/35 combination; zero removes only that component. This is broad diffuse lighting without cast-shadow visibility.')
replace('Verify runtime binding and appearance in Main.',
        'Main comparisons verified the runtime binding, square core and stronger local glow; core/halo/radius defaults are 4.50/2.00/1.50. Global bloom is unchanged. Core 2.80 and halo 0 retain the earlier sun contribution.')
replace('Verify the effect in the actual wet scene and document any compatibility migration.',
        'Actual Main off/default/maximum rain comparisons show a subtle grazing sheen; clear materials and tested nonporous metal remain matte. Deliberate semantic extension: saved `WET_SHEEN` values still control sheltered retention and now also scale a rain-only exposed absorbent film. The film uses approximate sky reflection and solar highlights, without scenery tracing or a new pass. Porosity is heuristic and rain response is instantaneous rather than accumulated.')
replace('`WATER_EXTINCTION` (0.90), `WATER_TURBIDITY` (1.00)', '`WATER_EXTINCTION` (3.00), `WATER_TURBIDITY` (6.00)')
replace('`REFLECTION_MODE` (1)', '`REFLECTION_MODE` (2)')
replace('Verify actual sky composition and visibility in Main; offline positive-density tests alone are insufficient.',
        'Main isolation captures show the brighter broad high veil with lower clouds disabled; zero removes it. Optical density is 0.045 times `CIRRUS_DENSITY` (default 1.00), increased from 0.016; daylight colour is brighter. Existing amount 0.65 and altitude 360 blocks are unchanged. This remains a wispy broad veil with finite slab/range limits, rather than dense storm clouds.')
replace('exact Story Mode style and live appearance remain unverified.', 'exact Story Mode style and exhaustive live motion/height coverage remain unverified. Lower-cloud forms were inspected in the normal-world sky and river captures; their shape code is unchanged in 1.6.7.')
replace('All current presets disable cast shadows and keep solids matte.', 'All current presets disable cast shadows. Dry and non-absorbing solids remain matte; exposed absorbent materials can show adjustable rain film.')
replace('This inventory was transcribed from `outputs/Stratus/shaders/core/options.glsl` on 21 October 2026 while the previous brief was still in progress.',
        'This inventory matches the completed 1.6.7 `outputs/Stratus/shaders/core/options.glsl` on 21 October 2026: all 53 previous controls retained and six added, for 59 total. The seven preferred Main values are now source defaults; all four preset definitions, including Reference, remain unchanged and selectable. Parsed Main state reports Custom with zero options changed by the user.')
replace('- The packaged 1.6.6 baseline added a vanilla-dominant lighting blend, polished square sun and exact-depth fog fallback. Its completed native/GPU evidence is in `CHANGE-LOG.md`. The newer controls listed above are in editable source while the previous brief is in progress; they are not certified by 1.6.6\'s results.',
        '- The 1.6.6 baseline added the vanilla-dominant blend, square sun and exact-depth fog fallback. Release 1.6.7 adds preferred defaults, local sun controls, independent face controls, visible high cirrus and restrained rain film. Its own 768 native links, 539 GPU samples / 21 relationships and 10 water-resolve cases pass; it does not rely on earlier release tests.')
replace('- Main\'s Iris configuration selects 1.6.6 at this snapshot. Confirm actual loading from the current log/game before making visual claims. No focused FPS/frame time, maximum-speed or full visual-equivalence claim is implied by this document.',
        '- Main actually loaded 1.6.7 and finite visual comparisons are recorded in `outputs/Stratus-1.6.7-visual-checks/index.html`. The recorded framebuffer is 1440×842, focus is false, and Dynamic FPS is enabled. No valid focused FPS/frame time, maximum-speed or exhaustive visual-equivalence claim is implied. Full night/sheltered-wet, all-preset motion and exhaustive mod coverage remain pending.')
replace('- The 1.6.6 release retained the previous settings inventory; the newer source adds separate face, sun and cirrus controls. Keep all useful options, allowed values, menus and saved overrides across future releases. Verify the new inventory when the in-progress build is packaged.',
        '- The 1.6.7 inventory audit confirms 59 reachable and labelled controls, unchanged prior allowed values, menu access, slider lists and all four presets. The original 1.6.6 saved settings bytes are preserved. Keep these controls and saved-value compatibility across future releases; document deliberate behaviour extensions such as the rain-film use of `WET_SHEEN`.')
progress = '''## Completed implementation and evidence — 21 October 2026

- Implemented all five requests from the archived brief; built, installed, selected and actually loaded **1.6.7** in normal Modrinth Main / Stratus Terrain Lab. [Release and detailed evidence](CHANGE-LOG.md), [install receipt](../../outputs/Stratus-1.6.7-install.json), [visual report](../../outputs/Stratus-1.6.7-visual-checks/index.html).
- Snapshotted Main's seven saved overrides before editing and adopted them as source defaults; the old preference file remains byte-identical. Reference remains available. [Snapshot](../stratus-refine-167/settings-snapshot.json), [option audit](../stratus-refine-167/option-inventory.json), [actual runtime settings](../stratus-refine-167/final-runtime-state.txt).
- Passed 768 native compile/link pairs, 539 targeted GPU samples / 21 relationships and 10 water-resolve regressions. Actual Main comparisons cover polished/native sun, cirrus-only/off, independent face components, rain strengths/material gating, clear materials, river/underwater and settings menus. Original captures include labelled preliminary and rejected frames.
- Restored player camera and HUD/pause/menu state, stopped the temporary test driver and removed unchanged test packs/settings from Main. The released ZIP remains selected. Focused performance and the remaining coverage limits above are explicitly pending.
- Reconciled this specification and its baseline only after completed implementation; no newer user delta was present. The historical `SHADER-SPEC.md` and archived brief remain untouched. Future work starts only from an explicit request to apply meaningful edits.

'''
replace('## Rebuild handoff rule\n', progress + '## Rebuild handoff rule\n')

# Optimistic concurrency check: do not overwrite a newer edit from the other chat.
assert task.read_bytes() == original and baseline.read_bytes() == original
task.write_text(spec)
baseline.write_text(spec)
for name, data in historical.items():
    assert (docs/name).read_bytes() == data

report = root/'outputs/Stratus-1.6.7-visual-checks'
rows = json.loads((report/'captures.json').read_text())
for shot in sorted((work/'screenshots').glob('s167-release-*.png')):
    shutil.copy2(shot, report/'screenshots'/shot.name)
    status = ('Final release: restoration capture; not visual acceptance evidence'
              if 'restored-position' in shot.name else 'Final released ZIP loaded in Main; reviewed actual capture')
    rows = [r for r in rows if r['file'] != shot.name]
    rows.append({'file': shot.name, 'status': status, 'sha256': hashlib.sha256(shot.read_bytes()).hexdigest()})
(report/'captures.json').write_text(json.dumps(rows, indent=2)+'\n')
page = (report/'index.html').read_text().split('<main>')[0]
body = ''.join('<figure><figcaption>'+html.escape(r['file'])+'<br><small>'+html.escape(r['status'])+'</small></figcaption><a href="screenshots/'+r['file']+'"><img loading="lazy" src="screenshots/'+r['file']+'"></a></figure>' for r in rows)
(report/'index.html').write_text(page+'<main>'+body+'</main>')
print(f'Reconciled spec/baseline; historical files preserved; gallery contains {len(rows)} original captures.')

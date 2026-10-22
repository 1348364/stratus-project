from pathlib import Path
import json,hashlib,shutil,html
root=Path(__file__).resolve().parents[2];src=root/'outputs/Stratus';qa=root/'work/stratus-main-qa';w=root/'work/stratus-transparent-blocks';report=root/'outputs/Stratus-1.5.3-visual-checks'
log=(qa/'minecraft-main-153b.log').read_text(errors='replace')
assert 'PACK Stratus-1.5.3.zip' in log and (qa/'qa-complete.txt').read_text().strip()=='v153-release-verified'
assert 'GRACEFUL_QUIT' in log and 'All dimensions are saved' in log
selected=log[log.index('PACK Stratus-1.5.3.zip'):]
assert 'Failed to load the shaderpack' not in selected and '[STRATUS_QA] ERROR' not in selected
names=['matched-before-glass','matched-before-glass-underwater','matched-after-glass','matched-after-glass-underwater','matched-before-river','matched-before-underwater','release-final-river','release-final-underwater','release-final-glass','release-final-ice','release-final-waterfall']
report.mkdir(exist_ok=True)
for n in names:
 f=qa/'screenshots'/f'v153-{n}.png';assert f.is_file(),f;shutil.copy2(f,report/f.name)
c=json.loads((src/'CHECKS.json').read_text());c['status']='release selected in Main; inspected glass/water comparisons; clean FPS pending'
c['runtime'].update(release_selected=True,shader_specific_errors_after_release_selection=0,test_client_closed_normally=True,test_world_saved=True)
c['inspection']={'captures':names,'glass':'Matching above-water and submerged cameras compare 1.5.2 with the 1.5.3 candidate; final release smoke views inspect glass, panes and ice.','river':'Generated forest river, above/below water; previous plain-blue reflection fallback remains.','release-final-waterfall':'Thin falling water over the fixture tower, with unchanged v1.3.1 refraction.'}
c['capture_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in report.glob('v153-*.png')}
(src/'CHECKS.json').write_text(json.dumps(c,indent=2)+'\n')
for name in ['VALIDATION.txt','IN-GAME-TEST.txt']:
 p=src/name;s=p.read_text().replace('Final release-name smoke checks are recorded in CHECKS.json.','Final release-name checks passed for glass, glass panes and ice. The test\nclient quit normally and all world dimensions were saved; see CHECKS.json.')
 p.write_text(s)
(report/'results.json').write_text(json.dumps(c,indent=2)+'\n')
fig=lambda n,label:f'<figure><figcaption>{html.escape(label)}</figcaption><a href="v153-{n}.png"><img src="v153-{n}.png" alt="{html.escape(label)}"></a></figure>'
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.5.3 — transparency checks</title><style>body{font:16px/1.55 system-ui;background:#111a20;color:#e8f0f3;margin:0 auto;padding:32px;max-width:1400px}h1,h2{line-height:1.2}p{max-width:85ch}a{color:#9cd9ff}section{margin:36px 0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}figcaption{font-weight:650;margin:12px 0}img{display:block;width:100%;border-radius:8px}code{color:#b6e4dc}@media(max-width:800px){.pair{grid-template-columns:1fr}}</style><h1>Stratus 1.5.3</h1><p>Transparent-block colour correction and falling-water transparency. Tests ran in <strong>Main / Stratus Terrain Lab</strong>, Creative, in a normal generated world.</p><p><a href="../Stratus-1.5.3.zip">Installable ZIP</a> · <a href="results.json">Exact validation scope</a></p><p>768 native compile/link checks, 65 GPU cases, and six actual framebuffer alpha-blend checks passed. The final release loaded in Iris and the test client saved and quit normally. No clean FPS claim is made.</p><section><h2>Glass over water</h2><p>Matching cameras and current settings (extinction 3.0, turbidity 6.0): the earlier water pass produced cyan/dark patches behind stained glass. The new pass preserves the glass tint and its background transmission.</p><div class="pair">'''
page+=fig('matched-before-glass','Before — Stratus 1.5.2')+fig('matched-after-glass','After — Stratus 1.5.3 candidate')+'</div></section><section><h2>Submerged glass</h2><p>Matching underwater cameras and current settings. Water absorption remains active; the signed colour-difference overlay has been removed.</p><div class="pair">'
page+=fig('matched-before-glass-underwater','Before — Stratus 1.5.2')+fig('matched-after-glass-underwater','After — Stratus 1.5.3 candidate')+'</div></section><section><h2>Final release checks</h2><div class="pair">'
page+=fig('release-final-glass','Clear, red, blue and lime glass')+fig('matched-after-glass','Glass panes and ice added to the comparison')+fig('release-final-ice','Ice close-up')+fig('release-final-waterfall','Falling water over the fixture tower')+'</div></section><section><h2>Generated river</h2><div class="pair">'
page+=fig('release-final-river','River bank')+fig('release-final-underwater','Underwater — existing reflection fallback visible')+'</div><p>Known limits remain: screen-space optics cannot recover arbitrary hidden water volumes or off-screen reflected terrain. Underwater reflection misses can look plain blue. Lower-resolution optics soften fine edges.</p></section><p>Review spot: <code>/tp @s 4127 98.5 4112 180 20</code>. The test ponds now have supported sand floors. Main’s original mod files were checked separately; the temporary QA driver is outside its mods folder.</p><p>Implementation reference: <a href="https://shaders.properties/current/reference/buffers/depthtex/">Iris depth buffers</a> and <a href="https://shaders.properties/current/reference/buffers/colortex/">colour buffers</a>.</p></html>'
(report/'index.html').write_text(page)
print('Report and release documentation finalized; repackage and install the updated documentation.')

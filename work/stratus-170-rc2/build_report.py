from pathlib import Path
import json,shutil,hashlib,html
w=Path(__file__).resolve().parent;r=w.parents[1]/'outputs/Stratus-1.7.0-rc2-visual-checks';(r/'captures').mkdir(parents=True,exist_ok=True)
notes={
'rc2-before-cave-flow.png':'rc1: pale strips along enclosed falling-water steps.',
'rc2-candidate-cave-flow.png':'Superseded v2: sky-exposure clamp alone did not repair the strips.',
'rc2-v3-cave-flow.png':'Final shader source: valid dark native colours retained; strips removed.',
'rc2-release-cave-flow.png':'Exact installed final rc2 ZIP: corrected enclosed stepped flow. Controlled reproduction, not the original screenshot location.',
'rc2-before-cave-down.png':'rc1 downward view: pale patch at lower step.',
'rc2-v3-cave-down.png':'Final source downward view: pale patch removed.',
'rc2-vanilla-underwater.png':'Shaders off: native underside comparison. Animation phase differs.',
'rc2-v2-underwater.png':'Final underside path after display-space blending correction. v3 changes the above-water cache path only.',
'rc2-half-underwater.png':'Native underside at half texture strength.',
'rc2-zero-underwater.png':'Texture strength zero: clear exit retained.',
'rc2-release-underwater.png':'Exact installed final rc2 ZIP: native atlas visible across underside. Strict loaded-chunk gate passed. Submerged-only fog differs deliberately from vanilla.',
'rc2-before-indoor-entity.png':'rc1: flattened sheep shading in enclosed lamp-lit room.',
'rc2-after-indoor-entity.png':'Final source: directional face shading restored, native warm lightmap retained.',
'rc2-vanilla-indoor-entity.png':'Shaders off at matched enclosed entity camera.',
'rc2-before-entity.png':'rc1 outdoor entity: flat white shading. Distant terrain is outside acceptance scope.',
'rc2-v3-entity.png':'Final source outdoor entity: restored face shading. Distant terrain has incomplete sections; only the complete local fixture is reviewed.',
'rc2-vanilla-entity.png':'Shaders off outdoor entity comparison; distant terrain excluded.',
'rc2-before-leaf-close.png':'rc1: shiny internal leaf quads, viewed from outside through cutout holes.',
'rc2-v3-leaf-close.png':'Final source: matte leaf quads, texture detail retained. Entire material4113 excluded; not voxel-exact interior detection.',
'rc2-before-sun-peak.png':'rc1 midday downward quartz-panel view. Not proof of analytical maximum highlight.',
'rc2-after-sun-peak.png':'Final source: modest reduction with native texture preserved. Additional adjacent/shaded-face acceptance remains pending.',
'rc2-dry-sun-peak.png':'Dry matched midday panel. Full solar-angle coverage remains pending.',
'rc2-native-under-glass.png':'Native-mode pool looking upward. Glass edge not distinct enough for complete layering acceptance.',
'rc2-vanilla-under-glass.png':'Shaders-off pool baseline; broad glass/waterline layering still pending.'}
rows=[]
for name,note in notes.items():
 f=w/'screenshots'/name;shutil.copy2(f,r/'captures'/name);rows.append({'file':'captures/'+name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'review':note})
manifest={'release':'1.7.0-rc2','profile':'Main / Minecraft (1)','world':'Stratus Terrain Lab','framebuffer':[1440,842],'render_distance':12,'FPS_samples':0,'installed_and_loaded':True,'capture_scope':(w/'visual-readiness-scope.txt').read_text(),'limitations':json.loads((w/'limitations.json').read_text()),'captures':rows}
(w/'review-notes.json').write_text(json.dumps(notes,indent=2)+'\n');(r/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
parts=['<!doctype html><html lang="en-AU"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus 1.7.0-rc2 checks</title><style>body{background:#121c28;color:#e6eef9;font:16px/1.5 system-ui;margin:0}main{max-width:1200px;margin:auto;padding:24px}a{color:#a0dcff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:20px}figure{margin:0;background:#233247;border-radius:8px;overflow:hidden}img{width:100%;display:block}figcaption{padding:14px}.note{background:#493c30;padding:16px}</style><main><h1>Stratus 1.7.0-rc2</h1><p>Actual Minecraft comparisons: native water, cave flow, leaf film and entity shading.</p><p class="note">Candidate installed and test-loaded. Finite local visual coverage; not full 1.7 acceptance. Some background sections are incomplete and excluded. Only specified views passed the stable loaded-chunk gate. No FPS samples. Solar-angle, solid-occluder and waterline/glass checks remain pending. Original session restored after testing.</p><p><a href="../Stratus-1.7.0-rc2.zip">Candidate ZIP</a> · <a href="../Stratus-1.7.0-rc2-install.json">Install/load receipt</a> · <a href="manifest.json">Evidence manifest</a></p><div class="grid">']
for row in rows:parts.append('<figure><img loading="lazy" src="'+html.escape(row['file'])+'" alt="'+html.escape(Path(row['file']).stem)+'"><figcaption><strong>'+html.escape(Path(row['file']).stem)+'</strong><p>'+html.escape(row['review'])+'</p></figcaption></figure>')
parts.append('</div></main></html>');(r/'index.html').write_text(''.join(parts));print(len(rows),'reviewed captures')

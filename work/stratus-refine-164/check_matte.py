from pathlib import Path
import json,math
w=Path(__file__).parent;j=json.loads((w/'matte-gpu.json').read_text());v={(s['variant'],s['case']):s['rgba'] for s in j['samples']};checks=[]
def check(name,truth):
 checks.append({'name':name,'passed':bool(truth)})
 if not truth:raise AssertionError(name)
def equal(a,b):return max(abs(x-y) for x,y in zip(a,b))<2e-6
for (variant,case),rgba in v.items():
 dry=[0,0,0] if case=='black' else [.3,.2,.1]
 check(variant+'/'+case+'/finite_bounded_absorption',all(math.isfinite(c) and -1e-7<=c<=d+2e-6 for c,d in zip(rgba[:3],dry)))
 if dry[0]:check(variant+'/'+case+'/neutral_material_chroma',abs(rgba[0]/3-rgba[1]/2)<1e-6 and abs(rgba[1]/2-rgba[2])<1e-6)
for variant in ['saved','retention-off','retention-max','dampness-max']:
 check(variant+'/view_invariant',equal(v[variant,'porous_top'],v[variant,'porous_grazing']))
 check(variant+'/no_sun_highlight',equal(v[variant,'porous_top'],v[variant,'porous_night']))
 for case in ['metal','metal_grazing','sealed_cave']:check(variant+'/'+case+'/dry',equal(v[variant,case][:3],[.3,.2,.1]))
 check(variant+'/rain_never_dries',v[variant,'rain'][0]<=v[variant,'porous_top'][0]+1e-6)
 check(variant+'/top_retains_more_than_side',v[variant,'porous_top'][0]<v[variant,'porous_side'][0])
 check(variant+'/material_order',v[variant,'porous_top'][0]<v[variant,'wood'][0]<v[variant,'polished'][0]<v[variant,'metal'][0])
for variant in ['dampness-off','nether','end']:
 for case in [s['case'] for s in j['samples'] if s['variant']==variant]:check(variant+'/'+case+'/unchanged',equal(v[variant,case][:3],[0,0,0] if case=='black' else [.3,.2,.1]))
check('legacy_retention_scales_only_sheltered_absorption',v['retention-max','sheltered_top'][0]<v['saved','sheltered_top'][0]<v['retention-off','sheltered_top'][0])
check('zero_gl_errors',j['opengl_errors']==0)
(w/'matte-assertions.json').write_text(json.dumps({'gpu_samples':len(v),'assertions':len(checks),'failures':0,'checks':checks},indent=2)+'\n')
print(len(v),'GPU samples;',len(checks),'independent invariants/relationship checks passed')

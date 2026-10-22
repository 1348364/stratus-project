from pathlib import Path
import json,numpy as np
w=Path(__file__).parent;d=json.loads((w/'gpu.json').read_text());v={(x['variant'],x['mode'],x['case']):np.array(x['rgba']) for x in d['samples']};checks=[]
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok:print('FAIL',name)
check('Default independent components reproduce 1.6.6 shading',all(np.max(abs(v['current',0,k]-v['before',0,k]))<1e-6 for k in range(24)))
check('Independent face components combine linearly',all(np.max(abs(v['current',0,k]-(v['no-vanilla',0,k]+v['no-realistic',0,k]-np.array([1,1,1,1]))))<1e-6 for k in range(24)))
for n in ['no-faces','master-off']:
 check(n+' bypasses face contrast',all(np.max(abs(v[n,0,k]-1))<1e-6 for k in range(24)))
check('Vanilla control has a visible separate contribution',np.max(abs(v['current',0,0]-v['no-vanilla',0,0]))>.1)
check('Realistic control has a visible separate contribution',np.max(abs(v['current',0,0]-v['no-realistic',0,0]))>.01)
check('Dry clear materials preserve previous matte response',np.max(abs(v['current',1,0]-v['before',1,0]))<1e-6)
for k,n in [(3,'nonporous metal'),(4,'glazed material'),(5,'sealed cave')]:
 check(n+' remains unchanged',np.max(abs(v['current',1,k]-v['before',1,k]))<1e-6)
check('Rain adds an observable response on absorbent wood',np.max(abs(v['current',1,1]-v['before',1,1]))>.0001)
check('Grazing wet sheen is observable',np.max(abs(v['current',1,2]-v['wet-off',1,2]))>.005)
check('Wet strength 2 visibly exceeds off at grazing angle',np.max(abs(v['wet-max',1,2]-v['wet-off',1,2]))>np.max(abs(v['current',1,2]-v['wet-off',1,2])))
check('Dry response does not depend on wet strength',np.max(abs(v['wet-max',1,0]-v['current',1,0]))<1e-6)
check('Nether wet film is disabled',np.max(abs(v['nether',1,1]-np.array([.3,.2,.1,1])))<1e-6)
check('Cirrus optical density is increased by intended factor',all(abs(v['current',2,k][0]/v['before',2,k][0]-2.8125)<1e-5 for k in range(16)))
check('Cirrus independent of lower cloud amount',all(np.array_equal(v['current',2,k],v['lower-off',2,k]) for k in range(16)))
check('Cirrus density zero hides upper layer',all(v['cirrus-off',2,k][0]==0 for k in range(16)))
check('All sampled outputs finite and nonnegative',all(np.all(np.isfinite(x)) and np.min(x)>=0 for x in v.values()))
check('No GPU API errors',d['opengl_errors']==0)
water=json.loads((w/'water-regression.json').read_text());check('All 10 water-resolve regressions pass',water['failures']==water['opengl_errors']==0)
result={'scope':'Actual native GLSL, face component/legacy equivalence, rain film/material gating and cirrus independence; not a performance measurement','total_samples':len(d['samples']),'candidate_samples':sum(x['variant']!='before' for x in d['samples']),'baseline_reference_samples':sum(x['variant']=='before' for x in d['samples']),'checks':checks,'failures':sum(not c['passed'] for c in checks)};(w/'gpu-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(len(checks),'checks,',result['failures'],'failures;',result['total_samples'],'renders');assert result['failures']==0

from pathlib import Path
import json,hashlib,zipfile,re
from urllib.parse import unquote
w=Path(__file__).parent;pack=Path('outputs/Stratus');docs=Path('work/Custom instructions');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(Path('outputs/Stratus-1.6.9-install.json').read_text());release=Path(r['source']);installed=Path(r['installed']);profile=installed.parents[1];assert r['loaded'] and sha(release)==sha(installed)==r['sha256']
with zipfile.ZipFile(release) as z:
 assert z.testzip() is None
 for n in z.namelist():assert z.read(n)==(pack/n).read_bytes(),n
 entries=len(z.namelist());assets=sum(n.startswith('shaders/') for n in z.namelist());assert entries==243 and assets==235
 with zipfile.ZipFile(w/'packs/Stratus-1.6.9-QA-v2-Candidate.zip') as q:
  assert set(n for n in q.namelist() if not Path(n).name.startswith('.'))==set(n for n in z.namelist() if n.startswith('shaders/'))
  assert all(q.read(n)==z.read(n) for n in q.namelist() if not Path(n).name.startswith('.'))
def opts(f):
 s=f.read_text();o=dict((k,(v,a.split())) for k,v,a in re.findall(r'^#define\s+(\w+)\s+(\S+)\s*//\s*\[([^\]]+)\]',s,re.M));o.update({k:(v,a.split()) for k,v,a in re.findall(r'^const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]',s,re.M)});return o
old=opts(w/'baseline/shaders/core/options.glsl');new=opts(pack/'shaders/core/options.glsl');assert len(old)==61 and len(new)==62
assert all(new[k][1]==v[1] for k,v in old.items());assert all(new[k][0]==v[0] for k,v in old.items() if k!='REALISTIC_LIGHTING');assert new['REALISTIC_LIGHTING'][0]=='0'
prop=(pack/'shaders/shaders.properties').read_text();oldprop=(w/'baseline/shaders/shaders.properties').read_text();profiles=lambda s:[l for l in s.splitlines() if l.startswith('profile.')];assert profiles(prop)==profiles(oldprop) and len(profiles(prop))==4
menus={l.split('=',1)[0].removeprefix('screen').lstrip('.'):l.split('=',1)[1].split() for l in prop.splitlines() if re.match(r'^screen(?:\.[A-Z_]+)?=',l)};seen=set();reachable=set()
def walk(n):
 if n in seen:return
 seen.add(n)
 for t in menus[n]:
  if t.startswith('['):walk(t[1:-1])
  elif not t.startswith('<'):reachable.add(t)
walk('');assert set(new)<=reachable
lang=(pack/'shaders/lang/en_us.lang').read_text();assert all('option.'+k+'=' in lang and 'option.'+k+'.comment=' in lang for k in new)
assert sha(pack/'shaders/core/environment.glsl')==sha(w/'baseline/shaders/core/environment.glsl')
values=lambda p:dict(l.split('=',1) for l in p.read_text().splitlines() if '=' in l and not l.startswith('#'))
before=values(w/'Main-release-settings-source.txt');after=values(profile/'shaderpacks/Stratus-1.6.9.zip.txt');olddefaults={k:v[0] for k,v in old.items()};newdefaults={k:v[0] for k,v in new.items()};assert all({**newdefaults,**after}[k]==v for k,v in {**olddefaults,**before}.items())
assert values(profile/'shaderpacks/Stratus-1.6.9-water-pole-test.zip.txt')==values(w/'Main-before-Stratus-1.6.9-water-pole-test.zip.txt')
assert (profile/'config/dynamic_fps.json').read_bytes()==(w/'Main-before-dynamic_fps.json').read_bytes()
assert not list((profile/'shaderpacks').glob('Stratus-1.6.9-QA-*'))
runtime=(w/'runtime-v3-Optional_Stratus-1.6.9.zip_.txt').read_text();assert 'selected_pack=Optional[Stratus-1.6.9.zip]' in runtime and 'IrisRenderingPipeline' in runtime
for text in ['REALISTIC_LIGHTING=0','WATER_TEXTURE=0.15','SURFACE_DAMPNESS=0.15','oldLighting=TRUE','composite=>false','DynamicFPS.powerState=FOCUSED']:assert text in runtime
assert 'shaderPack=Stratus-1.6.9.zip' in (profile/'config/iris.properties').read_text()
assert 'polling stopped' in (w/'driver-stopped.txt').read_text() and (w/'activity-stopped.txt').exists()
state=lambda p:dict(l.split('=',1) for l in p.read_text().splitlines() if '=' in l)
a=state(w/'original-client-state.txt');b=state(w/'final-client-state-v2.txt');assert all(abs(float(x)-float(y))<.0001 for x,y in zip(a['position'].split(','),b['position'].split(',')));assert abs((float(a['yaw'])-float(b['yaw'])+180)%360-180)<.001 and abs(float(a['pitch'])-float(b['pitch']))<.001
for k in ['hud','pause','flying']:assert a[k]==b[k],k
assert b['worldTime']=='6000' and b['rainGradient']=='0.0'
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text();assert json.loads((w/'gpu-checks.json').read_text())['failures']==0 and json.loads((w/'water-regression.json').read_text())['failures']==0
perf=json.loads((w/'performance-summary.json').read_text());assert perf['target_60_FPS_verified'] is False
for name in ['active-river-before','active-river-after','active-forest-before-repeat','active-forest-after-repeat']:
 d=json.loads((w/'benchmarks'/f'{name}.json').read_text());assert d['valid_focused_sample'] and d['unfocused_polls']==0 and d['framebuffer']==[1440,842] and len(d['raw_frame_ns'])==d['frames']
rows=json.loads(Path('outputs/Stratus-1.6.9-visual-checks/captures.json').read_text());assert len(rows)==35
for row in rows:assert sha(Path('outputs/Stratus-1.6.9-visual-checks/screenshots')/row['file'])==sha(w/'screenshots'/row['file'])==row['sha256']
q=(docs/'CHANGES.md').read_text();pending=q.split('## Pending changes',1)[1].split('## Completed changes',1)[0];assert len([l for l in pending.splitlines() if l.startswith('- ')])==1 and 'optimise performance' in pending and '[x]' not in pending
assert 'Stratus-1.6.9.zip' in (docs/'TASK.md').read_text()
for p,s in [(docs/'TASK.md',(docs/'TASK.md').read_text()),(docs/'CHANGES.md',q),(docs/'CHANGE-LOG.md',(docs/'CHANGE-LOG.md').read_text().split('## 22 October 2026 — Stratus 1.6.9 water-pole')[0])]:
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if not link.startswith(('http:','https:','#')):
   path=unquote(link.split('#',1)[0].strip('<>'));assert (p.parent/path).exists(),(p,link)
result={'version':'1.6.9','source_archive_installed_and_QA_runtime_equivalence':True,'archive_entries':entries,'runtime_assets':assets,'sha256':r['sha256'],'controls':{'all_61_prior_ids_ranges_and_access_retained':True,'total':62,'all_four_presets_unchanged':True,'deliberate_lighting_default_and_retired_dampness_migration':True},'latest_effective_Main_overrides_preserved':True,'preexisting_pole_filter_unchanged':True,'actual_release_pipeline_loaded':True,'camera_HUD_pause_flight_restored':True,'final_client_state':b,'both_test_helpers_stopped':True,'temporary_QA_files_removed':True,'DynamicFPS_config_unchanged':True,'native_pairs':768,'GPU_component_samples':795,'GPU_output_samples':12,'GPU_relationships':11,'underwater_cases':10,'original_capture_hashes_verified':len(rows),'focused_active_samples_accepted':4,'performance_target_still_pending':True,'completed_visual_requests_moved':4,'one_performance_request_pending':True,'frozen_snapshot_conflicts':[],'documentation_links_resolve':True}
(w/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

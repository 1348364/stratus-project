from pathlib import Path
import hashlib,json,re,zipfile
from urllib.parse import unquote
w=Path(__file__).parent;root=w.resolve().parents[1];pack=Path('outputs/Stratus');docs=Path('work/Custom instructions')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(Path('outputs/Stratus-1.6.8-install.json').read_text());release=Path(r['source']);installed=Path(r['installed']);profile=installed.parents[1]
assert sha(release)==sha(installed)==r['sha256']
with zipfile.ZipFile(release) as z:
 assert z.testzip() is None
 for n in z.namelist():assert z.read(n)==(pack/n).read_bytes(),n
 entries=len(z.namelist());assets=sum(n.startswith('shaders/') for n in z.namelist())
 assert entries==243 and assets==235
with zipfile.ZipFile(w/'packs/Stratus-1.6.8-QA-Final.zip') as z:
 for n in z.namelist():
  if n.startswith('shaders/') and n!='shaders/core/options.glsl':assert z.read(n)==(pack/n).read_bytes(),n
def options(path):
 s=path.read_text();o={k:(v,vals.split()) for k,v,vals in re.findall(r'^#define\s+(\w+)\s+(\S+)\s*//\s*\[([^\]]+)\]',s,re.M)}
 o.update({k:(v,vals.split()) for k,v,vals in re.findall(r'^const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]',s,re.M)})
 return o
old=options(w/'baseline/shaders/core/options.glsl');new=options(pack/'shaders/core/options.glsl');assert len(old)==59 and len(new)==61
assert all(new[k]==v for k,v in old.items())
props=(pack/'shaders/shaders.properties').read_text();oldprops=(w/'baseline/shaders/shaders.properties').read_text()
profiles=lambda s:dict(l.split('=',1) for l in s.splitlines() if l.startswith('profile.'))
assert profiles(props)==profiles(oldprops) and len(profiles(props))==4
menus={l.split('=',1)[0].removeprefix('screen').lstrip('.'):l.split('=',1)[1].split() for l in props.splitlines() if re.match(r'^screen(?:\.[A-Z_]+)?=',l)}
seen=set();reachable=set()
def walk(n):
 if n in seen:return
 seen.add(n)
 for t in menus[n]:
  if t.startswith('['):walk(t[1:-1])
  elif not t.startswith('<'):reachable.add(t)
walk('');assert set(new)<=reachable
lang=dict(l.split('=',1) for l in (pack/'shaders/lang/en_us.lang').read_text().splitlines() if '=' in l)
assert all('option.'+k in lang for k in new)
assert sha(profile/'shaderpacks/Stratus-1.6.7.zip.txt')==sha(w/'Main-before-Stratus-1.6.7.zip.txt')
# Iris updates the comment timestamp on load; compare actual option values.
saved_values=lambda p:dict(l.split('=',1) for l in p.read_text().splitlines() if '=' in l and not l.startswith('#'))
assert saved_values(profile/'shaderpacks/Stratus-1.6.8.zip.txt')==saved_values(w/'Main-before-Stratus-1.6.7.zip.txt')
assert not list((profile/'shaderpacks').glob('Stratus-1.6.8-QA-*'))
assert 'shaderPack=Stratus-1.6.8.zip' in (profile/'config/iris.properties').read_text()
runtime=(w/'runtime-Optional_Stratus-1.6.8.zip_.txt').read_text();assert 'selected_pack=Optional[Stratus-1.6.8.zip]' in runtime
assert 'SKY_AMBIENT=1.00' in runtime and 'WATER_TURBIDITY=3.00' in runtime
vanilla=(w/'runtime-Optional_Stratus-1.6.8-QA-FinalVanilla.zip_.txt').read_text()
assert 'oldLighting=TRUE' in vanilla and 'disableDirectionalShading=false' in vanilla and 'composite5=>false, composite6=>false' in vanilla
assert 'polling stopped' in (w/'driver-stopped.txt').read_text()
state=lambda p:dict(l.split('=',1) for l in p.read_text().splitlines() if '=' in l)
before=state(w/'original-client-state.txt');after=state(w/'final-client-state-v2.txt')
assert all(abs(float(a)-float(b))<.0001 for a,b in zip(before['position'].split(','),after['position'].split(',')))
assert abs((float(before['yaw'])-float(after['yaw'])+180)%360-180)<.001
assert abs(float(before['pitch'])-float(after['pitch']))<.001
for k in ['hud','pause','flying']:assert before[k]==after[k],k
assert after.get('rainGradient')=='0.0'
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text()
assert json.loads((w/'gpu-checks.json').read_text())['failures']==0
assert json.loads((w/'water-regression.json').read_text())['failures']==0
report=Path('outputs/Stratus-1.6.8-visual-checks');rows=json.loads((report/'captures.json').read_text());assert len(rows)==26
for row in rows:assert sha(report/'screenshots'/row['file'])==sha(w/'screenshots'/row['file'])==row['sha256']
target=(docs/'TASK.md').read_text();queue=(docs/'CHANGES.md').read_text()
assert 'Stratus-1.6.8.zip' in target and '22 October 2026' in queue and queue.count('- [ ]')==2
for p,text in [(docs/'TASK.md',target),(docs/'CHANGES.md',queue),(docs/'CHANGE-LOG.md',(docs/'CHANGE-LOG.md').read_text().split('## 21 October 2026')[0])]:
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if not link.startswith(('http:','https:','#')):assert (p.parent/unquote(link)).exists(),link
reconcile=json.loads((w/'reconciliation.json').read_text())
for name,digest in reconcile['historical_files_unchanged_sha256'].items():assert sha(docs/name)==digest
result={'version':'1.6.8','archive_entries':entries,'runtime_assets':assets,'source_archive_and_installed_equivalent':True,'sha256':sha(release),'prior_controls_defaults_ranges_preserved':59,'total_controls':61,'all_controls_reachable_labelled':True,'four_presets_preserved':True,'current_user_overrides_preserved':True,'actual_release_pipeline_and_mode_flags_verified':True,'camera_HUD_pause_flight_restoration_verified':True,'final_client_state':after,'test_driver_stopped':True,'temporary_QA_files_removed':True,'original_capture_hashes_verified':26,'historical_documents_unchanged':True,'target_reconciled_and_two_performance_items_pending':True,'new_documentation_links_resolve':True,'focused_gameplay_FPS_verified':False,'pending_reason':'Explicit user deferral to morning of 22 October 2026','source_state_files_sha256':{str(p.relative_to(pack)):sha(p) for p in pack.rglob('*') if p.is_file() and not p.name.startswith('.') and '__pycache__' not in p.parts}}
(w/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_state_files_sha256'},indent=2))

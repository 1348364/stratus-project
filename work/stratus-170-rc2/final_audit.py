from pathlib import Path
import json,hashlib,zipfile,math
w=Path(__file__).resolve().parent;root=w.parents[1];profile=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)'
def props(p):return dict(l.split('=',1) for l in p.read_text().splitlines() if '=' in l and not l.startswith('#'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=props(w/'initial-client-state.txt');b=props(w/'final-client-state-v2.txt')
checks={'fixture_exact_original':(w/'fixture-original.txt').read_bytes()==(w/'fixture-restored.txt').read_bytes(),'fixture_block_count':len((w/'fixture-restored.txt').read_text().splitlines()),'test_sheep_absent':'UUID sheep absent' in (w/'fixture-stopped.txt').read_text(),'world_exact_original':(w/'original-world-state.txt').read_bytes()==(w/'restored-world-state.txt').read_bytes(),'iris_config_original':props(w/'initial-iris.properties')==props(profile/'config/iris.properties'),'position_restored':max(abs(float(x)-float(y)) for x,y in zip(a['position'].split(','),b['position'].split(',')))<.0001,'angles_restored':abs((float(a['yaw'])-float(b['yaw'])+180)%360-180)<.001 and abs(float(a['pitch'])-float(b['pitch']))<.001,'HUD_pause_flight_menu_restored':all(a[k]==b[k] for k in ['hud','pause','flying','screen']),'watchers_stopped':all((w/n).exists() for n in ['visual-driver-stopped.txt','fixture-stopped.txt','world-time-stopped.txt'])}
(w/'restoration-checks.json').write_text(json.dumps(checks,indent=2)+'\n');assert all(v is True for k,v in checks.items() if k!='fixture_block_count') and checks['fixture_block_count']==3042
p=root/'outputs/Stratus-1.7.0-rc2.zip';z=zipfile.ZipFile(p);assert z.testzip() is None
assert all(z.read(n)==(root/'outputs/Stratus'/n).read_bytes() for n in z.namelist() if not n.endswith('/'))
installed=profile/'shaderpacks'/p.name;assert sha(p)==sha(installed)=='ba966b25c3160e2d325dbb8627634afa274dbaa37175dfc67a51e7a85b9cca2c'
assert not list((profile/'shaderpacks').glob('Stratus-1.7.0-rc2-QA-*'))
initial=json.loads((w/'initial-fingerprints.json').read_text());protected=['work/Custom instructions/CHANGES.md','work/Custom instructions/IN-PROGRESS/1af89474-f56a-4419-bc73-7f12d4950cfa/TASK.md'];assert all(sha(root/n)==initial[n] for n in protected)
result={'sha256':sha(p),'entries':len(z.namelist()),'archive_source_installed_bytes_equal':True,'protected_next_queue_and_target_snapshot_unchanged':True,'QA_temporary_files_remaining':0,'release_installed_and_previously_loaded':True,'current_selection':'Stratus-1.7.0-rc1.zip; shaders disabled, original session restored','restoration':checks,'FPS_samples':0}
(w/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n')
receipt=root/'outputs/Stratus-1.7.0-rc2-install.json';j=json.loads(receipt.read_text());j['restoration']=result['current_selection'];j['restoration_evidence']=str(w/'restoration-checks.json');j['QA_cleanup_evidence']=str(w/'qa-cleanup.json');receipt.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(result,indent=2))

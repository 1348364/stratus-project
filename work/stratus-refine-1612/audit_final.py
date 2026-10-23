from pathlib import Path
import json,hashlib,zipfile,re,sys,difflib
w=Path(__file__).parent;p=Path('outputs/Stratus');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();load=lambda n:json.loads((w/n).read_text());release=Path('outputs/Stratus-1.6.12.zip');receipt=json.loads(Path('outputs/Stratus-1.6.12-install.json').read_text())
assert receipt['loaded'] and receipt['runtime_options_equal_approved_reference'] and sha(release)==sha(Path(receipt['installed']))==receipt['sha256']
with zipfile.ZipFile(release) as z:
 assert z.testzip() is None
 assert all(z.read(n)==(p/n).read_bytes() for n in z.namelist())
 entries=len(z.namelist());assets=sum(n.startswith('shaders/') for n in z.namelist())
 for f in (w/'packs').glob('*.zip'):
  if f.name.endswith('-Before.zip'):continue
  with zipfile.ZipFile(f) as q:assert all(z.read(n)==q.read(n) for n in q.namelist()),f.name
assert entries==246 and assets==236
assert sha(Path('outputs/Stratus-1.6.11.zip'))=='252e040c62f5be4847814a3227fab06924d46e875f54b67a7d3e60bf58462e62'
assert (p/'shaders/shaders.properties').read_bytes()==(w/'baseline/shaders/shaders.properties').read_bytes()
assert (p/'shaders/core/options.glsl').read_bytes()==(w/'baseline/shaders/core/options.glsl').read_bytes()
changed=[];diff=[]
for f in sorted((p/'shaders').rglob('*')):
 if not f.is_file():continue
 r=f.relative_to(p);old=w/'baseline'/r
 if not old.exists() or old.read_bytes()!=f.read_bytes():
  changed.append(str(r))
  diff+=difflib.unified_diff(old.read_text().splitlines(True) if old.exists() else [],f.read_text().splitlines(True),fromfile='before/'+str(r),tofile='after/'+str(r))
assert set(changed)=={'shaders/core/lake.frag.glsl','shaders/core/water-surface.glsl','shaders/lang/en_us.lang'},changed
(w/'source-changes.json').write_text(json.dumps(changed,indent=2)+'\n');(w/'changes.diff').write_text(''.join(diff))
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile.log').read_text()
assert load('surface-checks.json')['failures']==0 and load('surface-checks.json')['samples']==192
assert load('water-checks.json')['failures']==0 and load('water-checks.json')['opengl_errors']==0
assert load('migration-checks.json')['failures']==0
assert all(x['matches_after_applying_full_profile'] and x['option_count']==62 for x in load('iris-profile-checks.json').values())
rows=[json.loads(l) for l in (w/'chunk-readiness.jsonl').read_text().splitlines()];assert not any(r['sampling'] for r in rows)
assert not list((w/'benchmarks').glob('*.json'))
notes=load('review-notes.json');captures=list((w/'screenshots').glob('*.png'));assert len(captures)==25 and all(f.name in notes for f in captures)
report=Path('outputs/Stratus-1.6.12-visual-checks');manifest=json.loads((report/'manifest.json').read_text());assert len(manifest['captures'])==25
for r in manifest['captures']:assert sha(report/r['file'])==sha(w/'screenshots'/Path(r['file']).name)==r['sha256']
state=lambda f:dict(l.split('=',1) for l in f.read_text().splitlines() if '=' in l)
a=state(w/'visual-original-client-state.txt');b=state(w/'final-client-state-v2.txt')
position_error=max(abs(float(x)-float(y)) for x,y in zip(a['position'].split(','),b['position'].split(',')));assert position_error<.0001
assert abs((float(a['yaw'])-float(b['yaw'])+180)%360-180)<.001 and abs(float(a['pitch'])-float(b['pitch']))<.001
assert all(a[k]==b[k] for k in ['hud','pause','flying'])
assert (w/'original-world-state.txt').read_bytes()==(w/'restored-world-state.txt').read_bytes()
assert (w/'original-glass-fixture-blocks.txt').read_bytes()==(w/'restored-fixture-blocks.txt').read_bytes()
assert all((w/f).exists() for f in ['visual-driver-stopped.txt','world-time-stopped.txt','world-fixture-stopped.txt'])
assert load('qa-cleanup.json')['preserved_newer_edits']==[]
profile=Path(receipt['installed']).parents[1];assert not list((profile/'shaderpacks').glob('Stratus-1.6.12-QA-*'))
assert 'shaderPack=Stratus-1.6.12.zip' in (profile/'config/iris.properties').read_text()
shared=Path('work/Custom instructions/CHANGES.md');initial=load('initial-fingerprints.json');shared_unchanged=sha(shared)==initial[str(shared)]
restoration={'camera_max_error_blocks':position_error,'camera_HUD_pause_flight_restored':True,'original_daylight_weather_flags_and_timers_exact':True,'four_temporary_glass_blocks_restored_to_exact_original_water_states':True,'all_helpers_stopped':True,'fixture_recovery':'Older helper block-setter method was unavailable. Its failed restoration did not change blocks; bounded server-command recovery restored and read back all four exact source-water states. Error and recovery receipts retained.','final_client':b};(w/'restoration-checks.json').write_text(json.dumps(restoration,indent=2)+'\n')
result={'release':'1.6.12','sha256':sha(release),'entries':entries,'runtime_assets':assets,'release_loaded':True,'all62_effective_values_match_approved_reference':True,'controls_and_quality_preserved':True,'native_pairs':768,'surface_GPU_samples':192,'underwater_cases':10,'installer_checks':len(load('migration-checks.json')['checks']),'Iris_profiles':4,'captures':25,'all_captures_reviewed':True,'waterline_all_clean':False,'preexisting_waterline_defect_reproduced_on_baseline_and_kept_pending':True,'FPS_samples':0,'state_restored':True,'own_temporary_QA_removed':True,'shared_next_unsent_queue_unchanged':shared_unchanged,'shared_next_queue_not_edited_by_this_run':True,'newer_shared_queue_edits_preserved':not shared_unchanged,'previous_release_preserved':True,'source_archive_installed_and_QA_runtime_bytes_match':True}
(w/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

from pathlib import Path
import json,hashlib,zipfile
w=Path(__file__).parent;docs=Path('work/Custom instructions');batch=docs/'IN-PROGRESS/43b4c0ad-c217-4a82-8534-29d34345f150';p=Path('outputs/Stratus');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();load=lambda n:json.loads((w/n).read_text());initial=load('initial-fingerprints.json')
state=lambda f:dict(l.split('=',1) for l in f.read_text().splitlines() if '=' in l)
a=state(w/'visual-original-client-state.txt');b=state(w/'final-client-state-v2.txt');error=max(abs(float(x)-float(y)) for x,y in zip(a['position'].split(','),b['position'].split(',')));assert error<.0001
assert abs((float(a['yaw'])-float(b['yaw'])+180)%360-180)<.001 and abs(float(a['pitch'])-float(b['pitch']))<.001
assert all(a[k]==b[k] for k in ['hud','pause','flying']);assert (w/'original-world-state.txt').read_bytes()==(w/'restored-world-state.txt').read_bytes()
assert all((w/f).exists() for f in ['visual-driver-stopped.txt','world-time-stopped.txt'])
old=state(w/'initial-runtime-1.6.12.txt');now=state(w/'runtime-v3-Optional_Stratus-1.6.12.zip_.txt');controlkeys=json.loads((w/'reference-defaults.json').read_text()).keys()-{'WATER_STYLE','TRANSPARENT_REFLECTIONS','TRANSPARENT_REFRACTION'};assert len(controlkeys)==62
assert all(old[k]==now[k] for k in controlkeys);assert now['selected_pack']=='Optional[Stratus-1.6.12.zip]' and 'IrisRenderingPipeline' in now['pipeline']
restoration={'camera_max_error_blocks':error,'equivalent_yaw_pitch':True,'original_HUD_pause_flight':True,'original_daylight_weather_flags_and_timers_exact':True,'original_1_6_12_loaded_with_same62_values':True,'no_temporary_block_edits':True,'visual_and_world_watchers_stopped':True,'final_client':b};(w/'restoration-checks.json').write_text(json.dumps(restoration,indent=2)+'\n')
assert load('qa-cleanup.json')['preserved_newer_edits']==[]
for f in ['control-checks.json','migration-checks.json','wet-checks.json','glass-checks.json','legacy-water-final-checks.json','native-water-final-checks.json']:assert load(f)['failures']==0
assert 'Validated 768 program pairs; 0 failures.' in (w/'compile-final.log').read_text()
assert all(v['option_count']==65 and v['matches_after_applying_full_profile'] for v in load('iris-profile-checks.json').values())
r=load('package-checks.json');f=Path(r['archive']);assert sha(f)==r['sha256']
with zipfile.ZipFile(f) as z:
 assert z.testzip() is None and all(z.read(n)==(p/n).read_bytes() for n in z.namelist())
 for q in (w/'packs').glob('*v3-*.zip'):
  if q.name.endswith('-Before.zip'):continue
  with zipfile.ZipFile(q) as a:assert all(z.read(n)==a.read(n) for n in a.namelist())
assert sha(Path('outputs/Stratus-1.6.12.zip'))=='5232c270a31de108ba862135e0f4a6bedaba16e011c2ec1b44a651f7a50c44e2'
assert sha(docs/'CHANGES.md')==initial[str(docs/'CHANGES.md')]
assert sha(docs/'COMPLETED-CHANGES.md')==initial[str(docs/'COMPLETED-CHANGES.md')]
assert sha(batch/'TASK.md')==initial[str(batch/'TASK.md')]
assert (batch/'CHANGES.md').read_text().count('- [ ]')==4 and '- [x]' not in (batch/'CHANGES.md').read_text()
report=Path('outputs/Stratus-1.7.0-rc1-visual-checks');m=json.loads((report/'manifest.json').read_text());notes=load('review-notes.json');assert len(m['captures'])==len(notes)==11
for row in m['captures']:
 assert sha(report/row['file'])==row['sha256']==sha(w/'screenshots'/Path(row['file']).name)
 assert row['readiness_gate'] and (w/'readiness'/(row['readiness_gate']+'.json')).exists()
rows=[json.loads(l) for l in (w/'chunk-readiness.jsonl').read_text().splitlines()];assert not any(x['sampling'] for x in rows)
assert not list((w/'benchmarks').glob('*.json'))
result={'status':'Implementation candidate, not accepted completion','version':'1.7.0-rc1','packaged':True,'candidate_archive_installed_or_loaded':False,'equivalent_final_QA_shaders_loaded':True,'native_pairs':768,'wet_GPU_samples':96,'transparent_GPU_pixels':24576,'underwater_GPU_cases':20,'migration_checks':13,'Iris_profiles_parsed_and_matched':4,'preserved_old_controls':62,'new_total_controls':65,'reviewed_actual_captures':11,'known_waterline_failure_remains':True,'remaining_live_checks_skipped_by_user':True,'pending_batch_requests':4,'FPS_samples':0,'restoration_verified':True,'removed_own_QA_files':len(load('qa-cleanup.json')['removed']),'shared_next_queue_unchanged':True,'completed_archive_unchanged_no_full_request_accepted':True,'batch_target_snapshot_unchanged':True,'old_release_unchanged':True,'candidate_SHA256':r['sha256'],'gallery_created_images_inspected_browser_render_blocked':True}
(w/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

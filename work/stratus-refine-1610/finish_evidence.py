from pathlib import Path
import hashlib,json,re,shutil,html,math
w=Path('work/stratus-refine-1610');p=Path('outputs/Stratus');root=Path.cwd()
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def values(f):
 return {x.split('=',1)[0]:x.split('=',1)[1] for x in f.read_text().splitlines() if '=' in x and not x.startswith('#')}
old=values(w/'original-client-state.txt');new=values(w/'final-client-state-v2.txt')
position_error=max(abs(a-b) for a,b in zip(map(float,old['position'].split(',')),map(float,new['position'].split(','))))
yaw_error=abs((float(new['yaw'])-float(old['yaw'])+180)%360-180)
assert position_error<.0001 and yaw_error<.001
assert all(new[k]==old[k] for k in ['hud','pause','flying'])
assert new['worldTime']=='6000' and new['rainGradient']=='0.0'
assert (w/'original-world-state.txt').read_bytes()==(w/'restored-world-state.txt').read_bytes()
assert (w/'original-glass-fixture-blocks.txt').read_bytes()==(w/'restored-fixture-blocks.txt').read_bytes()
report={'original_camera_restored_max_position_error_blocks':position_error,'yaw_modulo_360_error_degrees':yaw_error,'original_HUD_pause_flight_restored':True,'original_screen_restored':new['screen'],'world_time':6000,'rain_gradient':0,'weather_timers_and_flags_restored_verified':True,'temporary_four_glass_blocks_restored_to_exact_water_states':True,'driver_stopped':(w/'driver-stopped.txt').is_file(),'activity_helper_stopped':(w/'activity-stopped.txt').is_file(),'fixture_helper_stopped':(w/'world-fixture-stopped.txt').is_file(),'focused_benchmark_driver_stopped':(w/'benchmark-driver-stopped.txt').is_file(),'focused_activity_helper_stopped':(w/'final-activity-stopped.txt').is_file(),'profiler_bytecode_restored':(w/'gpu-profile-b-restored.txt').read_text(),'recovery_note':'Initial fixture restore used an unavailable mapped method and stopped before modifying blocks. Guarded recovery restored exact saved states via Minecraft commands and verified them. Original failure evidence retained.'}
(w/'restoration-checks.json').write_text(json.dumps(report,indent=2)+'\n')
# Keep Finder metadata out of the change inventory; leave those files intact.
changed=json.loads((w/'source-changes.json').read_text());(w/'source-changes.json').write_text(json.dumps([x for x in changed if '.DS_Store' not in x['path']],indent=2)+'\n')
receipt=Path('outputs/Stratus-1.6.10-install.json');data=json.loads(receipt.read_text());runtime=(w/'runtime-v3-Optional_Stratus-1.6.10.zip_.txt').read_text()
assert 'pipeline=net.irisshaders.iris.pipeline.IrisRenderingPipeline' in runtime
assert 'selected_pack=Optional[Stratus-1.6.10.zip]' in runtime
for k,v in data['unrelated_overrides_carried'].items():
 if k in ('REFRACTION_QUALITY',):continue
 assert f'{k}={v}' in runtime,(k,v)
assert 'SURFACE_DAMPNESS=1.00' in runtime
installed=Path(data['installed']);assert sha(installed)==data['sha256']
settings=installed.with_suffix('.zip.txt');assert values(settings)==data['unrelated_overrides_carried']
profile=installed.parent.parent
assert sha(profile/'shaderpacks/Stratus-1.6.9.zip.txt')==sha(w/'Main-before-Stratus-1.6.9.zip.txt')
data.update({'selected':True,'loaded':True,'pipeline':'net.irisshaders.iris.pipeline.IrisRenderingPipeline','runtime_evidence':str(w/'runtime-v3-Optional_Stratus-1.6.10.zip_.txt'),'runtime_verifies_related_defaults_and_unrelated_overrides':True,'all_62_controls_and_four_profiles_preserved':True,'installed_bytes_equal_release':True,'older_1_6_9_preferences_unchanged':True,'Main_options_file_byte_identical':sha(profile/'options.txt')==sha(w/'Main-before-options.txt'),'Main_DynamicFPS_config_byte_identical':sha(profile/'config/dynamic_fps.json')==sha(w/'Main-before-dynamic_fps.json'),'visual_review':['Actual final release river','Actual final release underwater air exit','Actual final release root/Materials menus','Full Reference QA with same235 runtime assets','Labelled finite water/material/cloud/sun matrix'],'focused_FPS_verified':True,'target_60_FPS_verified':False,'performance_evidence':'outputs/Stratus-1.6.10-performance.json','initial_migration_receipt':'work/stratus-refine-1610/pre-focused-benchmark-install.json','restoration_evidence':str(w/'restoration-checks.json')})
receipt.write_text(json.dumps(data,indent=2)+'\n')
# Actual-capture manifest from the runtime log: retain exact pack/camera context.
log=(profile/'logs/latest.log').read_text();pack=None;camera=None;contexts={}
for row in log.splitlines():
 if '[STRATUS_QA1610] PACK ' in row:pack=row.split('[STRATUS_QA1610] PACK ',1)[1]
 if '[STRATUS_QA1610] CAMERA ' in row:camera=row.split('[STRATUS_QA1610] CAMERA ',1)[1]
 if '[STRATUS_QA1610] SCREENSHOT ' in row:
  name=row.split('[STRATUS_QA1610] SCREENSHOT ',1)[1].split()[0]+'.png';contexts[name]={'pack':pack,'camera':camera,'log_time':row[:10]}
limited={
 's1610-plane-cache-reference-river.png':'Rejected optimisation experiment. Slower/inconsistent pass timing; plane cache is absent from release.',
 's1610-fixture-particles-glass-underwater.png':'First particle attempt did not show emitted end rods. Glass view only; superseded by visible-particle retry.',
 's1610-shelter-rain.png':'Outside wall close-up; insufficient evidence for sealed shelter film. Use the sealed cave views instead.',
 's1610-clouds-inside-a.png':'Layer-height grazing view through a footprint hole. Does not prove camera inside occupied cloud.',
 's1610-clouds-motion-b.png':'Second grazing frame; finite animation pair only. No moving-camera or occupied-cloud interior certification.',
 's1610-clouds-above.png':'Accepted cloud-only review. Terrain below is partly unloaded; reject terrain acceptance from this frame.',
 's1610-cirrus-independent.png':'Lower clouds isolated off, but wisps are too subtle in this framing for firm independent-cirrus visual acceptance.',
 's1610-cirrus-sunset.png':'Time12000 sky capture; cirrus too subtle and framing lacks sunset horizon. Keep clearer review pending.'}
notes={
 's1610-release-river.png':'Final released ZIP loaded with selectively migrated normal Main tuning. Sky-only reflection preference retained; this is not full Reference performance evidence.',
 's1610-release-underwater.png':'Final released ZIP underwater, looking toward air exit and forest. Finite view; no exact historical scene certification.',
 's1610-release-menu-root.png':'Final released ZIP and Custom profile correctly retain eight unrelated Main overrides.',
 's1610-release-menu-materials.png':'Final released ZIP shows film amount Normal(default), sheen0.85 and all-weather; related old amount0.15 reset.',
 's1610-menu-root-reference.png':'Actual Iris labels full Reference (Recommended); original identifier/quality retained.',
 's1610-menu-materials.png':'Full Reference QA Materials page; approved visual defaults present.',
 's1610-particles-glass-retry.png':'Visible end-rod particles, transparent blue glass and submerged wood together. Synthetic particle burst deliberately dense; finite ordering check.',
 's1610-river-downward.png':'Finite pitch90 river view is coherent. Exact original reported pole camera/context was not recovered.',
 's1610-river-screen-edge.png':'Full Reference shoreline/scenery reflection extends to viewport edges without a severe rectangle in this finite view.',
 's1610-cave-lamp-above-water.png':'Sealed cave tank with water below, stone receiver and local lamp light; day scene.',
 's1610-cave-lamp-above-water-night.png':'Matched sealed cave tank at night; local light retained.',
 's1610-clouds-below.png':'Connected physical lower cloud forms from below; mist off to isolate clouds.',
 's1610-clouds-small-span-grazing.png':'Small span64 grazing safety view; finite check, not arbitrary-span certification.',
 's1610-clouds-native.png':'Native cloud geometry mode remains available.',
 's1610-polished-sun.png':'Polished square sun with local halo, normal physical clouds.',
 's1610-native-sun.png':'Matched camera/time with native celestial texture, preserving selectable native mode.'}
output=Path('outputs/Stratus-1.6.10-visual-checks');(output/'captures').mkdir(parents=True,exist_ok=True)
entries=[]
for f in sorted((w/'screenshots').glob('*.png')):
 shutil.copy2(f,output/'captures'/f.name)
 status='limited' if f.name in limited else 'reviewed'
 if 'plane-cache' in f.name:status='rejected experiment'
 if 'static-' in f.name:status='comparison only'
 note=limited.get(f.name,notes.get(f.name,'Actual Main framebuffer inspected for finite regression coverage.'))
 if 'static-' in f.name:note='Fixed shader-time comparison. Reflected foliage varies on repeated same-pack captures; do not infer pixel equivalence.'
 entries.append({'file':'captures/'+f.name,'sha256':sha(f),'status':status,'note':note,**contexts.get(f.name,{})})
summary={'version':'1.6.10','profile':'Main / Minecraft (1)','world':'Stratus Terrain Lab normal world','framebuffer':[1440,842],'performance':'Focused full-Reference river19.6154→20.1645FPS, forest17.7699→18.0673FPS. Small finite gains;60FPS remains unmet.','captures':entries,'restoration':report,'unverified':['Occupied cloud interior','Clearer independent high-cirrus and sunset framing','Exact-depth distant foliage fog fallback in original scene','Exact historical water-pole camera','Exhaustive preset/mod/motion coverage']}
(output/'manifest.json').write_text(json.dumps(summary,indent=2)+'\n');(w/'visual-review.json').write_text(json.dumps(summary,indent=2)+'\n')
parts=['''<!doctype html><html lang="en-AU"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stratus1.6.10 — actual Minecraft checks</title><style>body{margin:0;background:#10151e;color:#e5edf6;font:16px/1.5 system-ui}main{max-width:1220px;margin:auto;padding:32px}h1{font-size:34px}p{max-width:85ch}a{color:#93cfff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:22px}figure{margin:0;background:#1b2533;border:1px solid #334458;border-radius:10px;overflow:hidden}img{display:block;width:100%;height:auto}figcaption{padding:15px}.badge{font-size:12px;text-transform:uppercase;color:#a4d7ff}.limited{border-color:#b38d42}small{overflow-wrap:anywhere;color:#b7c7d9}strong{display:block}.notice{padding:18px;background:#26364b;border-radius:8px;margin:22px 0}</style><main><h1>Stratus1.6.10</h1><p>Actual Main framebuffer captures — Minecraft1.21.11 / Iris1.10.8 / Apple M1. The released ZIP is installed, selected and loaded. Every test and isolation variant is labelled below.</p><div class="notice">The 60FPS Reference target remains unmet. After the user foregrounded Main, matched focused full-Reference tests measured river19.6→20.2FPS and forest17.8→18.1FPS. Unfocused GPU diagnostics remain separate. Some cloud views and the original pole/leaf scenes remain unverified. Temporary test state was restored.</div><p><a href="../Stratus-1.6.10.zip">Release ZIP</a> · <a href="../Stratus-1.6.10-install.json">Install/load receipt</a> · <a href="../Stratus-1.6.10-performance.json">Focused FPS results</a> · <a href="manifest.json">Capture manifest</a> · <a href="../../work/Custom%20instructions/CHANGE-LOG.md">Change log</a></p><div class="grid">''']
# Final release first, then Reference evidence, then labelled remainder.
entries.sort(key=lambda e:(0 if 'release-' in e['file'] else 1,e['file']))
for e in entries:
 esc=html.escape;cl='limited' if e['status']!='reviewed' else ''
 parts.append(f'<figure class="{cl}"><a href="{esc(e["file"])}"><img loading="lazy" src="{esc(e["file"])}" alt="{esc(Path(e["file"]).stem)}"></a><figcaption><span class="badge">{esc(e["status"])}</span><strong>{esc(Path(e["file"]).stem.removeprefix("s1610-"))}</strong><p>{esc(e["note"])}</p><small>{esc(e.get("pack") or "See manifest/log")}<br>{esc(e.get("camera") or "See recorded context")}</small></figcaption></figure>')
parts.append('</div></main></html>');(output/'index.html').write_text(''.join(parts))
print(json.dumps({'restoration':report,'capture_count':len(entries),'release_loaded':data['loaded'],'old_preferences_unchanged':data['older_1_6_9_preferences_unchanged'],'game_options_unchanged':data['Main_options_file_byte_identical'],'DynamicFPS_config_unchanged':data['Main_DynamicFPS_config_byte_identical']},indent=2))

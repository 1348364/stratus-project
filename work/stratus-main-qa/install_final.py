from pathlib import Path
import json,hashlib,re,shutil,zipfile,sys
root=Path.cwd();main=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)';w=root/'work/stratus-main-qa'
checks=json.loads((root/'outputs/Stratus/CHECKS.json').read_text());source=checks['source_hashes'];release=root/'outputs/Stratus-1.5.1.zip'
assert (w/'qa-complete.txt').read_text().strip()=='v151-main-saved-for-review'
log=(w/'minecraft-main-151.log').read_text(errors='replace');assert 'All dimensions are saved' in log and '[STRATUS_QA] GRACEFUL_QUIT' in log
with zipfile.ZipFile(release) as z,zipfile.ZipFile(main/'shaderpacks/Stratus-1.5.1-Refraction131.zip') as tested:
 assert z.testzip() is None
 for n,digest in source.items():assert hashlib.sha256(z.read(n)).hexdigest()==digest and tested.read(n)==z.read(n),n
for n in ['Stratus-1.5.1.zip','Stratus-1.5.1.zip.txt']:
 target=main/'shaderpacks'/n;pending=target.with_name(n+'.pending');shutil.copy2(root/'outputs'/n,pending);pending.replace(target)
# Restore only the field explicitly changed by this helper, keeping other current options.
before=(w/'before/options.txt').read_text();old=re.search(r'^pauseOnLostFocus:(.*)$',before,re.M)[1]
p=main/'options.txt';s=p.read_text();s=re.sub(r'^pauseOnLostFocus:.*$','pauseOnLostFocus:'+old,s,flags=re.M);p.write_text(s)
p=main/'config/iris.properties';s=p.read_text();s=re.sub(r'^shaderPack=.*$','shaderPack=Stratus-1.5.1.zip',s,flags=re.M);s=re.sub(r'^enableShaders=.*$','enableShaders=true',s,flags=re.M);p.write_text(s)
# Move only the shader experiments created by this task to recoverable workspace storage.
archive=w/'experimental-shaders';archive.mkdir(exist_ok=True)
for n in ['Stratus-1.5.1-SpeedCheck.zip','Stratus-1.5.1-CostBaseline.zip','Stratus-1.5.1-NearCache.zip','Stratus-1.5.1-Refraction131.zip']:
 for name in [n,n+'.txt']:
  p=main/'shaderpacks'/name
  if p.exists():shutil.move(p,archive/name)
initial=json.loads((w/'before-hashes.json').read_text());mods={n:hashlib.sha256((main/n).read_bytes()).hexdigest()==v for n,v in initial.items() if n.startswith('mods/')};assert all(mods.values())
assert sorted(p.name for p in (main/'mods').iterdir() if p.is_file())==sorted(Path(n).name for n in mods)
sys.path.insert(0,str(root/'work/stratus-check'));from nbt_local import load,plain
world=main/'saves/StratusTerrainLab';d=plain(load(world/'level.dat')[1])['Data'];assert d['LevelName']=='Stratus Terrain Lab' and d['GameType']==1
assert d['WorldGenSettings']['dimensions']['minecraft:overworld']['generator']['type']=='minecraft:noise'
record={'version':'1.5.1','installed_shader':str(main/'shaderpacks'/release.name),'sha256':hashlib.sha256(release.read_bytes()).hexdigest(),'bytes':release.stat().st_size,'tested_shader_assets_identical':len(source),'main_selected_shader':'Stratus-1.5.1.zip','new_world':str(world),'world_normal_generated':True,'world_creative':True,'main_mod_files_unchanged':len(mods),'temporary_pause_on_focus_restored':old,'existing_world_directories':json.loads((w/'before-worlds.json').read_text()),'main_test_client_closed_normally':True,'fps_validation':'pending user cleanup; no clean FPS claim','remaining_limit':'off-screen underwater reflection fallback can be plain blue'}
(root/'outputs/Stratus-1.5.1-install.json').write_text(json.dumps(record,indent=2)+'\n');(root/'outputs/Stratus-1.5.1-manifest.json').write_text(json.dumps(source,indent=2)+'\n');print(json.dumps(record,indent=2))

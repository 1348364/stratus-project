from pathlib import Path
import hashlib,json,re,shutil,zipfile
root=Path(__file__).resolve().parents[2];w=Path(__file__).parent;profile=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)';packs=profile/'shaderpacks';out=root/'outputs/Stratus-1.6.4-visual-checks'
source=root/'outputs/Stratus-1.6.4.zip';runtime=packs/'Stratus-1.6.4-Verify-CloudRange.zip'
assert 'All dimensions are saved' in (w/'minecraft-main-164.log').read_text(errors='replace')
with zipfile.ZipFile(source) as a,zipfile.ZipFile(runtime) as b:
 names=[n for n in a.namelist() if n.startswith('shaders/')];assert len(names)==235
 assert all(a.read(n)==b.read(n) for n in names),'Final shader assets differ from immutable runtime-tested copy'
def values(path,sep='='):
 return dict(row.split(sep,1) for row in path.read_text().splitlines() if sep in row and not row.startswith('#'))
before_options=values(w/'main-before/shaderpacks/Stratus-1.6.3.zip.txt')
assert values(packs/'Stratus-1.6.4.zip.txt')==before_options,'Do not overwrite changed shader preferences'
# The helper disabled pause-on-lost-focus only for this session. Restore only
# that known test-introduced option, without replacing the complete options file.
original=values(w/'main-before/options.txt',':');current=values(profile/'options.txt',':')
restored=[]
if original.get('pauseOnLostFocus')=='true' and current.get('pauseOnLostFocus')=='false':
 f=profile/'options.txt';s=f.read_text();f.write_text(re.sub(r'^pauseOnLostFocus:false$','pauseOnLostFocus:true',s,flags=re.M));restored.append('pauseOnLostFocus')
for k in ['renderDistance','simulationDistance','maxFps','enableVsync','fullscreen','overrideWidth','overrideHeight','fov']:
 assert values(profile/'options.txt',':').get(k)==original.get(k),'Unexpected change to '+k
pending=packs/'Stratus-1.6.4.release-pending';assert not pending.exists();shutil.copy2(source,pending);pending.replace(packs/source.name)
shutil.copy2(packs/'Stratus-1.6.4.zip.txt',root/'outputs/Stratus-1.6.4.zip.txt')
f=profile/'config/iris.properties';s=f.read_text();assert re.search(r'^shaderPack=',s,re.M);s=re.sub(r'^shaderPack=.*$','shaderPack=Stratus-1.6.4.zip',s,flags=re.M);f.write_text(s)
archive=w/'runtime-archives';archive.mkdir(exist_ok=True)
aliases=['Stratus-1.6.4-QA-'+t+'.zip' for t in ['FAST','BALANCED','REFERENCE','HIGH','VANILLA']]+['Stratus-1.6.4-Final-'+t+'.zip' for t in ['FAST','BALANCED','REFERENCE','HIGH','VANILLA']]+['Stratus-1.6.4-Verify-Midpoint.zip','Stratus-1.6.4-Verify-CloudRange.zip']
for name in aliases:
 for suffix in ['', '.txt']:
  src=packs/(name+suffix);dst=archive/src.name;assert src.is_file() and not dst.exists();shutil.move(src,dst)
old=json.loads((w/'main-before-hashes.json').read_text());protected={k:v for k,v in old.items() if k.startswith(('mods/','resourcepacks/'))}
assert all((profile/k).is_file() and hashlib.sha256((profile/k).read_bytes()).hexdigest()==v for k,v in protected.items()),'Protected Main content changed'
assert sorted(p.name for p in (profile/'saves').iterdir() if p.is_dir())==json.loads((w/'worlds-before.json').read_text())
assert not any('stratus' in f.name.lower() for f in (profile/'mods').iterdir()),'Unexpected helper installed in Main'
sha=hashlib.sha256(source.read_bytes()).hexdigest();assert hashlib.sha256((packs/source.name).read_bytes()).hexdigest()==sha
receipt={'version':'1.6.4','pack':source.name,'sha256':sha,'installed_to':str(packs/source.name),'tested_immutable_archive':str(archive/runtime.name),'tested_shader_assets_match_final':235,'native_compile_pairs':768,'gpu_candidate_samples':122,'runtime_visual_checks':True,'test_client_graceful_exit':True,'original_mod_files_unchanged':sum(k.startswith('mods/') for k in protected),'protected_resource_files_unchanged':sum(k.startswith('resourcepacks/') for k in protected),'all_saved_shader_overrides_preserved':True,'render_settings_preserved':True,'restored_test_options':restored,'temporary_shader_aliases_removed_from_Main':len(aliases),'helper_installed_in_Main_mods':False,'selected_shader_in_config':'Stratus-1.6.4.zip','main_reopened_normally':False,'foreground_fps_verified':False,'normal_reopen_blocker':'Mac is locked; desktop tool requires manual unlock.'}
(root/'outputs/Stratus-1.6.4-install.json').write_text(json.dumps(receipt,indent=2)+'\n');(w/'delivery.json').write_text(json.dumps(receipt,indent=2)+'\n')
r=json.loads((out/'results.json').read_text());r['delivery']={**receipt,'installed':True,'temporary_main_aliases_cleaned':True};(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
page=out/'index.html';text=page.read_text().replace('Final normal reopening is pending manual Mac unlock. The temporary test client saved and quit gracefully.','The final release is installed and selected for the next launch. Normal reopening is pending manual Mac unlock; the temporary client saved and quit, and test aliases were removed.');page.write_text(text)
print(json.dumps({k:receipt[k] for k in ['pack','sha256','tested_shader_assets_match_final','original_mod_files_unchanged','protected_resource_files_unchanged','temporary_shader_aliases_removed_from_Main','restored_test_options','main_reopened_normally']},indent=2))

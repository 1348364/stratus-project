from pathlib import Path
import hashlib,json,shutil,zipfile
root=Path(__file__).resolve().parents[2];w=root/'work/stratus-transparent-blocks';main=Path('/Users/william.lei/Library/Application Support/ModrinthApp/profiles/Minecraft (1)');packs=main/'shaderpacks';src=root/'outputs/Stratus-1.5.3.zip';dst=packs/src.name
with zipfile.ZipFile(src) as a,zipfile.ZipFile(dst) as tested:
 names=[n for n in a.namelist() if n.startswith('shaders/')];assert len(names)==230
 assert all(a.read(n)==tested.read(n) for n in names),'Final executable shader source differs from tested release'
before=json.loads((w/'before/mods.json').read_text());now={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (main/'mods').iterdir() if p.is_file()};assert before==now
shutil.copy2(src,dst)
def options(p):return dict(row.split(':',1) for row in p.read_text().splitlines() if ':' in row)
old=options(w/'before/options.txt');current=options(main/'options.txt')
if current.get('pauseOnLostFocus')!=old.get('pauseOnLostFocus'):
 p=main/'options.txt';rows=p.read_text().splitlines();p.write_text('\n'.join('pauseOnLostFocus:'+old['pauseOnLostFocus'] if row.startswith('pauseOnLostFocus:') else row for row in rows)+'\n')
settings=lambda p:dict(row.split('=',1) for row in p.read_text().splitlines() if '=' in row and not row.startswith('#'))
expected=settings(w/'Stratus-1.5.3-Transparency.zip.txt');actual=settings(packs/'Stratus-1.5.3.zip.txt');assert expected==actual,(expected,actual)
assert settings(main/'config/iris.properties')['shaderPack']=='Stratus-1.5.3.zip'
archive=w/'testing-archives';archive.mkdir(exist_ok=True)
for name in ['Stratus-1.5.3-Transparency.zip','Stratus-1.5.3-TransmissionDebug.zip','Stratus-1.5.3-Resolve-eb43759a.zip','Stratus-1.5.3-Control-CurrentOptions.zip','Stratus-1.5.2-WaterDebug.zip']:
 for suffix in ['', '.txt']:
  p=packs/(name+suffix)
  if p.exists():shutil.move(str(p),str(archive/p.name))
result={'archive':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'shader_files_matching_tested':230,'original_mods_unchanged':len(now),'shader_options_preserved':actual,'test_client_saved_and_closed':True,'normal_main_relaunch':'pending Mac unlock'}
(root/'outputs/Stratus-1.5.3-install.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['sha256','shader_files_matching_tested','original_mods_unchanged','test_client_saved_and_closed']}))

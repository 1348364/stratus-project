from pathlib import Path
import zipfile,json,hashlib
w=Path(__file__).parent;p=Path('outputs/Stratus');out=w/'packs';out.mkdir(exist_ok=True)
preferred=json.loads((w/'settings-snapshot.json').read_text())['saved_overrides']
variants={'QA-v2':{},'QA-v2-CirrusOnly':{'CLOUD_AMOUNT':'0.00','MIST_AMOUNT':'0.00'},'QA-v2-CirrusOff':{'CLOUD_AMOUNT':'0.00','CIRRUS_AMOUNT':'0.00','MIST_AMOUNT':'0.00'},'Baseline-v2-CirrusOnly':{'CLOUD_AMOUNT':'0.00','MIST_AMOUNT':'0.00'},'QA-v2-HaloOff':{'SUN_HALO_STRENGTH':'0.00','SUN_CORE_BRIGHTNESS':'2.80'},'QA-v2-VanillaSun':{'SUN_STYLE':'1'},'QA-v2-NoVanillaFace':{'VANILLA_FACE_CONTRAST':'0.00'},'QA-v2-NoRealisticFace':{'REALISTIC_FACE_CONTRAST':'0.00'},'QA-v2-NoFaces':{'VANILLA_FACE_CONTRAST':'0.00','REALISTIC_FACE_CONTRAST':'0.00'},'QA-v2-WetOff':{'WET_SHEEN':'0.00'},'QA-v2-WetMax':{'WET_SHEEN':'2.00'}}
for preset in ['FAST','BALANCED','REFERENCE','HIGH']:
 line=next(l for l in (p/'shaders/shaders.properties').read_text().splitlines() if l.startswith('profile.'+preset+'='))
 variants['QA-v2-'+preset]=dict(v.split(':') for v in line.split('=',1)[1].split())
receipt=[]
for name,values in variants.items():
 source=w/'baseline' if name.startswith('Baseline') else p
 pack=out/('Stratus-1.6.7-'+name+'.zip');assert not pack.exists(),pack
 with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted((source/'shaders').rglob('*')):
   if f.is_file():z.write(f,f.relative_to(source).as_posix())
  z.writestr('QA-BUILD.txt','Temporary Stratus 1.6.7 validation build; name='+name+'\nNot a released or accepted build.\n')
 options={**preferred,**values}
 pack.with_suffix('.zip.txt').write_text('\n'.join(k+'='+v for k,v in options.items())+'\n')
 receipt.append({'name':pack.name,'sha256':hashlib.sha256(pack.read_bytes()).hexdigest(),'settings':options,'baseline_source':name.startswith('Baseline')})
(w/'qa-pack-inventory.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Created',len(receipt),'immutable test packs.')

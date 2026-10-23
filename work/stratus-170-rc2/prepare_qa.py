from pathlib import Path
import sys,json,zipfile
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import profiles
w=Path(__file__).parent;p=Path('outputs/Stratus');out=w/'packs';out.mkdir(exist_ok=True);values=profiles((p/'shaders').resolve())['REFERENCE']
variants={'Before':(w/'baseline',{}),'Candidate':(p,{}),'TextureZero':(p,{'WATER_TEXTURE':'0.00'}),'TextureHalf':(p,{'WATER_TEXTURE':'0.50'}),'Dry':(p,{'SURFACE_DAMPNESS':'0.00'})}
for name,(root,extra) in variants.items():
 f=out/('Stratus-1.7.0-rc2-QA-v2-'+name+'.zip')
 with zipfile.ZipFile(f,'w',zipfile.ZIP_DEFLATED) as z:
  for item in sorted((root/'shaders').rglob('*')):
   if item.is_file() and item.name!='.DS_Store':z.write(item,item.relative_to(root))
 f.with_suffix('.zip.txt').write_text('# Exact QA values\n'+''.join(f'{k}={v}\n' for k,v in {**values,**extra}.items()))
(w/'reference-defaults.json').write_text(json.dumps(values,indent=2)+'\n');print('Prepared five controlled variants')

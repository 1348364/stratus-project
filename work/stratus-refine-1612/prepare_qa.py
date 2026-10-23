from pathlib import Path
import json,zipfile,sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import profiles
w=Path(__file__).parent;p=Path('outputs/Stratus');out=w/'packs';out.mkdir(exist_ok=True)
values=json.loads(Path('work/stratus-refine-1611/reference-defaults.json').read_text())
variants={'Before':(w/'baseline',{}),'On':(p,{}),'Off':(p,{'WATER_TEXTURE':'0.00'}),'Half':(p,{'WATER_TEXTURE':'0.50'})}
for key,vals in profiles((p/'shaders').resolve()).items():variants[key]=(p,{k:str(v) for k,v in vals.items() if not isinstance(v,bool)})
for name,(root,extra) in variants.items():
 f=out/('Stratus-1.6.12-QA-'+name+'.zip')
 with zipfile.ZipFile(f,'w',zipfile.ZIP_DEFLATED) as z:
  for item in sorted((root/'shaders').rglob('*')):
   if item.is_file() and item.name!='.DS_Store':z.write(item,item.relative_to(root))
 f.with_suffix('.zip.txt').write_text('# Temporary controlled water QA\n'+''.join(f'{k}={v}\n' for k,v in {**values,**extra}.items()))
print(len(variants),'QA variants; matched Reference, zero/half/max and all four exact preset values.')

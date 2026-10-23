from pathlib import Path
import sys,json,zipfile
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import profiles
w=Path(__file__).parent;p=Path('outputs/Stratus');out=w/'packs';out.mkdir(exist_ok=True);values=json.loads((w/'reference-defaults.json').read_text())
variants={'Before':(w/'baseline',{'WATER_STYLE':'0','TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'}),'Candidate':(p,{}),'Legacy':(p,{'WATER_STYLE':'0'}),'Dry':(p,{'SURFACE_DAMPNESS':'0.00','TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'}),'OpticsOff':(p,{'TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'}),'NativeIsolated':(p,{'WET_SHEEN':'0.00','REFLECT_LEVEL':'0.00','WATER_DISTORTION':'0.00','RIPPLE_HEIGHT':'0.00','MIST_AMOUNT':'0.00','CLOUD_STYLE':'1','SUN_STYLE':'1','CIRRUS_AMOUNT':'0.00','TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'})}
for tag,vals in profiles((p/'shaders').resolve()).items():variants[tag]=(p,vals)
for name,(root,extra) in variants.items():
 f=out/('Stratus-1.6.13-QA-v3-'+name+'.zip')
 with zipfile.ZipFile(f,'w',zipfile.ZIP_DEFLATED) as z:
  for item in sorted((root/'shaders').rglob('*')):
   if item.is_file() and item.name!='.DS_Store':z.write(item,item.relative_to(root))
 v={**values,**extra}
 if name=='Before':v={k:v for k,v in v.items() if k not in ['WATER_STYLE','TRANSPARENT_REFLECTIONS','TRANSPARENT_REFRACTION']}
 f.with_suffix('.zip.txt').write_text('# Temporary exact QA values\n'+''.join(f'{k}={v}\n' for k,v in v.items()))
print(len(variants),'controlled variants prepared')

from pathlib import Path
import json,zipfile
w=Path('work/stratus-refine-1611');packs=w/'packs';packs.mkdir(exist_ok=True);values=json.loads((w/'reference-defaults.json').read_text())
variants={'BaselineReference':(w/'baseline',{}),'CandidateReference':(Path('outputs/Stratus'),{}),'CloudInterior':(Path('outputs/Stratus'),{'MIST_AMOUNT':'0.00','CLOUD_DRIFT':'0.00','CIRRUS_AMOUNT':'0.00'}),'CirrusOn':(Path('outputs/Stratus'),{'MIST_AMOUNT':'0.00','CLOUD_AMOUNT':'0.00','CLOUD_DRIFT':'0.00'}),'CirrusOff':(Path('outputs/Stratus'),{'MIST_AMOUNT':'0.00','CLOUD_AMOUNT':'0.00','CLOUD_DRIFT':'0.00','CIRRUS_AMOUNT':'0.00'})}
for name,(root,extra) in variants.items():
 target=packs/f'Stratus-1.6.11-QA-{name}.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in sorted((root/'shaders').rglob('*')):
   if f.is_file() and f.name!='.DS_Store':z.write(f,f.relative_to(root))
 target.with_suffix('.zip.txt').write_text('# Temporary QA only; exact approved Reference values.\n'+''.join(k+'='+v+'\n' for k,v in {**values,**extra}.items()))
print('Five immutable QA packs created with matched62-option baseline/candidate and labelled cloud isolations.')

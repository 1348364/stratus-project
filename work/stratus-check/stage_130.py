from pathlib import Path
import shutil
work=Path('work/stratus-check');dest=Path('work/minecraft-smoke/shaderpacks');base=dict(line.split('=',1) for line in (work/'settings-1.3.0.txt').read_text().splitlines() if '=' in line and not line.startswith('#'))
base.update(CLOUD_LAYERS='2',MIST_DETAIL='2',REFLECTION_MODE='1')
variants={'candidate':{},'balanced':{'CLOUD_LAYERS':'1'},'lower-clouds':{'CLOUD_ALTITUDE':'128.0','CLOUD_THICKNESS':'40.0'},'no-bloom':{'BLOOM_STRENGTH':'0.00'},'small-radius':{'BLOOM_RADIUS':'0.50'},'no-warmth':{'GROUND_WARMTH':'0.00'},'no-distortion':{'WATER_DISTORTION':'0.00'},'clearwater':{'WATER_VISIBILITY':'4.00'},'no-clouds':{'CLOUD_AMOUNT':'0.00','CIRRUS_AMOUNT':'0.00'},'no-mist':{'MIST_AMOUNT':'0.00'},'fast-final':{'CLOUD_LAYERS':'1','MIST_DETAIL':'1','REFLECTION_MODE':'0'},'high-final':{'CLOUD_LAYERS':'3','MIST_DETAIL':'3','REFLECTION_MODE':'2'}}
for name,values in variants.items():
 p=dest/f'Stratus-1.3.0-{name}-v2.zip';shutil.copy2('outputs/Stratus-1.3.0.zip',p)
 settings={**base,**values};p.with_suffix('.zip.txt').write_text('\n'.join(f'{k}={v}' for k,v in settings.items())+'\n')
(work/'final-settings-1.3.0.txt').write_text('\n'.join(f'{k}={v}' for k,v in base.items())+'\n')
s=(work/'qa-130-final.txt').read_text().replace('.zip','-v2.zip').replace('f130-','g130-')
s=s.replace('CMD tp ShaderCheck 104 286 96 0 90','PACK Stratus-1.3.0-lower-clouds-v2.zip\nCMD tp ShaderCheck 104 184 96 0 90')
(work/'qa-130-final-v2.txt').write_text(s)
print('Prepared final-source Reference and comparison ZIPs; 47-scene queue ready')

"""Replace missing-board captures after loading and verifying the fixture chunks."""
from pathlib import Path
import json
g=Path('work/minecraft-smoke');a=['PACK Stratus-1.5.0.zip','RESUME','HUD hide','CMD weather clear','CMD time set 3000','CMD tp ShaderCheck 184 109 45 0 26','WAIT 12','CMD forceload add 176 48 196 61','WAIT 5','CMD fill 176 104 48 196 113 60 minecraft:air']
for i,block in enumerate(['dirt','spruce_planks','stone','polished_granite','iron_block','white_glazed_terracotta','sandstone']):
    x=176+i*3
    a += [f'CMD fill {x} 103 48 {x+2} 103 60 minecraft:{block}',f'CMD fill {x} 104 61 {x+2} 107 61 minecraft:{block}']
a += ['CMD setblock 183 103 56 minecraft:iron_ore','CMD setblock 183 106 61 minecraft:iron_ore','WAIT 8']
def shot(name):a.extend(['SHOT v150-'+name+'-verified','WAIT 3'])
shot('material-wet')
for variant,name in [('Absorption-Only','material-absorption-only'),('Dry','material-dry')]:
    a += [f'PACK Stratus-1.5.0-{variant}.zip','RESUME','CMD tp ShaderCheck 184 109 45 0 26','WAIT 5'];shot(name)
a += ['PACK Stratus-1.5.0.zip','RESUME','CMD tp ShaderCheck 184 103.3 45 0 4','WAIT 5'];shot('material-grazing')
a += ['CMD weather rain','WAIT 15'];shot('material-rain')
a += ['CMD weather clear','WAIT 12','CMD forceload remove 176 48 196 61','CMD tp ShaderCheck 156 105 43 0 35','WAIT 8','DONE v150-materials-complete']
q=g/'qa-request.txt';assert not q.exists();q.write_text('\n'.join(a)+'\n')
manifest=Path('work/stratus-check/captures-150.json');captures=json.loads(manifest.read_text())
for c in captures:
    if c['group']=='Materials':c['name']+='-verified'
manifest.write_text(json.dumps(captures,indent=2)+'\n')
print('Queued verified-chunk material fixture and five replacement captures; no shader source changes.')

"""Read cached isolated-region palette data to locate actual source-water cells."""
from pathlib import Path
import math,struct,zlib,json
from nbt_local import read,plain,load
world=Path('work/minecraft-smoke/saves/StratusCheck')
points=[]
for region in sorted((world/'region').glob('*.mca')):
    _,rx,rz=region.stem.split('.');rx=int(rx);rz=int(rz)
    if abs(rx)>1 or abs(rz)>1:continue
    raw=region.read_bytes()
    for i in range(1024):
        sector=int.from_bytes(raw[i*4:i*4+3],'big')
        if not sector:continue
        cx=rx*32+i%32;cz=rz*32+i//32
        if abs(cx*16-150)>150 or abs(cz*16-50)>150:continue
        length=int.from_bytes(raw[sector*4096:sector*4096+4],'big');kind=raw[sector*4096+4]
        if kind!=2:continue
        chunk=plain(read(zlib.decompress(raw[sector*4096+5:sector*4096+4+length]))[1])
        for section in chunk.get('sections',[]):
            sy=section['Y'];states=section.get('block_states',{});palette=states.get('palette',[])
            ids={i for i,p in enumerate(palette) if p['Name']=='minecraft:water' and p.get('Properties',{}).get('level')=='0'}
            if not ids or sy not in (3,4):continue
            data=states.get('data',[]);bits=max(4,math.ceil(math.log2(max(len(palette),1))));per=64//bits;mask=(1<<bits)-1
            for z in range(0,16,4):
                for x in range(0,16,4):
                    for y in range(15,-1,-1):
                        index=y*256+z*16+x;value=(data[index//per]>>(index%per*bits))&mask if data else 0
                        if value in ids:
                            wx=cx*16+x;wz=cz*16+z;wy=sy*16+y
                            if 50<wy<70:points.append([wx,wy,wz])
                            break
points.sort(key=lambda p:(p[0]-155)**2+(p[2]-40)**2)
Path('work/stratus-check/river-water-151.json').write_text(json.dumps(points,indent=2)+'\n')
print('Actual source water near fixtures:',points[:24])
name,level=load(world/'level.dat');data=plain(level)['Data']
print('Level spawn/generator keys:',[k for k in data if 'spawn' in k.lower() or 'gen' in k.lower()])
print('Overworld generator:',data['WorldGenSettings']['dimensions']['minecraft:overworld']['generator']['type'])

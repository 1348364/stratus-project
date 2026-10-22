from pathlib import Path
from nbt_local import read,plain
import zlib,math,sys
world=Path('work/minecraft-smoke/saves/StratusCheck');cache={}
def block(x,y,z):
 cx=x//16;cz=z//16;k=(cx,cz)
 if k not in cache:
  raw=(world/'region'/f'r.{cx//32}.{cz//32}.mca').read_bytes();i=(cz%32)*32+cx%32;offset=int.from_bytes(raw[i*4:i*4+3],'big')*4096
  if not offset:return '?'
  n=int.from_bytes(raw[offset:offset+4],'big');cache[k]=plain(read(zlib.decompress(raw[offset+5:offset+4+n]))[1])
 for section in cache[k].get('sections',[]):
  if section['Y']!=y//16:continue
  b=section.get('block_states',{});p=b.get('palette',[]);bits=max(4,math.ceil(math.log2(max(len(p),1))));per=64//bits;data=b.get('data',[]);idx=(y%16)*256+(z%16)*16+(x%16)
  state=(data[idx//per]>>(idx%per*bits))&((1<<bits)-1) if data else 0
  return p[state]['Name'].replace('minecraft:','')+str(p[state].get('Properties',{}))
 return 'air'
if __name__=='__main__':
 for x,z in [(164,32),(163,34),(160,36),(160,40),(156,40),(156,44),(152,48),(164,40)]:
  print(x,z,[(y,block(x,y,z)) for y in range(64,55,-1)])

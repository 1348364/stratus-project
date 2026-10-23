"""Generate Stratus's original periodic 3D weather-noise data (requires NumPy).
RGBA8,128x128x128: fractal body, rounded cellular lobes, fine erosion, broad fog.
No downloaded texture or shader-pack code is used. Run only to rebuild the data.
"""
from pathlib import Path
import json
import numpy as np
SIZE=128
rng=np.random.default_rng(0x53545241545553)
z,y,x=np.mgrid[0:SIZE,0:SIZE,0:SIZE].astype(np.float32)
def value_noise(cells):
 grid=rng.random((cells,cells,cells),dtype=np.float32)
 coords=[v*cells/SIZE for v in [z,y,x]];low=[v.astype(np.int32) for v in coords]
 f=[v-i for v,i in zip(coords,low)];t=[v*v*v*(v*(v*6-15)+10) for v in f];out=np.zeros_like(x)
 for dz in [0,1]:
  for dy in [0,1]:
   for dx in [0,1]:
    weight=(t[0] if dz else 1-t[0])*(t[1] if dy else 1-t[1])*(t[2] if dx else 1-t[2])
    out+=grid[(low[0]+dz)%cells,(low[1]+dy)%cells,(low[2]+dx)%cells]*weight
 return out
body=sum(w*value_noise(c) for c,w in [(4,.50),(8,.28),(16,.15),(32,.07)])
fine=.65*value_noise(16)+.35*value_noise(32);broad=value_noise(4)
cells=5;features=rng.random((cells,cells,cells,3),dtype=np.float32)
coords=np.stack([z,y,x],axis=-1)*cells/SIZE;base=np.floor(coords).astype(np.int32);nearest=np.full_like(x,100.)
for dz in [-1,0,1]:
 for dy in [-1,0,1]:
  for dx in [-1,0,1]:
   cell=base+np.array([dz,dy,dx]);feature=cell+features[cell[...,0]%cells,cell[...,1]%cells,cell[...,2]%cells]
   nearest=np.minimum(nearest,np.sum((coords-feature)**2,axis=-1))
lobes=np.clip(1.-np.sqrt(nearest)/1.15,0,1)
result=np.stack([body,lobes,fine,broad],axis=-1)
root=Path(__file__).resolve().parent/'shaders/volumes';root.mkdir(parents=True,exist_ok=True)
(root/'weather.rgba8').write_bytes(np.rint(np.clip(result,0,1)*255).astype(np.uint8).tobytes())
(root/'weather.rgba8.mcmeta').write_text(json.dumps({'texture':{'blur':True,'clamp':False}},indent=2)+'\n')
print('Generated',SIZE**3*4,'bytes of deterministic periodic3D weather data.')

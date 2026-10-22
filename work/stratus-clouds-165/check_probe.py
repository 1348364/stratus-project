from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
w=Path(__file__).parent
checks=[]
def check(name,success):
 checks.append({'check':name,'passed':bool(success)})
 if not success:print('FAIL',name)
def read(name):return np.fromfile(w/(name+'.rgba32f'),dtype=np.float32).reshape((256,256,4))
tex=np.asarray(Image.open(w/'vanilla-clouds-reference.png').convert('RGBA'));mask=tex[:,:,3]>=26
cloud=read('cloud-0')
check('All 65536 vanilla footprint cells match texture alpha',np.array_equal(cloud[:,:,0]>.5,mask))
check('Density preserves every occupied cell and hole',np.array_equal(cloud[:,:,1]>0,mask))
check('Lower amount zero fully disables density',np.all(read('cloud-low-off-0')[:,:,1]==0))
for variant in ['cloud-other-low','cloud-detail-off','cloud-detail-max']:
 check(variant+' preserves exact horizontal footprint',np.array_equal(read(variant+'-0')[:,:,1]>0,mask))
upper=read('cloud-1')[:,:,0]
check('High clouds have positive finite density throughout 24km sky sample',np.all(np.isfinite(upper)) and np.all(upper>0))
check('High layer zero turns it off',np.all(read('cloud-upper-off-1')[:,:,0]==0))
for variant in ['cloud-low-off','cloud-other-low']:
 check('High clouds independent of '+variant,np.array_equal(upper,read(variant+'-1')[:,:,0]))
# Offline previews are actual GLSL renders, explicitly not in-game acceptance.
thumbs=[]
for k,title in enumerate(['Below / noon','Inside / noon','Above / noon','Below / sunset','Below / night']):
 data=read('sky-'+str(k));check(title+' finite RGBA',np.all(np.isfinite(data)))
 rgb=np.maximum(data[:,:,:3],0);rgb=np.where(rgb<=.0031308,rgb*12.92,1.055*np.power(rgb,1/2.4)-.055)
 image=Image.fromarray((np.clip(rgb,0,1)*255).astype('uint8')).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 image.save(w/('sky-'+str(k)+'.png'))
 tile=Image.new('RGB',(384,285),'#181b20');tile.paste(image.resize((384,256)),(0,24));ImageDraw.Draw(tile).text((8,5),title,fill='white');thumbs.append(tile)
canvas=Image.new('RGB',(384*3,285*2+30),'#181b20');ImageDraw.Draw(canvas).text((8,8),'OFFLINE GLSL PREVIEWS - not Minecraft screenshots',fill='white')
for k,t in enumerate(thumbs):canvas.paste(t,((k%3)*384,30+(k//3)*285))
canvas.save(w/'offline-cloud-preview.jpg')
d=json.loads((w/'gpu.json').read_text());lookup={(v['variant'],v['condition'],v['normal']):v['value'] for v in d['faces']}
for variant in ['face','face-strong']:
 check(variant+' day sun-facing side brighter',lookup[variant,0,0]>lookup[variant,0,1]+.05)
 check(variant+' sun reversal reverses side contrast',lookup[variant,1,1]>lookup[variant,1,0]+.05)
 delta=lambda k:abs(lookup[variant,k,0]-lookup[variant,k,1])
 check(variant+' rain softens directional contrast',delta(2)<delta(0))
 check(variant+' night has no solar contrast',delta(3)<1e-6)
 check(variant+' caves keep fixed local-light face response',abs(lookup[variant,4,0]-lookup[variant,4,1])<1e-6)
for variant in ['face-off','face-blend-off']:
 check(variant+' exact bypass',all(abs(v['value']-1)<1e-6 for v in d['faces'] if v['variant']==variant))
for variant in ['face-nether','face-end']:
 check(variant+' ignores overworld sun and rain',all(abs(lookup[variant,0,n]-lookup[variant,k,n])<1e-6 for k in range(1,5) for n in range(6)))
check('Face shading is invariant under equivalent camera/sun rotation',all(abs(lookup[v,0,n]-lookup[v,5,n])<1e-6 for v in ['face','face-strong'] for n in range(6)))
check('All face samples finite bounded and nonblack',all(np.isfinite(v['value']) and .179<v['value']<=1.181 for v in d['faces']))
check('No GPU API errors',d['opengl_errors']==0)
summary={'scope':'Actual GLSL on Apple native OpenGL; 65536 map cells, 17 cloud renders, 216 face samples. Offline, not Minecraft visual QA or FPS.','checks':checks,'failures':sum(not c['passed'] for c in checks)}
(w/'gpu-checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(len(checks),'checks;',summary['failures'],'failures')
assert summary['failures']==0

from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
w=Path(__file__).parent;d=json.loads((w/'gpu.json').read_text());checks=[]
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok:print('FAIL',name)
def read(name):return np.fromfile(w/(name+'.rgba32f'),dtype=np.float32).reshape(256,256,4)
sun=read('sun-mask')[:,:,:3];tex=np.asarray(Image.open(w/'vanilla-sun-reference.png').convert('RGBA'))/255.
rgb=tex[:,:,:3];linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
t=np.clip((.6-.02)/(.65-.02),0,1);t=t*t*(3-2*t);colour=np.array([1,.53,.25])*(1-t)+np.array([1,.84,.61])*t
expected=linear*tex[:,:,3:]*colour*2.8;expected=np.repeat(np.repeat(expected,8,axis=0),8,axis=1)
check('Every sampled sun texel matches current vanilla RGB/alpha and documented HDR tint',np.max(np.abs(sun-expected))<2e-5)
check('Sun contains HDR core for existing highlight/bloom pipeline',np.max(sun)>1)
after=read('sun-after')[:,:,:3];zero=read('sun-zero')[:,:,:3];vanilla=read('sun-vanilla')[:,:,:3]
check('Sun visibility zero removes exactly the texture contribution',np.max(np.abs((after-zero)-sun*.85))<2e-5)
check('Native vanilla mode has no duplicate procedural disk',np.max(np.abs(vanilla-zero))<1e-6)
check('Sun renders finite and nonnegative',all(np.all(np.isfinite(read(name))) and np.min(read(name))>=0 for name in ['sun-after','sun-zero','sun-vanilla','sun-mask']))
faces={(f['variant'],f['condition'],f['normal']):f['value'] for f in d['faces']}
check('Default face result is 65% vanilla plus 35% previous physical result',all(abs(faces['face',k,n]-(.65*faces['face-vanilla',k,n]+.35*faces['face-before',k,n]))<1e-6 for k in range(6) for n in range(6)))
check('Camera rotation leaves mixture fixed in world space',all(abs(faces[v,0,n]-faces[v,5,n])<1e-6 for v in ['face','face-strong'] for n in range(6)))
for v in ['face','face-strong']:
 check(v+' sun reversal changes the facing side',faces[v,0,0]>faces[v,0,1]+.05 and faces[v,1,1]>faces[v,1,0]+.05)
 check(v+' rain softens directional contribution',abs(faces[v,2,0]-faces[v,2,1])<abs(faces[v,0,0]-faces[v,0,1]))
 check(v+' night and sealed cave disable solar side bias',all(abs(faces[v,k,0]-faces[v,k,1])<1e-6 for k in [3,4]))
for v in ['face-off','face-blend-off']:
 check(v+' is exact bypass',all(abs(f['value']-1)<1e-6 for f in d['faces'] if f['variant']==v))
for v in ['face-nether','face-end']:
 check(v+' preserves other-dimension response',all(abs(faces[v,0,n]-faces[v,k,n])<1e-6 for k in range(1,6) for n in range(6)))
check('All face samples finite and bounded',all(np.isfinite(f['value']) and .179<=f['value']<=1.181 for f in d['faces']))
fog={(f['variant'],f['case']):np.array(f['rgb']) for f in d['fog']}
check('Reproduced original dark unfogged leaf when all depth samples miss',np.max(np.abs(fog['before','missed_leaf']-[.01,.015,.01]))<1e-6)
check('Rejected-depth leaf now receives atmospheric scattering',np.min(fog['after','missed_leaf']-fog['before','missed_leaf'])>.1)
check('Valid cached depth is unchanged',np.max(np.abs(fog['after','matched_depth']-fog['before','matched_depth']))<1e-6)
check('Near foreground remains clear',np.max(np.abs(fog['after','clear_foreground']-fog['before','clear_foreground']))<1e-6)
check('Underwater fallback remains disabled',np.max(np.abs(fog['after','underwater']-fog['before','underwater']))<1e-6)
check('Far boundary receives opaque atmospheric colour',np.min(fog['after','chunk_border'])>.3)
check('Confidence transition never drops to unfogged black',all(np.min(fog['after','confidence_'+str(n)])>.1 for n in [10,11,12,13,15,20]))
check('All fog results finite',all(np.all(np.isfinite(v)) for v in fog.values()))
check('GPU API reports zero errors',d['opengl_errors']==0)
# Tone-map as final output does, for useful labelled offline inspection.
def display(data):
 rgb=data[:,:,:3]*2**.2;base=np.minimum(rgb,.6);rgb=base+.4*(1-np.exp(-np.maximum(rgb-.6,0)/.4));rgb=np.where(rgb<=.0031308,rgb*12.92,1.055*np.maximum(rgb,0)**(1/2.4)-.055);return Image.fromarray((np.clip(rgb,0,1)*255).astype('uint8')).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
canvas=Image.new('RGB',(768,350),'#181b20');draw=ImageDraw.Draw(canvas);draw.text((10,8),'OFFLINE GLSL - not Minecraft screenshots',fill='white')
for i,(name,title) in enumerate([('sun-before','1.6.5 round sun'),('sun-after','1.6.6 polished vanilla'),('sun-mask','Texture contribution')]):
 canvas.paste(display(read(name)),(i*256,56));draw.text((i*256+8,34),title,fill='white')
canvas.save(w/'offline-sun-preview.jpg')
canvas=Image.new('RGB',(768,220),'#181b20');draw=ImageDraw.Draw(canvas);draw.text((10,8),'OFFLINE FOG DEPTH-MISS REPRODUCTION - not an in-game capture',fill='white')
for i,(key,title) in enumerate([(('before','missed_leaf'),'1.6.5 missed leaf'),(('after','missed_leaf'),'1.6.6 fallback'),(('after','matched_depth'),'Valid cached sample')]):
 patch=np.tile(np.append(fog[key],1),(160,240,1));canvas.paste(display(patch),(i*256+8,54));draw.text((i*256+8,34),title,fill='white')
canvas.save(w/'offline-fog-preview.jpg')
result={'scope':'Actual expanded GLSL in native OpenGL. Offline, not Minecraft visual acceptance or FPS.','sun_renders':5,'fog_renders':22,'face_samples':288,'checks':checks,'failures':sum(not c['passed'] for c in checks)}
(w/'gpu-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(len(checks),'checks;',result['failures'],'failures');print('Fog before / after:',fog['before','missed_leaf'],fog['after','missed_leaf']);assert result['failures']==0

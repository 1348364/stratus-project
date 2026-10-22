from pathlib import Path
import sys,shutil
from PIL import Image
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve();old=(w/'baseline/shaders').resolve()
shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
base='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/options.glsl',p)+expand(p/'core/frame.glsl',p)
sunImage=Image.open(w/'vanilla-sun-reference.png').convert('RGBA');print('Sun dimensions:',sunImage.size);assert sunImage.size==(32,32);(w/'sun.rgba').write_bytes(sunImage.tobytes())
for name,r,values in [('sun-before',old,{}),('sun-after',p,{}),('sun-zero',p,{'SUN_VISIBILITY':'0.00'}),('sun-vanilla',p,{'SUN_STYLE':'1'}),('sun-mask',p,{})]:
 s=base+expand(r/'core/ceiling.glsl',r)+'''
in vec2 rasterUV;layout(location=0)out vec4 result;
void main(){
 vec3 sun=broadLightDirection();vec3 pole=abs(sun.z)<0.99?vec3(0,0,1):vec3(0,1,0);
 vec3 right=unitVector(cross(pole,sun)),up=cross(sun,right);
 vec3 ray=unitVector(sun+right*((rasterUV.x-.5)*.60)+up*((rasterUV.y-.5)*.60));
 result=vec4('''+('polishedVanillaSun(ray)' if name=='sun-mask' else 'skyBackdrop(ray)')+''',1.0);
}
'''
 (w/(name+'.fsh')).write_text(adapt(override(s,values),'.fsh'))
for name,r in [('fog-before',old),('fog-after',p)]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(r/'core/atmosphere-resolve.frag.glsl',r)
 # Isolate mist/depth reconstruction from unrelated physical cloud masks.
 (w/(name+'.fsh')).write_text(adapt(override(s,{'CLOUD_AMOUNT':'0.00','CIRRUS_AMOUNT':'0.00','MIST_BREAKUP':'0.00','MIST_LIGHT':'0.00'}),'.fsh'))
source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/water-resolve.frag.glsl',p)
(w/'current.fsh').write_text(adapt(override(source,{'WATER_EXTINCTION':'3.00','WATER_TURBIDITY':'6.00','WATER_VISIBILITY':'1.70'}),'.fsh'))
shutil.copy2('work/stratus-refine-164/fog_probe.c',w/'water_probe.c')
# Re-use the previous targeted face cases against CURRENT source, not old results.
for name,values in {'face':{},'face-strong':{'FACE_SHADING':'2.00'},'face-off':{'FACE_SHADING':'0.00'},'face-blend-off':{'FACE_BLEND':'0.00'},'face-nether':{'DIMENSION_TYPE':'-1'},'face-end':{'DIMENSION_TYPE':'1'}}.items():
 source=base+expand(p/'core/diffuse.glsl',p)+'''\nuniform vec3 probeNormal;uniform float probeSky;layout(location=0)out vec4 result;void main(){result=vec4(formIrradiance(probeNormal,probeSky),1);}\n'''
 (w/(name+'.fsh')).write_text(adapt(override(source,values),'.fsh'))
# An independent pure-vanilla reference for quantifying the 65/35 mixture.
source=base+expand(p/'core/diffuse.glsl',p)
source=source.replace('0.35*smoothstep(0.08,0.85,skyExposure)','0.0*smoothstep(0.08,0.85,skyExposure)')
source+='\nuniform vec3 probeNormal;uniform float probeSky;layout(location=0)out vec4 result;void main(){result=vec4(formIrradiance(probeNormal,probeSky),1);}\n'
(w/'face-vanilla.fsh').write_text(adapt(source,'.fsh'))
source=base+expand(old/'core/diffuse.glsl',old)+'\nuniform vec3 probeNormal;uniform float probeSky;layout(location=0)out vec4 result;void main(){result=vec4(formIrradiance(probeNormal,probeSky),1);}\n'
(w/'face-before.fsh').write_text(adapt(source,'.fsh'))

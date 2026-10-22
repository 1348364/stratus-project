from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
p=Path('outputs/Stratus/shaders').resolve();w=Path(__file__).parent
shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
base='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/options.glsl',p)+expand(p/'core/frame.glsl',p)
cloud=base+expand(p/'core/ceiling.glsl',p)
variants={'cloud':{},'cloud-low-off':{'CLOUD_AMOUNT':'0.00'},'cloud-upper-off':{'CIRRUS_AMOUNT':'0.00'},'cloud-other-low':{'CLOUD_AMOUNT':'0.35','CLOUD_SPAN':'900.0','CLOUD_DISTORTION':'2.00'},'cloud-detail-off':{'CLOUD_DETAIL':'0.00'},'cloud-detail-max':{'CLOUD_DETAIL':'2.00'}}
for name,v in variants.items():
 s=cloud+'''
uniform int probeMode;uniform float probeHeight;
layout(location=0)out vec4 result;
void main(){
 vec2 uv=gl_FragCoord.xy/256.0;
 if(probeMode==0){
   vec2 mapPoint=floor(gl_FragCoord.xy)+vec2(0.5);
   vec2 xz=(mapPoint-vec2(0,0.33))*max(CLOUD_SPAN*0.05,1.0);
   vec3 point=vec3(xz.x,CLOUD_ALTITUDE,xz.y);
   vec2 low=layeredCloudSample(point,true,false);
   result=vec4(vanillaCloudCell(mapPoint),low.x,low.y,1);
 }else if(probeMode==1){
   vec3 point=vec3((uv.x-0.5)*24000.0,CIRRUS_ALTITUDE,(uv.y-0.5)*24000.0);
   result=vec4(layeredCloudSample(point,true,true),0,1);
 }else{
   float azimuth=(uv.x-0.5)*6.283185307;
   float elevation=mix(-0.15,1.45,uv.y);
   vec3 ray=vec3(cos(azimuth)*cos(elevation),sin(elevation),sin(azimuth)*cos(elevation));
   vec4 c=marchCloudLayer(vec3(4096,probeHeight,4096),ray,7000.,72,true);
   result=vec4(mix(skyBackdrop(ray),c.rgb,c.a),c.a);
 }
}
'''
 (w/(name+'.fsh')).write_text(adapt(override(s,v),'.fsh'))
face=base+expand(p/'core/diffuse.glsl',p)+'''
uniform vec3 probeNormal;uniform float probeSky;
layout(location=0)out vec4 result;
void main(){result=vec4(formIrradiance(probeNormal,probeSky),1);}
'''
for name,v in {'face':{},'face-strong':{'FACE_SHADING':'2.00'},'face-off':{'FACE_SHADING':'0.00'},'face-blend-off':{'FACE_BLEND':'0.00'},'face-nether':{'DIMENSION_TYPE':'-1'},'face-end':{'DIMENSION_TYPE':'1'}}.items():
 (w/(name+'.fsh')).write_text(adapt(override(face,v),'.fsh'))
# Unchanged moisture and water regressions use the current expanded shaders.
source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/water-resolve.frag.glsl',p)
(w/'current.fsh').write_text(adapt(override(source,{'WATER_EXTINCTION':'3.00','WATER_TURBIDITY':'6.00','WATER_VISIBILITY':'1.70'}),'.fsh'))
for name in ['fog_probe.c']:
 shutil.copy2(Path('work/stratus-refine-164')/name,w/name)
from PIL import Image
image=Image.open(w/'vanilla-clouds-reference.png').convert('RGBA')
assert image.size==(256,256)
(w/'clouds.rgba').write_bytes(image.tobytes())
print('Prepared actual cloud/shading shaders, runtime vanilla test texture and water regression.')

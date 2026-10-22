from pathlib import Path
import sys, shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve();old=(w/'baseline/shaders').resolve()
shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
variants={'current':{'REALISTIC_LIGHTING':'1'},'before':{'REALISTIC_LIGHTING':'1'},'no-vanilla':{'VANILLA_FACE_CONTRAST':'0.00'},'no-realistic':{'REALISTIC_FACE_CONTRAST':'0.00'},'no-faces':{'VANILLA_FACE_CONTRAST':'0.00','REALISTIC_FACE_CONTRAST':'0.00'},'master-off':{'FACE_SHADING':'0.00'},'wet-off':{'WET_SHEEN':'0.00'},'wet-max':{'WET_SHEEN':'2.00'},'cirrus-off':{'CIRRUS_DENSITY':'0.00'},'lower-off':{'CLOUD_AMOUNT':'0.00'},'nether':{'DIMENSION_TYPE':'-1'},'weather-only':{'WET_WEATHER_MODE':'1'},'vanilla':{'REALISTIC_LIGHTING':'0'},'vanilla-extreme':{'REALISTIC_LIGHTING':'0','SKY_AMBIENT':'4.00','LAMP_LEVEL':'3.00','LAMP_HEAT':'1.50','FACE_SHADING':'2.00','GROUND_WARMTH':'2.00'},'dry':{'SURFACE_DAMPNESS':'0.00'}}
for name,v in variants.items():
 if name not in ('vanilla','vanilla-extreme'):v={'REALISTIC_LIGHTING':'1',**v}
 r=old if name=='before' else p
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(r/'core/options.glsl',r)+expand(r/'core/frame.glsl',r)+expand(r/'core/ceiling.glsl',r)+expand(r/'core/diffuse.glsl',r)
 s+='''
uniform int probeMode;uniform vec3 probeNormal,probePoint;uniform float probeSky,probeAbsorb,probeRough;
layout(location=0)out vec4 result;
void main(){
 if(probeMode==0)result=vec4(formIrradiance(probeNormal,probeSky),1);
 else if(probeMode==1)result=vec4(wetSurfaceResponse(vec3(.3,.2,.1),probeNormal,probePoint,probeSky,vec2(probeAbsorb,probeRough)),1);
 else if(probeMode==2)result=vec4(layeredCloudSample(probePoint,true,true),0,1);
 else result=vec4(diffuseRadiance(vec3(.7,.4,.2),vec3(.65,.8,.9),probeSky,probeNormal,1.3,probePoint,4111),1);
}
'''
 (w/(name+'.fsh')).write_text(adapt(override(s,v),'.fsh'))
s=Path('work/stratus-refine-167/probe.c').read_text().replace('j<11','j<15').replace('mode<3','mode<4')
s=s.replace('"lower-off","nether"','"lower-off","nether","weather-only","vanilla","vanilla-extreme","dry"')
s=s.replace('int cases=mode==0?24:(mode==1?9:16);','int cases=mode==0?24:(mode==1?9:(mode==2?16:4));')
s=s.replace('if(mode==2)glUniform3f','if(mode==3){scalar(p,"probeSky",k==0?0:1);integer(p,"worldTime",k==2?18000:6000);scalar(p,"rainStrength",k==3?1:0);}\n if(mode==2)glUniform3f')
(w/'probe.c').write_text(s)
# Actual output shader, with an input texture supplied by the probe.
for name,v in {'output-vanilla':{'REALISTIC_LIGHTING':'0'},'output-vanilla-extreme':{'REALISTIC_LIGHTING':'0','EXPOSURE':'3.00','WHITE_BALANCE':'0.24','SURFACE_SATURATION':'2.00','BLOOM_STRENGTH':'1.00'},'output-enhanced':{'REALISTIC_LIGHTING':'1'}}.items():
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/output.frag.glsl',p)
 (w/(name+'.fsh')).write_text(adapt(override(s,v),'.fsh'))
water='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/water-resolve.frag.glsl',p)
(w/'water.fsh').write_text(adapt(water,'.fsh'))
shutil.copy2('work/stratus-refine-167/water_probe.c',w/'water_probe.c')
# Matched full atmosphere integration, rather than a mirror of the shader.
for name,r in [('atmosphere-before',old),('atmosphere-after',p)]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(r/'core/options.glsl',r)+expand(r/'core/frame.glsl',r)+expand(r/'core/ceiling.glsl',r)+expand(r/'core/volume.glsl',r)
 s+='''
uniform int probeScene;
layout(location=0)out vec4 result;
void main(){
 vec2 uv=gl_FragCoord.xy/128.0;
 float azimuth=(uv.x-.5)*6.283185307;
 float elevation=mix(-.1,1.4,uv.y);
 vec3 ray=vec3(cos(azimuth)*cos(elevation),sin(elevation),sin(azimuth)*cos(elevation));
 float height=probeScene==1?256.0:(probeScene==2?400.0:64.0);
 float limit=probeScene==3?140.0:7000.0;
 vec4 v=completeAtmosphereSegment(vec3(4096,height,4096),ray,limit,1.0,true);
 result=vec4(v.rgb*v.a,v.a);
}
'''
 (w/(name+'.fsh')).write_text(adapt(s,'.fsh'))
shutil.copy2('work/stratus-clouds-165/clouds.rgba',w/'clouds.rgba')
print('Prepared actual lighting, film, output, water and atmosphere shader probes.')

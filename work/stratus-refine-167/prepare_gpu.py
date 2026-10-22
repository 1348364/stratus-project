from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve();old=(w/'baseline/shaders').resolve();shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
variants={'current':{},'before':{},'no-vanilla':{'VANILLA_FACE_CONTRAST':'0.00'},'no-realistic':{'REALISTIC_FACE_CONTRAST':'0.00'},'no-faces':{'VANILLA_FACE_CONTRAST':'0.00','REALISTIC_FACE_CONTRAST':'0.00'},'master-off':{'FACE_SHADING':'0.00'},'wet-off':{'WET_SHEEN':'0.00'},'wet-max':{'WET_SHEEN':'2.00'},'cirrus-off':{'CIRRUS_DENSITY':'0.00'},'lower-off':{'CLOUD_AMOUNT':'0.00'},'nether':{'DIMENSION_TYPE':'-1'}}
for name,v in variants.items():
 r=old if name=='before' else p
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(r/'core/options.glsl',r)+expand(r/'core/frame.glsl',r)+expand(r/'core/ceiling.glsl',r)+expand(r/'core/diffuse.glsl',r)
 s+='''
uniform int probeMode;uniform vec3 probeNormal,probePoint;uniform float probeSky,probeAbsorb,probeRough;
layout(location=0)out vec4 result;
void main(){
 if(probeMode==0)result=vec4(formIrradiance(probeNormal,probeSky),1);
 else if(probeMode==1)result=vec4(wetSurfaceResponse(vec3(.3,.2,.1),probeNormal,probePoint,probeSky,vec2(probeAbsorb,probeRough)),1);
 else result=vec4(layeredCloudSample(probePoint,true,true),0,1);
}
'''
 (w/(name+'.fsh')).write_text(adapt(override(s,v),'.fsh'))
s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/water-resolve.frag.glsl',p)
(w/'water.fsh').write_text(adapt(s,'.fsh'));shutil.copy2('work/stratus-refine-166/water_probe.c',w/'water_probe.c')
s=(w/'water_probe.c').read_text().replace('current.fsh','water.fsh');(w/'water_probe.c').write_text(s)

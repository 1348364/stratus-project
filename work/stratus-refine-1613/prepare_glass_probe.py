from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve()
for tag,vals in {'solid-off':{'TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'},'solid-reflection':{'TRANSPARENT_REFLECTIONS':'0.75','TRANSPARENT_REFRACTION':'0.00'},'solid-refraction':{'TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'2.00'},'solid-both':{'TRANSPARENT_REFLECTIONS':'0.75','TRANSPARENT_REFRACTION':'2.00'}}.items():
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/options.glsl',p)+expand(p/'core/frame.glsl',p)+'\nuniform sampler2D colortex3,depthtex0,depthtex1;\n'+expand(p/'core/transparent-optics.glsl',p)
 s+='\nin vec2 rasterUV;layout(location=0)out vec4 result;void main(){result=vec4(transparentSolidOptics(texture(colortex3,rasterUV).rgb,rasterUV),1);}\n'
 (w/(tag+'.fsh')).write_text(adapt(override(s,vals),'.fsh'))

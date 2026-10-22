from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt
w=Path(__file__).parent
for name,root in [('atmosphere-before',(w/'baseline/shaders').resolve()),('atmosphere-after',Path('outputs/Stratus/shaders').resolve())]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+''.join(expand(root/f'core/{n}.glsl',root) for n in ['options','frame','ceiling','volume'])
 s+='''
uniform int probeScene;layout(location=0)out vec4 result;
void main(){vec2 uv=gl_FragCoord.xy/128.0;float azimuth=(uv.x-.5)*6.283185307;float elevation=mix(-.1,1.4,uv.y);vec3 ray=vec3(cos(azimuth)*cos(elevation),sin(elevation),sin(azimuth)*cos(elevation));int scene=probeScene%4;float height=scene==1?256.0:(scene==2?400.0:64.0);float limit=scene==3?140.0:7000.0;vec4 v=completeAtmosphereSegment(vec3(4096,height,4096),ray,limit,1.0,true);result=vec4(v.rgb*v.a,v.a);}
''';(w/(name+'.fsh')).write_text(adapt(s,'.fsh'))
shutil.copy2('work/stratus-clouds-165/clouds.rgba',w/'clouds.rgba')
s=Path('work/stratus-refine-168/isolate_probe.c').read_text();start=s.index(' const char*outputs[]=');end=s.index(' const char*labels[]=',start);s=s[:start]+''' printf("{\\\"scope\\\":\\\"Actual full atmosphere before/after with unchanged budgets, day/night; GPU microbenchmark, not FPS\\\",\\\"timings\\\":[");int serial=0;\n'''+s[end:]
s=s.replace('const char*labels[]={"before","after","hoist","bounds"};GLuint programs[]={make_program(root,"atmosphere-before"),make_program(root,"atmosphere-after"),make_program(root,"atmosphere-hoist"),make_program(root,"atmosphere-bounds")}', 'const char*labels[]={"before","after"};GLuint programs[]={make_program(root,"atmosphere-before"),make_program(root,"atmosphere-after")}')
s=s.replace('printf("],\\\"timings\\\":[");serial=0;','serial=0;').replace('scene<4','scene<8').replace('o<4','o<2').replace('(round+o)%4','(round+o)%2').replace('iuniform(p,"worldTime",6000)','iuniform(p,"worldTime",scene<4?6000:18000)')
(w/'mist_probe.c').write_text(s)

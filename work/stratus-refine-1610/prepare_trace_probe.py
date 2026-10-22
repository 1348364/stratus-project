from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt
w=Path(__file__).parent;old=(w/'baseline/shaders').resolve();new=Path('outputs/Stratus/shaders').resolve();shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
for name,root in [('trace-before',old),('trace-after',new)]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(root/'core/options.glsl',root)+expand(root/'core/frame.glsl',root)+'uniform sampler2D depthtex1,colortex4;\n'+expand(root/'core/scene-trace.glsl',root)
 s+='''
in vec2 rasterUV;uniform int probeMode,probeQuality;layout(location=0)out vec4 result;
void main(){
 if(probeMode==0){vec4 n;vec3 p=opticsReceiver(ivec2(gl_FragCoord.xy),n,false);result=vec4(p,n.a);}
 else{float path;vec3 direction=unitVector(vec3((rasterUV.x-.5)*1.4,(rasterUV.y-.5)*.8,-1));vec4 h=traceOpticalScene(vec3(0,0,-2),direction,vec3(0,0,-1),1,probeQuality,120,false,path);result=vec4(h.rgb,h.a>0?path:0);}
}
''';(w/(name+'.fsh')).write_text(adapt(s,'.fsh'))
s='#version 330 compatibility\n'+expand(new/'core/frame.glsl',new)+'''
uniform sampler2D depthtex1,normalTex;in vec2 rasterUV;layout(location=0)out vec4 opaqueReceiverNormal;
void main(){float z=texture(depthtex1,rasterUV).r;bool geometry=z<.999999;vec3 viewPoint=positionFromDepth(rasterUV,min(z,.999999));vec4 normalData=texture(normalTex,rasterUV);
'''
# Use the exact current producer statements, not a second implementation.
r=(new/'core/resolve.frag.glsl').read_text();a=r.index('    vec3 receiverNormal=');b=r.index('\n    emptyWaterTint=',a);s+=r[a:b]+'\n}\n';(w/'trace-planes.fsh').write_text(adapt(s,'.fsh'))

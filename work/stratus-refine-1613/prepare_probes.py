from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve()
for tag in ['legacy','native']:
 d=w/tag;d.mkdir(exist_ok=True);shutil.copy2(w/'screen.vsh',d/'screen.vsh');shutil.copy2(w/('water-'+tag+'.fsh'),d/'water.fsh')
# Native expectation runs the same full-res resolve and real exit/glass/particle inputs.
s=(w/'water_probe.c').read_text();s=s.replace('static float body[3],sigma[3];','''static float body[3],sigma[3];
static float enc(float x){return x<=.0031308f?12.92f*x:1.055f*powf(x,1.f/2.4f)-.055f;}
static float dec(float x){return x<=.04045f?x/12.92f:powf((x+.055f)/1.055f,2.4f);}
static float fogC[3]={.03f,.09f,.2f};
static float trans(float d){return fmaxf(0,fminf(1,1-d/16.f));}
''')
s=s.replace('GLuint p=makeProgram(argv[1]);glUseProgram(p);','GLuint p=makeProgram(argv[1]);glUseProgram(p);glUniform1f(glGetUniformLocation(p,"fogStart"),0);glUniform1f(glGetUniformLocation(p,"fogEnd"),16);glUniform3fv(glGetUniformLocation(p,"fogColor"),1,fogC);')
a='float expected[3],back[3];water(opaque,bg,back);for(int j=0;j<3;j++){float att=expf(-sigma[j]*fg);if(cases[k].tr>=.999)expected[j]=back[j]+(scene[j]-opaque[j])*att;else expected[j]=back[j]*cases[k].tr+fore[j]*(1-cases[k].tr)*att+body[j]*(1-cases[k].tr)*(1-att);}'
b='''float expected[3];for(int j=0;j<3;j++){float att=trans(fg),back=enc(opaque[j])*trans(bg)+fogC[j]*(1-trans(bg));float display;if(cases[k].tr>=.999)display=back+(enc(scene[j])-enc(opaque[j]))*att;else{float foreground=fmaxf(enc(scene[j])-enc(opaque[j])*cases[k].tr,0.f)*att+fogC[j]*(1-cases[k].tr)*(1-att);display=back*cases[k].tr+foreground;}expected[j]=dec(display);}''';assert a in s;s=s.replace(a,b);(w/'native_water_probe.c').write_text(s)
for tag,values in {'wet-current':{},'wet-film-zero':{'SURFACE_DAMPNESS':'0.00'},'wet-sheen-zero':{'WET_SHEEN':'0.00'},'wet-rain-only':{'WET_WEATHER_MODE':'1'}}.items():
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/options.glsl',p)+expand(p/'core/frame.glsl',p)+expand(p/'core/ceiling.glsl',p)+expand(p/'core/diffuse.glsl',p)
 s+='\nuniform vec3 probeNormal,probePoint;uniform float probeSky;layout(location=0)out vec4 result;void main(){result=vec4(wetSurfaceResponse(vec3(.3,.2,.1),probeNormal,probePoint,probeSky,vec2(0,.4)),1);}\n';(w/(tag+'.fsh')).write_text(adapt(override(s,values),'.fsh'))
print('Prepared native/legacy full resolve and six-face actual wet-film shader variants.')

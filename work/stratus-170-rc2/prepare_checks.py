from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import expand,adapt,override
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders').resolve();shutil.copy2('work/stratus-refine-1613/screen.vsh',w/'screen.vsh')
vertex='''#version 330 core
uniform int probeMaterial;uniform vec3 probeNormal;
out vec4 tintAndOpacity;out vec2 atlasCoordinate;out vec2 illuminationCoordinate;out vec3 relativeLocation;out vec3 orientedNormal;flat out int blockCategory;
void main(){vec2 q=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(q*2.-1.,0,1);tintAndOpacity=vec4(1);atlasCoordinate=vec2(.5);illuminationCoordinate=vec2(.95);relativeLocation=vec3(0,0,-3);orientedNormal=probeNormal;blockCategory=probeMaterial;}
'''
(w/'raster.vsh').write_text(vertex)
for tag,kind,extra in [('terrain',3,{}),('underside',6,{}),('underside-half',6,{'WATER_TEXTURE':'0.50'}),('underside-zero',6,{'WATER_TEXTURE':'0.00'}),('underside-stratus',6,{'WATER_STYLE':'0'})]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n#define PASS_KIND '+str(kind)+'\n#define LATE_SURFACE '+('1' if kind==6 else '0')+'\n'+expand(p/'core/raster.frag.glsl',p)
 (w/(tag+'.fsh')).write_text(adapt(override(s,extra),'.fsh'))
s='#version 330 compatibility\n'+expand(p/'core/entity-lighting.glsl',p)+'\nuniform vec3 probeNormal;layout(location=0)out vec4 result;void main(){result=vec4(vec3(nativeEntityLighting(probeNormal)),1);}\n';(w/'entity.fsh').write_text(adapt(s,'.fsh'))
for tag,root in [('atmos-before',(w/'baseline/shaders').resolve()),('atmos-after',p)]:
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(root/'core/atmosphere-resolve.frag.glsl',root)
 (w/(tag+'.fsh')).write_text(adapt(override(s,{'TRANSPARENT_REFLECTIONS':'0.00','TRANSPARENT_REFRACTION':'0.00'}),'.fsh'))
# Reuse the actual prior resolve probe, expanded against current source.
for mode in ['legacy','native']:
 d=w/mode;d.mkdir(exist_ok=True);shutil.copy2(w/'screen.vsh',d/'screen.vsh');s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/water-resolve.frag.glsl',p)
 (d/'water.fsh').write_text(adapt(override(s,{'WATER_STYLE':'0' if mode=='legacy' else '1'}),'.fsh'))
for n in ['water_probe','native_water_probe','wet_probe']:shutil.copy2(Path('work/stratus-refine-1613')/n,w/n)
for tag,vals in {'wet-current':{},'wet-film-zero':{'SURFACE_DAMPNESS':'0.00'},'wet-sheen-zero':{'WET_SHEEN':'0.00'},'wet-rain-only':{'WET_WEATHER_MODE':'1'}}.items():
 s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(p/'core/options.glsl',p)+expand(p/'core/frame.glsl',p)+expand(p/'core/ceiling.glsl',p)+expand(p/'core/diffuse.glsl',p)+'\nuniform vec3 probeNormal,probePoint;uniform float probeSky;layout(location=0)out vec4 result;void main(){result=vec4(wetSurfaceResponse(vec3(.3,.2,.1),probeNormal,probePoint,probeSky,vec2(0,.4)),1);}\n'
 (w/(tag+'.fsh')).write_text(adapt(override(s,vals),'.fsh'))
print('Prepared current actual raster, entity, underwater and atmosphere programs.')

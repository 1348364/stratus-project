from pathlib import Path
import sys,shutil,json
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
from prepare import expand,adapt,override
w=Path('work/stratus-refine-164');root=Path('outputs/Stratus/shaders').resolve()
shutil.copy2('work/stratus-water-163/screen.vsh',w/'screen.vsh')
shutil.copy2('work/stratus-water-163/raster.vsh',w/'raster.vsh')
for name in ['fog_probe.c','raster_probe.c']:shutil.copy2(Path('work/stratus-water-163')/name,w/name)
source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(root/'core/water-resolve.frag.glsl',root)
(w/'current.fsh').write_text(adapt(override(source,{'WATER_EXTINCTION':'3.00','WATER_TURBIDITY':'6.00','WATER_VISIBILITY':'1.70'}),'.fsh'))
source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n#define PASS_KIND 6\n#define LATE_SURFACE 1\n'+expand(root/'core/raster.frag.glsl',root)
(w/'raster.fsh').write_text(adapt(source,'.fsh'))
variants={'saved':{'WET_SHEEN':'.65'},'retention-off':{'WET_SHEEN':'0.00'},'retention-max':{'WET_SHEEN':'2.00'},'dampness-off':{'SURFACE_DAMPNESS':'0.00'},'dampness-max':{'SURFACE_DAMPNESS':'3.00'},'nether':{'DIMENSION_TYPE':'-1'},'end':{'DIMENSION_TYPE':'1'}}
for name,values in variants.items():
 source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(root/'core/options.glsl',root)+expand(root/'core/frame.glsl',root)+expand(root/'core/diffuse.glsl',root)
 source+='\nuniform vec3 probeDry,probeNormal,probePoint;\nuniform float probeSky,probeAbsorption;\nlayout(location=0) out vec4 result;\nvoid main(){result=vec4(wetSurfaceResponse(probeDry,probeNormal,probePoint,probeSky,vec2(probeAbsorption,.8)),retainedSurfaceMoisture(probeSky,probeNormal,probeAbsorption));}\n'
 (w/(name+'.fsh')).write_text(adapt(override(source,values),'.fsh'))
(w/'gpu-variants.json').write_text(json.dumps(variants,indent=2)+'\n')
print('Prepared actual current water shaders and seven matte-material variants.')

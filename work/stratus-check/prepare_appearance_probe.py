from pathlib import Path
from prepare import expand,override,adapt
work=Path('work/stratus-check');out=work/'appearance-probe';out.mkdir(exist_ok=True)
(out/'screen.vsh').write_text('#version 330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.0-1.0,0.0,1.0);}\n')
root=Path('outputs/Stratus/shaders');source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'
for lib in ['options','frame','ceiling','diffuse','medium']:
 source+=expand(root/'core'/f'{lib}.glsl',root)+'\n'
source+='''
uniform float probeDistance;
layout(location=0) out vec4 result;
void main(){
 int c=int(probeDistance+0.5);vec3 base=vec3(0.5);vec3 n=vec3(0,1,0);vec3 p=vec3(0);
 if(c==0)result=vec4(dampDiffuseColour(base,1,n,1.3,p),1);
 if(c==1)result=vec4(dampDiffuseColour(base,1,n,1.3,vec3(100000,87,-524)),1);
 if(c==2)result=vec4(dampDiffuseColour(base,0,n,1.3,p),1);
 if(c==3)result=vec4(dampDiffuseColour(base,1,n,1.0,p),1);
 if(c==4)result=vec4(abs(dampDiffuseColour(base,1,n,1.1,p)-dampDiffuseColour(base,1,n,1.3,p)),1);
 if(c==5)result=vec4(abs(dampDiffuseColour(base,1,n,1.3,p)-dampDiffuseColour(base,1,vec3(1,0,0),1.3,p)),1);
 if(c==6)result=vec4(abs(travelThroughWater(travelThroughWater(base,2,1),3,1)-travelThroughWater(base,5,1)),1);
 if(c==7)result=vec4(travelThroughWater(base,2,1),1);
 if(c==8)result=vec4(travelThroughWater(base,8,1),1);
 if(c==9)result=vec4(physicalCloudLayer(vec3(200,140,200),normalize(vec3(0.2,1,0.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,245,200),normalize(vec3(0.2,-1,0.1)),7000).a,1);
 if(c==10)result=vec4(physicalCloudLayer(vec3(200,140,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(0,1,0),10).a,1);
 if(c==11)result=vec4(skyBackdrop(broadLightDirection()),1);
 if(c==12)result=vec4(diffuseRadiance(base,vec3(0.8),0,n,1.3,p),1);
}
'''
for name,values in [('current',{}),('previous',{'FACE_SHADING':'0.00','SKY_LEAK':'0.00'})]:
 (out/f'{name}.fsh').write_text(adapt(override(source,values),'.fsh'))
c=(work/'air_probe.c').read_text()
a=c.index('    struct { const char *name;');b=c.index('    printf(',a)
rows=['wet_origin','wet_far_away','covered_dry','entity_dry','all_materials_same','all_faces_same','water_split_path','water_two_blocks','water_eight_blocks','cloud_below_inside_above','cloud_direction_and_occlusion','sky_light_leak','face_shading']
cases=',\n'.join('{"'+name+'",'+str(i)+',1,0,0,0}' for i,name in enumerate(rows))
c=c[:a]+'    struct { const char *name; float distance, sky; int eye; float status; int mode; } cases[] = {\n'+cases+'\n};\n'+c[b:]
(work/'appearance_probe.c').write_text(c)
print('Prepared 13 GPU probe cases from actual GLSL libraries')

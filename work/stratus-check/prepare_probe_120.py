from pathlib import Path
from prepare import expand,override,adapt
work=Path('work/stratus-check');out=work/'probe-120';out.mkdir(exist_ok=True)
(out/'screen.vsh').write_text('#version 330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.0-1.0,0.0,1.0);}\n')
root=Path('outputs/Stratus/shaders');source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'
for lib in ['options','frame','ceiling','diffuse','medium']:source+=expand(root/'core'/f'{lib}.glsl',root)+'\n'
cases=[
 ('wet_absorption', 'absorbedWetAlbedo(vec3(0.08,0.25,0.60),outdoorMoisture(1.0,1.3),0.58)',0),
 ('covered_moisture', 'vec3(outdoorMoisture(0.0,1.3))',0),
 ('entity_moisture', 'vec3(outdoorMoisture(1.0,1.0))',0),
 ('smooth_material_absorption', 'absorbedWetAlbedo(vec3(0.08,0.25,0.60),outdoorMoisture(1.0,1.3),0.04)',0),
 ('wet_grazing', 'diffuseRadiance(vec3(0.1),vec3(0.8),1.0,vec3(0,1,0),1.3,vec3(0,-0.15,-10),4112)',0),
 ('wet_front', 'diffuseRadiance(vec3(0.1),vec3(0.8),1.0,vec3(0,1,0),1.3,vec3(0,-10,0),4112)',0),
 ('entity_top', 'diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_side', 'diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(1,0,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_bottom', 'diffuseRadiance(vec3(0.65),vec3(0.8),1.0,vec3(0,-1,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_in_darkness', 'diffuseRadiance(vec3(0.85),vec3(0),0.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112)',0),
 ('emissive_in_darkness', 'diffuseRadiance(vec3(0.95),vec3(0),0.0,vec3(0,1,0),2.0,vec3(0,0,-10),4101)',0),
 ('billboard_orientation', 'abs(diffuseRadiance(vec3(0.5),vec3(0.8),1.0,vec3(0,1,0),0.8,vec3(0,0,-10),4112)-diffuseRadiance(vec3(0.5),vec3(0.8),1.0,vec3(1,0,0),0.8,vec3(0,0,-10),4112))',0),
 ('water_split_path', 'abs(travelThroughWater(travelThroughWater(vec3(0.5),2,1),3,1)-travelThroughWater(vec3(0.5),5,1))',0),
 ('water_twenty_blocks', 'travelThroughWater(vec3(0.5),20,1)',0),
 ('cloud_volume_y', 'vec3(smoothVolume(vec3(1.2,0.3,4.5)),smoothVolume(vec3(1.2,0.9,4.5)),smoothVolume(vec3(1.2,1.6,4.5)))',0),
 ('cloud_view_alpha', 'vec3(physicalCloudLayer(vec3(200,140,200),normalize(vec3(0.2,1,0.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,245,200),normalize(vec3(0.2,-1,0.1)),7000).a)',0),
 ('cloud_occlusion', 'vec3(physicalCloudLayer(vec3(200,140,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,140,200),vec3(0,1,0),10).a)',0),
 ('cloud_shadow', 'vec3(cloudSunTransmission(vec3(200,180,200)),cloudSunTransmission(vec3(200,205,200)),cloudSunTransmission(vec3(200,240,200)))',0),
 ('sun_day', 'skyBackdrop(broadLightDirection())',0),
 ('sun_night', 'skyBackdrop(broadLightDirection())',1),
 ('sky_away_from_sun', 'skyBackdrop(-broadLightDirection())',0),
]
source+='\nuniform float probeDistance;\nlayout(location=0) out vec4 result;\nvoid main(){\nint c=int(probeDistance+0.5);\n'
for i,(_,expr,_) in enumerate(cases):source+=f'if(c=={i}) result=vec4({expr},1.0);\n'
source+='}\n'
for name,values in [('current',{}),('previous',{'FACE_SHADING':'0.00','WET_SHEEN':'0.00','SUN_VISIBILITY':'0.00','WATER_VISIBILITY':'4.00'})]:(out/f'{name}.fsh').write_text(adapt(override(source,values),'.fsh'))
c=(work/'appearance_probe.c').read_text();a=c.index('    struct { const char *name;');b=c.index('    printf(',a)
rows=',\n'.join('{"'+name+'",'+str(i)+',1,0,0,'+str(mode)+'}' for i,(name,_,mode) in enumerate(cases))
c=c[:a]+'    struct { const char *name; float distance, sky; int eye; float status; int mode; } cases[] = {\n'+rows+'\n};\n'+c[b:]
c=c.replace('integer(p, "worldTime", 6000);','integer(p, "worldTime", mode == 1 ? 18000 : 6000);')
(work/'probe_120.c').write_text(c)
print('Prepared',len(cases),'cases executing the delivered GLSL libraries.')

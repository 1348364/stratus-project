from pathlib import Path
from prepare import expand,override,adapt
work=Path('work/stratus-check');out=work/'probe-130';out.mkdir(exist_ok=True)
(out/'screen.vsh').write_text('#version 330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.0-1.0,0.0,1.0);}\n')
root=Path('outputs/Stratus/shaders');source='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'
for lib in ['options','frame','ceiling','volume','diffuse','medium']:source+=expand(root/'core'/f'{lib}.glsl',root)+'\n'
cases=[
 ('covered_moisture','vec3(outdoorMoisture(0.0,1.3))',0),
 ('entity_moisture','vec3(outdoorMoisture(1.0,1.0))',0),
 ('wet_absorption','absorbedWetAlbedo(vec3(.08,.25,.60),outdoorMoisture(1.0,1.3),.58)',0),
 ('wet_grazing','diffuseRadiance(vec3(.1),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,-.15,-10),4112)',0),
 ('entity_top','diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_side','diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(1,0,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_bottom','diffuseRadiance(vec3(.65),vec3(.8),1.0,vec3(0,-1,0),1.0,vec3(0,0,-10),4112)',0),
 ('entity_in_darkness','diffuseRadiance(vec3(.85),vec3(0),0.0,vec3(0,1,0),1.0,vec3(0,0,-10),4112)',0),
 ('emissive_in_darkness','diffuseRadiance(vec3(.95),vec3(0),0.0,vec3(0,1,0),2.0,vec3(0,0,-10),4101)',0),
 ('billboard_orientation','abs(diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),.8,vec3(0,0,-10),4112)-diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(1,0,0),.8,vec3(0,0,-10),4112))',0),
 ('water_split_path','abs(travelThroughWater(travelThroughWater(vec3(.5),2,1),3,1)-travelThroughWater(vec3(.5),5,1))',0),
 ('water_two_blocks','travelThroughWater(vec3(.5),2,1)',0),
 ('water_eight_blocks','travelThroughWater(vec3(.5),8,1)',0),
 ('water_twenty_blocks','travelThroughWater(vec3(.5),20,1)',0),
 ('face_top','formIrradiance(vec3(0,1,0),1.0)',0),
 ('face_east','formIrradiance(vec3(1,0,0),1.0)',0),
 ('face_west','formIrradiance(vec3(-1,0,0),1.0)',0),
 ('face_south','formIrradiance(vec3(0,0,1),1.0)',0),
 ('face_north','formIrradiance(vec3(0,0,-1),1.0)',0),
 ('face_bottom','formIrradiance(vec3(0,-1,0),1.0)',0),
 ('ground_warmth','diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,0,-10),4112)',0),
 ('ground_night','diffuseRadiance(vec3(.5),vec3(.8),1.0,vec3(0,1,0),1.3,vec3(0,0,-10),4112)',1),
 ('simplex_xyz','vec3(simplexVolume(vec3(1.2,.3,4.5)),simplexVolume(vec3(1.2,.9,4.5)),simplexVolume(vec3(1.2,1.6,4.5)))',0),
 ('cloud_view_alpha','vec3(physicalCloudLayer(vec3(200,100,200),normalize(vec3(.2,1,.1)),7000).a,physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,285,200),normalize(vec3(.2,-1,.1)),7000).a)',0),
 ('cloud_occlusion','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,-1,0),7000).a,physicalCloudLayer(vec3(200,100,200),vec3(1,0,0),7000).a,physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),10).a)',0),
 ('cirrus_alpha','vec3(marchSingleCloud(vec3(200,290,200),vec3(0,1,0),7000,8,false,true).a)',0),
 ('mist_xyz','vec3(mistDensityWorld(vec3(0,70,0)),mistDensityWorld(vec3(100,70,100)),mistDensityWorld(vec3(0,120,0)))',0),
 ('mist_near_clear','vec3(volumetricMist(cameraPosition,vec3(1,0,0),60,1,8).a)',0),
 ('mist_covered','vec3(volumetricMist(cameraPosition,vec3(1,0,0),300,0,8).a)',0),
 ('mist_far','vec3(volumetricMist(cameraPosition,vec3(1,0,0),300,1,8).a)',0),
 ('sun_colour','sunlightColour()',0),
 ('sun_day','skyBackdrop(broadLightDirection())',0),
 ('sun_night','skyBackdrop(broadLightDirection())',1),
 ('sky_away_from_sun','skyBackdrop(-broadLightDirection())',0),
]
source+='\nuniform float probeDistance;\nlayout(location=0) out vec4 result;\nvoid main(){\nint c=int(probeDistance+0.5);\n'
for i,(_,expr,_) in enumerate(cases):source+=f'if(c=={i})result=vec4({expr},1.0);\n'
source+='}\n'
for name,values in [('current',{}),('previous',{'FACE_BLEND':'0.00','GROUND_WARMTH':'0.00','SUN_VISIBILITY':'0.00','WATER_VISIBILITY':'4.00'})]:(out/f'{name}.fsh').write_text(adapt(override(source,values),'.fsh'))
c=(work/'appearance_probe.c').read_text();a=c.index('    struct { const char *name;');b=c.index('    printf(',a)
rows=',\n'.join('{"'+name+'",'+str(i)+',1,0,0,'+str(mode)+'}' for i,(name,_,mode) in enumerate(cases))
c=c[:a]+'    struct { const char *name; float distance,sky; int eye; float status; int mode; } cases[]={\n'+rows+'\n};\n'+c[b:]
c=c.replace('integer(p, "worldTime", 6000);','integer(p, "worldTime", mode==1?18000:6000);')
(work/'probe_130.c').write_text(c)
print('Prepared',len(cases),'actual-GLSL probes')

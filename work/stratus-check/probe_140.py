from pathlib import Path
from prepare import expand,adapt
w=Path('work/stratus-check');o=w/'probe-140';o.mkdir(exist_ok=True);root=Path('outputs/Stratus/shaders')
(o/'screen.vsh').write_text('#version 330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.-1.,0,1);}\n')
s='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'
for lib in ['options','frame','ceiling','diffuse','medium']:s+=expand(root/'core'/f'{lib}.glsl',root)+'\n'
cases=[
('normal_fresnel','vec3(dielectricWaterFresnel(1.,1.,1.333))'),
('grazing_fresnel','vec3(dielectricWaterFresnel(.02,1.,1.333))'),
('underwater_TIR','vec3(dielectricWaterFresnel(.5,1.333,1.))'),
('underwater_window','vec3(dielectricWaterFresnel(.9,1.333,1.))'),
('snell_direction','refract(normalize(vec3(.70710678,-.70710678,0)),vec3(0,1,0),1./1.333)'),
('normal_tir_direction','refract(normalize(vec3(.8660254,.5,0)),vec3(0,-1,0),1.333)'),
('flat_wet','vec3(retainedMoistureAmount(1.,1.,.58,0.))'),
('trapped_wet','vec3(retainedMoistureAmount(1.,1.,.58,1.))'),
('wall_wet','vec3(retainedMoistureAmount(1.,0.,.58,0.))'),
('sheltered_wet','vec3(retainedMoistureAmount(0.,1.,.58,1.))'),
('soil_wet','vec3(retainedMoistureAmount(1.,1.,.90,0.))'),
('smooth_wet','vec3(retainedMoistureAmount(1.,1.,.04,0.))'),
('water_2m','travelThroughWater(vec3(.5),2.,vec3(.247,.463,.894),1.,0.)'),
('water_8m','travelThroughWater(vec3(.5),8.,vec3(.247,.463,.894),1.,0.)'),
('water_24m','travelThroughWater(vec3(.5),24.,vec3(.247,.463,.894),1.,0.)'),
('split_path_error','abs(travelThroughWater(travelThroughWater(vec3(.5),2.,1.),3.,1.)-travelThroughWater(vec3(.5),5.,1.))'),
('clear_extinction','waterExtinction(vec3(.247,.463,.894),1.)'),
('swamp_extinction','waterExtinction(vec3(.38,.482,.392),1.)'),
('cave_body','waterBodyColour(vec3(.247,.463,.894),0.,0.)'),
('outdoor_body','waterBodyColour(vec3(.247,.463,.894),1.,0.)'),
('lit_cave_body','waterBodyColour(vec3(.247,.463,.894),0.,1.)'),
('cloud_below','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),7000.).a)'),
('cloud_inside','vec3(physicalCloudLayer(vec3(200,192,200),vec3(1,0,0),7000.).a)'),
('cloud_above','vec3(physicalCloudLayer(vec3(200,285,200),vec3(0,-1,0),7000.).a)'),
('cloud_wrong_side','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,-1,0),7000.).a)'),
('cloud_depth_clip','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),10.).a)'),
('face_top','formIrradiance(vec3(0,1,0),1.)'),
('face_side','formIrradiance(vec3(1,0,0),1.)'),
('entity_dark','diffuseRadiance(vec3(.8),vec3(0),0.,vec3(0,1,0),1.,vec3(0,0,-10),4112)'),
]
s+='uniform float probeDistance;\nlayout(location=0) out vec4 result;\nvoid main(){int c=int(probeDistance+.5);\n'
for i,(name,expr) in enumerate(cases):s+=f'if(c=={i})result=vec4({expr},1.);\n'
s+='}\n'
for n in ['current','previous']:(o/(n+'.fsh')).write_text(adapt(s,'.fsh'))
c=(w/'appearance_probe.c').read_text();a=c.index('    struct { const char *name;');b=c.index('    printf(',a)
c=c[:a]+'    struct {const char *name;float distance,sky;int eye;float status;int mode;} cases[]={\n'+',\n'.join('{"'+n+'",'+str(i)+',1,0,0,0}' for i,(n,e) in enumerate(cases))+'\n};\n'+c[b:]
c=c.replace('glUseProgram(p);','glUseProgram(p);\n    glUniform3f(glGetUniformLocation(p,"biomeWaterTint"),.247,.463,.894);\n    scalar(p,"biomeHumidity",.75); scalar(p,"biomeSilt",.05);')
(w/'probe_140.c').write_text(c)
print('Prepared',len(cases),'GPU optical invariants')

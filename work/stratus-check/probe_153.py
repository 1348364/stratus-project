from pathlib import Path
from prepare import expand,adapt
w=Path('work/stratus-check');o=w/'probe-153';o.mkdir(exist_ok=True);root=Path('outputs/Stratus/shaders')
(o/'screen.vsh').write_text('#version330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.-1.,0,1);}\n'.replace('#version330','#version330'.replace('330',' 330')))
s='#version330 compatibility\n#define DIMENSION_TYPE0\n'.replace('#version330','#version 330').replace('DIMENSION_TYPE0','DIMENSION_TYPE 0')
for lib in ['options','frame','ceiling','volume','diffuse','medium','water-path','forward']:s+=expand(root/'core'/f'{lib}.glsl',root)+'\n'
s+='uniform sampler2D depthtex1;uniform sampler2D colortex4;\n'+expand(root/'core/refraction.glsl',root)+'\n'+expand(root/'core/scene-trace.glsl',root)+'\n'
s+='''vec3 screenProbe(vec3 origin,vec3 direction,vec3 normal,int side){float path;vec4 h=traceOpticalScene(origin,normalize(direction),normal,side,1,100.,false,path);return vec3(h.a,path,h.r);}
'''
cases=[
('normal_fresnel','vec3(dielectricWaterFresnel(1.,1.,1.333))',1),
('grazing_fresnel','vec3(dielectricWaterFresnel(.02,1.,1.333))',1),
('underwater_TIR','vec3(dielectricWaterFresnel(.5,1.333,1.))',1),
('underwater_window','vec3(dielectricWaterFresnel(.9,1.333,1.))',1),
('snell_air_to_water','refract(normalize(vec3(.70710678,-.70710678,0)),vec3(0,1,0),1./1.333)',1),
('snell_water_to_air','refract(normalize(vec3(.5,.8660254,0)),vec3(0,-1,0),1.333)',1),
('TIR_direction','refract(normalize(vec3(.8660254,.5,0)),vec3(0,-1,0),1.333)',1),
('soil_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4110).x))',1),
('wood_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4111).x))',1),
('stone_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4112).x))',1),
('polished_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4116).x))',1),
('masonry_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4117).x))',1),
('fabric_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4115).x))',1),
('metal_no_darkening','vec3(materialWetDarkening(1.,wetMaterialProperties(4114).x))',1),
('sheltered_no_darkening','vec3(materialWetDarkening(0.,.9))',0),
('exposed_film','vec3(exposedWetFilm(1.))',1),
('sheltered_no_film','vec3(exposedWetFilm(0.))',0),
('water_2m','travelThroughWater(vec3(.5),2.,vec3(.247,.463,.894),1.,0.)',1),
('water_8m','travelThroughWater(vec3(.5),8.,vec3(.247,.463,.894),1.,0.)',1),
('water_24m','travelThroughWater(vec3(.5),24.,vec3(.247,.463,.894),1.,0.)',1),
('split_path_error','abs(travelThroughWater(travelThroughWater(vec3(.5),2.,1.),3.,1.)-travelThroughWater(vec3(.5),5.,1.))',1),
('cave_body','waterBodyColour(vec3(.247,.463,.894),0.,0.)',0),
('outdoor_body','waterBodyColour(vec3(.247,.463,.894),1.,0.)',1),
('lit_cave_body','waterBodyColour(vec3(.247,.463,.894),0.,1.)',0),
('cloud_below','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),7000.).a)',1),
('cloud_inside','vec3(physicalCloudLayer(vec3(200,256,200),vec3(1,0,0),7000.).a)',1),
('cloud_above','vec3(physicalCloudLayer(vec3(200,420,200),vec3(0,-1,0),7000.).a)',1),
('cloud_wrong_side','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,-1,0),7000.).a)',1),
('cloud_depth_clip','vec3(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),10.).a)',1),
('fog_below','vec3(mistDensityWorld(vec3(0,70,0)))',1),
('fog_offset','vec3(mistDensityWorld(vec3(40,70,30)))',1),
('fog_high','vec3(mistDensityWorld(vec3(0,600,0)))',1),
('fog_foreground_clear','vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),20.,1.,60).a)',1),
('fog_local_volume','vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),120.,1.,60).a)',1),
('fog_sheltered','vec3(volumetricMist(vec3(0,70,0),vec3(1,0,0),120.,0.,60).a)',0),
('face_top','formIrradiance(vec3(0,1,0),1.)',1),
('face_side','formIrradiance(vec3(1,0,0),1.)',1),
('face_z','formIrradiance(vec3(0,0,1),1.)',1),
('face_bottom','formIrradiance(vec3(0,-1,0),1.)',1),
('cache_offscreen_floor','cacheProbe(vec3(0,-1,-1),vec3(0,-1,-.1),vec3(0,1,0),-1)',1),
('cache_behind_eye_reflection','cacheProbe(vec3(0,1,-.5),vec3(0,-.6,.8),vec3(0,-1,0),1)',1),
('cache_upward_air_refraction','cacheProbe(vec3(0,1,-2),vec3(.1,.8,-.6),vec3(0,-1,0),-1)',1),
('cache_wrong_medium_rejected','cacheProbe(vec3(0,-1,-1),vec3(0,1,0),vec3(0,1,0),-1)',1),
('cache_seam','cacheProbe(vec3(0),vec3(1,-1,1),normalize(vec3(-1,1,-1)),-1)',1),
('cache_positive_x','cacheProbe(vec3(0),vec3(1,0,0),vec3(-1,0,0),-1)',1),
('cache_negative_x','cacheProbe(vec3(0),vec3(-1,0,0),vec3(1,0,0),-1)',1),
('cache_positive_y','cacheProbe(vec3(0),vec3(0,1,0),vec3(0,-1,0),-1)',1),
('cache_negative_y','cacheProbe(vec3(0),vec3(0,-1,0),vec3(0,1,0),-1)',1),
('cache_positive_z','cacheProbe(vec3(0),vec3(0,0,1),vec3(0,0,-1),-1)',1),
('cache_negative_z','cacheProbe(vec3(0),vec3(0,0,-1),vec3(0,0,1),-1)',1),
('cloud_stationary_world_error','vec3(abs(physicalCloudLayer(vec3(200,100,200),vec3(0,1,0),7000.).a-physicalCloudLayer(vec3(200,110,200),vec3(0,1,0),6990.).a))',1),
('entity_dark','diffuseRadiance(vec3(.8),vec3(0),0.,vec3(0,1,0),1.,vec3(0,0,-10),4112)',0),
('refracted_cube_top','transmissionProbe(vec2(.5,.35),true)',1),
('unbent_floor','transmissionProbe(vec2(.5,.35),false)',1),
('refracted_open_floor','transmissionProbe(vec2(.20,.35),true)',1),
]
cases=[c for c in cases if not c[0].startswith('cache_') and c[0] not in {'snell_air_to_water','snell_water_to_air','TIR_direction','refracted_cube_top','unbent_floor','refracted_open_floor'}]
cases += [
 ('legacy_refraction_zero','vec3(legacyWaterRefractionUV(vec2(.5,.35),vec3(0,1,0),vec3(0,1,0),4.,1.),0)',1),
 ('legacy_refraction_offset','vec3(legacyWaterRefractionUV(vec2(.5,.35),vec3(.15,.98,0),vec3(0,1,0),4.,1.),0)',1),
 ('legacy_refraction_foreground_guard','vec3(legacyWaterRefractionUV(vec2(.5,.35),vec3(.15,.98,0),vec3(0,1,0),4.,100.),0)',1),
 ('screen_visible_receiver','screenProbe(vec3(0,0,-2),vec3(0,.2,-1),vec3(0,1,0),1)',1),
 ('screen_behind_eye_miss','screenProbe(vec3(0,0,-2),vec3(0,0,1),vec3(0,1,0),1)',1),
 ('screen_wrong_medium_rejected','screenProbe(vec3(0,0,-2),vec3(0,.2,-1),vec3(0,1,0),-1)',1),
]

cases += [
 ('falling_sheet_far_receiver','vec3(fallingWaterThickness(vec3(0,70,0),vec3(1,0,0),vec3(-1,0,0),100.))',1),
 ('falling_sheet_near_receiver','vec3(fallingWaterThickness(vec3(0,70,0),vec3(1,0,0),vec3(-1,0,0),.2))',1),
 ('background_ocean_accepted','vec3(float(hasBackgroundWater(vec4(20,1,0,1),10.,50.)))',1),
 ('same_surface_not_doubled','vec3(float(hasBackgroundWater(vec4(10,1,0,1),10.,50.)))',1),
 ('water_behind_solid_rejected','vec3(float(hasBackgroundWater(vec4(60,1,0,1),10.,50.)))',1),
 ('empty_secondary_rejected','vec3(float(hasBackgroundWater(vec4(20,1,0,0),10.,50.)))',1),
 ('air_zero_segment','airBehindWater(vec3(.1,.2,.3),vec3(0,70,0),vec3(1,0,0),0.,1.,true)',1),
 ('air_near_segment','airBehindWater(vec3(.1,.2,.3),vec3(0,70,0),vec3(1,0,0),5.,1.,true)',1),
 ('air_far_border_error','abs(airBehindWater(vec3(.1,.2,.3),vec3(0,70,0),vec3(1,0,0),200.,1.,true)-atmosphericColour())',1),
 ('water_join_confirmed','vec3(float(joinsSurroundingWater(probeHorizontalWater,vec2(.5,.35),vec3(0,69,-2),normalize(vec3(0,-1,-3)),30.)))',1),
 ('water_join_solid_before_plane','vec3(float(joinsSurroundingWater(probeHorizontalWater,vec2(.5,.35),vec3(0,69,-2),normalize(vec3(0,-1,-3)),1.)))',1),
 ('water_join_upward_rejected','vec3(float(joinsSurroundingWater(probeHorizontalWater,vec2(.5,.35),vec3(0,69,-2),normalize(vec3(0,1,-3)),30.)))',1),
 ('water_join_missing_neighbours','vec3(float(joinsSurroundingWater(probeHorizontalWater,vec2(.5,.65),vec3(0,69,-2),normalize(vec3(0,-1,-3)),30.)))',1),
 ('air_cave_no_fog','airBehindWater(vec3(.1,.2,.3),vec3(0,20,0),vec3(1,0,0),80.,0.,true)',0),
]

s+='vec3 testForward(vec3 background,vec3 replacement,vec3 surface,float alpha){float t=1.-alpha;vec3 scene=surface*alpha+background*t;return compositeForward(replacement,forwardRadiance(scene,background,t),t); }\n'
cases += [
 ('glass_red_colour_preserved','testForward(vec3(1.,.8,.3),vec3(.04,.18,.25),vec3(.5,.02,.01),.4)',1),
 ('glass_blue_colour_preserved','testForward(vec3(.9,.7,.2),vec3(.07,.23,.12),vec3(.01,.03,.8),.6)',1),
 ('glass_no_alpha','testForward(vec3(.9,.7,.2),vec3(.07,.23,.12),vec3(.01,.03,.8),0.)',1),
 ('glass_full_alpha','testForward(vec3(.9,.7,.2),vec3(.07,.23,.12),vec3(.01,.03,.8),1.)',1),
 ('glass_black_tint','testForward(vec3(3.,2.,1.),vec3(.12,.2,.3),vec3(0),.75)',1),
 ('glass_stacked','compositeForward(vec3(.04,.18,.25),forwardRadiance(vec3(.3,0,.25)+vec3(.9,.7,.2)*.45,vec3(.9,.7,.2),.45),.45)',1),
 ('forward_additive','compositeForward(vec3(.07,.23,.12),forwardRadiance(vec3(.9,.7,.2)+vec3(.4,.2,.1),vec3(.9,.7,.2),1.),1.)',1),
]
s+='uniform sampler2D probeHorizontalWater;\n'
s+='uniform float probeDistance;layout(location=0)out vec4 result;void main(){int c=int(probeDistance+.5);\n'
for i,(n,e,sky) in enumerate(cases):s+=f'if(c=={i})result=vec4({e},1.);\n'
s+='}\n';(o/'current.fsh').write_text(adapt(s,'.fsh'))
c=(w/'appearance_probe.c').read_text();a=c.index('static void sample(');b=c.index('int main(',a)
c=c[:a]+'''static void setup(GLuint p){
 glUseProgram(p);glUniform3f(glGetUniformLocation(p,"biomeWaterTint"),.247,.463,.894);
 scalar(p,"biomeHumidity",.75);scalar(p,"biomeSilt",.05);scalar(p,"far",100);
 scalar(p,"viewWidth",256);scalar(p,"viewHeight",256);integer(p,"worldTime",6000);
 glUniform3f(glGetUniformLocation(p,"cameraPosition"),0,70,0);
 glUniform3f(glGetUniformLocation(p,"fogColor"),.65,.70,.75);
 GLfloat identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
 GLfloat projection[16]={1,0,0,0,0,1,0,0,0,0,-1.002002,-1,0,0,-.2002002,0};
 GLfloat inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.995,0,0,-1,5.005};
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjection"),1,GL_FALSE,projection);
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelView"),1,GL_FALSE,identity);
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);
 integer(p,"probeHorizontalWater",1);integer(p,"shadowcolor0",5);integer(p,"shadowcolor1",6);integer(p,"depthtex1",2);integer(p,"colortex4",3);integer(p,"colortex10",4);integer(p,"weatherNoise",7);
}
static void texture2size(int unit,int channels,const float* data,int width,int height){
 GLuint t;glGenTextures(1,&t);glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);
 glTexImage2D(GL_TEXTURE_2D,0,channels==1?GL_R32F:GL_RGBA32F,width,height,0,channels==1?GL_RED:GL_RGBA,GL_FLOAT,data);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
}
static void texture2(int unit,int channels,const float* data){texture2size(unit,channels,data,256,256);}
static void scene(void){
 float *depth=calloc(256*256,sizeof(float)),*normal=calloc(256*256*4,sizeof(float)),*colour=calloc(256*256*4,sizeof(float));
 for(int y=0;y<256;y++)for(int x=0;x<256;x++){
  float r[3]={2*(x+.5)/256-1,2*(y+.5)/256-1,-1};float t=16,n[3]={0,0,1};int cube=0;
  if(r[1]<-.00001&&-4/r[1]<t){t=-4/r[1];n[0]=0;n[1]=1;n[2]=0;}
  if(r[1]>.00001&&4/r[1]<t){t=4/r[1];n[0]=0;n[1]=-1;n[2]=0;}
  float lo[3]={-1,-4,-5},hi[3]={1,-2,-3},entry=0,exit=100,axisNormal[3]={0};int possible=1;
  for(int axis=0;axis<3;axis++){
   if(fabsf(r[axis])<.000001){if(0<lo[axis]||0>hi[axis])possible=0;continue;}
   float a=lo[axis]/r[axis],b=hi[axis]/r[axis],near=fminf(a,b),far=fmaxf(a,b);
   if(near>entry){entry=near;axisNormal[0]=axisNormal[1]=axisNormal[2]=0;axisNormal[axis]=a<b?-1:1;}
   exit=fminf(exit,far);
  }
  if(possible&&entry<exit&&entry>0&&entry<t){t=entry;memcpy(n,axisNormal,sizeof n);cube=1;}
  int i=y*256+x;float z=-t;depth[i]=((-1.002002*z-.2002002)/(-z))*.5+.5;
  for(int j=0;j<3;j++)normal[i*4+j]=n[j];normal[i*4+3]=1;
  colour[i*4]=cube?.9:.12;colour[i*4+1]=cube?.2:.4;colour[i*4+2]=cube?.1:.9;colour[i*4+3]=1;
 }
 float *horizontal=calloc(256*256*4,sizeof(float));
 for(int y=0;y<128;y++)for(int x=0;x<256;x++){int i=(y*256+x)*4;float ry=2*(y+.5)/256-1;horizontal[i]=-3/ry;horizontal[i+1]=1;horizontal[i+3]=1;}
 texture2(1,4,horizontal);free(horizontal);
 texture2(2,1,depth);texture2(3,4,colour);texture2(4,4,normal);free(depth);free(colour);free(normal);
 float *cacheColour=calloc(1024*512*4,sizeof(float)),*cacheNormal=calloc(1024*512*4,sizeof(float));
 const float fw[8][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1},{0,0,-1},{0,-1,0}};
 const float rt[8][3]={{0,0,1},{0,0,1},{1,0,0},{1,0,0},{1,0,0},{1,0,0},{1,0,0},{1,0,0}};
 for(int face=0;face<8;face++)for(int y=0;y<256;y++)for(int x=0;x<256;x++){
  float up[3]={rt[face][1]*fw[face][2]-rt[face][2]*fw[face][1],rt[face][2]*fw[face][0]-rt[face][0]*fw[face][2],rt[face][0]*fw[face][1]-rt[face][1]*fw[face][0]};
  float o[3]={0,face>=6?2.5:0,0};float extent=face>=6?2.5:1.02;
  float r[3],n[3]={0};for(int j=0;j<3;j++)r[j]=fw[face][j]+rt[face][j]*(2*(x+.5)/256-1)*extent+up[j]*(2*(y+.5)/256-1)*extent;
  float t=1e5;int cube=0;
  for(int j=0;j<3;j++){float limit=j==1?4:16;float hit=(limit-(r[j]>0?o[j]:-o[j]))/fmaxf(fabsf(r[j]),.000001);if(hit<t){t=hit;n[0]=n[1]=n[2]=0;n[j]=r[j]>0?-1:1;}}
  float lo[3]={-1,-4,-5},hi[3]={1,-2,-3},entry=0,exit=100,an[3]={0};int possible=1;
  for(int j=0;j<3;j++){if(fabsf(r[j])<.000001){if(o[j]<lo[j]||o[j]>hi[j])possible=0;continue;}float a=(lo[j]-o[j])/r[j],b=(hi[j]-o[j])/r[j],near=fminf(a,b);if(near>entry){entry=near;an[0]=an[1]=an[2]=0;an[j]=a<b?-1:1;}exit=fminf(exit,fmaxf(a,b));}
  if(possible&&entry<exit&&entry>0&&entry<t){t=entry;memcpy(n,an,sizeof n);cube=1;}
  int i=((face/4)*256+y)*1024+(face%4)*256+x;
  for(int j=0;j<3;j++)cacheNormal[i*4+j]=n[j];cacheNormal[i*4+3]=t*sqrtf(r[0]*r[0]+r[1]*r[1]+r[2]*r[2]);
  cacheColour[i*4]=cube?.9:.12;cacheColour[i*4+1]=cube?.2:.4;cacheColour[i*4+2]=cube?.1:.9;cacheColour[i*4+3]=1;
 }
 texture2size(5,4,cacheColour,1024,512);texture2size(6,4,cacheNormal,1024,512);free(cacheColour);free(cacheNormal);
 const char* path="outputs/Stratus/shaders/volumes/weather.rgba8";FILE*f=fopen(path,"rb");if(!f)exit(6);unsigned char*bytes=malloc(128*128*128*4);if(fread(bytes,1,128*128*128*4,f)!=128*128*128*4)exit(6);fclose(f);
 GLuint noise;glGenTextures(1,&noise);glActiveTexture(GL_TEXTURE7);glBindTexture(GL_TEXTURE_3D,noise);
 glTexImage3D(GL_TEXTURE_3D,0,GL_RGBA8,128,128,128,0,GL_RGBA,GL_UNSIGNED_BYTE,bytes);free(bytes);
 glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
 glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_S,GL_REPEAT);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_T,GL_REPEAT);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_R,GL_REPEAT);
}
'''+c[b:]
c=c.replace('#include "native_compile.c"','#include "native_compile.c"\n#include <math.h>')
a=c.index('    GLuint previous =');c=c[:a]+'''    GLuint current=program(argv[1],"current");scene();setup(current);
    struct{const char*name;int index;float sky;}cases[]={
'''+',\n'.join('{"'+n+'",'+str(i)+','+str(sky)+'}' for i,(n,e,sky) in enumerate(cases))+'''};
    printf("{\\"cases\\":{\\n");
    for(int i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
        float value[4];scalar(current,"probeDistance",cases[i].index);
        glUniform2i(glGetUniformLocation(current,"eyeBrightnessSmooth"),0,(int)(cases[i].sky*240));
        glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,value);
        printf("%s\\"%s\\":[%.8f,%.8f,%.8f,%.8f]\\n",i?",":"",cases[i].name,value[0],value[1],value[2],value[3]);
    }
    GLenum error=glGetError();printf("},\\"opengl_errors\\":%u}\\n",error);CGLDestroyContext(context);return error?5:0;
}
'''
(w/'probe_153.c').write_text(c);print('Prepared',len(cases),'GPU optical/material/volume/3D-scene cases.')

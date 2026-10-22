#define main validation_entry
#include "native_compile.c"
#include <math.h>
#undef main

static GLuint program(const char *root, const char *name) {
    char v[2048], f[2048];
    snprintf(v, sizeof v, "%s/screen.vsh", root);
    snprintf(f, sizeof f, "%s/%s.fsh", root, name);
    GLuint vertex = compile(GL_VERTEX_SHADER, v), fragment = compile(GL_FRAGMENT_SHADER, f);
    if (!vertex || !fragment) exit(3);
    GLuint p = glCreateProgram(); glAttachShader(p, vertex); glAttachShader(p, fragment); glLinkProgram(p);
    GLint ok; glGetProgramiv(p, GL_LINK_STATUS, &ok); if (!ok) exit(3);
    return p;
}
static void scalar(GLuint p, const char *name, float value) { glUniform1f(glGetUniformLocation(p, name), value); }
static void integer(GLuint p, const char *name, int value) { glUniform1i(glGetUniformLocation(p, name), value); }
static void setup(GLuint p){
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
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    CGLPixelFormatAttribute attributes[] = {kCGLPFAOpenGLProfile, (CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core, kCGLPFAAccelerated, 0};
    CGLPixelFormatObj format; GLint count;
    if (CGLChoosePixelFormat(attributes, &format, &count) || !format) return 2;
    CGLContextObj context; CGLCreateContext(format, 0, &context); CGLDestroyPixelFormat(format); CGLSetCurrentContext(context);
    GLuint vao, texture, framebuffer;
    glGenVertexArrays(1, &vao); glBindVertexArray(vao);
    glGenTextures(1, &texture); glBindTexture(GL_TEXTURE_2D, texture);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 1, 1, 0, GL_RGBA, GL_FLOAT, NULL);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glGenFramebuffers(1, &framebuffer); glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0);
    if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) return 4;
    glViewport(0, 0, 1, 1);
    GLuint current=program(argv[1],"current");scene();setup(current);
    struct{const char*name;int index;float sky;}cases[]={
{"normal_fresnel",0,1},
{"grazing_fresnel",1,1},
{"underwater_TIR",2,1},
{"underwater_window",3,1},
{"soil_darkening",4,1},
{"wood_darkening",5,1},
{"stone_darkening",6,1},
{"polished_darkening",7,1},
{"masonry_darkening",8,1},
{"fabric_darkening",9,1},
{"metal_no_darkening",10,1},
{"sheltered_no_darkening",11,0},
{"exposed_film",12,1},
{"sheltered_no_film",13,0},
{"water_2m",14,1},
{"water_8m",15,1},
{"water_24m",16,1},
{"split_path_error",17,1},
{"cave_body",18,0},
{"outdoor_body",19,1},
{"lit_cave_body",20,0},
{"cloud_below",21,1},
{"cloud_inside",22,1},
{"cloud_above",23,1},
{"cloud_wrong_side",24,1},
{"cloud_depth_clip",25,1},
{"fog_below",26,1},
{"fog_offset",27,1},
{"fog_high",28,1},
{"fog_foreground_clear",29,1},
{"fog_local_volume",30,1},
{"fog_sheltered",31,0},
{"face_top",32,1},
{"face_side",33,1},
{"face_z",34,1},
{"face_bottom",35,1},
{"cloud_stationary_world_error",36,1},
{"entity_dark",37,0},
{"legacy_refraction_zero",38,1},
{"legacy_refraction_offset",39,1},
{"legacy_refraction_foreground_guard",40,1},
{"screen_visible_receiver",41,1},
{"screen_behind_eye_miss",42,1},
{"screen_wrong_medium_rejected",43,1},
{"falling_sheet_far_receiver",44,1},
{"falling_sheet_near_receiver",45,1},
{"background_ocean_accepted",46,1},
{"same_surface_not_doubled",47,1},
{"water_behind_solid_rejected",48,1},
{"empty_secondary_rejected",49,1},
{"air_zero_segment",50,1},
{"air_near_segment",51,1},
{"air_far_border_error",52,1},
{"water_join_confirmed",53,1},
{"water_join_solid_before_plane",54,1},
{"water_join_upward_rejected",55,1},
{"water_join_missing_neighbours",56,1},
{"air_cave_no_fog",57,0},
{"glass_red_colour_preserved",58,1},
{"glass_blue_colour_preserved",59,1},
{"glass_no_alpha",60,1},
{"glass_full_alpha",61,1},
{"glass_black_tint",62,1},
{"glass_stacked",63,1},
{"forward_additive",64,1},
{"boundary_submerged_normal",65,1},
{"boundary_submerged_30deg",66,1},
{"boundary_above_45deg",67,1},
{"boundary_below_critical",68,1},
{"boundary_above_critical",69,1},
{"boundary_TIR_no_transmission",70,1},
{"boundary_TIR_full_weight",71,1},
{"boundary_reciprocity_error",72,1},
{"boundary_orientation_error",73,1},
{"submerged_air_receiver",74,1},
{"submerged_wrong_side_rejected",75,1}};
    printf("{\"cases\":{\n");
    for(int i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
        float value[4];scalar(current,"probeDistance",cases[i].index);
        glUniform2i(glGetUniformLocation(current,"eyeBrightnessSmooth"),0,(int)(cases[i].sky*240));
        glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,value);
        printf("%s\"%s\":[%.8f,%.8f,%.8f,%.8f]\n",i?",":"",cases[i].name,value[0],value[1],value[2],value[3]);
    }
    GLenum error=glGetError();printf("},\"opengl_errors\":%u}\n",error);CGLDestroyContext(context);return error?5:0;
}

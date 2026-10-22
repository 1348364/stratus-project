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
 integer(p,"depthtex1",2);integer(p,"colortex4",3);integer(p,"colortex10",4);integer(p,"weatherNoise",7);
}
static void texture2(int unit,int channels,const float* data){
 GLuint t;glGenTextures(1,&t);glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);
 glTexImage2D(GL_TEXTURE_2D,0,channels==1?GL_R32F:GL_RGBA32F,256,256,0,channels==1?GL_RED:GL_RGBA,GL_FLOAT,data);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
}
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
 texture2(2,1,depth);texture2(3,4,colour);texture2(4,4,normal);free(depth);free(colour);free(normal);
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
{"snell_air_to_water",4,1},
{"snell_water_to_air",5,1},
{"TIR_direction",6,1},
{"soil_darkening",7,1},
{"wood_darkening",8,1},
{"stone_darkening",9,1},
{"polished_darkening",10,1},
{"masonry_darkening",11,1},
{"fabric_darkening",12,1},
{"metal_no_darkening",13,1},
{"sheltered_no_darkening",14,0},
{"exposed_film",15,1},
{"sheltered_no_film",16,0},
{"water_2m",17,1},
{"water_8m",18,1},
{"water_24m",19,1},
{"split_path_error",20,1},
{"cave_body",21,0},
{"outdoor_body",22,1},
{"lit_cave_body",23,0},
{"cloud_below",24,1},
{"cloud_inside",25,1},
{"cloud_above",26,1},
{"cloud_wrong_side",27,1},
{"cloud_depth_clip",28,1},
{"fog_below",29,1},
{"fog_offset",30,1},
{"fog_high",31,1},
{"fog_foreground_clear",32,1},
{"fog_local_volume",33,1},
{"fog_sheltered",34,0},
{"face_top",35,1},
{"face_side",36,1},
{"entity_dark",37,0},
{"refracted_cube_top",38,1},
{"unbent_floor",39,1},
{"refracted_open_floor",40,1}};
    printf("{\"cases\":{\n");
    for(int i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
        float value[4];scalar(current,"probeDistance",cases[i].index);
        glUniform2i(glGetUniformLocation(current,"eyeBrightnessSmooth"),0,(int)(cases[i].sky*240));
        glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,value);
        printf("%s\"%s\":[%.8f,%.8f,%.8f,%.8f]\n",i?",":"",cases[i].name,value[0],value[1],value[2],value[3]);
    }
    GLenum error=glGetError();printf("},\"opengl_errors\":%u}\n",error);CGLDestroyContext(context);return error?5:0;
}

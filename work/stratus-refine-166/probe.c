#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint program(const char*r,const char*n){char v[2048],f[2048];snprintf(v,sizeof v,"%s/screen.vsh",r);snprintf(f,sizeof f,"%s/%s.fsh",r,n);GLuint vs=compile(GL_VERTEX_SHADER,v),fs=compile(GL_FRAGMENT_SHADER,f);if(!vs||!fs)exit(3);GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);return p;}
static void scalar(GLuint p,const char*n,float v){glUniform1f(glGetUniformLocation(p,n),v);}static void integer(GLuint p,const char*n,int v){glUniform1i(glGetUniformLocation(p,n),v);}
static float identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
static void setup(GLuint p){glUseProgram(p);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);glUniform3f(glGetUniformLocation(p,"sunPosition"),0,.6,.8);integer(p,"worldTime",6000);integer(p,"vanillaSun",6);integer(p,"weatherNoise",5);integer(p,"vanillaClouds",7);}
static void texture(GLuint t,int unit,float*rgba){glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,rgba);}
int main(int argc,char**argv){if(argc!=2)return 2;const char*r=argv[1];CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj fmt;GLint n;if(CGLChoosePixelFormat(a,&fmt,&n)||!fmt)return 2;CGLContextObj ctx;if(CGLCreateContext(fmt,0,&ctx))return 2;CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);GLuint vao,out,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,256,256,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;
 GLuint sun;glGenTextures(1,&sun);glActiveTexture(GL_TEXTURE6);glBindTexture(GL_TEXTURE_2D,sun);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);unsigned char data[32*32*4];char path[2048];snprintf(path,sizeof path,"%s/sun.rgba",r);FILE*f=fopen(path,"rb");if(!f||fread(data,1,sizeof data,f)!=sizeof data)return 4;fclose(f);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,32,32,0,GL_RGBA,GL_UNSIGNED_BYTE,data);
 GLuint dummyCloud;glGenTextures(1,&dummyCloud);float clearCloud[4]={0,0,0,0};texture(dummyCloud,7,clearCloud);
 const char*suns[]={"sun-before","sun-after","sun-zero","sun-vanilla","sun-mask"};float*pixels=malloc(256*256*4*sizeof(float));glViewport(0,0,256,256);
 for(int k=0;k<5;k++){fprintf(stderr,"DRAW %s\n",suns[k]);GLuint p=program(r,suns[k]);setup(p);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,256,256,GL_RGBA,GL_FLOAT,pixels);snprintf(path,sizeof path,"%s/%s.rgba32f",r,suns[k]);f=fopen(path,"wb");fwrite(pixels,sizeof(float),256*256*4,f);fclose(f);glDeleteProgram(p);}free(pixels);
 GLuint tex[5];glGenTextures(5,tex);float weather[4]={.5,.5,.5,.5};glActiveTexture(GL_TEXTURE5);glBindTexture(GL_TEXTURE_3D,tex[4]);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);glTexImage3D(GL_TEXTURE_3D,0,GL_RGBA32F,1,1,1,0,GL_RGBA,GL_FLOAT,weather);glViewport(0,0,1,1);
 float distances[]={200,200,4,200,512,200,200,200,200,200,200};float meta[]={7000,200,7000,7000,7000,210,211,212,213,215,220};
 const char*names[]={"missed_leaf","matched_depth","clear_foreground","underwater","chunk_border","confidence_10","confidence_11","confidence_12","confidence_13","confidence_15","confidence_20"};
 printf("{\"scope\":\"actual before/after atmosphere resolve and actual diffuse GLSL, offline native OpenGL\",\"fog\":[");int count=0;
 for(int variant=0;variant<2;variant++){
 fprintf(stderr,"DRAW %s\n",variant?"fog-after":"fog-before");GLuint p=program(r,variant?"fog-after":"fog-before");setup(p);glUniform3f(glGetUniformLocation(p,"cameraPosition"),0,70,0);glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),240,240);scalar(p,"far",512);float inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.9995f,0,0,-1,5.0005f};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);
 integer(p,"colortex3",1);integer(p,"colortex11",2);integer(p,"colortex2",3);integer(p,"depthtex0",4);integer(p,"depthtex1",4);
 for(int k=0;k<11;k++){
 float scene[4]={.01,.015,.01,1},volume[4]={.28,.30,.32,.8},metadata[4]={0,1,meta[k],0},depth[4]={1.00010001f-.100010001f/distances[k],0,0,0};
 texture(tex[0],1,scene);texture(tex[1],2,volume);texture(tex[2],3,metadata);texture(tex[3],4,depth);integer(p,"isEyeInWater",k==3?1:0);
 if(k==0){GLint num;glGetProgramiv(p,GL_ACTIVE_UNIFORMS,&num);for(int u=0;u<num;u++){char nm[256];GLint sz;GLenum type;glGetActiveUniform(p,u,256,0,&sz,&type,nm);if(type==GL_SAMPLER_2D||type==GL_SAMPLER_3D){GLint value;glGetUniformiv(p,glGetUniformLocation(p,nm),&value);fprintf(stderr,"SAMPLER %s type=%x unit=%d\n",nm,type,value);}}}

 glDrawArrays(GL_TRIANGLES,0,3);float v[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,v);printf("%s{\"variant\":\"%s\",\"case\":\"%s\",\"rgb\":[%.9f,%.9f,%.9f]}",count++?",":"",variant?"after":"before",names[k],v[0],v[1],v[2]);
 }glDeleteProgram(p);
 }
 const char*faces[]={"face","face-strong","face-off","face-blend-off","face-nether","face-end","face-vanilla","face-before"};float normals[6][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};printf("],\"faces\":[");count=0;
 for(int j=0;j<8;j++){GLuint p=program(r,faces[j]);setup(p);for(int k=0;k<6;k++)for(int n=0;n<6;n++){
 glUniform3f(glGetUniformLocation(p,"sunPosition"),k==1?-.8:.8,k==3?-.6:.6,0);integer(p,"worldTime",k==3?18000:6000);scalar(p,"rainStrength",k==2?1:0);float rotated[16]={0,0,-1,0,0,1,0,0,1,0,0,0,0,0,0,1};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,k==5?rotated:identity);if(k==5)glUniform3f(glGetUniformLocation(p,"sunPosition"),0,.6,.8);scalar(p,"probeSky",k==4?0:1);glUniform3fv(glGetUniformLocation(p,"probeNormal"),1,normals[n]);glDrawArrays(GL_TRIANGLES,0,3);float v[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,v);printf("%s{\"variant\":\"%s\",\"condition\":%d,\"normal\":%d,\"value\":%.9f}",count++?",":"",faces[j],k,n,v[0]);
 }glDeleteProgram(p);}
 GLenum e=glGetError();printf("],\"opengl_errors\":%u}\n",e);CGLDestroyContext(ctx);return e?6:0;}

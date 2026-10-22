#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint program(const char*r,const char*n){char v[2048],f[2048];snprintf(v,sizeof v,"%s/screen.vsh",r);snprintf(f,sizeof f,"%s/%s.fsh",r,n);GLuint vs=compile(GL_VERTEX_SHADER,v),fs=compile(GL_FRAGMENT_SHADER,f);if(!vs||!fs)exit(3);GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);return p;}
static void scalar(GLuint p,const char*n,float v){glUniform1f(glGetUniformLocation(p,n),v);}static void integer(GLuint p,const char*n,int v){glUniform1i(glGetUniformLocation(p,n),v);}
int main(int argc,char**argv){if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj fmt;GLint n;if(CGLChoosePixelFormat(a,&fmt,&n)||!fmt)return 2;CGLContextObj ctx;if(CGLCreateContext(fmt,0,&ctx))return 2;CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);GLuint vao,t,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&t);glBindTexture(GL_TEXTURE_2D,t);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,t,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,1,1);
 GLuint dummy;glGenTextures(1,&dummy);glActiveTexture(GL_TEXTURE1);glBindTexture(GL_TEXTURE_2D,dummy);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);float clear[4]={0,0,0,0};glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,clear);
 const char*variants[]={"current","before","no-vanilla","no-realistic","no-faces","master-off","wet-off","wet-max","cirrus-off","lower-off","nether"};float normals[][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};float identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
 printf("{\"scope\":\"actual current/baseline GLSL, independent component, rain-film and cirrus relationships\",\"samples\":[");int count=0;
 for(int j=0;j<11;j++){GLuint p=program(argv[1],variants[j]);glUseProgram(p);integer(p,"vanillaClouds",1);integer(p,"vanillaSun",1);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);glUniform3f(glGetUniformLocation(p,"sunPosition"),.8,.6,0);scalar(p,"biomeHumidity",.75);
 for(int mode=0;mode<3;mode++){integer(p,"probeMode",mode);int cases=mode==0?24:(mode==1?9:16);
 for(int k=0;k<cases;k++){
 scalar(p,"rainStrength",0);integer(p,"worldTime",6000);scalar(p,"probeSky",1);scalar(p,"probeAbsorb",.64);scalar(p,"probeRough",.8);glUniform3f(glGetUniformLocation(p,"probeNormal"),0,1,0);glUniform3f(glGetUniformLocation(p,"probePoint"),0,-5,-10);
 if(mode==0){glUniform3fv(glGetUniformLocation(p,"probeNormal"),1,normals[k%6]);if(k>=6&&k<12)scalar(p,"rainStrength",1);if(k>=12&&k<18)integer(p,"worldTime",18000);if(k>=18)scalar(p,"probeSky",0);}
 if(mode==1){scalar(p,"rainStrength",k==0?0:1);if(k==2)glUniform3f(glGetUniformLocation(p,"probePoint"),0,-.2,-10);if(k==3)scalar(p,"probeAbsorb",0);if(k==4)scalar(p,"probeAbsorb",.02);if(k==5)scalar(p,"probeSky",0);if(k==6){scalar(p,"probeAbsorb",.9);glUniform3f(glGetUniformLocation(p,"probePoint"),8,-6,0);}if(k==7)integer(p,"worldTime",18000);if(k==8)scalar(p,"rainStrength",.5);}
 if(mode==2)glUniform3f(glGetUniformLocation(p,"probePoint"),(k%4-2)*8000,360,(k/4-2)*8000);
 glDrawArrays(GL_TRIANGLES,0,3);float v[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,v);printf("%s{\"variant\":\"%s\",\"mode\":%d,\"case\":%d,\"rgba\":[%.9f,%.9f,%.9f,%.9f]}",count++?",":"",variants[j],mode,k,v[0],v[1],v[2],v[3]);
 }}glDeleteProgram(p);}
 GLenum e=glGetError();printf("],\"opengl_errors\":%u}\n",e);CGLDestroyContext(ctx);return e?6:0;}

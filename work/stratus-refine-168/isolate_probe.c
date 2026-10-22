#define main native_compile_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint make_program(const char *root,const char *name){
 char v[2048],f[2048];snprintf(v,sizeof v,"%s/screen.vsh",root);snprintf(f,sizeof f,"%s/%s.fsh",root,name);
 GLuint vs=compile(GL_VERTEX_SHADER,v),fs=compile(GL_FRAGMENT_SHADER,f);if(!vs||!fs)exit(3);
 GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);return p;
}
static void iuniform(GLuint p,const char*n,int v){glUniform1i(glGetUniformLocation(p,n),v);}
static void funiform(GLuint p,const char*n,float v){glUniform1f(glGetUniformLocation(p,n),v);}
static GLuint image2d(int unit,int size,const void *data,GLenum internal,GLenum type){
 GLuint t;glGenTextures(1,&t);glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
 glTexImage2D(GL_TEXTURE_2D,0,internal,size,size,0,GL_RGBA,type,data);return t;
}
int main(int argc,char**argv){
 if(argc!=3)return 2;const char*root=argv[1];CGLPixelFormatAttribute attrs[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj fmt;GLint count;
 if(CGLChoosePixelFormat(attrs,&fmt,&count)||!fmt)return 2;CGLContextObj ctx;if(CGLCreateContext(fmt,0,&ctx))return 2;CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);
 GLuint vao;glGenVertexArrays(1,&vao);glBindVertexArray(vao);GLuint target=image2d(0,128,0,GL_RGBA32F,GL_FLOAT),fb;glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,target,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;
 char path[2048];unsigned char*cloud=malloc(256*256*4);snprintf(path,sizeof path,"%s/clouds.rgba",root);FILE*f=fopen(path,"rb");if(!f||fread(cloud,1,256*256*4,f)!=256*256*4)return 4;fclose(f);image2d(1,256,cloud,GL_RGBA8,GL_UNSIGNED_BYTE);free(cloud);
 unsigned char*volume=malloc(128*128*128*4);f=fopen(argv[2],"rb");if(!f||fread(volume,1,128*128*128*4,f)!=128*128*128*4)return 4;fclose(f);GLuint weather;glGenTextures(1,&weather);glActiveTexture(GL_TEXTURE3);glBindTexture(GL_TEXTURE_3D,weather);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_S,GL_REPEAT);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_T,GL_REPEAT);glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_R,GL_REPEAT);glTexImage3D(GL_TEXTURE_3D,0,GL_RGBA8,128,128,128,0,GL_RGBA,GL_UNSIGNED_BYTE,volume);free(volume);
 float zero[4]={0,0,0,0};GLuint input=image2d(2,1,zero,GL_RGBA32F,GL_FLOAT);image2d(4,1,zero,GL_RGBA32F,GL_FLOAT);
 const char*outputs[]={"output-vanilla","output-vanilla-extreme","output-enhanced"};float colours[][4]={{.001,.01,.03,1},{.04,.2,.5,1},{.6,.8,1,1},{1.5,.7,.1,1}};
 printf("{\"scope\":\"Native actual-output and full-atmosphere tests; GPU microbenchmark, not Minecraft FPS\",\"renderer\":\"%s\",\"output\":[",glGetString(GL_RENDERER));int serial=0;
 for(int j=0;j<3;j++){GLuint p=make_program(root,outputs[j]);glUseProgram(p);iuniform(p,"colortex3",2);iuniform(p,"colortex6",4);glViewport(0,0,1,1);
 for(int k=0;k<4;k++){glActiveTexture(GL_TEXTURE2);glBindTexture(GL_TEXTURE_2D,input);glTexSubImage2D(GL_TEXTURE_2D,0,0,0,1,1,GL_RGBA,GL_FLOAT,colours[k]);glDrawArrays(GL_TRIANGLES,0,3);float out[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,out);printf("%s{\"variant\":\"%s\",\"case\":%d,\"rgba\":[%.9f,%.9f,%.9f,%.9f]}",serial++?",":"",outputs[j],k,out[0],out[1],out[2],out[3]);}glDeleteProgram(p);}
 const char*labels[]={"before","after","hoist","bounds"};GLuint programs[]={make_program(root,"atmosphere-before"),make_program(root,"atmosphere-after"),make_program(root,"atmosphere-hoist"),make_program(root,"atmosphere-bounds")};float identity[]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};glViewport(0,0,128,128);float*pixels=malloc(128*128*4*sizeof(float));GLuint query;glGenQueries(1,&query);printf("],\"timings\":[");serial=0;
 // Alternating order counters warm-up/order bias; all options/budgets match.
 for(int scene=0;scene<4;scene++)for(int round=0;round<6;round++)for(int o=0;o<4;o++){
 int j=(round+o)%4;GLuint p=programs[j];glUseProgram(p);iuniform(p,"vanillaClouds",1);iuniform(p,"vanillaSun",4);iuniform(p,"weatherNoise",3);iuniform(p,"probeScene",scene);iuniform(p,"worldTime",6000);glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),240,240);glUniform3f(glGetUniformLocation(p,"sunPosition"),.8,.6,0);glUniform3f(glGetUniformLocation(p,"cameraPosition"),4096,scene==1?256:(scene==2?400:64),4096);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);funiform(p,"far",192);funiform(p,"frameTimeCounter",17);funiform(p,"rainStrength",0);
 glDrawArrays(GL_TRIANGLES,0,3);glFinish();glBeginQuery(GL_TIME_ELAPSED,query);for(int n=0;n<32;n++)glDrawArrays(GL_TRIANGLES,0,3);glEndQuery(GL_TIME_ELAPSED);GLuint64 ns;glGetQueryObjectui64v(query,GL_QUERY_RESULT,&ns);
 printf("%s{\"scene\":%d,\"round\":%d,\"variant\":\"%s\",\"gpu_ms_per_draw\":%.6f}",serial++?",":"",scene,round,labels[j],(double)ns/32000000.0);fflush(stdout);
 if(round==5){glReadPixels(0,0,128,128,GL_RGBA,GL_FLOAT,pixels);snprintf(path,sizeof path,"%s/atmosphere-%s-%d.rgba32f",root,labels[j],scene);f=fopen(path,"wb");fwrite(pixels,sizeof(float),128*128*4,f);fclose(f);}
 }
 GLenum error=glGetError();printf("],\"opengl_errors\":%u}\n",error);free(pixels);CGLDestroyContext(ctx);return error?5:0;
}

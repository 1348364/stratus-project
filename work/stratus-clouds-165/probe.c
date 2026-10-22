#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint program(const char*root,const char*name){
 char vp[2048],fp[2048];snprintf(vp,sizeof vp,"%s/screen.vsh",root);snprintf(fp,sizeof fp,"%s/%s.fsh",root,name);
 GLuint v=compile(GL_VERTEX_SHADER,vp),f=compile(GL_FRAGMENT_SHADER,fp);if(!v||!f)exit(3);
 GLuint p=glCreateProgram();glAttachShader(p,v);glAttachShader(p,f);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);glDeleteShader(v);glDeleteShader(f);return p;
}
static void setup(GLuint p){
 glUseProgram(p);float identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);
 glUniform1i(glGetUniformLocation(p,"vanillaClouds"),1);
 glUniform1i(glGetUniformLocation(p,"worldTime"),6000);glUniform3f(glGetUniformLocation(p,"sunPosition"),.8,.6,0);
}
int main(int argc,char**argv){
 if(argc!=2)return 2;const char*root=argv[1];CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj fmt;GLint count;if(CGLChoosePixelFormat(a,&fmt,&count)||!fmt)return 2;CGLContextObj ctx;if(CGLCreateContext(fmt,0,&ctx))return 2;CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);
 GLuint vao,target,fb,cloud;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&target);glBindTexture(GL_TEXTURE_2D,target);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,256,256,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,target,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,256,256);
 char path[2048];snprintf(path,sizeof path,"%s/clouds.rgba",root);unsigned char data[256*256*4];FILE*f=fopen(path,"rb");if(!f||fread(data,1,sizeof data,f)!=sizeof data)return 4;fclose(f);glGenTextures(1,&cloud);glActiveTexture(GL_TEXTURE1);glBindTexture(GL_TEXTURE_2D,cloud);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,256,256,0,GL_RGBA,GL_UNSIGNED_BYTE,data);
 const char*variants[]={"cloud","cloud-low-off","cloud-upper-off","cloud-other-low","cloud-detail-off","cloud-detail-max"};float *pixels=malloc(256*256*4*sizeof(float));int renders=0;
 for(int j=0;j<6;j++){
 GLuint p=program(root,variants[j]);setup(p);
 for(int mode=0;mode<2;mode++){
 glUniform1i(glGetUniformLocation(p,"probeMode"),mode);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,256,256,GL_RGBA,GL_FLOAT,pixels);
 snprintf(path,sizeof path,"%s/%s-%d.rgba32f",root,variants[j],mode);f=fopen(path,"wb");fwrite(pixels,sizeof(float),256*256*4,f);fclose(f);renders++;
 }
 if(j==0){for(int k=0;k<5;k++){
 int heights[]={64,256,400,64,64},times[]={6000,6000,6000,12500,18000};
 glUniform3f(glGetUniformLocation(p,"sunPosition"),k==3?.998:.8,k==3?.05:(k==4?-.6:.6),0);
 glUniform1i(glGetUniformLocation(p,"probeMode"),2);glUniform1f(glGetUniformLocation(p,"probeHeight"),heights[k]);glUniform1i(glGetUniformLocation(p,"worldTime"),times[k]);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,256,256,GL_RGBA,GL_FLOAT,pixels);
 snprintf(path,sizeof path,"%s/sky-%d.rgba32f",root,k);f=fopen(path,"wb");fwrite(pixels,sizeof(float),256*256*4,f);fclose(f);renders++;
 }}glDeleteProgram(p);
 }
 const char*faces[]={"face","face-strong","face-off","face-blend-off","face-nether","face-end"};float normals[6][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
 printf("{\"cloud_renders\":%d,\"faces\":[",renders);int num=0;glViewport(0,0,1,1);
 for(int j=0;j<6;j++){GLuint p=program(root,faces[j]);setup(p);
 for(int k=0;k<6;k++)for(int n=0;n<6;n++){
 // daylight +X, daylight -X, rain, night, sealed cave, rotated camera
 glUniform3f(glGetUniformLocation(p,"sunPosition"),k==1?-.8:.8,k==3?-.6:.6,0);
 glUniform1i(glGetUniformLocation(p,"worldTime"),k==3?18000:6000);glUniform1f(glGetUniformLocation(p,"rainStrength"),k==2?1:0);
 float identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
 float rotated[16]={0,0,-1,0,0,1,0,0,1,0,0,0,0,0,0,1};
 glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,k==5?rotated:identity);
 if(k==5)glUniform3f(glGetUniformLocation(p,"sunPosition"),0,.6,.8);
 glUniform1f(glGetUniformLocation(p,"probeSky"),k==4?0:1);glUniform3fv(glGetUniformLocation(p,"probeNormal"),1,normals[n]);
 glDrawArrays(GL_TRIANGLES,0,3);float v[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,v);
 printf("%s{\"variant\":\"%s\",\"condition\":%d,\"normal\":%d,\"value\":%.9f}",num++?",":"",faces[j],k,n,v[0]);
 }glDeleteProgram(p);}
 GLenum err=glGetError();printf("],\"opengl_errors\":%u}\n",err);free(pixels);CGLDestroyContext(ctx);return err?6:0;
}

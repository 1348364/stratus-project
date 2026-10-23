#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
#define W 64
#define H 32
static float depth(float d){return 1.001001001f-.1001001001f/d;}
int main(int argc,char**argv){if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);GLuint vao,out,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,W,H,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);glViewport(0,0,W,H);
 const char*names[]={"solid-off","solid-reflection","solid-refraction","solid-both"},*texnames[]={"colortex3","depthtex0","depthtex1","colortex15","colortex9","colortex4","colortex10"};GLuint textures[7];glGenTextures(7,textures);static float data[7][W*H*4],readings[4][W*H*4];int errors=0,samples=0,changedReflection=0,changedRefraction=0;
 for(int mode=0;mode<3;mode++){
 for(int y=0;y<H;y++)for(int x=0;x<W;x++){int q=(y*W+x)*4;for(int t=0;t<7;t++)for(int j=0;j<4;j++)data[t][q+j]=0;
 data[0][q]=.1f+x*.005f;data[0][q+1]=.2f+y*.008f;data[0][q+2]=.12;data[0][q+3]=1;data[1][q]=depth(mode==2?1:2);data[2][q]=depth(8);
 data[3][q]=.65;data[3][q+2]=2;data[3][q+3]=(mode==0||x>=48)?0:1;data[4][q]=.7;data[4][q+1]=.8;data[4][q+2]=.9;data[4][q+3]=1;
 }
 for(int v=0;v<4;v++){char vp[2048],fp[2048];snprintf(vp,sizeof vp,"%s/screen.vsh",argv[1]);snprintf(fp,sizeof fp,"%s/%s.fsh",argv[1],names[v]);GLuint vs=compile(GL_VERTEX_SHADER,vp),fs=compile(GL_FRAGMENT_SHADER,fp);if(!vs||!fs)return 3;GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)return 3;glUseProgram(p);
 float inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.995f,0,0,-1,5.005f},identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelViewInverse"),1,GL_FALSE,identity);glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),0,240);
 for(int t=0;t<7;t++){glActiveTexture(GL_TEXTURE0+t);glBindTexture(GL_TEXTURE_2D,textures[t]);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,t==0?GL_LINEAR:GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,t==0?GL_LINEAR:GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,W,H,0,GL_RGBA,GL_FLOAT,data[t]);glUniform1i(glGetUniformLocation(p,texnames[t]),t);}
 glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,W,H,GL_RGBA,GL_FLOAT,readings[v]);glDeleteProgram(p);samples+=W*H;
 for(int y=0;y<H;y++)for(int x=0;x<W;x++){int q=(y*W+x)*4;float err=0;for(int j=0;j<3;j++){if(!isfinite(readings[v][q+j])||readings[v][q+j]<0)errors++;err=fmaxf(err,fabsf(readings[v][q+j]-data[0][q+j]));}if((v==0||mode!=1||x>=48)&&err>.00001)errors++;if(mode==1&&x>4&&x<42&&y>4&&y<H-5&&err>.00001){if(v==1)changedReflection++;if(v==2)changedRefraction++;}}
 }
 }
 if(changedReflection<100||changedRefraction<100)errors++;GLenum err=glGetError();if(err)errors++;printf("{\"scope\":\"actual transparent-solid GLSL, no-interface/foreground guards and zero/independent optics\",\"pixel_samples\":%d,\"reflection_changed_interior_pixels\":%d,\"refraction_changed_interior_pixels\":%d,\"failures\":%d,\"gl_error\":%u}\n",samples,changedReflection,changedRefraction,errors,err);return errors?1:0;}

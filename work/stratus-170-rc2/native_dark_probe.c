#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint makeProgram(const char *root){
 char v[2048],f[2048];snprintf(v,sizeof v,"%s/screen.vsh",root);snprintf(f,sizeof f,"%s/water.fsh",root);
 GLuint vs=compile(GL_VERTEX_SHADER,v),fs=compile(GL_FRAGMENT_SHADER,f);if(!vs||!fs)exit(3);
 GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);return p;
}
static float zdepth(float d){return d>999?1.f:1.001001001f-.1001001001f/d;}
static float enc(float x){return x<=.0031308f?12.92f*x:1.055f*powf(x,1.f/2.4f)-.055f;}
static float dec(float x){return x<=.04045f?x/12.92f:powf((x+.055f)/1.055f,2.4f);}
static float body[3],sigma[3];
static void water(const float*c,float d,float*out){for(int j=0;j<3;j++){float t=expf(-sigma[j]*d);out[j]=c[j]*t+body[j]*(1-t);}}
int main(int argc,char**argv){
 if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);
 GLuint vao,out,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,1,1);
 GLuint p=makeProgram(argv[1]);glUseProgram(p);
 glUniform1i(glGetUniformLocation(p,"isEyeInWater"),0);glUniform1i(glGetUniformLocation(p,"worldTime"),6000);glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),0,240);glUniform3f(glGetUniformLocation(p,"biomeWaterTint"),.247,.463,.894);
 GLfloat inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.995f,0,0,-1,5.005f};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);
 const char*names[]={"colortex0","colortex1","colortex2","colortex3","colortex4","colortex8","colortex12","colortex13","colortex14","depthtex0","depthtex1"};GLuint tex[11];glGenTextures(11,tex);for(int i=0;i<11;i++){glActiveTexture(GL_TEXTURE0+i);glBindTexture(GL_TEXTURE_2D,tex[i]);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);glUniform1i(glGetUniformLocation(p,names[i]),i);}

 int fails=0;float worst=0;printf("{\"scope\":\"actual full-resolution native water resolve: valid dark, valid black, absent native cache\",\"cases\":[");
 for(int k=0;k<3;k++){float data[11][4]={{0}},behind[3]={.02,.03,.04};data[0][0]=.4;data[0][1]=.6;data[0][3]=1;data[1][1]=1;data[1][3]=1;data[2][0]=3;data[2][3]=1;for(int j=0;j<3;j++){data[3][j]=behind[j];data[4][j]=behind[j];data[6][j]=behind[j];data[5][j]=k==0?.0001*(j+1):0;}data[5][3]=k==2?0:1;data[8][0]=1;data[9][0]=zdepth(3);data[10][0]=zdepth(10);
 for(int i=0;i<11;i++){glActiveTexture(GL_TEXTURE0+i);glBindTexture(GL_TEXTURE_2D,tex[i]);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,data[i]);}
 glDrawArrays(GL_TRIANGLES,0,3);float got[4],error=0;glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,got);for(int j=0;j<3;j++){float coverage=k==2?0:.6f;float expected=dec(enc(behind[j])*(1-coverage)+enc(data[5][j])*coverage);error=fmaxf(error,fabsf(got[j]-expected));}worst=fmaxf(worst,error);if(error>.00015||!isfinite(error))fails++;printf("%s{\"case\":%d,\"max_error\":%.8f,\"rgb\":[%.6f,%.6f,%.6f]}",k?",":"",k,error,got[0],got[1],got[2]);}
 GLenum error=glGetError();printf("],\"failures\":%d,\"gl_error\":%u,\"worst_error\":%.8f}\n",fails,error,worst);return error?5:0;}

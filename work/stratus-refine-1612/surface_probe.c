#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
int main(int argc,char**argv){
 if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);
 GLuint vao,out,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,1,1);
 const char*names[]={"surface-zero","surface-half","surface-one","surface-no-biome"};float readings[4][3][4][4][4];float colours[4][3]={{0,0,0},{.1,.2,.4},{.2,.4,.8},{4,2,1}},tints[3][3]={{.247,.463,.894},{.25,.6,.2},{.6,.3,.1}};
 int errors=0,samples=0;
 for(int v=0;v<4;v++){
 char vp[2048],fp[2048];snprintf(vp,sizeof vp,"%s/screen.vsh",argv[1]);snprintf(fp,sizeof fp,"%s/%s.fsh",argv[1],names[v]);GLuint vs=compile(GL_VERTEX_SHADER,vp),fs=compile(GL_FRAGMENT_SHADER,fp);if(!vs||!fs)return 3;GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)return 3;glUseProgram(p);
 for(int t=0;t<3;t++)for(int k=0;k<4;k++)for(int c=0;c<4;c++){
 glUniform3fv(glGetUniformLocation(p,"probeRadiance"),1,colours[c]);glUniform3fv(glGetUniformLocation(p,"probeTint"),1,tints[t]);glUniform1f(glGetUniformLocation(p,"probePattern"),k/3.f);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,readings[v][t][k][c]);samples++;
 for(int j=0;j<3;j++){float val=readings[v][t][k][c][j];if(!isfinite(val)||val<0||val>colours[c][j]+.0001)errors++;if(v==0&&fabsf(val-colours[c][j])>.0001)errors++;}
 }
 glDeleteProgram(p);glDeleteShader(vs);glDeleteShader(fs);
 }
 for(int t=0;t<3;t++)for(int k=0;k<4;k++)for(int c=0;c<4;c++)for(int j=0;j<3;j++){
 float zero=readings[0][t][k][c][j],half=readings[1][t][k][c][j],one=readings[2][t][k][c][j];if(fabsf(half-(zero+one)*.5f)>.0001)errors++;
 if(c==2&&fabsf(one-2*readings[2][t][k][1][j])>.0001)errors++;
 if(t>0&&fabsf(readings[3][t][k][c][j]-readings[3][0][k][c][j])>.0001)errors++;
 if(k>0&&one+.0001<readings[2][t][k-1][c][j])errors++;
 }
 GLenum e=glGetError();if(e!=GL_NO_ERROR)errors++;
 printf("{\"scope\":\"actual water-surface GLSL on native GPU, not Minecraft visual acceptance\",\"samples\":%d,\"variants\":4,\"relationships\":[\"zero exact identity\",\"bounded HDR and black preservation\",\"continuous strength interpolation\",\"radiance contrast retained\",\"native pattern monotonic\",\"biome off independent of biome input\"],\"failures\":%d,\"gl_error\":%u}\n",samples,errors,e);return errors?1:0;
}

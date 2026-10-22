#define main native_validation_main
#include "native_compile.c"
#undef main
#include <math.h>
static GLuint link_program(const char *root,const char *name) {
 char v[1024],f[1024];snprintf(v,sizeof v,"%s/screen.vsh",root);snprintf(f,sizeof f,"%s/%s.fsh",root,name);
 GLuint vs=compile(GL_VERTEX_SHADER,v),fs=compile(GL_FRAGMENT_SHADER,f);if(!vs||!fs)exit(3);
 GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(3);return p;
}
static GLuint image_texture(int w,int h,float *data) {
 GLuint t;glGenTextures(1,&t);glBindTexture(GL_TEXTURE_2D,t);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,w,h,0,GL_RGBA,GL_FLOAT,data);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);return t;
}
static GLuint emissionMask,depthMask;
static void draw(GLuint p,GLuint input,GLuint output,GLuint framebuffer) {
 glBindFramebuffer(GL_FRAMEBUFFER,framebuffer);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,output,0);
 if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)exit(4);
 glViewport(0,0,128,128);glUseProgram(p);glActiveTexture(GL_TEXTURE0);glBindTexture(GL_TEXTURE_2D,input);
 glUniform1i(glGetUniformLocation(p,"colortex3"),0);glUniform1i(glGetUniformLocation(p,"colortex5"),0);
 glActiveTexture(GL_TEXTURE1);glBindTexture(GL_TEXTURE_2D,emissionMask);glUniform1i(glGetUniformLocation(p,"colortex0"),1);
 glActiveTexture(GL_TEXTURE2);glBindTexture(GL_TEXTURE_2D,depthMask);glUniform1i(glGetUniformLocation(p,"depthtex0"),2);
 glUniform1f(glGetUniformLocation(p,"viewWidth"),512);glUniform1f(glGetUniformLocation(p,"viewHeight"),512);glDrawArrays(GL_TRIANGLES,0,3);
}
int main(int argc,char **argv) {
 if(argc!=2)return 2;
 CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;
 if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj c;CGLCreateContext(f,0,&c);CGLDestroyPixelFormat(f);CGLSetCurrentContext(c);
 GLuint vao,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenFramebuffers(1,&fb);
 float *source=calloc(512*512*4,sizeof(float)),*pixels=calloc(128*128*4,sizeof(float));
 for(int y=252;y<260;y++)for(int x=252;x<260;x++)for(int ch=0;ch<3;ch++)source[(y*512+x)*4+ch]=4;
 GLuint input=image_texture(512,512,source),mid=image_texture(128,128,0),output=image_texture(128,128,0);free(source);
 float *mask=calloc(512*512*4,sizeof(float));for(int i=0;i<512*512;i++)mask[i*4+1]=1;emissionMask=image_texture(512,512,mask);memset(mask,0,512*512*4*sizeof(float));depthMask=image_texture(512,512,mask);free(mask);
 double radii[2]={0};printf("{\"cases\":{\n");
 for(int k=0;k<2;k++) {
  const char *tag=k?"normal":"small";char name[64];snprintf(name,sizeof name,"%s-horizontal",tag);GLuint h=link_program(argv[1],name);
  snprintf(name,sizeof name,"%s-vertical",tag);GLuint v=link_program(argv[1],name);draw(h,input,mid,fb);draw(v,mid,output,fb);glReadPixels(0,0,128,128,GL_RGBA,GL_FLOAT,pixels);
  double energy=0,moment=0;int extent=0;
  for(int y=0;y<128;y++)for(int x=0;x<128;x++) {double b=pixels[(y*128+x)*4];if(!isfinite(b)||b<0)return 5;energy+=b;double d=(x-63.5)*(x-63.5)+(y-63.5)*(y-63.5);moment+=d*b;if(b>0.00001&&d>extent)extent=(int)d;}
  radii[k]=sqrt(moment/fmax(energy,0.000001));printf("%s\"%s\":{\"energy\":%.6f,\"rms_radius_quarterres_pixels\":%.6f,\"nonzero_support_radius\":%.3f}",k?",\n":"",tag,energy,radii[k],sqrt(extent));glDeleteProgram(h);glDeleteProgram(v);
 }
 GLenum error=glGetError();printf("},\"opengl_errors\":%u,\"larger_radius_spreads_further\":%s}\n",error,radii[1]>radii[0]*1.5?"true":"false");CGLDestroyContext(c);free(pixels);return error||radii[1]<=radii[0]*1.5?6:0;
}

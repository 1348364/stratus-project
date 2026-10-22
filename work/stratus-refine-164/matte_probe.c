#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
int main(int argc,char**argv){
 if(argc!=2)return 2;
 CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);
 GLuint vao,texture,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&texture);glBindTexture(GL_TEXTURE_2D,texture);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,texture,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,1,1);
 const char*variants[]={"saved","retention-off","retention-max","dampness-off","dampness-max","nether","end"};
 struct {char*name;float sky,absorb,ny,px,pz,humidity,rain;int time;float dry;}cases[]={
 {"porous_top",1,.9,1,0,-4,.75,0,6000,1},{"porous_side",1,.9,0,0,-4,.75,0,6000,1},
 {"porous_grazing",1,.9,1,40,-.1,.75,0,6000,1},{"porous_night",1,.9,1,0,-4,.75,0,18000,1},
 {"sheltered_top",.4,.9,1,0,-4,.75,0,6000,1},{"sheltered_side",.4,.9,0,0,-4,.75,0,6000,1},
 {"sealed_cave",0,.9,1,0,-4,.75,1,6000,1},{"metal",1,0,1,0,-4,1,1,6000,1},
 {"metal_grazing",1,0,1,40,-.1,1,1,6000,1},{"rain",1,.9,1,0,-4,.75,1,6000,1},
 {"wood",1,.64,1,0,-4,.75,0,6000,1},{"polished",1,.02,1,0,-4,.75,0,6000,1},
 {"black",1,.9,1,0,-4,1,1,6000,0}};
 printf("{\"scope\":\"actual wetSurfaceResponse GLSL; camera invariance, no added light and material relationships\",\"samples\":[");int count=0;
 for(int j=0;j<7;j++){
 char vp[2048],fp[2048];snprintf(vp,sizeof vp,"%s/screen.vsh",argv[1]);snprintf(fp,sizeof fp,"%s/%s.fsh",argv[1],variants[j]);GLuint vs=compile(GL_VERTEX_SHADER,vp),fs=compile(GL_FRAGMENT_SHADER,fp);if(!vs||!fs)return 3;GLuint p=glCreateProgram();glAttachShader(p,vs);glAttachShader(p,fs);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)return 3;glUseProgram(p);
 for(int k=0;k<13;k++){
 glUniform3f(glGetUniformLocation(p,"probeDry"),.3*cases[k].dry,.2*cases[k].dry,.1*cases[k].dry);glUniform3f(glGetUniformLocation(p,"probeNormal"),cases[k].ny==0?1:0,cases[k].ny,0);glUniform3f(glGetUniformLocation(p,"probePoint"),cases[k].px,0,cases[k].pz);glUniform1f(glGetUniformLocation(p,"probeSky"),cases[k].sky);glUniform1f(glGetUniformLocation(p,"probeAbsorption"),cases[k].absorb);glUniform1f(glGetUniformLocation(p,"biomeHumidity"),cases[k].humidity);glUniform1f(glGetUniformLocation(p,"rainStrength"),cases[k].rain);glUniform1i(glGetUniformLocation(p,"worldTime"),cases[k].time);
 glDrawArrays(GL_TRIANGLES,0,3);float v[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,v);for(int b=0;b<4;b++)if(!isfinite(v[b]))return 5;
 printf("%s{\"variant\":\"%s\",\"case\":\"%s\",\"rgba\":[%.9f,%.9f,%.9f,%.9f]}",count++?",":"",variants[j],cases[k].name,v[0],v[1],v[2],v[3]);
 }glDeleteProgram(p);glDeleteShader(vs);glDeleteShader(fs);
 }
 GLenum e=glGetError();printf("],\"opengl_errors\":%u}\n",e);CGLDestroyContext(ctx);return e?6:0;
}

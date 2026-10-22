#define main validation_entry
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static double expected(double angle){
 double rayY=sin(angle),rayZ=cos(angle),finish=fmin(960.,(325.12-257.62)/rayY),tau=0.;int count=32768;double stride=finish/count;
 for(int i=0;i<count;i++){double t=(i+.5)*stride,h=(257.62+rayY*t-256.)/18.;tau+=.0004*exp(-h*h)*(1.+.6*sin((4096.+rayZ*t)*.025))*stride;}
 return 1.-exp(-tau);
}
int main(int argc,char**argv){if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);
 GLuint vao,tex,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&tex);glBindTexture(GL_TEXTURE_2D,tex);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,tex,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 3;glViewport(0,0,1,1);
 GLuint programs[2];char vp[2048],fp[2048];snprintf(vp,sizeof vp,"%s/screen.vsh",argv[1]);
 for(int k=0;k<2;k++){snprintf(fp,sizeof fp,"%s/cloud-%s.fsh",argv[1],k?"after":"before");GLuint v=compile(GL_VERTEX_SHADER,vp),s=compile(GL_FRAGMENT_SHADER,fp);if(!v||!s)return 4;GLuint p=glCreateProgram();glAttachShader(p,v);glAttachShader(p,s);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)return 4;programs[k]=p;}
 int budgets[]={32,72,152},widths[]={32,64,128};printf("{\"scope\":\"actual cloud integrator, analytic volume and independent dense CPU quadrature\",\"cases\":[");int total=0,failures=0;
 for(int i=0;i<3;i++)for(int j=0;j<3;j++){
 double boundary=atan(67.5/(widths[j]*(budgets[i]-2))),alpha[2][2],gold[2];
 for(int side=0;side<2;side++){
  double angle=boundary+(side?1:-1)*1e-6;gold[side]=expected(angle);
  for(int k=0;k<2;k++){GLuint p=programs[k];glUseProgram(p);glUniform1f(glGetUniformLocation(p,"probeAngle"),angle);glUniform1i(glGetUniformLocation(p,"probeSteps"),budgets[i]);glUniform1i(glGetUniformLocation(p,"worldTime"),6000);glUniform3f(glGetUniformLocation(p,"sunPosition"),0,1,0);glDrawArrays(GL_TRIANGLES,0,3);float value[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,value);alpha[k][side]=value[3];}
 }
 double old=fabs(alpha[0][0]-alpha[0][1]),now=fabs(alpha[1][0]-alpha[1][1]),reference=fabs(gold[0]-gold[1]),error=fmax(fabs(alpha[1][0]-gold[0]),fabs(alpha[1][1]-gold[1]));
 // A one-microradian crossing must remain continuous even when an old spacing
 // threshold falls there. Quadrature error is separately bounded, not hidden.
 if(!isfinite(now)||now>.0005||error>.035)failures++;
 printf("%s{\"steps\":%d,\"old_cell_threshold\":%d,\"old_alpha_jump\":%.9f,\"new_alpha_jump\":%.9f,\"reference_jump\":%.9f,\"max_quadrature_error\":%.9f}",total++?",":"",budgets[i],widths[j],old,now,reference,error);
 }
 GLenum error=glGetError();printf("],\"candidate_samples\":18,\"failures\":%d,\"opengl_errors\":%u}\n",failures,error);CGLDestroyContext(ctx);return failures||error?5:0;
}

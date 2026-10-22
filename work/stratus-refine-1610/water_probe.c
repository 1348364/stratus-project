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
static float body[3],sigma[3];
static void water(const float*c,float d,float*out){for(int j=0;j<3;j++){float t=expf(-sigma[j]*d);out[j]=c[j]*t+body[j]*(1-t);}}
int main(int argc,char**argv){
 if(argc!=2)return 2;CGLPixelFormatAttribute a[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj f;GLint n;if(CGLChoosePixelFormat(a,&f,&n)||!f)return 2;CGLContextObj ctx;if(CGLCreateContext(f,0,&ctx))return 2;CGLDestroyPixelFormat(f);CGLSetCurrentContext(ctx);
 GLuint vao,out,fb;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,0);glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;glViewport(0,0,1,1);
 GLuint p=makeProgram(argv[1]);glUseProgram(p);
 glUniform1i(glGetUniformLocation(p,"isEyeInWater"),1);glUniform1i(glGetUniformLocation(p,"worldTime"),6000);glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),0,240);glUniform3f(glGetUniformLocation(p,"biomeWaterTint"),.247,.463,.894);
 GLfloat inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.995f,0,0,-1,5.005f};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);
 const char*names[]={"colortex0","colortex1","colortex2","colortex3","colortex4","colortex8","colortex12","colortex13","colortex14","depthtex0","depthtex1"};GLuint tex[11];glGenTextures(11,tex);for(int i=0;i<11;i++){glActiveTexture(GL_TEXTURE0+i);glBindTexture(GL_TEXTURE_2D,tex[i]);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);glUniform1i(glGetUniformLocation(p,names[i]),i);}
 float absorption[3]={.205,.067,.026},blue[3]={.035,.125,.18},brown[3]={.16,.13,.065};float sediment=6.f*.035f;
 for(int j=0;j<3;j++){sigma[j]=(absorption[j]+sediment*.42f)*3.f/1.7f;body[j]=(blue[j]*(1-sediment*.8f)+brown[j]*(sediment*.8f))*.925f;}
 struct{char*name;float bg,fg,exit,tr;int special;}cases[]={
 {"air_receiver_near",5,2,2,1,0},{"air_receiver_far",50,2,2,1,0},{"submerged_receiver",1,1,2,1,0},{"deep_submerged",8,8,0,1,0},{"sky_after_exit",10000,2,2,1,0},{"sky_missing_exit",10000,10000,0,1,0},{"glass_before_exit",20,.5,2,.5,1},{"glass_after_exit",50,3,2,.5,1},{"additive_particle",20,.5,2,1,2},{"vertical_exit",50,1.2,1.2,1,0}};
 int fails=0;printf("{\"scope\":\"actual full-resolution water-resolve shader\",\"cases\":[");
 for(int k=0;k<10;k++){
 float data[11][4]={{0}},opaque[3]={.8,.4,.2},scene[3],fore[3]={.6,.01,.01};for(int j=0;j<3;j++){scene[j]=opaque[j];if(cases[k].special==1)scene[j]=opaque[j]*cases[k].tr+fore[j]*(1-cases[k].tr);if(cases[k].special==2)scene[j]+=j==0?.3f:(j==1?.1f:0.f);data[3][j]=scene[j];data[4][j]=opaque[j];}data[7][0]=cases[k].exit;data[7][3]=cases[k].exit>0?1:0;data[8][0]=cases[k].tr;data[9][0]=zdepth(cases[k].fg);data[10][0]=zdepth(cases[k].bg);
 for(int i=0;i<11;i++){glActiveTexture(GL_TEXTURE0+i);glBindTexture(GL_TEXTURE_2D,tex[i]);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,1,1,0,GL_RGBA,GL_FLOAT,data[i]);}
 float bg=cases[k].bg>999?0:cases[k].bg,fg=cases[k].fg>999?0:cases[k].fg;if(cases[k].exit>0){bg=bg>0?fminf(bg,cases[k].exit):cases[k].exit;fg=fg>0?fminf(fg,cases[k].exit):cases[k].exit;}
 float expected[3],back[3];water(opaque,bg,back);for(int j=0;j<3;j++){float att=expf(-sigma[j]*fg);if(cases[k].tr>=.999)expected[j]=back[j]+(scene[j]-opaque[j])*att;else expected[j]=back[j]*cases[k].tr+fore[j]*(1-cases[k].tr)*att+body[j]*(1-cases[k].tr)*(1-att);}
 glDrawArrays(GL_TRIANGLES,0,3);float value[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,value);float err=0;for(int j=0;j<3;j++){if(!isfinite(value[j]))fails++;err=fmaxf(err,fabsf(value[j]-expected[j]));}if(err>.00015)fails++;
 printf("%s{\"name\":\"%s\",\"rgb\":[%.7f,%.7f,%.7f],\"max_error\":%.8f}",k?",":"",cases[k].name,value[0],value[1],value[2],err);
 }
 GLenum error=glGetError();printf("],\"failures\":%d,\"opengl_errors\":%u}\n",fails,error);CGLDestroyContext(ctx);return fails||error?5:0;
}

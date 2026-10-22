#define main compile_main
#include "../stratus-check/native_compile.c"
#undef main
#include <math.h>
static GLuint program(const char*r,const char*n){char v[2048],f[2048];snprintf(v,sizeof v,"%s/screen.vsh",r);snprintf(f,sizeof f,"%s/%s.fsh",r,n);GLuint a=compile(GL_VERTEX_SHADER,v),b=compile(GL_FRAGMENT_SHADER,f);if(!a||!b)exit(3);GLuint p=glCreateProgram();glAttachShader(p,a);glAttachShader(p,b);glLinkProgram(p);GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok)exit(4);return p;}
static void integer(GLuint p,const char*n,int v){glUniform1i(glGetUniformLocation(p,n),v);}
static GLuint texture(int unit,GLenum format,float*data){GLuint t;glGenTextures(1,&t);glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);glTexImage2D(GL_TEXTURE_2D,0,format,128,128,0,GL_RGBA,GL_FLOAT,data);return t;}
static void matrices(GLuint p,float*c){float inv[]={1,0,0,0,0,1,0,0,0,0,0,-4.9995f,0,0,-1,5.0005f};float proj[]={1,0,0,0,0,1,0,0,0,0,-1.00020002f,-1,0,0,-.200020002f,0};glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inv);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjection"),1,GL_FALSE,proj);glUniformMatrix4fv(glGetUniformLocation(p,"gbufferModelView"),1,GL_FALSE,c);}
int main(int argc,char**argv){if(argc!=2)return 2;CGLPixelFormatAttribute attrs[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};CGLPixelFormatObj fmt;GLint n;if(CGLChoosePixelFormat(attrs,&fmt,&n)||!fmt)return 2;CGLContextObj ctx;if(CGLCreateContext(fmt,0,&ctx))return 2;CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);GLuint vao;glGenVertexArrays(1,&vao);glBindVertexArray(vao);GLuint fb;glGenFramebuffers(1,&fb);glBindFramebuffer(GL_FRAMEBUFFER,fb);glViewport(0,0,128,128);
float *depth=calloc(128*128*4,sizeof(float)),*normal=calloc(128*128*4,sizeof(float)),*colour=calloc(128*128*4,sizeof(float)),*pixels=malloc(128*128*4*sizeof(float));GLuint dt=texture(1,GL_RGBA32F,depth),nt=texture(2,GL_RGBA16F,normal),ct=texture(3,GL_RGBA32F,colour),planes=texture(4,GL_RGBA32F,0),out=texture(5,GL_RGBA32F,0);GLuint programs[]={program(argv[1],"trace-before"),program(argv[1],"trace-after")},producer=program(argv[1],"trace-planes"),query;glGenQueries(1,&query);printf("{\"scope\":\"Actual baseline/candidate receiver and optical trace GLSL with exact current GPU plane producer; isolated timings are not game FPS\",\"renderer\":\"%s\",\"timings\":[",glGetString(GL_RENDERER));int serial=0;
for(int scene=0;scene<7;scene++){
 float model[]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};if(scene==6){model[0]=.70710678f;model[2]=-.70710678f;model[8]=.70710678f;model[10]=.70710678f;}
 for(int y=0;y<128;y++)for(int x=0;x<128;x++){int i=(y*128+x)*4;float rx=(x+.5f)/64.f-1,ry=(y+.5f)/64.f-1,z=20,nx=0,ny=0,nz=1;
 if(scene==1){ny=1;nz=0;z=ry<-.03f?-2.5f/ry:2000;}
 if(scene==2)z=x<64?4:20;
 if(scene==3)z=x>55&&x<72&&y>40&&y<100?5:25;
 if(scene==4){nx=.3f;ny=.4f;nz=.8660254f;z=20.f/(nz-nx*rx-ny*ry);}
 if(scene==5)z=x<24?3:500;
 depth[i]=z>=1000?1:1.00010001f-.100010001f/z;
 // Stored world normal; scene6 rotates it into the view-space plane.
 if(scene==6){nx=-.70710678f;nz=.70710678f;}
 normal[i]=nx;normal[i+1]=ny;normal[i+2]=nz;normal[i+3]=z>=1000?0:1;
 colour[i]=.2f+.5f*(x/8%2);colour[i+1]=.1f+.5f*(y/8%2);colour[i+2]=.25f+.25f*((x+y)/8%2);colour[i+3]=1;
 }
 GLuint ts[]={dt,nt,ct};float*inputs[]={depth,normal,colour};for(int j=0;j<3;j++){glActiveTexture(GL_TEXTURE1+j);glBindTexture(GL_TEXTURE_2D,ts[j]);glTexSubImage2D(GL_TEXTURE_2D,0,0,0,128,128,GL_RGBA,GL_FLOAT,inputs[j]);}
 glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,planes,0);glUseProgram(producer);integer(producer,"depthtex1",1);integer(producer,"normalTex",2);matrices(producer,model);glDrawArrays(GL_TRIANGLES,0,3);
 glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);
 for(int mode=0;mode<2;mode++)for(int quality=0;quality<3;quality++)for(int j=0;j<2;j++){GLuint p=programs[j];glUseProgram(p);matrices(p,model);integer(p,"depthtex1",1);integer(p,"colortex10",2);integer(p,"colortex4",3);integer(p,"probeMode",mode);integer(p,"probeQuality",quality);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,128,128,GL_RGBA,GL_FLOAT,pixels);char file[2048];snprintf(file,sizeof file,"%s/interval-%d-%d-%d-%d.rgba32f",argv[1],scene,mode,quality,j);FILE*f=fopen(file,"wb");fwrite(pixels,sizeof(float),128*128*4,f);fclose(f);}
 for(int round=0;round<6;round++)for(int order=0;order<2;order++){int j=(round+order)%2;GLuint p=programs[j];glUseProgram(p);integer(p,"colortex10",2);integer(p,"probeMode",1);integer(p,"probeQuality",2);glDrawArrays(GL_TRIANGLES,0,3);glFinish();glBeginQuery(GL_TIME_ELAPSED,query);for(int k=0;k<16;k++)glDrawArrays(GL_TRIANGLES,0,3);glEndQuery(GL_TIME_ELAPSED);GLuint64 ns;glGetQueryObjectui64v(query,GL_QUERY_RESULT,&ns);printf("%s{\"scene\":%d,\"round\":%d,\"variant\":%d,\"gpu_ms\":%.7f}",serial++?",":"",scene,round,j,(double)ns/16000000.0);fflush(stdout);}
}
GLenum e=glGetError();printf("],\"opengl_errors\":%u}\n",e);CGLDestroyContext(ctx);return e?5:0;}

#include "probe-support.h"
#include <math.h>

enum{WIDTH=1280,HEIGHT=720};
static void textureInput(GLuint p,int unit,const char *name,int kind){
    size_t count=WIDTH*HEIGHT*4;float *data=calloc(count,sizeof(float));
    for(int y=0;y<HEIGHT;y++)for(int x=0;x<WIDTH;x++){
        int i=(y*WIDTH+x)*4;float u=(x+.5f)/WIDTH,v=(y+.5f)/HEIGHT;
        float alpha=x<WIDTH/3?0.f:(x<2*WIDTH/3?.4f:.75f);
        float base[3]={.12f+u*.4f,.2f+v*.2f,.3f};
        switch(kind){
        case 0:data[i+3]=(x>20&&y>20)?1.f:0.f;break;
        case 1:data[i+(x<WIDTH/2?1:2)]=1.f;data[i+3]=1.f;break;
        case 2:data[i]=5.f+u*30.f;data[i+1]=1.f;data[i+3]=1.f;break;
        case 3:for(int j=0;j<3;j++)data[i+j]=base[j]*(1.f-alpha)+(j==0?.65f:.04f)*alpha;data[i+3]=1.f;break;
        case 4:for(int j=0;j<3;j++)data[i+j]=base[j];data[i+3]=1.f;break;
        case 8:data[i]=.247f;data[i+1]=.463f;data[i+2]=.894f;break;
        case 12:data[i]=.03f+u*.05f;data[i+1]=.12f+v*.1f;data[i+2]=.2f;data[i+3]=1.f;break;
        case 14:data[i]=1.f-alpha;break;
        default:data[i]=.99f;
        }
    }
    GLuint t;glGenTextures(1,&t);glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,WIDTH,HEIGHT,0,GL_RGBA,GL_FLOAT,data);free(data);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
    integer(p,name,unit);
}
static void setupProgram(GLuint p,int eye){
    glUseProgram(p);integer(p,"isEyeInWater",eye);integer(p,"worldTime",6000);
    scalar(p,"viewWidth",WIDTH);scalar(p,"viewHeight",HEIGHT);scalar(p,"biomeHumidity",.75f);scalar(p,"biomeSilt",.05f);
    glUniform2i(glGetUniformLocation(p,"eyeBrightnessSmooth"),0,240);
    glUniform3f(glGetUniformLocation(p,"biomeWaterTint"),.247f,.463f,.894f);
    GLfloat inverse[16]={1,0,0,0,0,1,0,0,0,0,0,-4.995f,0,0,-1,5.005f};
    glUniformMatrix4fv(glGetUniformLocation(p,"gbufferProjectionInverse"),1,GL_FALSE,inverse);
    const char*names[]={"colortex0","colortex1","colortex2","colortex3","colortex4","colortex8","colortex12","colortex14","depthtex0","depthtex1"};
    for(int i=0;i<10;i++)integer(p,names[i],i);
}
static double batch(GLuint p){
    GLuint q;glGenQueries(1,&q);glUseProgram(p);glBeginQuery(GL_TIME_ELAPSED,q);
    for(int i=0;i<24;i++)glDrawArrays(GL_TRIANGLES,0,3);
    glEndQuery(GL_TIME_ELAPSED);GLuint64 ns;glGetQueryObjectui64v(q,GL_QUERY_RESULT,&ns);glDeleteQueries(1,&q);
    return (double)ns/24000000.;
}
int main(int argc,char**argv){
    if(argc!=2)return 2;
    CGLPixelFormatAttribute attrs[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};
    CGLPixelFormatObj format;GLint n;if(CGLChoosePixelFormat(attrs,&format,&n)||!format)return 2;
    CGLContextObj context;if(CGLCreateContext(format,0,&context))return 2;CGLDestroyPixelFormat(format);CGLSetCurrentContext(context);
    GLuint vao,out,fbo;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&out);glBindTexture(GL_TEXTURE_2D,out);
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,WIDTH,HEIGHT,0,GL_RGBA,GL_FLOAT,0);
    glGenFramebuffers(1,&fbo);glBindFramebuffer(GL_FRAMEBUFFER,fbo);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,out,0);
    if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 4;
    glViewport(0,0,WIDTH,HEIGHT);
    GLuint p[2]={program(argv[1],"previous"),program(argv[1],"current")};
    const char*names[]={"colortex0","colortex1","colortex2","colortex3","colortex4","colortex8","colortex12","colortex14","depthtex0","depthtex1"};
    int kinds[]={0,1,2,3,4,8,12,14,20,21};glUseProgram(p[0]);
    for(int i=0;i<10;i++)textureInput(p[0],i,names[i],kinds[i]);
    float *before=malloc(WIDTH*HEIGHT*4*sizeof(float)),*after=malloc(WIDTH*HEIGHT*4*sizeof(float));
    int failures=0;printf("{\"scope\":\"synthetic actual water-resolve pass, not Minecraft FPS\",\"size\":[%d,%d],\"cases\":[",WIDTH,HEIGHT);
    for(int eye=0;eye<2;eye++){
        for(int a=0;a<2;a++){setupProgram(p[a],eye);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,WIDTH,HEIGHT,GL_RGBA,GL_FLOAT,a?after:before);}
        double max=0;for(int i=0;i<WIDTH*HEIGHT*4;i++){double d=fabs(before[i]-after[i]);if(!isfinite(d))failures++;if(d>max)max=d;}
        if(max>0.0001)failures++;
        for(int a=0;a<2;a++){setupProgram(p[a],eye);for(int i=0;i<8;i++)glDrawArrays(GL_TRIANGLES,0,3);}glFinish();
        double times[2]={0,0};int order[]={0,1,1,0,0,1,1,0};
        for(int i=0;i<8;i++){setupProgram(p[order[i]],eye);times[order[i]]+=batch(p[order[i]])/4.;}
        printf("%s{\"underwater\":%d,\"max_rgb_error\":%.9f,\"previous_pass_ms\":%.6f,\"current_pass_ms\":%.6f}",eye?",":"",eye,max,times[0],times[1]);
    }
    unsigned error=glGetError();printf("],\"failures\":%d,\"opengl_errors\":%u}\n",failures,error);
    free(before);free(after);CGLDestroyContext(context);return failures||error?5:0;
}

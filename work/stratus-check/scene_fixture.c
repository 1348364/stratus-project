#define main validation_entry
#include "native_compile.c"
#undef main
#include <math.h>

typedef struct { float p[4], c[4], n[3], uv[4], lm[4], material[4]; } Vertex;
static Vertex vertices[300000]; static int vertex_count=0;
static float camera[3]={0,76,22}, mv[16], inv[16], proj[16], pinv[16];
static int W=1100,H=680;
static void identity(float *m){ memset(m,0,64);m[0]=m[5]=m[10]=m[15]=1; }
static void uniform1(GLuint p,const char*n,float x){glUniform1f(glGetUniformLocation(p,n),x);}
static void integer(GLuint p,const char*n,int x){glUniform1i(glGetUniformLocation(p,n),x);}
static void matrix(GLuint p,const char*n,float*m){glUniformMatrix4fv(glGetUniformLocation(p,n),1,GL_FALSE,m);}
static void vec3(GLuint p,const char*n,float x,float y,float z){glUniform3f(glGetUniformLocation(p,n),x,y,z);}
static void point(float x,float y,float z,float r,float g,float b,float nx,float ny,float nz,int material){
 Vertex*v=&vertices[vertex_count++]; memset(v,0,sizeof(*v));
 v->p[0]=x-camera[0];v->p[1]=y-camera[1];v->p[2]=z-camera[2];v->p[3]=1;
 v->c[0]=r;v->c[1]=g;v->c[2]=b;v->c[3]=1;
 v->n[0]=nx;v->n[1]=ny;v->n[2]=nz;v->uv[0]=v->uv[1]=.5;
 v->lm[0]=.03125;v->lm[1]=.96875;v->material[0]=material;
}
static void quad(float*p,float r,float g,float b,float nx,float ny,float nz,int mat){
 int index[6]={0,1,2,0,2,3}; for(int i=0;i<6;i++){int j=index[i]*3;point(p[j],p[j+1],p[j+2],r,g,b,nx,ny,nz,mat);}
}
static void box(float x,float y,float z,float sx,float sy,float sz,float r,float g,float b,int mat){
 float a=x-sx*.5,c=x+sx*.5,d=z-sz*.5,e=z+sz*.5,f=y+sy;
 float top[]={a,f,d,c,f,d,c,f,e,a,f,e};quad(top,r,g,b,0,1,0,mat);
 float front[]={a,y,e,c,y,e,c,f,e,a,f,e};quad(front,r,g,b,0,0,1,mat);
 float back[]={c,y,d,a,y,d,a,f,d,c,f,d};quad(back,r,g,b,0,0,-1,mat);
 float left[]={a,y,d,a,y,e,a,f,e,a,f,d};quad(left,r,g,b,-1,0,0,mat);
 float right[]={c,y,e,c,y,d,c,f,d,c,f,e};quad(right,r,g,b,1,0,0,mat);
}
static void tree(float x,float y,float z,float height){
 box(x,y,z,.8,height*.85,.8,.32,.24,.15,4111);
 for(int k=0;k<4;k++){float width=5.8-k*1.25; box(x,y+height*.35+k*height*.16,z,width,height*.22,width,.20+k*.007,.34+k*.005,.24,4113);}
}
static void build_opaque(void){
 vertex_count=0;
 box(0,56,-65,90,2,210,.44,.45,.43,4112);
 // Broad stepped banks, visible through the shallow margin.
 for(int k=0;k<4;k++){
  float x=25+k*8;
  box(-x,58,-70,10,6+k*5,205,.38,.48,.25,4110);
  box( x,58,-70,10,8+k*6,205,.37,.46,.26,4110);
 }
 for(int row=0;row<13;row++){
  float z=8-row*12;
  for(int side=-1;side<=1;side+=2){
   tree(side*(27+(row%3)*4),66+(row%3)*3,z,12+(row%4)*2);
   tree(side*(42+(row%2)*5),76,z-5,15);
  }
 }
 box(6,58,-48,10,8,14,.40,.50,.30,4110);tree(5,66,-48,14);tree(10,66,-52,10);
 // A matte dock plus an emissive interior that must not appear in SSR.
 for(int i=0;i<9;i++)box(-13+i*1.0,64.7,6,1,0.35,4,.45,.32,.20,4111);
 box(-13,60,7,.5,5.1,.5,.34,.25,.16,4111);
 box(-13,65.2,7,.65,.75,.65,1,.56,.15,4101);
}
static void build_water(void){
 vertex_count=0;float p[]={-21,64,-170,21,64,-170,21,64,15,-21,64,15};quad(p,.20,.40,.61,0,1,0,4100);
}
static GLuint program(const char*root,const char*name){
 char a[2048],b[2048];snprintf(a,sizeof a,"%s/%s.vsh",root,name);snprintf(b,sizeof b,"%s/%s.fsh",root,name);
 GLuint v=compile(GL_VERTEX_SHADER,a),f=compile(GL_FRAGMENT_SHADER,b);if(!v||!f)exit(3);
 GLuint p=glCreateProgram();glAttachShader(p,v);glAttachShader(p,f);glLinkProgram(p);
 GLint ok;glGetProgramiv(p,GL_LINK_STATUS,&ok);if(!ok){char log[4096];glGetProgramInfoLog(p,4096,0,log);fprintf(stderr,"%s\n",log);exit(3);}return p;
}
static GLuint texture(GLint format,GLenum type){
 GLuint t;glGenTextures(1,&t);glBindTexture(GL_TEXTURE_2D,t);
 glTexImage2D(GL_TEXTURE_2D,0,format,W,H,0,format==GL_DEPTH_COMPONENT32F?GL_DEPTH_COMPONENT:GL_RGBA,type,NULL);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);return t;
}
static GLuint framebuffer(GLuint a,GLuint b,GLuint c,GLuint d,GLuint depth){
 GLuint f;glGenFramebuffers(1,&f);glBindFramebuffer(GL_FRAMEBUFFER,f);
 GLuint textures[]={a,b,c,d};GLenum draws[4];int total=0;
 for(int i=0;i<4;i++)if(textures[i]){draws[total++]=GL_COLOR_ATTACHMENT0+i;glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0+i,GL_TEXTURE_2D,textures[i],0);}
 if(depth)glFramebufferTexture2D(GL_FRAMEBUFFER,GL_DEPTH_ATTACHMENT,GL_TEXTURE_2D,depth,0);
 glDrawBuffers(total,draws);if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE){fprintf(stderr,"Bad framebuffer\n");exit(4);}return f;
}
static void bind(GLuint p,const char*n,GLuint t,int unit){glActiveTexture(GL_TEXTURE0+unit);glBindTexture(GL_TEXTURE_2D,t);integer(p,n,unit);}
static void setup(GLuint p,GLuint white){
 glUseProgram(p);matrix(p,"shim_ModelViewMatrix",mv);matrix(p,"shim_ProjectionMatrix",proj);
 // ftransform uses the combined transform.
 float mvp[16]={0};for(int c=0;c<4;c++)for(int r=0;r<4;r++)for(int k=0;k<4;k++)mvp[c*4+r]+=proj[k*4+r]*mv[c*4+k];
 matrix(p,"shim_ModelViewProjectionMatrix",mvp);matrix(p,"gbufferModelView",mv);matrix(p,"gbufferModelViewInverse",inv);
 matrix(p,"gbufferProjection",proj);matrix(p,"gbufferProjectionInverse",pinv);
 float m3[]={mv[0],mv[1],mv[2],mv[4],mv[5],mv[6],mv[8],mv[9],mv[10]};
 glUniformMatrix3fv(glGetUniformLocation(p,"shim_NormalMatrix"),1,GL_FALSE,m3);
 float tex[128];for(int i=0;i<8;i++)identity(tex+i*16);glUniformMatrix4fv(glGetUniformLocation(p,"shim_TextureMatrix"),8,GL_FALSE,tex);
 vec3(p,"cameraPosition",camera[0],camera[1],camera[2]);vec3(p,"fogColor",.70,.75,.81);
 uniform1(p,"far",240);uniform1(p,"fogStart",100000);uniform1(p,"fogEnd",100001);integer(p,"fogMode",9729);integer(p,"fogShape",1);
 integer(p,"worldTime",6000);integer(p,"isEyeInWater",0);uniform1(p,"viewWidth",W);uniform1(p,"viewHeight",H);
 uniform1(p,"frameTimeCounter",10);bind(p,"gtexture",white,0);bind(p,"lightmap",white,1);
}
static void draw(GLuint p,GLuint buffer){
 glUseProgram(p);glBindBuffer(GL_ARRAY_BUFFER,buffer);glBufferData(GL_ARRAY_BUFFER,vertex_count*sizeof(Vertex),vertices,GL_STREAM_DRAW);
 const char*names[]={"shim_Vertex","shim_Color","shim_Normal","shim_MultiTexCoord0","shim_MultiTexCoord1","mc_Entity"};
 int sizes[]={4,4,3,4,4,4},offs[]={0,4,8,11,15,19};
 for(int i=0;i<6;i++){GLint loc=glGetAttribLocation(p,names[i]);if(loc>=0){glEnableVertexAttribArray(loc);glVertexAttribPointer(loc,sizes[i],GL_FLOAT,GL_FALSE,sizeof(Vertex),(void*)(offs[i]*sizeof(float)));}}
 glDrawArrays(GL_TRIANGLES,0,vertex_count);
 for(int i=0;i<6;i++){GLint loc=glGetAttribLocation(p,names[i]);if(loc>=0)glDisableVertexAttribArray(loc);}
}
static void fullscreen(GLuint p,GLuint buffer){
 float eye[3];memcpy(eye,camera,12);camera[0]=camera[1]=camera[2]=0;vertex_count=0;
 float a[]={-1,-1,0,1,-1,0,1,1,0,-1,1,0};quad(a,1,1,1,0,0,1,0);memcpy(camera,eye,12);
 for(int i=0;i<vertex_count;i++){vertices[i].uv[0]=(vertices[i].p[0]+1)*.5;vertices[i].uv[1]=(vertices[i].p[1]+1)*.5;}
 float id[16];identity(id);matrix(p,"shim_ModelViewProjectionMatrix",id);draw(p,buffer);
}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: render_fixture expanded-variant output.ppm\n");return 2;}
 CGLPixelFormatAttribute attrs[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};
 CGLPixelFormatObj fmt;GLint n;CGLError e=CGLChoosePixelFormat(attrs,&fmt,&n);if(e||!fmt){fprintf(stderr,"%s\n",CGLErrorString(e));return 2;}
 CGLContextObj ctx;CGLCreateContext(fmt,0,&ctx);CGLDestroyPixelFormat(fmt);CGLSetCurrentContext(ctx);
 GLuint vao,buffer;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenBuffers(1,&buffer);
 float angle=.19,c=cosf(angle),s=sinf(angle);identity(mv);mv[5]=c;mv[6]=s;mv[9]=-s;mv[10]=c;
 identity(inv);inv[5]=c;inv[6]=-s;inv[9]=s;inv[10]=c;
 memset(proj,0,64);float f=1/tanf(.95*.5),near=.1,far=500;proj[0]=f/((float)W/H);proj[5]=f;proj[10]=-(far+near)/(far-near);proj[11]=-1;proj[14]=-2*far*near/(far-near);
 memset(pinv,0,64);pinv[0]=1/proj[0];pinv[5]=1/proj[5];pinv[11]=1/proj[14];pinv[14]=-1;pinv[15]=proj[10]/proj[14];
 GLuint white;glGenTextures(1,&white);glBindTexture(GL_TEXTURE_2D,white);unsigned char pixel[]={255,255,255,255};glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,1,1,0,GL_RGBA,GL_UNSIGNED_BYTE,pixel);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
 GLuint albedo=texture(GL_RGBA8,GL_UNSIGNED_BYTE),shape=texture(GL_RGBA16F,GL_FLOAT),illumination=texture(GL_RGBA8,GL_UNSIGNED_BYTE);
 GLuint depth=texture(GL_DEPTH_COMPONENT32F,GL_FLOAT),depth1=texture(GL_DEPTH_COMPONENT32F,GL_FLOAT);
 framebuffer(albedo,shape,illumination,0,depth);glViewport(0,0,W,H);glClearColor(0,0,0,0);glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);glEnable(GL_DEPTH_TEST);glDisable(GL_CULL_FACE);glDisable(GL_BLEND);
 GLuint geometry=program(argv[1],"gbuffers_terrain");setup(geometry,white);build_opaque();draw(geometry,buffer);
 glBindTexture(GL_TEXTURE_2D,depth1);glCopyTexSubImage2D(GL_TEXTURE_2D,0,0,0,0,0,W,H);
 GLuint scene3=texture(GL_RGBA16F,GL_FLOAT),snapshot4=texture(GL_RGBA16F,GL_FLOAT);
 GLuint water0=texture(GL_RGBA8,GL_UNSIGNED_BYTE),water1=texture(GL_RGBA16F,GL_FLOAT);
 framebuffer(scene3,snapshot4,water0,water1,0);
 GLuint deferred=program(argv[1],"deferred");setup(deferred,white);
 bind(deferred,"colortex0",albedo,2);bind(deferred,"colortex1",shape,3);bind(deferred,"colortex2",illumination,4);bind(deferred,"depthtex1",depth1,5);
 glDisable(GL_DEPTH_TEST);fullscreen(deferred,buffer);
 framebuffer(scene3,water0,water1,0,depth);GLuint water=program(argv[1],"gbuffers_water");setup(water,white);
 glEnable(GL_DEPTH_TEST);glEnable(GL_BLEND);glBlendFuncSeparate(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA,GL_ONE,GL_ONE_MINUS_SRC_ALPHA);build_water();draw(water,buffer);glDisable(GL_BLEND);
 GLuint finished3=texture(GL_RGBA16F,GL_FLOAT);framebuffer(finished3,0,0,0,0);
 GLuint composite=program(argv[1],"composite");setup(composite,white);
 bind(composite,"colortex0",water0,0);bind(composite,"colortex1",water1,1);bind(composite,"colortex2",illumination,2);
 bind(composite,"colortex3",scene3,3);bind(composite,"colortex4",snapshot4,4);bind(composite,"depthtex0",depth,5);bind(composite,"depthtex1",depth1,6);
 glDisable(GL_DEPTH_TEST);fullscreen(composite,buffer);
 GLuint display=texture(GL_RGBA8,GL_UNSIGNED_BYTE);framebuffer(display,0,0,0,0);GLuint final=program(argv[1],"final");setup(final,white);bind(final,"colortex3",finished3,2);fullscreen(final,buffer);glFinish();
 GLenum error=glGetError();if(error){fprintf(stderr,"GL ERROR 0x%x\n",error);return 5;}
 unsigned char*pixels=malloc(W*H*4);glReadPixels(0,0,W,H,GL_RGBA,GL_UNSIGNED_BYTE,pixels);FILE*out=fopen(argv[2],"wb");fprintf(out,"P6\n%d %d\n255\n",W,H);
 for(int y=H-1;y>=0;y--)for(int x=0;x<W;x++)fwrite(pixels+(y*W+x)*4,1,3,out);fclose(out);free(pixels);
 printf("Rendered standalone synthetic fixture: %s\n",argv[2]);CGLDestroyContext(ctx);return 0;
}

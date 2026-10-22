#define main compiler_main
#include "../stratus-check/native_compile.c"
#undef main
int main(void){
 CGLPixelFormatAttribute attrs[]={kCGLPFAOpenGLProfile,(CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,kCGLPFAAccelerated,0};
 CGLPixelFormatObj pf;GLint n;if(CGLChoosePixelFormat(attrs,&pf,&n)||!pf)return 2;
 CGLContextObj context;if(CGLCreateContext(pf,0,&context))return 2;CGLDestroyPixelFormat(pf);CGLSetCurrentContext(context);
 GLuint vao,tex,fbo;glGenVertexArrays(1,&vao);glBindVertexArray(vao);glGenTextures(1,&tex);glBindTexture(GL_TEXTURE_2D,tex);
 glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA16F,1,1,0,GL_RGBA,GL_FLOAT,0);
 glGenFramebuffers(1,&fbo);glBindFramebuffer(GL_FRAMEBUFFER,fbo);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,tex,0);
 if(glCheckFramebufferStatus(GL_FRAMEBUFFER)!=GL_FRAMEBUFFER_COMPLETE)return 3;
 const char*vs="#version 330 core\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.-1.,0.,1.);}";
 const char*fs="#version 330 core\nuniform vec4 layer;out vec4 result;void main(){result=layer;}";
 GLuint v=glCreateShader(GL_VERTEX_SHADER),f=glCreateShader(GL_FRAGMENT_SHADER);glShaderSource(v,1,&vs,0);glCompileShader(v);glShaderSource(f,1,&fs,0);glCompileShader(f);
 GLuint program=glCreateProgram();glAttachShader(program,v);glAttachShader(program,f);glLinkProgram(program);GLint ok;glGetProgramiv(program,GL_LINK_STATUS,&ok);if(!ok)return 4;
 glUseProgram(program);glViewport(0,0,1,1);GLint uniform=glGetUniformLocation(program,"layer");
 glClearColor(.9,.7,.2,1.);glClear(GL_COLOR_BUFFER_BIT);glEnable(GL_BLEND);
 glBlendFuncSeparate(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA,GL_ZERO,GL_ONE_MINUS_SRC_ALPHA);
 glUniform4f(uniform,1.,0.,0.,.4);glDrawArrays(GL_TRIANGLES,0,3);
 float first[4],second[4],additive[4];glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,first);
 glUniform4f(uniform,0.,0.,1.,.25);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,second);
 glBlendFuncSeparate(GL_SRC_ALPHA,GL_ONE,GL_ZERO,GL_ONE);glUniform4f(uniform,.4,.2,.1,.5);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,additive);
 printf("{\"red_layer\":[%.6f,%.6f,%.6f,%.6f],\"stacked\":[%.6f,%.6f,%.6f,%.6f],\"additive\":[%.6f,%.6f,%.6f,%.6f],\"gl_error\":%u}\n",first[0],first[1],first[2],first[3],second[0],second[1],second[2],second[3],additive[0],additive[1],additive[2],additive[3],glGetError());
 glTexImage2D(GL_TEXTURE_2D,0,GL_R16F,1,1,0,GL_RED,GL_FLOAT,0);glClearColor(1.,1.,1.,1.);glClear(GL_COLOR_BUFFER_BIT);
 glBlendFuncSeparate(GL_ZERO,GL_ONE_MINUS_SRC_ALPHA,GL_ZERO,GL_ONE);
 glUniform4f(uniform,0.,0.,0.,.4);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,first);
 glUniform4f(uniform,0.,0.,0.,.25);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,second);
 glUniform4f(uniform,0.,0.,0.,0.);glDrawArrays(GL_TRIANGLES,0,3);glReadPixels(0,0,1,1,GL_RGBA,GL_FLOAT,additive);
 fprintf(stderr,"{\"R16F_red_layer\":%.6f,\"R16F_stacked\":%.6f,\"R16F_water_preserves\":%.6f,\"gl_error\":%u}\n",first[0],second[0],additive[0],glGetError());
 CGLDestroyContext(context);return 0;
}

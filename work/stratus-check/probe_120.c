#define main validation_entry
#include "native_compile.c"
#undef main

static GLuint program(const char *root, const char *name) {
    char v[2048], f[2048];
    snprintf(v, sizeof v, "%s/screen.vsh", root);
    snprintf(f, sizeof f, "%s/%s.fsh", root, name);
    GLuint vertex = compile(GL_VERTEX_SHADER, v), fragment = compile(GL_FRAGMENT_SHADER, f);
    if (!vertex || !fragment) exit(3);
    GLuint p = glCreateProgram(); glAttachShader(p, vertex); glAttachShader(p, fragment); glLinkProgram(p);
    GLint ok; glGetProgramiv(p, GL_LINK_STATUS, &ok); if (!ok) exit(3);
    return p;
}
static void scalar(GLuint p, const char *name, float value) { glUniform1f(glGetUniformLocation(p, name), value); }
static void integer(GLuint p, const char *name, int value) { glUniform1i(glGetUniformLocation(p, name), value); }
static void sample(GLuint p, float distance, float sky, int eye, float status, int mode, float *out) {
    glUseProgram(p);
    glUniform3f(glGetUniformLocation(p, "cameraPosition"), 0, 70, 0);
    glUniform3f(glGetUniformLocation(p, "fogColor"), .65, .70, .75);
    scalar(p, "far", 512); scalar(p, "fogStart", 0); scalar(p, "fogEnd", 160);
    integer(p, "fogMode", 9729); integer(p, "fogShape", 0); integer(p, "worldTime", mode == 1 ? 18000 : 6000);
    integer(p, "isEyeInWater", eye); scalar(p, "blindness", status); scalar(p, "darknessFactor", 0);
    scalar(p, "rainStrength", 0); scalar(p, "probeDistance", distance);
    scalar(p, "probeSky", sky); integer(p, "probeMode", mode);
    glDrawArrays(GL_TRIANGLES, 0, 3); glReadPixels(0, 0, 1, 1, GL_RGBA, GL_FLOAT, out);
}
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    CGLPixelFormatAttribute attributes[] = {kCGLPFAOpenGLProfile, (CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core, kCGLPFAAccelerated, 0};
    CGLPixelFormatObj format; GLint count;
    if (CGLChoosePixelFormat(attributes, &format, &count) || !format) return 2;
    CGLContextObj context; CGLCreateContext(format, 0, &context); CGLDestroyPixelFormat(format); CGLSetCurrentContext(context);
    GLuint vao, texture, framebuffer;
    glGenVertexArrays(1, &vao); glBindVertexArray(vao);
    glGenTextures(1, &texture); glBindTexture(GL_TEXTURE_2D, texture);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 1, 1, 0, GL_RGBA, GL_FLOAT, NULL);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glGenFramebuffers(1, &framebuffer); glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0);
    if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) return 4;
    glViewport(0, 0, 1, 1);
    GLuint previous = program(argv[1], "previous"), current = program(argv[1], "current");
    struct { const char *name; float distance, sky; int eye; float status; int mode; } cases[] = {
{"wet_absorption",0,1,0,0,0},
{"covered_moisture",1,1,0,0,0},
{"entity_moisture",2,1,0,0,0},
{"smooth_material_absorption",3,1,0,0,0},
{"wet_grazing",4,1,0,0,0},
{"wet_front",5,1,0,0,0},
{"entity_top",6,1,0,0,0},
{"entity_side",7,1,0,0,0},
{"entity_bottom",8,1,0,0,0},
{"entity_in_darkness",9,1,0,0,0},
{"emissive_in_darkness",10,1,0,0,0},
{"billboard_orientation",11,1,0,0,0},
{"water_split_path",12,1,0,0,0},
{"water_twenty_blocks",13,1,0,0,0},
{"cloud_volume_y",14,1,0,0,0},
{"cloud_view_alpha",15,1,0,0,0},
{"cloud_occlusion",16,1,0,0,0},
{"cloud_shadow",17,1,0,0,0},
{"sun_day",18,1,0,0,0},
{"sun_night",19,1,0,0,1},
{"sky_away_from_sun",20,1,0,0,0}
};
    printf("{\"cases\":{\n");
    for (int i=0; i<sizeof(cases)/sizeof(cases[0]); i++) {
        float a[4], b[4];
        sample(previous,cases[i].distance,cases[i].sky,cases[i].eye,cases[i].status,cases[i].mode,a);
        sample(current,cases[i].distance,cases[i].sky,cases[i].eye,cases[i].status,cases[i].mode,b);
        printf("%s\"%s\":{\"previous\":[%.8f,%.8f,%.8f,%.8f],\"current\":[%.8f,%.8f,%.8f,%.8f]}\n",
               i?",":"",cases[i].name,a[0],a[1],a[2],a[3],b[0],b[1],b[2],b[3]);
    }
    GLenum error=glGetError(); printf("},\"opengl_errors\":%u}\n",error);
    CGLDestroyContext(context); return error?5:0;
}

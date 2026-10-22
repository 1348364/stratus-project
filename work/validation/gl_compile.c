#define GL_SILENCE_DEPRECATION
#include <OpenGL/OpenGL.h>
#include <OpenGL/gl3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *read_text(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) { perror(path); exit(2); }
    fseek(f, 0, SEEK_END); long n = ftell(f); rewind(f);
    char *text = calloc((size_t)n + 1, 1);
    if (!text || fread(text, 1, (size_t)n, f) != (size_t)n) exit(2);
    fclose(f); return text;
}

static GLuint compile(GLenum type, const char *path) {
    char *text = read_text(path);
    const GLchar *sources[] = {text};
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, sources, NULL); glCompileShader(shader);
    GLint ok = 0, length = 0;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &ok);
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
    if (length > 1) {
        char *log = calloc((size_t)length, 1);
        glGetShaderInfoLog(shader, length, NULL, log);
        fprintf(stderr, "%s:\n%s\n", path, log); free(log);
    }
    free(text);
    if (!ok) { glDeleteShader(shader); return 0; }
    return shader;
}

static int validate_pair(const char *vertex, const char *fragment) {
    GLuint vs = compile(GL_VERTEX_SHADER, vertex);
    GLuint fs = compile(GL_FRAGMENT_SHADER, fragment);
    if (!vs || !fs) return 1;
    GLuint program = glCreateProgram();
    glAttachShader(program, vs); glAttachShader(program, fs); glLinkProgram(program);
    GLint ok = 0, length = 0;
    glGetProgramiv(program, GL_LINK_STATUS, &ok);
    glGetProgramiv(program, GL_INFO_LOG_LENGTH, &length);
    if (length > 1) {
        char *log = calloc((size_t)length, 1);
        glGetProgramInfoLog(program, length, NULL, log);
        fprintf(stderr, "Link %s:\n%s\n", vertex, log); free(log);
    }
    glDeleteProgram(program); glDeleteShader(vs); glDeleteShader(fs);
    printf("%s %s\n", ok ? "PASS" : "FAIL", vertex);
    return ok ? 0 : 1;
}

int main(int argc, char **argv) {
    CGLPixelFormatAttribute attrs[] = {
        kCGLPFAOpenGLProfile, (CGLPixelFormatAttribute)kCGLOGLPVersion_3_2_Core,
        kCGLPFAAccelerated, (CGLPixelFormatAttribute)0
    };
    CGLPixelFormatObj format = NULL; GLint count = 0;
    CGLError error = CGLChoosePixelFormat(attrs, &format, &count);
    if (error != kCGLNoError || !format) {
        fprintf(stderr, "CGLChoosePixelFormat: %s\n", CGLErrorString(error)); return 2;
    }
    CGLContextObj context = NULL;
    error = CGLCreateContext(format, NULL, &context); CGLDestroyPixelFormat(format);
    if (error != kCGLNoError || !context) {
        fprintf(stderr, "CGLCreateContext: %s\n", CGLErrorString(error)); return 2;
    }
    CGLSetCurrentContext(context);
    fprintf(stderr, "Native GL renderer: %s; GL: %s; GLSL: %s\n", glGetString(GL_RENDERER), glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION));
    if (argc == 1) { CGLDestroyContext(context); return 0; }
    if (argc != 3) { fprintf(stderr, "usage: %s vertex.glsl fragment.glsl OR --manifest pairs.tsv\n", argv[0]); return 2; }
    int failures = 0, total = 0;
    if (strcmp(argv[1], "--manifest") == 0) {
        FILE *manifest = fopen(argv[2], "r");
        if (!manifest) { perror(argv[2]); return 2; }
        char *line = NULL; size_t capacity = 0;
        while (getline(&line, &capacity, manifest) != -1) {
            char *vertex = strtok(line, "\t\r\n");
            char *fragment = strtok(NULL, "\t\r\n");
            if (!vertex || !fragment) continue;
            failures += validate_pair(vertex, fragment); ++total;
        }
        free(line); fclose(manifest);
    } else {
        failures = validate_pair(argv[1], argv[2]); total = 1;
    }
    CGLDestroyContext(context);
    printf("Validated %d program pairs; %d failures. Offline compatibility-shim validation only.\n", total, failures);
    return failures ? 1 : 0;
}

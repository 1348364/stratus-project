#version 330 core
in vec4 shim_MultiTexCoord0;
#define DIMENSION_TYPE -1

// BEGIN INCLUDE /core/screen.vert.glsl
out vec2 rasterUV;
void main() {
    rasterUV = shim_MultiTexCoord0.st;
    gl_Position = vec4(rasterUV * 2.0 - 1.0, 0.0, 1.0);
}

// END INCLUDE /core/screen.vert.glsl

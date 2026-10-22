#version 330 core
#define RGBA16F 34842
#define RGBA8 32856
in vec4 shim_MultiTexCoord0;
in vec4 shim_Vertex;
uniform mat4 shim_ModelViewProjectionMatrix;
#define WM_OVERWORLD

// BEGIN INCLUDE /lib/fullscreen.vsh
out vec2 screenUV;
void main() {
    gl_Position = (shim_ModelViewProjectionMatrix * shim_Vertex);
    screenUV = shim_MultiTexCoord0.xy;
}

// END INCLUDE /lib/fullscreen.vsh

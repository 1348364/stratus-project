#version 330 core
#define RGBA16F 34842
#define RGBA8 32856
in vec4 shim_Vertex;
in vec4 shim_Color;
in vec3 shim_Normal;
in vec4 shim_MultiTexCoord0;
in vec4 shim_MultiTexCoord1;
uniform mat4 shim_ModelViewMatrix;
uniform mat3 shim_NormalMatrix;
uniform mat4 shim_TextureMatrix[8];
uniform mat4 shim_ModelViewProjectionMatrix;

#define WM_NETHER
#define WM_TEXTURED
#define WM_FOGGED
#define WM_EMISSIVE

// BEGIN INCLUDE /lib/geometry.vsh

// BEGIN INCLUDE /lib/settings.glsl
#ifndef WM_SETTINGS
#define WM_SETTINGS
// Shared artistic defaults. Presets change only sampling budgets.
#define AMBIENT_BRIGHTNESS 1.05 // [0.85 0.95 1.05 1.15 1.25]
const float ambientOcclusionLevel = 0.35; // [0.00 0.20 0.35 0.50 0.70]
#define COLOUR_TEMPERATURE 0.00 // [-0.10 -0.05 0.00 0.05 0.10]
#define SATURATION 0.98 // [0.85 0.92 0.98 1.05 1.12]
#define CLOUD_COVERAGE 1.00 // [0.70 0.85 1.00]
#define CLOUD_SCALE 600.0 // [350.0 450.0 600.0 800.0 1000.0]
#define CLOUD_IRREGULARITY 0.75 // [0.25 0.50 0.75 1.00]
#define CLOUD_SHADING 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_SPEED 0.35 // [0.00 0.15 0.35 0.60 1.00]
#define CLOUD_QUALITY 2 //  [1 2 3]
#define FOG_DENSITY 0.85 // [0.00 0.45 0.65 0.85 1.10 1.35]
#define FOG_HEIGHT 72.0 // [48.0 64.0 72.0 88.0 104.0 128.0 160.0]
#define FOG_FALLOFF 28.0 // [16.0 22.0 28.0 40.0 56.0]
#define FOG_START 28.0 // [12.0 20.0 28.0 40.0 56.0]
#define FOG_QUALITY 2 //  [1 2 3]
#define WATER_REFLECTION 0.80 // [0.40 0.60 0.80 1.00]
#define REFLECTION_QUALITY 1 //  [0 1 2]
#define REFLECTION_DISTANCE 96.0 // [48.0 72.0 96.0 128.0]
#define WATER_TRANSPARENCY 0.90 // [0.60 0.75 0.90 1.00]
#define WATER_ABSORPTION 0.80 // [0.40 0.60 0.80 1.00 1.25]
#define RIPPLE_STRENGTH 0.55 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SCALE 1.00 // [0.60 0.80 1.00 1.30 1.60]
#define RIPPLE_SPEED 0.50 // [0.00 0.25 0.50 0.75 1.00]
#define BLOCKLIGHT_BRIGHTNESS 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define BLOCKLIGHT_WARMTH 0.35 // [0.00 0.20 0.35 0.50 0.70]
#endif

// END INCLUDE /lib/settings.glsl


// BEGIN INCLUDE /lib/uniforms.glsl
#ifndef WM_UNIFORMS
#define WM_UNIFORMS
uniform mat4 gbufferModelView;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferProjectionInverse;
uniform vec3 cameraPosition;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform int worldTime;
uniform float frameTimeCounter;
uniform float rainStrength;
uniform float blindness;
uniform float darknessFactor;
uniform float far;
uniform float viewWidth;
uniform float viewHeight;
#endif

// END INCLUDE /lib/uniforms.glsl

out vec4 vertexColor;
out vec3 playerPosition;
out vec3 surfaceNormal;
#ifdef WM_TEXTURED
out vec2 textureUV;
#endif
#ifdef WM_LIT
out vec2 lightUV;
#endif
#ifdef WM_MATERIAL
in vec4 mc_Entity;
flat out int materialID;
#endif
void main() {
    gl_Position = (shim_ModelViewProjectionMatrix * shim_Vertex);
    vertexColor = shim_Color;
    playerPosition = (gbufferModelViewInverse * shim_ModelViewMatrix * shim_Vertex).xyz;
    surfaceNormal = mat3(gbufferModelViewInverse) * shim_NormalMatrix * shim_Normal;
#ifdef WM_TEXTURED
    textureUV = (shim_TextureMatrix[0] * shim_MultiTexCoord0).xy;
#endif
#ifdef WM_LIT
    lightUV = (shim_TextureMatrix[1] * shim_MultiTexCoord1).xy;
#endif
#ifdef WM_MATERIAL
    materialID = int(mc_Entity.x + 0.5);
#endif
}

// END INCLUDE /lib/geometry.vsh

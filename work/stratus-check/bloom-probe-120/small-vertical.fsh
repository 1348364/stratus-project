#version 330 core

// BEGIN INCLUDE /core/options.glsl
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Reference defaults; quality profiles only change sampling counts.
#define SKY_AMBIENT 1.40 // [0.80 1.00 1.20 1.40 1.60 1.80 2.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.08 -0.04 0.00 0.04 0.08]
#define SURFACE_SATURATION 1.00 // [0.85 0.93 1.00 1.07 1.15]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.35 0.65 1.00 1.35 1.70 2.00]
#define CLOUD_AMOUNT 1.00 // [0.00 0.35 0.60 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 192.0 // [128.0 160.0 192.0 224.0 256.0 320.0]
#define CLOUD_THICKNESS 56.0 // [20.0 32.0 40.0 56.0 72.0]
#define SKY_LEAK 0.35 // [0.00 0.15 0.25 0.35 0.50 0.70]
#define CLOUD_SPAN 240.0 // [160.0 240.0 360.0 540.0 700.0 900.0]
#define CLOUD_DISTORTION 0.65 // [0.25 0.45 0.65 0.85 1.00]
#define CLOUD_RELIEF 0.55 // [0.25 0.40 0.55 0.70]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70]
#define CLOUD_LAYERS 2 // [1 2 3]
#define MIST_AMOUNT 0.75 // [0.00 0.40 0.60 0.75 1.00 1.25]
#define MIST_Y 70.0 // [48.0 64.0 70.0 88.0 112.0 144.0]
#define MIST_THICKNESS 12.0 // [7.0 9.0 12.0 16.0 22.0]
#define MIST_CLEAR 80.0 // [16.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 2 // [1 2 3]
#define REFLECT_LEVEL 0.85 // [0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 1 // [0 1 2]
#define REFLECT_RANGE 88.0 // [48.0 64.0 88.0 120.0]
#define WATER_VISIBILITY 0.90 // [0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00]
#define WATER_EXTINCTION 0.90 // [0.45 0.65 0.90 1.15 1.40]
#define RIPPLE_HEIGHT 0.55 // [0.00 0.30 0.55 0.80 1.00]
#define RIPPLE_SIZE 1.00 // [0.65 0.80 1.00 1.25 1.50]
#define RIPPLE_RATE 0.45 // [0.00 0.20 0.45 0.70 1.00]
#define FACE_SHADING 1.00 // [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00]
#define WET_SHEEN 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define BLOOM_STRENGTH 0.06 // [0.00 0.03 0.06 0.09 0.12 0.18]
#define BLOOM_RADIUS 0.50 //  [0.50 1.00 1.50 2.00 3.00]
#define SUN_VISIBILITY 0.65 // [0.00 0.25 0.45 0.65 0.85 1.00]
#define LAMP_LEVEL 1.00 // [0.70 0.85 1.00 1.15 1.30]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60]
#endif

// END INCLUDE /core/options.glsl


// BEGIN INCLUDE /core/frame.glsl
#ifndef STRATUS_FRAME_INCLUDED
#define STRATUS_FRAME_INCLUDED
uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferModelView;
uniform vec3 cameraPosition;
uniform vec3 sunPosition;
uniform float frameTimeCounter;
uniform int worldTime;
uniform float rainStrength;
uniform float viewWidth;
uniform float viewHeight;
uniform float far;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform float blindness;
uniform float darknessFactor;

vec3 unitVector(vec3 inputVector) {
    return inputVector * inversesqrt(max(dot(inputVector, inputVector), 1e-12));
}
vec3 decodeDisplay(vec3 displayValue) {
    vec3 lo = displayValue / 12.92;
    vec3 hi = pow(max((displayValue + 0.055) / 1.055, vec3(0.0)), vec3(2.4));
    return mix(hi, lo, lessThanEqual(displayValue, vec3(0.04045)));
}
vec3 encodeDisplay(vec3 linearValue) {
    linearValue = max(linearValue, vec3(0.0));
    vec3 lo = linearValue * 12.92;
    vec3 hi = 1.055 * pow(linearValue, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, lessThanEqual(linearValue, vec3(0.0031308)));
}
float daytimeWeight() {
    float hour = mod(float(worldTime) + 24000.0, 24000.0);
    float dawn = smoothstep(22500.0, 23999.0, hour) + 1.0 - smoothstep(12000.0, 13700.0, hour);
    return clamp(dawn, 0.0, 1.0);
}
vec3 positionFromDepth(vec2 screen, float deviceDepth) {
    vec4 unprojected = gbufferProjectionInverse * vec4(screen * 2.0 - 1.0, deviceDepth * 2.0 - 1.0, 1.0);
    return unprojected.xyz / max(unprojected.w, 1e-7);
}
vec3 playerFromView(vec3 viewPoint) {
    return (gbufferModelViewInverse * vec4(viewPoint, 1.0)).xyz;
}
vec3 broadLightDirection() {
    vec3 direction = mat3(gbufferModelViewInverse) * sunPosition;
    if (dot(direction, direction) < 0.001) direction = vec3(-0.35, 0.85, 0.40);
    return unitVector(direction);
}
vec2 viewportSize() { return max(vec2(viewWidth, viewHeight), vec2(1.0)); }
#endif

// END INCLUDE /core/frame.glsl

uniform sampler2D colortex5;
in vec2 rasterUV;
/* RENDERTARGETS: 6 */
layout(location = 0) out vec4 glow;
void main() {
    vec2 pixel = vec2(0.0, 3.0 * BLOOM_RADIUS / 1080.0);
    vec3 sum = texture(colortex5, rasterUV).rgb * 0.227027;
    for (int i = 1; i <= 4; i++) {
        float weight = i == 1 ? 0.1945946 : i == 2 ? 0.1216216 : i == 3 ? 0.054054 : 0.016216;
        vec2 delta = pixel * float(i);
        sum += (texture(colortex5, clamp(rasterUV + delta, vec2(0.0), vec2(1.0))).rgb
              + texture(colortex5, clamp(rasterUV - delta, vec2(0.0), vec2(1.0))).rgb) * weight;
    }
    glow = vec4(sum, 1.0);
}

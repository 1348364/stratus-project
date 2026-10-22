#version 330 core
#define RGBA16F 34842
#define RGBA8 32856
#define WM_OVERWORLD

// BEGIN INCLUDE /lib/final.fsh

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
#define CLOUD_QUALITY 1 //  [1 2 3]
#define FOG_DENSITY 0.85 // [0.00 0.45 0.65 0.85 1.10 1.35]
#define FOG_HEIGHT 72.0 // [48.0 64.0 72.0 88.0 104.0 128.0 160.0]
#define FOG_FALLOFF 28.0 // [16.0 22.0 28.0 40.0 56.0]
#define FOG_START 28.0 // [12.0 20.0 28.0 40.0 56.0]
#define FOG_QUALITY 1 //  [1 2 3]
#define WATER_REFLECTION 0.80 // [0.40 0.60 0.80 1.00]
#define REFLECTION_QUALITY 0 //  [0 1 2]
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


// BEGIN INCLUDE /lib/math.glsl
#ifndef WM_MATH
#define WM_MATH

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

const float WM_PI = 3.14159265359;
vec3 wmLinear(vec3 c) { return pow(max(c, vec3(0.0)), vec3(2.2)); }
vec3 wmDisplay(vec3 c) { return pow(max(c, vec3(0.0)), vec3(1.0 / 2.2)); }
float wmLuma(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
vec3 wmSafeNormal(vec3 v) { return v / max(length(v), 0.00001); }
float wmHash(vec2 p) {
    // Polynomial hash avoids large-angle sine precision errors on mobile GPUs.
    vec3 q = fract(vec3(p.xyx) * vec3(0.1031, 0.1030, 0.0973));
    q += dot(q, q.yzx + 33.33);
    return fract((q.x + q.y) * q.z);
}
float wmNoise(vec2 p) {
    vec2 cell = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(wmHash(cell), wmHash(cell + vec2(1.0, 0.0)), u.x),
        mix(wmHash(cell + vec2(0.0, 1.0)), wmHash(cell + vec2(1.0)), u.x), u.y);
}
float wmDaylight() {
    float elevation = cos((float(worldTime) - 6000.0) * (2.0 * WM_PI / 24000.0));
    return smoothstep(-0.16, 0.24, elevation);
}
vec3 wmViewPosition(vec2 uv, float depth) {
    vec4 p = gbufferProjectionInverse * vec4(uv * 2.0 - 1.0, depth * 2.0 - 1.0, 1.0);
    return p.xyz / max(p.w, 0.000001);
}
vec3 wmWorldDirection(vec3 viewDirection) {
    return wmSafeNormal(mat3(gbufferModelViewInverse) * viewDirection);
}
#endif

// END INCLUDE /lib/math.glsl

uniform sampler2D colortex0;
in vec2 screenUV;
layout(location = 0) out vec4 finalColor;
void main() {
    // Fixed exposure: no history, sky metering, bloom, vignette or lens effects.
    vec3 color = max(texture(colortex0, screenUV).rgb, vec3(0.0));
    color *= vec3(1.0 + COLOUR_TEMPERATURE, 1.0, 1.0 - COLOUR_TEMPERATURE);
    color = max(mix(vec3(wmLuma(color)), color, SATURATION), vec3(0.0));
    // A shoulder above normal surface values retains lantern pixel detail.
    color = color / (vec3(1.0) + 0.075 * color);
    color = clamp(wmDisplay(color), 0.0, 1.0);
    finalColor = vec4(color, 1.0);
}

// END INCLUDE /lib/final.fsh

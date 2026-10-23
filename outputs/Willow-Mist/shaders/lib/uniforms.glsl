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

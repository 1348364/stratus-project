#version 330 core

// BEGIN INCLUDE /core/optics-cache.geom.glsl

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
uniform vec3 biomeWaterTint;
uniform float biomeSilt;
uniform float biomeHumidity;
uniform float biomeWarmth;
uniform ivec2 eyeBrightnessSmooth;
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
vec3 sunlightColour() {
    float height = max(broadLightDirection().y, 0.0);
    return mix(vec3(1.0, 0.53, 0.25), vec3(1.0, 0.84, 0.61), smoothstep(0.02, 0.65, height));
}
vec2 viewportSize() { return max(vec2(viewWidth, viewHeight), vec2(1.0)); }
#endif

// END INCLUDE /core/frame.glsl


// BEGIN INCLUDE /core/optics-cube.glsl
#ifndef STRATUS_OPTICS_CUBE
#define STRATUS_OPTICS_CUBE
const float cubeScale=1.02;
// Six surrounding views plus two raised views recover more refracted
// surfaces hidden behind foreground block edges, within one 4 by 2 atlas.
vec3 cubeOrigin(int face){return face>=6?vec3(0,2.5,0):vec3(0);}
float cubeExtent(int face){return face>=6?2.5:cubeScale;}
vec3 cubeForward(int face){
 if(face==6)return mat3(gbufferModelViewInverse)*vec3(0,0,-1);
 if(face==7)return vec3(0,-1,0);
 if(face==0)return vec3(1,0,0);if(face==1)return vec3(-1,0,0);
 if(face==2)return vec3(0,1,0);if(face==3)return vec3(0,-1,0);
 return face==4?vec3(0,0,1):vec3(0,0,-1);
}
vec3 cubeRight(int face){return face==6?mat3(gbufferModelViewInverse)*vec3(1,0,0):(face<2?vec3(0,0,1):vec3(1,0,0));}
vec3 cubeUp(int face){return cross(cubeRight(face),cubeForward(face));}
vec3 cubeCoordinates(vec3 p,int face){return vec3(dot(p,cubeRight(face)),dot(p,cubeUp(face)),dot(p,cubeForward(face)));}
vec2 cubeTile(int face){return vec2(face%4,face/4);}
vec2 cubeAtlas(vec2 uv,int face){return (cubeTile(face)+uv)/vec2(4,2);}
vec3 cubeRay(vec2 uv,int face){return cubeForward(face)+cubeRight(face)*((uv.x*2.-1.)*cubeExtent(face))+cubeUp(face)*((uv.y*2.-1.)*cubeExtent(face));}
#endif

// END INCLUDE /core/optics-cube.glsl

layout(triangles)in;
layout(triangle_strip,max_vertices=24)out;
in vec4 vertexTint[];in vec2 vertexUV[];in vec2 vertexLight[];
in vec3 vertexPoint[];in vec3 vertexNormal[];flat in int vertexMaterial[];
out vec4 cacheTint;out vec2 cacheUV;out vec2 cacheLight;
out vec3 cachePoint;out vec3 cacheNormal;flat out int cacheMaterial;flat out int cacheFace;
void main(){
 for(int face=0;face<8;face++){
  // Reject triangles outside each individual view before geometry expansion.
  // Atlas-wide raster clipping alone otherwise draws irrelevant faces repeatedly.
  vec3 a=cubeCoordinates(vertexPoint[0]-cubeOrigin(face),face);
  vec3 b=cubeCoordinates(vertexPoint[1]-cubeOrigin(face),face);
  vec3 c=cubeCoordinates(vertexPoint[2]-cubeOrigin(face),face);
  float e=cubeExtent(face);
  if(max(max(a.z,b.z),c.z)<=0.025)continue;
  if(min(min(a.x-a.z*e,b.x-b.z*e),c.x-c.z*e)>0.0)continue;
  if(max(max(a.x+a.z*e,b.x+b.z*e),c.x+c.z*e)<0.0)continue;
  if(min(min(a.y-a.z*e,b.y-b.z*e),c.y-c.z*e)>0.0)continue;
  if(max(max(a.y+a.z*e,b.y+b.z*e),c.y+c.z*e)<0.0)continue;
  for(int i=0;i<3;i++){
   vec3 p=cubeCoordinates(vertexPoint[i]-cubeOrigin(face),face);float w=p.z;p.xy/=cubeExtent(face);
   vec2 tile=cubeTile(face);
   vec2 atlasClip=vec2((p.x+(tile.x*2.+1.)*w)/4.-w,(p.y+(tile.y*2.+1.)*w)/2.-w);
   gl_Position=vec4(atlasClip,1.000500125*w-0.100025006,w);
   cacheTint=vertexTint[i];cacheUV=vertexUV[i];cacheLight=vertexLight[i];
   cachePoint=vertexPoint[i];cacheNormal=vertexNormal[i];cacheMaterial=vertexMaterial[i];cacheFace=face;
   EmitVertex();
  }
  EndPrimitive();
 }
}

// END INCLUDE /core/optics-cache.geom.glsl

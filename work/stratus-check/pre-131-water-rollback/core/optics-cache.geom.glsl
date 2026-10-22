#include "/core/frame.glsl"
#include "/core/optics-cube.glsl"
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

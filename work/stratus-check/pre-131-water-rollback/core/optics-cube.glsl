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

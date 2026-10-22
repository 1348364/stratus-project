#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform mat4 shadowModelViewInverse;
out vec4 vertexTint;
out vec2 vertexUV;
out vec2 vertexLight;
out vec3 vertexPoint;
out vec3 vertexNormal;
in vec4 mc_Entity;
flat out int vertexMaterial;
void main(){
    vec4 p=shadowModelViewInverse*(gl_ModelViewMatrix*gl_Vertex);
    vertexPoint=mat3(gbufferModelViewInverse)*(gbufferModelView*p).xyz;
    vertexNormal=unitVector(mat3(shadowModelViewInverse)*(gl_NormalMatrix*gl_Normal));
    vertexTint=gl_Color;
    vertexUV=(gl_TextureMatrix[0]*gl_MultiTexCoord0).st;
    vertexLight=(gl_TextureMatrix[1]*gl_MultiTexCoord1).st;
    vertexMaterial=int(round(mc_Entity.x));
    gl_Position=p;
}

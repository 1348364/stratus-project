#include "/lib/settings.glsl"
#include "/lib/uniforms.glsl"
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
    gl_Position = ftransform();
    vertexColor = gl_Color;
    playerPosition = (gbufferModelViewInverse * gl_ModelViewMatrix * gl_Vertex).xyz;
    surfaceNormal = mat3(gbufferModelViewInverse) * gl_NormalMatrix * gl_Normal;
#ifdef WM_TEXTURED
    textureUV = (gl_TextureMatrix[0] * gl_MultiTexCoord0).xy;
#endif
#ifdef WM_LIT
    lightUV = (gl_TextureMatrix[1] * gl_MultiTexCoord1).xy;
#endif
#ifdef WM_MATERIAL
    materialID = int(mc_Entity.x + 0.5);
#endif
}

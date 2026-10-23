#include "/core/options.glsl"
#include "/core/frame.glsl"
out vec4 tintAndOpacity;
out vec2 atlasCoordinate;
out vec2 illuminationCoordinate;
out vec3 relativeLocation;
out vec3 orientedNormal;
#if PASS_KIND == 3 || PASS_KIND == 6
in vec4 mc_Entity;
flat out int blockCategory;
#endif
void main() {
    vec4 cameraVertex = gl_ModelViewMatrix * gl_Vertex;
    relativeLocation = playerFromView(cameraVertex.xyz);
    orientedNormal = mat3(gbufferModelViewInverse) * (gl_NormalMatrix * gl_Normal);
    tintAndOpacity = gl_Color;
    atlasCoordinate = (gl_TextureMatrix[0] * gl_MultiTexCoord0).st;
    illuminationCoordinate = (gl_TextureMatrix[1] * gl_MultiTexCoord1).st;
#if PASS_KIND == 3 || PASS_KIND == 6
    blockCategory = int(round(mc_Entity.x));
#endif
    // This entry point also permits Iris's compatibility line fallback.
    gl_Position = ftransform();
}

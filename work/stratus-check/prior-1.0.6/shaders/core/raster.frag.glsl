#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/diffuse.glsl"
in vec4 tintAndOpacity;
in vec2 atlasCoordinate;
in vec2 illuminationCoordinate;
in vec3 relativeLocation;
in vec3 orientedNormal;
uniform sampler2D gtexture;
uniform sampler2D lightmap;
uniform int entityId;
#if PASS_KIND == 3 || PASS_KIND == 6
flat in int blockCategory;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
uniform vec4 entityColor;
#endif

#if LATE_SURFACE == 1
/* RENDERTARGETS: 3,0,1 */
#elif PASS_KIND == 9
/* RENDERTARGETS: 0 */
#else
/* RENDERTARGETS: 0,1,2 */
#endif
void main() {
#if PASS_KIND == 8
    discard;
#else
#if PASS_KIND == 1 || PASS_KIND == 2 || PASS_KIND == 4
    // Iris's dedicated vanilla entity-shadow draw must not enter the gbuffer.
    if (entityId == 4200) discard;
#endif
    vec4 surface = tintAndOpacity;
#if PASS_KIND != 0
    surface *= texture(gtexture, atlasCoordinate);
#endif
#if PASS_KIND == 3
    // Some emissive terrain layers disable the engine alpha test. Their empty
    // texels must not overwrite the opaque material/normal attachments.
    if (surface.a < 0.10) discard;
#endif
#if LATE_SURFACE == 0 && PASS_KIND != 0 && PASS_KIND != 9
    // A zero-alpha fragment must not replace the opaque material metadata.
    if (surface.a <= 0.001) discard;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
    surface.rgb = mix(surface.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 lm = vec3(1.0);
    float sky = 1.0;
    float category = 0.0;
#if PASS_KIND >= 2 && PASS_KIND <= 7
    lm = texture(lightmap, illuminationCoordinate).rgb;
    sky = clamp((illuminationCoordinate.t * 32.0 - 1.0) / 30.0, 0.0, 1.0);
    category = 1.0;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6
    if (blockCategory == 4101 || blockCategory == 4102) category = 2.0;
#if PASS_KIND == 3
    // Soil, wood, mineral and foliage absorbency; no new render attachment.
    if (blockCategory >= 4110 && blockCategory <= 4113)
        category = 1.0 + float(blockCategory - 4109) * 0.1;
#endif
#endif
#if PASS_KIND == 5
    category = 3.0;
#endif
#if LATE_SURFACE == 1
    vec3 lateColour = diffuseRadiance(surface.rgb, lm, sky, orientedNormal, category, relativeLocation);
    lateColour = throughAir(lateColour, relativeLocation, sky);
    float mark = 0.0;
#if PASS_KIND == 6
    if (blockCategory == 4100 && orientedNormal.y > 0.5 && isEyeInWater == 0) {
        mark = 1.0;
        // Composite will replace this baseline when water is frontmost.
        surface.a = 0.40;
    }
#endif
    gl_FragData[0] = vec4(lateColour, surface.a);
    // With alpha zero for glass, these data targets preserve earlier water.
    gl_FragData[1] = vec4(lateColour, mark);
    vec3 n = unitVector(orientedNormal);
    float waterViewDepth = -(gbufferModelView * vec4(relativeLocation, 1.0)).z;
    gl_FragData[2] = vec4(n.x, n.z, waterViewDepth, mark);
#elif PASS_KIND == 9
    gl_FragData[0] = surface;
#else
    gl_FragData[0] = surface;
    gl_FragData[1] = vec4(unitVector(orientedNormal), category);
    gl_FragData[2] = vec4(lm, sky);
#endif
    // Iris still applies each draw type's ordinary alpha test.
#endif
}

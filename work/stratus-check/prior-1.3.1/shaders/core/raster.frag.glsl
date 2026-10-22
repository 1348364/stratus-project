#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/diffuse.glsl"
#include "/core/medium.glsl"
#ifndef BLOCK_SURFACE
#define BLOCK_SURFACE 0
#endif
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
/* RENDERTARGETS: 3,0,1,2 */
void main() {
#if PASS_KIND == 8
    discard;
#else
    if (entityId == 4200) discard;
    vec4 surface = tintAndOpacity;
#if PASS_KIND != 0
    surface *= texture(gtexture, atlasCoordinate);
#endif
    if (surface.a <= 0.001) discard;
#if PASS_KIND == 3
    if (surface.a < 0.10) discard;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
    surface.rgb = mix(surface.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 lm = vec3(1.0);
    float sky = 1.0;
    float category = 0.0;
    int material = 4112;
#if (PASS_KIND >= 2 && PASS_KIND <= 7)
    lm = texture(lightmap, illuminationCoordinate).rgb;
    sky = clamp((illuminationCoordinate.t * 32.0 - 1.0) / 30.0, 0.0, 1.0);
    category = 1.0;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6 || BLOCK_SURFACE == 1
    // Includes unlisted, modded and translucent blocks. Water has its own medium.
    category = 1.3;
#endif
#if PASS_KIND == 3 || PASS_KIND == 6
    material = blockCategory;
    if (blockCategory == 4101 || blockCategory == 4102) category = 2.0;
#endif
#if PASS_KIND == 2 || PASS_KIND == 7
    // Billboard normals do not describe a solid material surface.
    category = 0.8;
#endif
#if PASS_KIND == 5
    category = 3.0;
#endif
    vec3 colour = diffuseRadiance(surface.rgb, lm, sky, orientedNormal, category, relativeLocation, material);
    float emission=category>1.5&&category<2.5?smoothstep(0.48,0.94,max(surface.r,max(surface.g,surface.b))):0.0;
#if PASS_KIND == 10 || PASS_KIND == 12 || PASS_KIND == 1
    emission=1.0;
#endif
    colour = throughAir(colour, relativeLocation, sky);
    float mark = 0.0;
    float depth = 0.0;
    float radialDepth = 0.0;
    float reflectable = 0.0;
#if PASS_KIND == 3 || BLOCK_SURFACE == 1
    reflectable = float(category < 1.5);
#endif
#if PASS_KIND == 6
    if (blockCategory == 4100) {
        mark = 1.0;
        vec3 waterView = (gbufferModelView * vec4(relativeLocation, 1.0)).xyz;
        depth = -waterView.z;
        radialDepth = length(waterView);
        // Identical baseline on top, side and underside; no texture seam.
        colour = waterBodyColour(sky);
        // Water itself is composed once, after all water faces are captured.
        // Zero colour alpha avoids accumulating overlapping blue baselines.
        surface.a = 0.0;
    }
#endif
#if PASS_KIND == 9
    // Breaking cracks multiply the already-lit HDR scene.
    colour = surface.rgb;
#elif PASS_KIND == 12
    colour = decodeDisplay(surface.rgb);
#endif
    gl_FragData[0] = vec4(colour, surface.a);
#if LATE_SURFACE == 1
    #if PASS_KIND == 6
    gl_FragData[1] = vec4(0.0, emission, 0.0, mark);
#else
    gl_FragData[1] = vec4(0.0, emission, 0.0, surface.a);
#endif
    gl_FragData[2] = vec4(unitVector(orientedNormal), mark);
    gl_FragData[3] = vec4(depth, sky, radialDepth, mark);
#else
    gl_FragData[1] = vec4(sky, emission, 0.0, reflectable);
    gl_FragData[2] = vec4(0.0);
    gl_FragData[3] = vec4(0.0);
#endif
#endif
}

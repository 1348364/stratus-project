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
#if PASS_KIND == 6
/* RENDERTARGETS: 3,0,1,2,8,13,14 */
#elif LATE_SURFACE == 1
/* RENDERTARGETS: 3,0,1,2,8,14 */
#else
/* RENDERTARGETS: 3,0,1,2,8 */
#endif
void main() {
#if PASS_KIND == 8 || (PASS_KIND == 12 && SUN_STYLE == 0) || (PASS_KIND == 13 && CLOUD_STYLE != 1)
    discard;
#else
    if (entityId == 4200) discard;
    vec4 surface = tintAndOpacity;
#if PASS_KIND != 0
    surface *= texture(gtexture, atlasCoordinate);
#endif
#if PASS_KIND == 12
    // Vanilla sun/moon textures use black additive backgrounds, not cutout alpha.
    if(max(surface.r,max(surface.g,surface.b))<0.012)discard;
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
#if PASS_KIND == 6
    if (isEyeInWater == 1 && (blockCategory == 4100 || blockCategory == 4103)) {
        // Invisible exit-depth capture only. The scene and interface-optics
        // buffers stay untouched, so no surface window/reflection is drawn.
        // This independent attachment survives glass and particles and lets
        // the resolve stop water fog before objects in the air beyond it.
        vec3 exitView = (gbufferModelView * vec4(relativeLocation, 1.0)).xyz;
        gl_FragData[0] = vec4(0.0);
        gl_FragData[1] = vec4(0.0);
        gl_FragData[2] = vec4(0.0);
        gl_FragData[3] = vec4(0.0);
        gl_FragData[4] = vec4(0.0);
        gl_FragData[5] = vec4(-exitView.z, sky,
            clamp((illuminationCoordinate.s * 32.0 - 1.0) / 30.0, 0.0, 1.0), 1.0);
        gl_FragData[6] = vec4(0.0);
        return;
    }
#endif
#if PASS_KIND == 2 || PASS_KIND == 7
    // Billboard normals do not describe a solid material surface.
    category = 0.8;
#endif
#if PASS_KIND == 5
    category = 3.0;
#endif
    vec3 colour = diffuseRadiance(surface.rgb, lm, sky, orientedNormal, category, relativeLocation, material);
#if PASS_KIND == 6
    if(blockCategory!=4100&&blockCategory!=4103)
        colour=wetSurfaceResponse(colour,unitVector(orientedNormal),relativeLocation,sky,wetMaterialProperties(material));
#elif BLOCK_SURFACE == 1 && LATE_SURFACE == 1
    // Translucent block entities use the same film without treating their
    // unknown material as absorbent stone. Ordinary entities remain excluded.
    colour=wetSurfaceResponse(colour,unitVector(orientedNormal),relativeLocation,sky,vec2(0.0,0.40));
#endif
    float emission=category>1.5&&category<2.5?smoothstep(0.48,0.94,max(surface.r,max(surface.g,surface.b))):0.0;
#if PASS_KIND == 10 || PASS_KIND == 12 || PASS_KIND == 1
    emission=1.0;
#endif
    colour = throughAir(colour, relativeLocation, sky);
    float mark = 0.0;
    float depth = 0.0;
    float radialDepth = 0.0;
    float reflectable = 0.0;
#if PASS_KIND == 3 || PASS_KIND == 4 || PASS_KIND == 10 || BLOCK_SURFACE == 1
    reflectable = 1.0;
#endif
#if PASS_KIND == 6
    if (blockCategory == 4100 || blockCategory == 4103) {
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
    gl_FragData[4] = vec4(0.0);
#if PASS_KIND == 6
    if(mark>0.5)gl_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));
    // Preserve a horizontal water entry behind a falling curtain. Vertical
    // fragments have zero coverage in this attachment and cannot erase it.
    float horizontalEntry=mark*float(orientedNormal.y>0.5&&isEyeInWater==0);
    gl_FragData[5]=vec4(depth,sky,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0),horizontalEntry);
    gl_FragData[6]=vec4(0.0,0.0,0.0,surface.a);
#elif LATE_SURFACE == 1
    gl_FragData[5]=vec4(0.0,0.0,0.0,surface.a);
#endif
#if LATE_SURFACE == 1
    #if PASS_KIND == 6
    gl_FragData[1] = vec4(0.0, emission, float(blockCategory==4103), mark);
#else
    gl_FragData[1] = vec4(0.0, emission, 0.0, surface.a);
#endif
    gl_FragData[2] = vec4(unitVector(orientedNormal), mark);
    gl_FragData[3] = vec4(depth, sky, radialDepth, mark);
#else
    gl_FragData[1] = vec4(sky, emission, 0.0, reflectable);
    gl_FragData[2] = vec4(unitVector(orientedNormal),float(category>1.05&&category<1.5));
    gl_FragData[3] = vec4(wetMaterialProperties(material),0.0,0.0);
#endif
#endif
}

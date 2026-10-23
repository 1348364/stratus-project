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
#if PASS_KIND == 6 && WATER_STYLE == 1
uniform sampler2D colortex4;
#endif
uniform int entityId;
#if PASS_KIND == 3 || PASS_KIND == 6
flat in int blockCategory;
#endif
#if PASS_KIND == 4 || PASS_KIND == 5
uniform vec4 entityColor;
#endif
#if PASS_KIND == 6
/* RENDERTARGETS: 3,0,1,2,8,13,14,15 */
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
    vec4 atlasTexel=texture(gtexture, atlasCoordinate);
    surface *= atlasTexel;
#endif
#if PASS_KIND == 12
    // Vanilla sun/moon textures use black additive backgrounds, not cutout alpha.
    if(max(surface.r,max(surface.g,surface.b))<0.012)discard;
#endif
#if PASS_KIND == 6
    bool opticalSolid=blockCategory>=4120&&blockCategory<=4123;
    // Clear glass interiors still have a reflective interface.
    if(surface.a<=0.001&&!opticalSolid)discard;
#else
    if(surface.a<=0.001)discard;
#endif
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
        // Independent exit depth stops fog before air beyond the interface.
        // Stratus mode stays clear; native mode also supplies its atlas layer.
        vec3 exitView = (gbufferModelView * vec4(relativeLocation, 1.0)).xyz;
        // Native mode restores the animated underside at the actual exit.
        // Ordinary alpha blending keeps nearer glass/particles in draw order;
        // the dedicated transmission buffer carries its coverage into fog.
        vec4 underside=vec4(0.0);
#if WATER_STYLE == 1
        vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
        vec3 fn=unitVector(orientedNormal);
        nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
        float nativeAlpha=clamp(surface.a*WATER_TEXTURE,0.0,1.0);
        vec3 behind=texture(colortex4,gl_FragCoord.xy/viewportSize()).rgb;
        // Invert the HDR fixed-function alpha blend so the native layer blends
        // in display space, as vanilla does. Opaque background is snapshotted
        // before translucency; nearer layers retain the existing draw order.
        vec3 nativeResult=decodeDisplay(mix(encodeDisplay(behind),nativeColour,nativeAlpha));
        vec3 blendColour=nativeAlpha>0.00001
            ?(nativeResult-behind*(1.0-nativeAlpha))/nativeAlpha:vec3(0.0);
        underside=vec4(blendColour,nativeAlpha);
#endif
        gl_FragData[0] = underside;
        gl_FragData[1] = vec4(0.0);
        gl_FragData[2] = vec4(0.0);
        gl_FragData[3] = vec4(0.0);
        gl_FragData[4] = vec4(0.0);
        gl_FragData[5] = vec4(-exitView.z, sky,
            clamp((illuminationCoordinate.s * 32.0 - 1.0) / 30.0, 0.0, 1.0), 1.0);
        gl_FragData[6] = vec4(0.0,0.0,0.0,underside.a);
        gl_FragData[7] = vec4(0.0);
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
    // Translucent block entities receive film; ordinary entities stay excluded.
    colour=wetSurfaceResponse(colour,unitVector(orientedNormal),relativeLocation,sky,vec2(0.0,0.40));
#endif
    float emission=category>1.5&&category<2.5?smoothstep(0.48,0.94,max(surface.r,max(surface.g,surface.b))):0.0;
#if PASS_KIND == 10 || PASS_KIND == 12 || PASS_KIND == 1
    emission=1.0;
#endif
    colour = throughAir(colour, relativeLocation, sky);
    vec4 nativeWater=vec4(0.0);
#if PASS_KIND == 6 && WATER_STYLE == 1
    vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
    vec3 fn=unitVector(orientedNormal);nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
    nativeWater=vec4(decodeDisplay(nativeColour),surface.a);
#endif
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
    if(mark>0.5){
#if WATER_STYLE == 1
        gl_FragData[4]=vec4(nativeWater.rgb,1.0);
#else
        gl_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));
#endif
    }
    vec3 opticalNormal=unitVector(mat3(gbufferModelView)*orientedNormal);
    opticalNormal/=max(abs(opticalNormal.x)+abs(opticalNormal.y)+abs(opticalNormal.z),0.00001);
    vec2 encoded=opticalNormal.xy;
    if(opticalNormal.z<0.0)encoded=(1.0-abs(encoded.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(encoded,vec2(0)));
    vec3 opticalView=(gbufferModelView*vec4(relativeLocation,1.0)).xyz;
    gl_FragData[7]=opticalSolid?vec4(encoded,-opticalView.z,1.0):vec4(0.0);
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
    #if WATER_STYLE == 1
    gl_FragData[1] = vec4(dot(atlasTexel.rgb,vec3(0.2126,0.7152,0.0722)), mark>0.5?nativeWater.a:emission, float(blockCategory==4103), mark);
#else
    gl_FragData[1] = vec4(dot(atlasTexel.rgb,vec3(0.2126,0.7152,0.0722)), emission, float(blockCategory==4103), mark);
#endif
#else
    gl_FragData[1] = vec4(0.0, emission, 0.0, surface.a);
#endif
    gl_FragData[2] = vec4(unitVector(orientedNormal), mark);
    gl_FragData[3] = vec4(depth, sky, radialDepth, mark);
#else
    gl_FragData[1] = vec4(sky, emission, 0.0, reflectable);
    gl_FragData[2] = vec4(unitVector(orientedNormal),float(category>1.05&&category<1.5&&material!=4113));
    gl_FragData[3] = vec4(wetMaterialProperties(material),0.0,0.0);
#endif
#endif
}

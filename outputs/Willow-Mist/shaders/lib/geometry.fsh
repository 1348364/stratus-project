#include "/lib/settings.glsl"
#include "/lib/uniforms.glsl"
#include "/lib/math.glsl"
#include "/lib/sky.glsl"
#include "/lib/fog.glsl"
in vec4 vertexColor;
in vec3 playerPosition;
in vec3 surfaceNormal;
#ifdef WM_TEXTURED
uniform sampler2D gtexture;
in vec2 textureUV;
#endif
#ifdef WM_LIT
in vec2 lightUV;
#include "/lib/lighting.glsl"
#endif
#ifdef WM_ENTITY
uniform vec4 entityColor;
#endif
#ifdef WM_MATERIAL
flat in int materialID;
#endif
#ifdef WM_WATER
#include "/lib/water.glsl"
#endif

#ifdef WM_MASK
/* RENDERTARGETS: 0,1 */
#else
/* RENDERTARGETS: 0 */
#endif
void main() {
#ifdef WM_HIDE_SKY
    // Sky is generated once in deferred, then reused as the reflection fallback.
    discard;
#else
    vec4 color = vertexColor;
#ifdef WM_TEXTURED
    color *= texture(gtexture, textureUV);
#endif
#ifdef WM_ENTITY
    color.rgb = mix(color.rgb, entityColor.rgb, entityColor.a);
#endif
    vec3 albedo = wmLinear(color.rgb);
    vec3 shaded = albedo;
    float skyLight = 1.0;
    float reflectable = 1.0;
#ifdef WM_LIT
    skyLight = wmLightLevels(lightUV).y;
    shaded *= wmLight(lightUV, surfaceNormal);
#endif
#ifdef WM_MATERIAL
    if (materialID == 1002 || materialID == 1003) {
        float bright = smoothstep(0.30, 0.85, max(color.r, max(color.g, color.b)));
        shaded = max(shaded, albedo * bright * BLOCKLIGHT_BRIGHTNESS);
        reflectable = 0.0;
    }
#endif
#ifdef WM_HAND
    reflectable = 0.0;
#endif
#ifdef WM_EMISSIVE
    reflectable = 0.0;
#endif
    bool waterSurface = false;
#ifdef WM_WATER
    if (materialID == 1001 && wmSafeNormal(surfaceNormal).y > 0.5 && isEyeInWater == 0) {
        vec2 uv = gl_FragCoord.xy / vec2(max(viewWidth, 1.0), max(viewHeight, 1.0));
        shaded = wmWater(albedo, playerPosition, surfaceNormal, skyLight, uv);
        // Depth absorption and opaque-scene transmission are already composed.
        color.a = 1.0;
        waterSurface = true;
    }
#endif
#ifdef WM_FOGGED
    if (!waterSurface) shaded = wmApplyFog(shaded, playerPosition, skyLight);
#endif
    // Legacy output preserves Iris's per-draw alpha tests, including entities.
    gl_FragData[0] = vec4(shaded, color.a);
#ifdef WM_MASK
    gl_FragData[1] = vec4(reflectable, skyLight, 0.0, 1.0);
#endif
#endif
}

#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform sampler2D colortex3;
uniform sampler2D colortex6;
in vec2 rasterUV;
layout(location = 0) out vec4 displayPixel;
void main() {
    vec3 physicalColour = max(texture(colortex3, rasterUV).rgb, vec3(0.0));
#if REALISTIC_LIGHTING == 0
    // Original game lightmap/vertex colours: no exposure, colour grading,
    // bloom or highlight shoulder changes their brightness or ambient level.
    displayPixel=vec4(clamp(encodeDisplay(physicalColour),0.0,1.0),1.0);
    return;
#endif
    physicalColour += max(texture(colortex6, rasterUV).rgb, vec3(0.0)) * BLOOM_STRENGTH;
    // Camera exposure changes the complete scene, independently of the local
    // skylight/lamplight controls; UI brightness remains Minecraft's own.
    physicalColour *= exp2(EXPOSURE);
    physicalColour *= vec3(exp2(WHITE_BALANCE * 0.6), 1.0, exp2(-WHITE_BALANCE * 0.6));
    float neutral = dot(physicalColour, vec3(0.2126, 0.7152, 0.0722));
    physicalColour = max(vec3(neutral) + (physicalColour - neutral) * SURFACE_SATURATION, vec3(0.0));
    // Fixed exposure and an analytic highlight shoulder preserve nearby colour.
    vec3 base = min(physicalColour, vec3(0.60));
    vec3 shoulder = 0.40 * (1.0 - exp(-max(physicalColour - 0.60, 0.0) / 0.40));
    // Sub-code-value display dither suppresses banding in slow sky gradients.
    float dither=fract(52.9829189*fract(dot(gl_FragCoord.xy,vec2(0.06711056,0.00583715))))-0.5;
    displayPixel = vec4(clamp(encodeDisplay(base + shoulder)+dither/255.0, 0.0, 1.0), 1.0);
}

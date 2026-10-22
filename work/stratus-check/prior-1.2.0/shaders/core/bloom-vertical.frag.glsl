#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform sampler2D colortex5;
in vec2 rasterUV;
/* RENDERTARGETS: 6 */
layout(location = 0) out vec4 glow;
void main() {
    vec2 pixel = vec2(0.0, 3.0 * BLOOM_RADIUS / 1080.0);
    vec3 sum = texture(colortex5, rasterUV).rgb * 0.227027;
    for (int i = 1; i <= 4; i++) {
        float weight = i == 1 ? 0.1945946 : i == 2 ? 0.1216216 : i == 3 ? 0.054054 : 0.016216;
        vec2 delta = pixel * float(i);
        sum += (texture(colortex5, clamp(rasterUV + delta, vec2(0.0), vec2(1.0))).rgb
              + texture(colortex5, clamp(rasterUV - delta, vec2(0.0), vec2(1.0))).rgb) * weight;
    }
    glow = vec4(sum, 1.0);
}

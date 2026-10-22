#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform sampler2D colortex3;
in vec2 rasterUV;
/* RENDERTARGETS: 5 */
layout(location = 0) out vec4 glow;
vec3 brightPixels(vec2 coordinate) {
    vec3 colour = max(texture(colortex3, clamp(coordinate, vec2(0.0), vec2(1.0))).rgb, vec3(0.0));
    float brightness = dot(colour, vec3(0.2126, 0.7152, 0.0722));
    float knee = clamp(brightness - 0.40, 0.0, 0.50);
    float excess = max(brightness - 0.65, knee * knee);
    return colour * excess / max(brightness, 0.001);
}
void main() {
    // Radius is measured relative to image height, keeping the halo stable at 4K.
    vec2 pixel = vec2(3.0 * BLOOM_RADIUS * viewHeight / (1080.0 * max(viewWidth, 1.0)), 0.0);
    vec3 sum = brightPixels(rasterUV) * 0.227027;
    for (int i = 1; i <= 4; i++) {
        float weight = i == 1 ? 0.1945946 : i == 2 ? 0.1216216 : i == 3 ? 0.054054 : 0.016216;
        sum += (brightPixels(rasterUV + pixel * float(i)) + brightPixels(rasterUV - pixel * float(i))) * weight;
    }
    glow = vec4(sum, 1.0);
}

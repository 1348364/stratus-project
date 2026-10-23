#include "/lib/settings.glsl"
#include "/lib/math.glsl"
uniform sampler2D colortex0;
in vec2 screenUV;
layout(location = 0) out vec4 finalColor;
void main() {
    // Fixed exposure: no history, sky metering, bloom, vignette or lens effects.
    vec3 color = max(texture(colortex0, screenUV).rgb, vec3(0.0));
    color *= vec3(1.0 + COLOUR_TEMPERATURE, 1.0, 1.0 - COLOUR_TEMPERATURE);
    color = max(mix(vec3(wmLuma(color)), color, SATURATION), vec3(0.0));
    // A shoulder above normal surface values retains lantern pixel detail.
    color = color / (vec3(1.0) + 0.075 * color);
    color = clamp(wmDisplay(color), 0.0, 1.0);
    finalColor = vec4(color, 1.0);
}

#include "/lib/settings.glsl"
#include "/lib/uniforms.glsl"
#include "/lib/math.glsl"
#include "/lib/sky.glsl"
uniform sampler2D colortex0;
uniform sampler2D depthtex0;
in vec2 screenUV;
const int colortex0Format = RGBA16F;
const int colortex1Format = RGBA8;
const int colortex3Format = RGBA16F;
const vec4 colortex1ClearColor = vec4(0.0);
/* RENDERTARGETS: 0,3 */
layout(location = 0) out vec4 litScene;
layout(location = 1) out vec4 opaqueSnapshot;
void main() {
    vec3 color = texture(colortex0, screenUV).rgb;
    float depth = texture(depthtex0, screenUV).r;
    if (depth >= 0.999999) {
        vec3 ray = wmWorldDirection(wmViewPosition(screenUV, 0.99999));
        color = wmSky(ray);
        if (isEyeInWater == 1) color = wmLinear(vec3(0.13, 0.29, 0.36));
        if (isEyeInWater == 2 || isEyeInWater == 3) color = wmLinear(fogColor);
        color *= 1.0 - clamp(max(blindness, darknessFactor), 0.0, 1.0);
    }
    litScene = vec4(color, 1.0);
    opaqueSnapshot = vec4(color, 1.0);
}

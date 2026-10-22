#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/diffuse.glsl"
in vec2 rasterUV;
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D depthtex1;
// Keep symbolic names for Iris's format parser and declare them for GLSL.
const int RGBA8 = 32856;
const int RGBA16F = 34842;
const int colortex0Format = RGBA8;
const int colortex1Format = RGBA16F;
const int colortex2Format = RGBA8;
const int colortex3Format = RGBA16F;
const int colortex4Format = RGBA16F;
const vec4 colortex0ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 colortex1ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 colortex2ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
/* RENDERTARGETS: 3,4,0,1 */
layout(location = 0) out vec4 resolvedScene;
layout(location = 1) out vec4 reflectionScene;
layout(location = 2) out vec4 emptyWaterColour;
layout(location = 3) out vec4 emptyWaterGeometry;
void main() {
    float z = texture(depthtex1, rasterUV).r;
    vec3 viewPoint = positionFromDepth(rasterUV, min(z, 0.999999));
    vec3 point = playerFromView(viewPoint);
    vec3 radiance;
    float reflectable = 0.0;
    if (z < 0.999999) {
        vec3 colour = texture(colortex0, rasterUV).rgb;
        vec4 shape = texture(colortex1, rasterUV);
        vec4 illumination = texture(colortex2, rasterUV);
        radiance = diffuseRadiance(colour, illumination.rgb, illumination.a, shape.xyz, shape.a, point);
        radiance = throughAir(radiance, point, illumination.a);
        reflectable = float(shape.a < 1.5);
    } else {
        vec3 direction = mat3(gbufferModelViewInverse) * unitVector(viewPoint);
        radiance = overcastCeiling(direction);
        if (isEyeInWater == 1) radiance = decodeDisplay(vec3(0.13, 0.28, 0.36));
        if (isEyeInWater > 1) radiance = decodeDisplay(fogColor);
        radiance *= 1.0 - clamp(max(blindness, darknessFactor), 0.0, 1.0);
    }
    resolvedScene = vec4(radiance, 1.0);
    reflectionScene = vec4(radiance, reflectable);
    // Reuse the albedo/normal attachments as water attributes after deferred.
    emptyWaterColour = vec4(0.0);
    emptyWaterGeometry = vec4(0.0);
}

#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
in vec2 rasterUV;
uniform sampler2D colortex0;
uniform sampler2D colortex3;
uniform sampler2D depthtex1;
const int RGBA8 = 32856;
const int RGBA16F = 34842;
const int colortex0Format = RGBA8;
const int colortex1Format = RGBA16F;
const int colortex2Format = RGBA16F;
const int colortex3Format = RGBA16F;
const int colortex4Format = RGBA16F;
const int colortex5Format = RGBA16F;
const int colortex6Format = RGBA16F;
const int colortex7Format = RGBA16F;
const vec4 colortex0ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 colortex1ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 colortex2ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 colortex3ClearColor = vec4(0.0, 0.0, 0.0, 0.0);
/* RENDERTARGETS: 3,4,0,1,2 */
layout(location = 0) out vec4 resolvedScene;
layout(location = 1) out vec4 reflectionScene;
layout(location = 2) out vec4 emptyWaterColour;
layout(location = 3) out vec4 emptyWaterGeometry;
layout(location = 4) out vec4 emptyWaterDepth;
void main() {
    float z = texture(depthtex1, rasterUV).r;
    vec3 viewPoint = positionFromDepth(rasterUV, min(z, 0.999999));
    vec3 point = playerFromView(viewPoint);
    // Use a finite-depth ray to reconstruct the sky direction.
    vec3 direction = unitVector(mat3(gbufferModelViewInverse) * positionFromDepth(rasterUV, 0.5));
    bool geometry = z < 0.999999;
    vec4 layer = texture(colortex3, rasterUV);
    vec3 radiance = geometry ? layer.rgb : layer.rgb + skyBackdrop(direction) * (1.0 - layer.a);
    if (isEyeInWater > 1 && !geometry) radiance = decodeDisplay(fogColor);
    if (!geometry) radiance *= 1.0 - clamp(max(blindness, darknessFactor), 0.0, 1.0);
    resolvedScene = vec4(radiance, 1.0);
    reflectionScene = vec4(radiance, geometry ? texture(colortex0, rasterUV).a : 0.0);
    emptyWaterColour = vec4(0.0, texture(colortex0,rasterUV).g, 0.0, 0.0);
    emptyWaterGeometry = vec4(0.0);
    emptyWaterDepth = vec4(0.0, geometry ? texture(colortex0,rasterUV).r : 1.0, geometry ? length(viewPoint) : 7000.0, 0.0);
}

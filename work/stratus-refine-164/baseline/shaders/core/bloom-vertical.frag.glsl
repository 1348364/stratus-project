#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform sampler2D colortex5;
in vec2 rasterUV;
/* RENDERTARGETS: 6 */
layout(location=0)out vec4 glow;
vec3 tap(vec2 uv){return texture(colortex5,clamp(uv,vec2(0.0),vec2(1.0))).rgb;}
void main(){
    vec2 pixel=vec2(0.0,4.0*BLOOM_RADIUS/1080.0);
    vec3 sum=tap(rasterUV)*0.227027;
    sum+=(tap(rasterUV+pixel*1.384615)+tap(rasterUV-pixel*1.384615))*0.3162162;
    sum+=(tap(rasterUV+pixel*3.230769)+tap(rasterUV-pixel*3.230769))*0.0702703;
    glow=vec4(sum,1.0);
}

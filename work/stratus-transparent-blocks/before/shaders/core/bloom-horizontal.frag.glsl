#include "/core/options.glsl"
#include "/core/frame.glsl"
uniform sampler2D colortex3;
uniform sampler2D colortex0;
uniform sampler2D depthtex0;
in vec2 rasterUV;
/* RENDERTARGETS: 5 */
layout(location=0)out vec4 glow;
vec3 brightPixels(vec2 coordinate){
    vec2 uv=clamp(coordinate,vec2(0.0),vec2(1.0));
    vec3 colour=max(texture(colortex3,uv).rgb,vec3(0.0));
    float brightness=dot(colour,vec3(0.2126,0.7152,0.0722));
    float emission=clamp(texture(colortex0,uv).g,0.0,1.0);
    float threshold=mix(2.2,0.22,emission);
    if(texture(depthtex0,uv).r>=0.999999)threshold=min(threshold,0.72);
    float knee=clamp(brightness-threshold+0.20,0.0,0.40);
    float excess=max(brightness-threshold,knee*knee/0.80);
    return colour*excess/max(brightness,0.001)*mix(1.0,2.0,emission);
}
void main(){
    vec2 pixel=vec2(4.0*BLOOM_RADIUS*viewHeight/(1080.0*max(viewWidth,1.0)),0.0);
    vec3 sum=brightPixels(rasterUV)*0.227027;
    sum+=(brightPixels(rasterUV+pixel*1.384615)+brightPixels(rasterUV-pixel*1.384615))*0.3162162;
    sum+=(brightPixels(rasterUV+pixel*3.230769)+brightPixels(rasterUV-pixel*3.230769))*0.0702703;
    glow=vec4(sum,1.0);
}

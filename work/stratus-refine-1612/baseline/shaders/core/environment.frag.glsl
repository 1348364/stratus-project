#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
in vec2 rasterUV;
/* RENDERTARGETS: 9 */
layout(location=0)out vec4 environmentRadiance;
void main(){
    float azimuth=(rasterUV.x-0.5)*6.283185307;
    float height=rasterUV.y*2.0-1.0;
    vec3 ray=vec3(cos(azimuth)*sqrt(max(1.0-height*height,0.0)),height,sin(azimuth)*sqrt(max(1.0-height*height,0.0)));
    vec3 sky=skyBackdrop(ray);
    vec4 cloud=marchCloudLayer(cameraPosition,ray,7000.0,ATMOSPHERE_QUALITY==2?12+CLOUD_LAYERS*8:12+CLOUD_LAYERS*4,true);
    environmentRadiance=vec4(mix(sky,cloud.rgb,cloud.a),1.0);
}

#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/scene-depth.glsl"
uniform sampler2D colortex3;
uniform sampler2D colortex7;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 scene=texture(colortex3,rasterUV).rgb;
    float distanceToScene=sceneDistance(rasterUV);
    ivec2 size=textureSize(colortex7,0);
    vec2 p=rasterUV*vec2(size)-0.5;
    ivec2 cell=ivec2(floor(p));vec2 f=fract(p);
    vec4 volume=vec4(0.0);float sum=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 sampleCell=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec2 uv=(vec2(sampleCell)+0.5)/vec2(size);
        // Radial opaque/water depth is cached in the unused metadata channel.
        // The centre still uses exact depth, retaining near translucent edges.
        float depth=texture(colortex2,uv).z;
        float depthWeight=exp(-abs(depth-distanceToScene)/max(1.0,distanceToScene*0.025));
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y)*depthWeight;
        volume+=texelFetch(colortex7,sampleCell,0)*weight;sum+=weight;
    }
    if(sum>0.0001)volume/=sum;else volume=vec4(0.0);
    completedScene=vec4(max(scene*(1.0-volume.a)+volume.rgb,vec3(0.0)),1.0);
}

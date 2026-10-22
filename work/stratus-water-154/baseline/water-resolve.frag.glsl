#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/medium.glsl"
#include "/core/forward.glsl"
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D colortex4;
uniform sampler2D colortex8;
uniform sampler2D colortex12;
uniform sampler2D colortex14;
uniform sampler2D depthtex0;
uniform sampler2D depthtex1;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 scene=texture(colortex3,rasterUV).rgb;
    vec4 mark=texture(colortex0,rasterUV),depth=texture(colortex2,rasterUV);
    vec3 n=texture(colortex1,rasterUV).xyz;
    float sky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float lamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    if(mark.a<=0.5||depth.a<=0.5){
        if(isEyeInWater==1){
            float z=texture(depthtex0,rasterUV).r;
            float path=z<0.999999?length(positionFromDepth(rasterUV,z)):64.0;
            scene=travelThroughWater(scene,path,biomeWaterTint,sky,lamp);
        }
        completedScene=vec4(max(scene,vec3(0)),1.0);return;
    }
    ivec2 size=textureSize(colortex12,0);vec2 grid=rasterUV*vec2(size)-0.5;
    ivec2 cell=ivec2(floor(grid));vec2 f=fract(grid);vec3 optics=vec3(0);float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));vec2 uv=(vec2(c)+0.5)/vec2(size);
        vec4 d=texture(colortex2,uv);vec3 normal=texture(colortex1,uv).xyz;
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y);
        weight*=step(0.5,d.a)*step(0.8,dot(n,normal));
        weight*=exp(-abs(depth.x-d.x)/max(0.10,depth.x*0.025));
        optics+=texelFetch(colortex12,c,0).rgb*weight;total+=weight;
    }
    vec4 tint=texture(colortex8,rasterUV);if(dot(tint.rgb,tint.rgb)<0.001)tint.rgb=biomeWaterTint;
    vec3 ray=positionFromDepth(rasterUV,0.5),water=ray*(depth.x/max(-ray.z,0.00001));
    if(total>0.0001)optics/=total;
    else{
        float z=texture(depthtex1,rasterUV).r;
        float path=isEyeInWater==1?length(water):(z<0.999999?length(positionFromDepth(rasterUV,z)-water):24.0);
        optics=travelThroughWater(texture(colortex4,rasterUV).rgb,path,tint.rgb,depth.y,tint.a);
    }
    // Keep glass, particles and other forward surfaces at full resolution.
    // A dark/tinted pane replaces part of the background; it is not a signed
    // colour delta that can be added to a different water background.
    float transmission=clamp(texture(colortex14,rasterUV).r,0.0,1.0);
    if(transmission>=0.999){
        // Preserve the existing full-resolution correction where no ordinary
        // alpha-blended surface replaces the background. Only covered pixels
        // need the new foreground/background transparency composition below.
        vec3 correction=scene-texture(colortex4,rasterUV).rgb;
        if(isEyeInWater==1)correction*=exp(-waterExtinction(tint.rgb,depth.y)*length(water));
        completedScene=vec4(max(optics+correction,vec3(0)),1.0);return;
    }
    vec3 foreground=forwardRadiance(scene,texture(colortex4,rasterUV).rgb,transmission);
    if(isEyeInWater==1){
        float z=texture(depthtex0,rasterUV).r;
        float path=z<0.999999?min(length(positionFromDepth(rasterUV,z)),length(water)):length(water);
        vec3 mediumTransmission=exp(-waterExtinction(tint.rgb,depth.y)*path);
        foreground=foreground*mediumTransmission+waterBodyColour(tint.rgb,depth.y,tint.a)*(1.0-transmission)*(1.0-mediumTransmission);
    }
    completedScene=vec4(max(compositeForward(optics,foreground,transmission),vec3(0)),1.0);
}

#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/medium.glsl"
#include "/core/lake-normal.glsl"
uniform sampler2D colortex4;
uniform sampler2D depthtex1;
uniform sampler2D colortex7;
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D depthtex0;
in vec2 rasterUV;
/* RENDERTARGETS: 3 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 image=texture(colortex3,rasterUV).rgb;
    vec4 markedColour=texture(colortex0,rasterUV);
    if(isEyeInWater==0&&markedColour.a<=0.5){
        completedScene=vec4(max(image,vec3(0.0)),1.0);return;
    }
    vec4 markedNormal=texture(colortex1,rasterUV),markedDepth=texture(colortex2,rasterUV);
    float cameraWaterPath=64.0;
    if(isEyeInWater==1){
        float frontDepth=texture(depthtex0,rasterUV).r;
        cameraWaterPath=frontDepth<0.999999?length(positionFromDepth(rasterUV,frontDepth)):64.0;
    }
    float waterSky=1.0;
    if(markedColour.a>0.5&&markedNormal.a>0.5&&markedDepth.a>0.5&&markedDepth.x>0.0){
        vec3 viewRay=positionFromDepth(rasterUV,0.5);
        vec3 waterView=viewRay*(markedDepth.x/max(-viewRay.z,0.00001));waterSky=markedDepth.y;
        vec3 point=playerFromView(waterView);
        vec3 faceView=unitVector(mat3(gbufferModelView)*markedNormal.xyz);
        vec3 nWorld=lakeNormal(point,markedNormal.xyz,markedDepth.x);
        vec3 nView=unitVector(mat3(gbufferModelView)*nWorld);
        if(dot(nView,-waterView)<0.0){nView=-nView;nWorld=-nWorld;faceView=-faceView;}
        vec3 reflectedRay=reflect(unitVector(waterView),nView);
        vec3 reflectedWorld=mat3(gbufferModelViewInverse)*reflectedRay;
        vec3 fallback=isEyeInWater==1?waterBodyColour(waterSky):overcastCeiling(reflectedWorld);
        if(isEyeInWater==0)fallback*=mix(0.03,1.0,smoothstep(0.04,0.8,waterSky));
        vec4 traced=vec4(0.0);
#if REFLECTION_MODE != 0
        // Reconstruct premultiplied half-resolution screen reflections.
        vec2 grid=rasterUV*vec2(textureSize(colortex7,0))-0.5;
        ivec2 cell=ivec2(floor(grid)),size=textureSize(colortex7,0);vec2 fraction=fract(grid);
        float total=0.0;
        for(int y=0;y<2;y++)for(int x=0;x<2;x++){
            ivec2 sampleCell=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
            vec2 uv=(vec2(sampleCell)+0.5)/vec2(size);
            vec4 neighbourDepth=texture(colortex2,uv),neighbourNormal=texture(colortex1,uv);
            float weight=(x==0?1.0-fraction.x:fraction.x)*(y==0?1.0-fraction.y:fraction.y);
            weight*=step(0.5,neighbourDepth.a)*step(0.8,dot(neighbourNormal.xyz,markedNormal.xyz));
            weight*=exp(-abs(neighbourDepth.x-markedDepth.x)/max(0.25,markedDepth.x*0.02));
            traced+=texelFetch(colortex7,sampleCell,0)*weight;total+=weight;
        }
        if(total>0.0001)traced/=total;
        traced.rgb/=max(traced.a,0.0001);
#endif
        vec3 reflected=mix(fallback,traced.rgb,traced.a);
        vec3 originalOpaque=texture(colortex4,rasterUV).rgb;
        vec3 overlay=image-originalOpaque;
        float opaqueDepth=texture(depthtex1,rasterUV).r;
        float thickness=opaqueDepth<0.999999?length(positionFromDepth(rasterUV,opaqueDepth)-waterView):24.0;
        // Refraction changes the sampled scene, not only the reflection normal.
        vec2 distortion=(nView.xy-faceView.xy)*WATER_DISTORTION*0.15*clamp(thickness*0.3,0.25,1.0);
        vec2 shifted=clamp(rasterUV+distortion,vec2(0.001),vec2(0.999));
        float shiftedDepth=texture(depthtex1,shifted).r;
        if(shiftedDepth<0.999999&&-positionFromDepth(shifted,shiftedDepth).z<markedDepth.x+0.03)shifted=rasterUV;
        vec3 transmitted=texture(colortex4,shifted).rgb;
        // The foreground cloud pass runs after water. Integrate the segment behind
        // the interface here so underwater sky and elevated water are both ordered.
        vec3 backRay=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(shifted,0.5));
        float tail=opaqueDepth<0.999999?max(thickness,0.0):7000.0;
        vec4 behind=marchCloudLayer(cameraPosition+point+backRay*0.05,backRay,tail,6,false);
        transmitted=mix(transmitted,behind.rgb,behind.a);
        if(isEyeInWater==0){
            float side=1.0-abs(markedNormal.y);
            thickness=mix(clamp(thickness,0.0,36.0),min(thickness,1.8),side);
            transmitted=travelThroughWater(transmitted,max(thickness,0.12),waterSky);
        }else cameraWaterPath=length(waterView);
        float cosine=clamp(dot(nView,unitVector(-waterView)),0.0,1.0);
        float fresnel=0.025+0.975*pow(1.0-cosine,5.0);
        if(isEyeInWater==1)fresnel=max(fresnel,1.0-smoothstep(0.63,0.69,cosine));
        float weight=REFLECT_LEVEL*mix(0.16,1.0,fresnel);
        image=mix(transmitted,reflected,weight)+overlay;
    }
    if(isEyeInWater==1)image=travelThroughWater(image,cameraWaterPath,waterSky);
    completedScene=vec4(max(image,vec3(0.0)),1.0);
}

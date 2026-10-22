#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/medium.glsl"
#include "/core/lake-normal.glsl"
#include "/core/environment.glsl"
#include "/core/volume.glsl"
#include "/core/water-path.glsl"
uniform sampler2D colortex13;
uniform sampler2D colortex8;
uniform sampler2D colortex4;
uniform sampler2D depthtex1;
uniform sampler2D colortex7;
uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D depthtex0;
#include "/core/refraction.glsl"
in vec2 rasterUV;
/* RENDERTARGETS: 12 */
layout(location=0)out vec4 completedScene;
void main(){
    vec3 image=texture(colortex3,rasterUV).rgb;
    vec4 markedColour=texture(colortex0,rasterUV);
    float opaqueDepth=texture(depthtex1,rasterUV).r;
    vec3 opaqueView=positionFromDepth(rasterUV,opaqueDepth);
    if(isEyeInWater==0&&markedColour.a<=0.5){
        completedScene=vec4(max(image,vec3(0.0)),1.0);return;
    }
    vec4 markedNormal=texture(colortex1,rasterUV),markedDepth=texture(colortex2,rasterUV);
    float cameraWaterPath=64.0;
    if(isEyeInWater==1){
        float frontDepth=texture(depthtex0,rasterUV).r;
        cameraWaterPath=frontDepth<0.999999?length(positionFromDepth(rasterUV,frontDepth)):64.0;
    }
    float waterSky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float waterLamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    vec3 waterTint=biomeWaterTint;
    if(markedColour.a>0.5&&markedNormal.a>0.5&&markedDepth.a>0.5&&markedDepth.x>0.0){
        vec3 viewRay=positionFromDepth(rasterUV,0.5);
        vec3 waterView=viewRay*(markedDepth.x/max(-viewRay.z,0.00001));waterSky=markedDepth.y;
        vec4 opticalData=texture(colortex8,rasterUV);
        waterTint=opticalData.rgb;waterLamp=opticalData.a;
        if(dot(waterTint,waterTint)<0.001)waterTint=biomeWaterTint;
        vec3 point=playerFromView(waterView);
        vec3 faceView=unitVector(mat3(gbufferModelView)*markedNormal.xyz);
        vec3 nWorld=lakeNormal(point,markedNormal.xyz,markedDepth.x,markedDepth.y);
        vec3 nView=unitVector(mat3(gbufferModelView)*nWorld);
        if(dot(nView,-waterView)<0.0){nView=-nView;nWorld=-nWorld;faceView=-faceView;}
        vec3 reflectedRay=reflect(unitVector(waterView),nView);
        vec3 reflectedWorld=mat3(gbufferModelViewInverse)*reflectedRay;
        vec3 fallback=isEyeInWater==1?waterBodyColour(waterTint,waterSky,waterLamp):reflectedEnvironment(reflectedWorld);
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
        float thickness=opaqueDepth<0.999999?length(opaqueView-waterView):24.0;
        // v1.3.1 screen-space water refraction, with the original shoreline guard.
        vec2 shifted=legacyWaterRefractionUV(rasterUV,nView,faceView,thickness,markedDepth.x);
        float shiftedDepth=texture(depthtex1,shifted).r;
        vec3 transmitted=texture(colortex4,shifted).rgb;
        vec3 backRay=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(shifted,0.5));
        if(shiftedDepth>=0.999999)transmitted=reflectedEnvironment(backRay);
        bool backgroundGeometry=shiftedDepth<0.999999;
        vec3 receiver=backgroundGeometry?positionFromDepth(shifted,shiftedDepth):waterView+unitVector(waterView)*7000.0;
        float receiverDistance=length(receiver-waterView);
        float opticalPath=backgroundGeometry?receiverDistance:24.0;
        float cosine=clamp(dot(nView,unitVector(-waterView)),0.0,1.0);
        float fresnel=dielectricWaterFresnel(cosine,isEyeInWater==1?1.333:1.0,isEyeInWater==1?1.0:1.333);
        bool totalReflection=isEyeInWater==1&&fresnel>=0.99999;
        if(isEyeInWater==0){
            if(markedColour.b>0.5){
                vec3 worldViewRay=unitVector(mat3(gbufferModelViewInverse)*waterView);
                opticalPath=fallingWaterThickness(point+cameraPosition,markedNormal.xyz,worldViewRay,receiverDistance);
                float airDistance=max(receiverDistance-opticalPath,0.0);
                // depthtex1 omits ALL water. Keep a second horizontal entry so
                // an ocean behind a waterfall retains its own water depth.
                vec4 background=texture(colortex13,shifted);
                if(hasBackgroundWater(background,markedDepth.x,-receiver.z)){
                    vec3 r=positionFromDepth(shifted,0.5);
                    vec3 backgroundView=r*(background.x/max(-r.z,0.00001));
                    transmitted=travelThroughWater(transmitted,min(length(receiver-backgroundView),96.0),biomeWaterTint,background.y,background.z);
                    vec3 backgroundNormal=lakeNormal(playerFromView(backgroundView),vec3(0,1,0),background.x,background.y);
                    vec3 reflectedBackground=reflect(unitVector(mat3(gbufferModelViewInverse)*backgroundView),backgroundNormal);
                    float backgroundFresnel=dielectricWaterFresnel(clamp(dot(backgroundNormal,-backRay),0.0,1.0),1.0,1.333);
                    transmitted=mix(transmitted,reflectedEnvironment(reflectedBackground)*mix(0.03,1.0,smoothstep(0.04,0.8,background.y)),clamp(REFLECT_LEVEL*backgroundFresnel,0.0,1.0));
                    airDistance=max(length(backgroundView-waterView)-opticalPath,0.0);
                }else if(backgroundGeometry&&joinsSurroundingWater(colortex13,shifted,cameraPosition+point,backRay,receiverDistance)){
                    // The falling volume joins the ocean without an air/water
                    // face. Attenuate the continuous water path to its floor.
                    opticalPath=receiverDistance;airDistance=0.0;
                }
                transmitted=airBehindWater(transmitted,cameraPosition+point+backRay*opticalPath,backRay,airDistance,waterSky,backgroundGeometry);
            }
            transmitted=travelThroughWater(transmitted,min(opticalPath,96.0),waterTint,waterSky,waterLamp);
        }else{
            // Looking out from underwater also crosses air beyond the surface.
            if(!totalReflection)transmitted=airBehindWater(transmitted,cameraPosition+point,backRay,receiverDistance,waterSky,backgroundGeometry);
            cameraWaterPath=length(waterView);
        }
        // Fresnel conserves reflected/transmitted energy; TIR remains complete
        // even if the artistic reflection-strength control is reduced.
        float weight=totalReflection?1.0:clamp(REFLECT_LEVEL*fresnel,0.0,1.0);
        image=mix(transmitted,reflected,weight);
    }
    if(isEyeInWater==1)image=travelThroughWater(image,cameraWaterPath,waterTint,waterSky,waterLamp);
    completedScene=vec4(max(image,vec3(0.0)),1.0);
}

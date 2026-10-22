#include "/core/options.glsl"
#include "/core/frame.glsl"
#include "/core/ceiling.glsl"
#include "/core/air.glsl"
#include "/core/medium.glsl"
#include "/core/lake-normal.glsl"
#include "/core/environment.glsl"
uniform sampler2D colortex8;
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
    float opaqueDepth=texture(depthtex1,rasterUV).r;
    vec3 opaqueView=positionFromDepth(rasterUV,opaqueDepth);
    // Derivatives precede divergent water/land branches. The local opaque
    // tangent plane gives a stable Snell-ray intersection on Minecraft faces.
    vec3 opaquePlane=cross(dFdx(opaqueView),dFdy(opaqueView));
    float planeLength=length(opaquePlane);
    opaquePlane/=max(planeLength,0.00000001);
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
        vec3 originalOpaque=texture(colortex4,rasterUV).rgb;
        vec3 overlay=image-originalOpaque;
        float thickness=opaqueDepth<0.999999?length(opaqueView-waterView):24.0;
        vec3 incident=unitVector(waterView);
        float etaI=isEyeInWater==1?1.333:1.0;
        float etaT=isEyeInWater==1?1.0:1.333;
        float cosine=clamp(dot(nView,-incident),0.0,1.0);
        float fresnel=dielectricWaterFresnel(cosine,etaI,etaT);
        vec3 bent=refract(incident,nView,etaI/etaT);
        bool totalReflection=dot(bent,bent)<0.001;
        vec3 refracted=totalReflection?incident:unitVector(mix(incident,bent,clamp(WATER_DISTORTION,0.0,1.35)));
        vec2 shifted=rasterUV;
        float opticalPath=max(thickness,0.0);
        // Intersect the actual receiver plane, rather than repeatedly solving
        // a constant-view-Z slice (which folds floors at grazing angles).
        bool validRefraction=!totalReflection&&opaqueDepth<0.999999&&planeLength>0.00000001;
        vec3 candidate=opaqueView;
        if(validRefraction){
            float denominator=dot(refracted,opaquePlane);
            float t=abs(denominator)>0.0001?dot(opaqueView-waterView,opaquePlane)/denominator:-1.0;
            validRefraction=t>=0.0&&t<=128.0;
            candidate=waterView+refracted*max(t,0.0);
            vec4 clip=gbufferProjection*vec4(candidate,1.0);
            vec2 physicalUV=clip.xy/max(clip.w,0.0001)*0.5+0.5;
            vec2 delta=physicalUV-rasterUV;
            // A single screen layer cannot supply the wide-angle disocclusion
            // of true refraction. Bound displacement continuously instead of
            // cross-fading a magnified floor with its undistorted double.
            vec2 border=min(rasterUV,1.0-rasterUV);
            float budget=min(0.035,max(0.0001,0.7*min(border.x,border.y)));
            shifted=rasterUV+delta*(budget/sqrt(budget*budget+dot(delta,delta)));
            validRefraction=validRefraction&&clip.w>0.0;
            opticalPath=max(t,0.0);
        }
        float shiftedDepth=texture(depthtex1,shifted).r;
        if(shiftedDepth<0.999999&&-positionFromDepth(shifted,shiftedDepth).z<markedDepth.x+0.02)validRefraction=false;
        float refractionConfidence=validRefraction?1.0:0.0;
        if(validRefraction&&shiftedDepth<0.999999){
            vec3 target=positionFromDepth(shifted,shiftedDepth);
            float residual=abs(dot(target-opaqueView,opaquePlane));
            // Reject receiver changes at silhouettes; a single opaque depth
            // layer cannot reconstruct hidden floor/wall geometry.
            refractionConfidence*=1.0-smoothstep(0.04,0.35,residual);
        }
        if(!validRefraction){shifted=rasterUV;opticalPath=thickness;shiftedDepth=opaqueDepth;}
        vec3 fallbackTransmission=opaqueDepth>=0.999999
            ?reflectedEnvironment(mat3(gbufferModelViewInverse)*incident):originalOpaque;
        vec3 sampledTransmission=shiftedDepth>=0.999999
            ?reflectedEnvironment(mat3(gbufferModelViewInverse)*refracted):texture(colortex4,shifted).rgb;
        vec3 transmitted=mix(fallbackTransmission,sampledTransmission,refractionConfidence);
        opticalPath=mix(thickness,opticalPath,refractionConfidence);
        if(isEyeInWater==0){
            // A single path length is shared by top, waterfall sides and underside.
            // No artificial 1.8-block side cap.
            // Flowing water has a finite sheet/slab thickness. A distant sky or
            // land sample is not evidence that the entire ray lies inside water.
            if(markedColour.b>0.5){
                float vertical=abs(markedNormal.y);
                float height=clamp(fract((point+cameraPosition).y+0.02),0.08,0.90);
                float slab=mix(0.95,height,vertical);
                opticalPath=min(opticalPath,slab/max(abs(dot(refracted,faceView)),0.15));
            }
            transmitted=travelThroughWater(transmitted,min(opticalPath,96.0),waterTint,waterSky,waterLamp);
        }else cameraWaterPath=length(waterView);
        // Fresnel conserves reflected/transmitted energy; TIR remains complete
        // even if the artistic reflection-strength control is reduced.
        float weight=totalReflection?1.0:clamp(REFLECT_LEVEL*fresnel,0.0,1.0);
        image=mix(transmitted,reflected,weight)+overlay;
    }
    if(isEyeInWater==1)image=travelThroughWater(image,cameraWaterPath,waterTint,waterSky,waterLamp);
    completedScene=vec4(max(image,vec3(0.0)),1.0);
}

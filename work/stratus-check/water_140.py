from pathlib import Path
C=Path('outputs/Stratus/shaders/core')
p=C/'trace.glsl';s=p.read_text().replace('vec4 sceneryReflection(vec3 viewOrigin, vec3 viewDirection) {','vec4 sceneryReflection(vec3 viewOrigin, vec3 viewDirection, out float hitDistance) {\n    hitDistance=0.0;');s=s.replace('    vec3 projectiveEnd = rayEnd * reciprocalEnd;','''    vec3 projectiveEnd = rayEnd * reciprocalEnd;
    // Clip the projected ray to the viewport before distributing samples.
    // Otherwise a mostly off-screen ray spends almost no samples on visible water.
    vec2 delta=screenEnd-screenBegin;
    float visibleFraction=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visibleFraction=min(visibleFraction,(0.998-screenBegin[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visibleFraction=min(visibleFraction,(0.002-screenBegin[axis])/delta[axis]);
    }
    visibleFraction=clamp(visibleFraction,0.0,1.0);
    screenEnd=mix(screenBegin,screenEnd,visibleFraction);
    projectiveEnd=mix(projectiveBegin,projectiveEnd,visibleFraction);
    reciprocalEnd=mix(reciprocalBegin,reciprocalEnd,visibleFraction);''');s=s.replace('            vec4 centre = texture(colortex4, hitScreen);','            hitDistance=length(hitPoint-viewOrigin);\n            confidence*=smoothstep(0.10,0.35,hitDistance);\n            vec4 centre = texture(colortex4, hitScreen);');p.write_text(s)
p=C/'water-reflection.frag.glsl';s=p.read_text().replace('#include "/core/trace.glsl"','#include "/core/trace.glsl"\n#include "/core/medium.glsl"\nuniform sampler2D colortex8;');s=s.replace('    vec4 traced=sceneryReflection(view+n*0.075,reflect(unitVector(view),n));','''    float hitDistance;
    vec4 traced=sceneryReflection(view+n*0.075,reflect(unitVector(view),n),hitDistance);
    if(isEyeInWater==1){
        vec4 tint=texture(colortex8,rasterUV);
        traced.rgb=travelThroughWater(traced.rgb,hitDistance,tint.rgb,depth.y,tint.a);
    }''');p.write_text(s)
p=C/'lake.frag.glsl';s=p.read_text();s=s.replace('#include "/core/lake-normal.glsl"','#include "/core/lake-normal.glsl"\n#include "/core/environment.glsl"\nuniform sampler2D colortex8;')
s=s.replace('    float waterSky=1.0;','''    float waterSky=clamp(float(eyeBrightnessSmooth.y)/240.0,0.0,1.0);
    float waterLamp=clamp(float(eyeBrightnessSmooth.x)/240.0,0.0,1.0);
    vec3 waterTint=biomeWaterTint;''')
s=s.replace('        vec3 point=playerFromView(waterView);','''        vec4 opticalData=texture(colortex8,rasterUV);
        waterTint=opticalData.rgb;waterLamp=opticalData.a;
        if(dot(waterTint,waterTint)<0.001)waterTint=biomeWaterTint;
        vec3 point=playerFromView(waterView);''')
s=s.replace('vec3 fallback=isEyeInWater==1?waterBodyColour(waterSky):overcastCeiling(reflectedWorld);','vec3 fallback=isEyeInWater==1?waterBodyColour(waterTint,waterSky,waterLamp):reflectedEnvironment(reflectedWorld);')
a=s.index('        // Refraction changes');b=s.index('        image=mix(transmitted,reflected,weight)+overlay;')
s=s[:a]+'''        vec3 incident=unitVector(waterView);
        float etaI=isEyeInWater==1?1.333:1.0;
        float etaT=isEyeInWater==1?1.0:1.333;
        float cosine=clamp(dot(nView,-incident),0.0,1.0);
        float fresnel=dielectricWaterFresnel(cosine,etaI,etaT);
        vec3 bent=refract(incident,nView,etaI/etaT);
        bool totalReflection=dot(bent,bent)<0.001;
        vec3 refracted=totalReflection?incident:unitVector(mix(incident,bent,clamp(WATER_DISTORTION,0.0,1.35)));
        vec2 shifted=rasterUV;
        float opticalPath=max(thickness,0.0);
        // Iteratively intersect Snell's refracted ray with the visible opaque
        // depth field. A foreground/depth validity check prevents shore leaks.
        bool validRefraction=!totalReflection;
        for(int iteration=0;iteration<4;iteration++){
            float deviceZ=texture(depthtex1,shifted).r;
            if(deviceZ>=0.999999)break;
            vec3 target=positionFromDepth(shifted,deviceZ);
            float t=(target.z-waterView.z)/min(refracted.z,-0.0001);
            if(t<0.0||t>128.0){validRefraction=false;break;}
            vec3 candidate=waterView+refracted*t;
            vec4 clip=gbufferProjection*vec4(candidate,1.0);
            vec2 nextUV=clip.xy/max(clip.w,0.0001)*0.5+0.5;
            if(min(nextUV.x,nextUV.y)<0.002||max(nextUV.x,nextUV.y)>0.998){validRefraction=false;break;}
            shifted=nextUV;opticalPath=t;
        }
        float shiftedDepth=texture(depthtex1,shifted).r;
        if(shiftedDepth<0.999999&&-positionFromDepth(shifted,shiftedDepth).z<markedDepth.x+0.02)validRefraction=false;
        if(!validRefraction){shifted=rasterUV;opticalPath=thickness;}
        vec3 transmitted=texture(colortex4,shifted).rgb;
        if(shiftedDepth>=0.999999&&isEyeInWater==1)
            transmitted=reflectedEnvironment(mat3(gbufferModelViewInverse)*refracted);
        if(isEyeInWater==0){
            // A single path length is shared by top, waterfall sides and underside.
            // No artificial 1.8-block side cap.
            transmitted=travelThroughWater(transmitted,min(opticalPath,96.0),waterTint,waterSky,waterLamp);
        }else cameraWaterPath=length(waterView);
        // Fresnel conserves reflected/transmitted energy; TIR remains complete
        // even if the artistic reflection-strength control is reduced.
        float weight=totalReflection?1.0:clamp(REFLECT_LEVEL*fresnel,0.0,1.0);
''' +s[b:]
s=s.replace('travelThroughWater(image,cameraWaterPath,waterSky)','travelThroughWater(image,cameraWaterPath,waterTint,waterSky,waterLamp)');p.write_text(s)

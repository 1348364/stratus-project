#ifndef STRATUS_CEILING_INCLUDED
#define STRATUS_CEILING_INCLUDED
#include "/core/field.glsl"
#include "/core/weather-volume.glsl"
vec3 atmosphericColour() {
#if DIMENSION_TYPE == 0
    vec3 day=decodeDisplay(vec3(0.69,0.72,0.76));
    return mix(decodeDisplay(vec3(0.06,0.085,0.14)),day,daytimeWeight())*(1.0-0.12*rainStrength);
#else
    return decodeDisplay(fogColor);
#endif
}
float solarDaylight(){return daytimeWeight()*smoothstep(-0.06,0.10,broadLightDirection().y);}
vec3 softSkyReflection(vec3 worldRay){
    vec3 ray=unitVector(worldRay);
    vec3 sky=atmosphericColour()*mix(0.65,1.05,smoothstep(-0.1,0.8,ray.y));
    float glow=exp(-max(1.0-dot(ray,broadLightDirection()),0.0)/0.08);
    return sky+sunlightColour()*glow*0.16*solarDaylight()*SKY_LEAK;
}
vec3 skyBackdrop(vec3 worldRay){
#if DIMENSION_TYPE != 0
    return decodeDisplay(fogColor);
#else
    vec3 ray=unitVector(worldRay);
    float horizon=exp(-max(ray.y,0.0)*5.0);
    vec3 zenith=decodeDisplay(mix(vec3(0.045,0.072,0.12),vec3(0.56,0.65,0.76),daytimeWeight()));
    vec3 sky=mix(zenith,atmosphericColour(),horizon);
    sky=mix(sky,atmosphericColour(),CLOUD_AMOUNT*0.20);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float glow=exp(-separation/0.08)*SKY_LEAK*0.22;
    float core=exp(-separation/0.00032)*3.4;
#if SUN_STYLE == 1
    core=0.0;
#endif
    float aureole=exp(-separation/0.008)*0.70;
#if SUN_STYLE == 1
    aureole=0.0;
#endif
    sky+=sunlightColour()*solarDaylight()*(glow+(core+aureole)*SUN_VISIBILITY*(1.0-0.65*rainStrength));
    return sky;
#endif
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    if(amount<=0.0)return vec2(0.0);
    vec2 wind=frameTimeCounter*CLOUD_DRIFT*vec2(0.31,-0.14)*(upper?1.55:1.0);
    vec2 weatherPoint=(worldPoint.xz+wind)/max(CLOUD_SPAN,16.0);
    float weather=weatherVolume(vec3(weatherPoint.x*0.073,0.37,weatherPoint.y*0.073)).a;
    float centre=altitude+(weather-0.5)*thickness*CLOUD_DISTORTION*1.35;
    float height=(worldPoint.y-centre)/max(thickness,1.0)+0.5;
    float envelope=smoothstep(-0.08,0.24,height)*(1.0-smoothstep(0.62,1.12,height));
    if(envelope<=0.0)return vec2(0.0);
    vec3 p=vec3(weatherPoint.x*0.65,(worldPoint.y-altitude)/max(thickness,1.0)*0.55,weatherPoint.y*0.65);
    p.xz=mat2(0.8,-0.6,0.6,0.8)*p.xz;
    p.x+=(weather-0.5)*CLOUD_DISTORTION*0.12;
    if(upper){p.x*=0.24;p.z*=1.65;p.x+=sin(p.z*14.0+weather*3.0)*0.035;}
    vec4 volume=weatherVolume(p);
    float body=upper?volume.b:mix(volume.r,volume.g,0.65);
    float threshold=mix(0.78,upper?0.25:0.23,clamp(amount,0.0,1.0));
    float profile=pow(abs(height-0.5)*1.60,2.0)*0.80;
    float potential=body+(weather-0.5)*0.18-profile;
    float bulk=smoothstep(threshold-0.05,threshold+0.12,potential);
    if(detailed){
        float fine=weatherVolume(p*2.17+vec3(0.29,0.63,0.12)).b;
        float erosion=(1.0-fine)*CLOUD_DETAIL*0.20*(1.0-bulk*0.75);
#if CLOUD_LAYERS > 2
        erosion+=weatherVolume(p*4.13-vec3(0.17,0.42,0.28)).g*CLOUD_DETAIL*0.045*(1.0-bulk*0.8);
#endif
        bulk=clamp((bulk-erosion)/max(1.0-erosion,0.1),0.0,1.0);
    }
    // No minimum-density floor: filled overcast comes from overlapping rounded
    // volumes, not a flat compulsory sheet. Fine detail erodes their edges.
    return vec2(envelope*bulk*amount*CLOUD_DENSITY*(upper?0.024:0.050),height);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float tau=0.0;
    const int samples=2+CLOUD_LAYERS;
    float distance=CLOUD_THICKNESS*1.8;
    for(int i=0;i<samples;i++){
        float t=(float(i)+0.5)/float(samples);
        tau+=layeredCloudSample(point+l*distance*t,false,false).x*distance/float(samples);
    }
    return exp(-tau);
}
float cloudPhase(float cosine){
    float forward=0.64,backward=-0.25;
    float f=(1.0-forward*forward)/pow(max(1.0+forward*forward-2.0*forward*cosine,0.02),1.5);
    float b=(1.0-backward*backward)/pow(max(1.0+backward*backward-2.0*backward*cosine,0.02),1.5);
    return 0.85*f+0.15*b;
}
vec4 overLayers(vec4 front,vec4 back){
    float alpha=front.a+(1.0-front.a)*back.a;
    return vec4((front.rgb*front.a+back.rgb*back.a*(1.0-front.a))/max(alpha,0.00001),alpha);
}
vec4 marchSingleCloud(vec3 origin,vec3 worldRay,float distanceLimit,int steps,bool shadows,bool upper){
#if DIMENSION_TYPE != 0 || CLOUD_STYLE != 0
    return vec4(0.0);
#else
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;if(amount<=0.0)return vec4(0.0);
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?32.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*1.55,top=altitude+thickness*1.55;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    if(finish<=begin)return vec4(0.0);
    // One continuous horizon limit avoids a horizontal seam while flying inside.
    finish=min(finish,begin+2400.0);
    float closeSampling=1.0-smoothstep(0.0,thickness,begin);
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float separation=max(1.0-dot(ray,broadLightDirection()),0.0);
    float phase=cloudPhase(dot(ray,broadLightDirection()));
    float solarPatch=exp(-separation/0.0014)*SUN_VISIBILITY;
    for(int i=0;i<steps;i++){
        float u0=float(i)/float(steps),u1=float(i+1)/float(steps);
        u0=mix(u0,u0*u0,closeSampling);u1=mix(u1,u1*u1,closeSampling);
        float stride=(finish-begin)*(u1-u0);
        vec3 point=origin+ray*(begin+(u0+u1)*0.5*(finish-begin));
        vec2 sampleData=layeredCloudSample(point,shadows||upper,upper);if(sampleData.x<=0.00001)continue;
        float opacity=1.0-exp(-sampleData.x*stride);
        float h=clamp(sampleData.y,0.0,1.0);
        float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.35,1.0,h);
        float ambientSky=exp(-layeredCloudSample(point+vec3(0.0,CLOUD_THICKNESS*0.28,0.0),false,upper).x*CLOUD_THICKNESS*0.9);
        float ambient=mix(0.42,1.0,h)*mix(0.60,1.25,ambientSky);
        float powder=1.0-exp(-sampleData.x*35.0);
        vec3 daylight=vec3(0.35,0.39,0.46)*ambient;
        daylight+=sunlightColour()*sunlight*(0.27+phase*0.065*SUN_VISIBILITY);
        daylight+=vec3(0.13,0.145,0.165)*powder*(0.4+0.6*h);
        daylight*=mix(1.0,0.70+0.30*sunlight,CLOUD_RELIEF);
        // Forward scattering exposes a soft warm solar location from below too.
        daylight+=sunlightColour()*(phase*SKY_LEAK*0.08*sunlight+solarPatch*(0.45+1.25*sunlight));
        vec3 colour=mix(vec3(0.006,0.010,0.019)*ambient,daylight,daytimeWeight());
        colour*=1.0-0.17*rainStrength;
        scattered+=transmission*opacity*colour;transmission*=1.0-opacity;
        if(transmission<0.015)break;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,1.0-transmission);
#endif
}
vec4 marchCloudLayer(vec3 origin,vec3 ray,float limit,int steps,bool shadows){
    vec4 low=marchSingleCloud(origin,ray,limit,steps,shadows,false);
    vec4 high=marchSingleCloud(origin,ray,limit,max(4,steps/2),false,true);
    return ray.y<0.0?overLayers(high,low):overLayers(low,high);
}
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,20+CLOUD_LAYERS*16,true);}
vec3 overcastCeiling(vec3 worldRay){
    // A prefiltered reflection approximation avoids a cloud ray march per water pixel.
    vec3 ray=unitVector(worldRay);vec3 sky=skyBackdrop(ray);
    if(abs(ray.y)<0.01)return mix(sky,atmosphericColour(),0.75);
    float distanceToLayer=(CLOUD_ALTITUDE-cameraPosition.y)/ray.y;
    if(distanceToLayer>0.0){
        vec3 point=cameraPosition+ray*distanceToLayer;
        vec2 density=layeredCloudSample(point,false,false);
        // Prefilter the broad cloud contribution: sharp density patches do not
        // survive a rough, rippling water reflection.
        float coverage=smoothstep(0.0,0.040,density.x);
        vec3 colour=atmosphericColour()*mix(0.90,1.13,coverage);
        sky=mix(sky,colour,CLOUD_AMOUNT*0.72);
    }
    return sky;
}
#endif

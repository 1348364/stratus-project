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
// Vanilla-like connected islands, with softened grid corners. The layout and
// porous billows are original fields; no other shader's texture/code is used.
float cloudIslandField(vec2 p){
    ivec2 cell=ivec2(floor(p));vec2 f=smoothstep(vec2(0.18),vec2(0.82),fract(p));
    float a=latticeValue(cell),b=latticeValue(cell+ivec2(1,0));
    float c=latticeValue(cell+ivec2(0,1)),d=latticeValue(cell+ivec2(1,1));
    float blocks=mix(mix(a,b,f.x),mix(c,d,f.x),f.y);
    return mix(blocks,smoothField(p*0.41+vec2(13.2,-8.5)),0.28);
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?28.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    if(amount<=0.0)return vec2(0.0);
    vec2 wind=frameTimeCounter*CLOUD_DRIFT*vec2(0.31,-0.14)*(upper?1.55:1.0);
    vec2 xz=(worldPoint.xz+wind)/max(CLOUD_SPAN,16.0);
    float weather=smoothField(xz*0.31+vec2(9.8,2.7));
    vec2 islandPoint=xz*2.25;
    islandPoint+=vec2(smoothField(xz*0.7)-0.5,smoothField(xz*0.7+17.2)-0.5)*CLOUD_DISTORTION*0.32;
    float islandLayout=cloudIslandField(islandPoint);
    float threshold=mix(0.90,0.20,clamp(amount,0.0,1.0));
    float island=smoothstep(threshold-0.03,threshold+0.16,islandLayout);
    if(island<0.001)return vec2(0.0);
    float h=(worldPoint.y-altitude)/max(thickness,1.0)+0.5;
    h-=(weather-0.5)*CLOUD_DISTORTION*0.15;
    float envelope=smoothstep(0.0,0.17,h)*(1.0-smoothstep(0.64,1.04,h));
    if(envelope<=0.0)return vec2(0.0);
    vec3 point=vec3(xz.x*1.75,(worldPoint.y-altitude)/max(thickness,1.0)*0.8,xz.y*1.75);
    if(upper){point.x*=0.23;point.z*=2.4;point.x+=sin(point.z*11.0)*0.024;}
    vec4 volume=weatherVolume(point);
    float shape=upper?volume.b:mix(volume.g,volume.r,0.58);
    float cap=pow(abs(h-0.45)*1.70,2.0);
    float bulk=smoothstep(0.37,0.70,shape+island*0.13-cap*0.52);
    if(detailed){
        vec4 detail=weatherVolume(point*4.37+vec3(0.19,0.53,0.31));
        float pores=pow(max(0.0,1.0-detail.g),1.25)*CLOUD_DETAIL;
        bulk=max(0.0,bulk-pores*(0.35+0.22*(1.0-bulk)));
        bulk*=mix(1.0,0.65+detail.b*0.6,clamp(CLOUD_DETAIL,0.0,1.0));
    }
    return vec2(island*envelope*bulk*CLOUD_DENSITY*(upper?0.016:0.040),h);
}
vec2 cloudVolumeSample(vec3 p,bool detailed){return layeredCloudSample(p,detailed,false);}
vec2 cloudSample(vec3 p){return layeredCloudSample(p,true,false);}
float cloudSunTransmission(vec3 point){
    vec3 l=broadLightDirection();float tau=0.0;
    const int samples=ATMOSPHERE_QUALITY==2?2+CLOUD_LAYERS:3;
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
    float thickness=upper?28.0:CLOUD_THICKNESS;
    float bottom=altitude-thickness*0.72,top=altitude+thickness*0.72;
    vec3 ray=unitVector(worldRay);float begin=0.0,finish=min(distanceLimit,7000.0);
    if(abs(ray.y)<0.0001){if(origin.y<bottom||origin.y>top)return vec4(0.0);}
    else{float a=(bottom-origin.y)/ray.y,b=(top-origin.y)/ray.y;begin=max(min(a,b),0.0);finish=min(finish,max(a,b));}
    // From inside a cloud, kilometre-long grazing rays spent almost the whole
    // budget on distant cells and resolved the nearby volume as thin sheets.
    // Keep four broad formations in range, blending the bound through the slab
    // edges so vertical movement does not switch integration domains abruptly.
    float interior=smoothstep(bottom,bottom+thickness*0.22,origin.y)
        *(1.0-smoothstep(top-thickness*0.22,top,origin.y));
    finish=min(finish,mix(7000.0,max(512.0,CLOUD_SPAN*4.0),interior));
    if(finish<=begin)return vec4(0.0);
    // Continuous midpoint quadrature over the clipped segment. Direction-
    // dependent world-plane sizes changed grid phase across pixels, producing
    // seams and moire inside the layer. The density field remains world-space;
    // no temporal jitter or camera-anchored noise is introduced.
    float advance=(finish-begin)/max(float(steps),1.0),start=begin;
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float phase=cloudPhase(dot(ray,broadLightDirection()));
    for(int i=0;i<512;i++){
        if(i>=steps||start>=finish)break;
        float end=min(begin+float(i+1)*advance,finish),stride=max(end-start,0.0);
        vec3 point=origin+ray*(start+end)*0.5;
        vec2 sampleData=layeredCloudSample(point,true,upper);
        if(sampleData.x>0.00001){
            float opacity=1.0-exp(-sampleData.x*stride);
            float h=clamp(sampleData.y,0.0,1.0);
            float sunlight=shadows&&!upper?cloudSunTransmission(point):mix(0.3,1.0,h);
            float overburden=layeredCloudSample(point+vec3(0.0,thickness*0.22,0.0),false,upper).x;
            float ambientSky=exp(-overburden*thickness*0.85);
            float ambient=mix(0.48,1.0,h)*mix(0.62,1.2,ambientSky);
            float powder=1.0-exp(-sampleData.x*35.0);
            vec3 daylight=vec3(0.32,0.37,0.45)*ambient;
            daylight+=sunlightColour()*sunlight*(0.30+phase*0.055*SUN_VISIBILITY);
            daylight+=vec3(0.12,0.135,0.16)*powder*(0.4+0.6*h);
            daylight*=mix(1.0,0.72+0.28*sunlight,CLOUD_RELIEF);
            daylight+=sunlightColour()*phase*SKY_LEAK*0.055*sunlight;
            vec3 colour=mix(vec3(0.006,0.010,0.019)*ambient,daylight,solarDaylight());
            colour*=1.0-0.17*rainStrength;
            scattered+=transmission*opacity*colour;transmission*=1.0-opacity;
            if(transmission<0.012)break;
        }
        start=end;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,(1.0-transmission)*(1.0-smoothstep(3500.0,7000.0,begin)));
#endif
}
vec4 marchCloudLayer(vec3 origin,vec3 ray,float limit,int steps,bool shadows){
    vec4 low=marchSingleCloud(origin,ray,limit,steps,shadows,false);
    vec4 high=marchSingleCloud(origin,ray,limit,max(4,steps/2),false,true);
    return ray.y<0.0?overLayers(high,low):overLayers(low,high);
}
vec4 physicalCloudLayer(vec3 origin,vec3 ray,float limit){return marchCloudLayer(origin,ray,limit,32+CLOUD_LAYERS*40,true);}
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

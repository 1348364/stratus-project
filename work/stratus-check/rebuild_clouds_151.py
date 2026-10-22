from pathlib import Path
p=Path('outputs/Stratus/shaders/core/ceiling.glsl');s=p.read_text()
a=s.index('vec2 layeredCloudSample(');b=s.index('vec2 cloudVolumeSample',a)
s=s[:a]+'''// Vanilla-like connected islands, with softened grid corners. The layout and
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
    float layout=cloudIslandField(islandPoint);
    float threshold=mix(0.90,0.20,clamp(amount,0.0,1.0));
    float island=smoothstep(threshold-0.03,threshold+0.16,layout);
    if(island<0.001)return vec2(0.0);
    float h=(worldPoint.y-altitude)/max(thickness,1.0)+0.5;
    h-=(weather-0.5)*CLOUD_DISTORTION*0.15;
    float envelope=smoothstep(0.0,0.17,h)*(1.0-smoothstep(0.64,1.04,h));
    if(envelope<=0.0)return vec2(0.0);
    vec3 point=vec3(xz.x*0.88,(worldPoint.y-altitude)/max(thickness,1.0)*0.8,xz.y*0.88);
    if(upper){point.x*=0.23;point.z*=2.4;point.x+=sin(point.z*11.0)*0.024;}
    vec4 volume=weatherVolume(point);
    float shape=upper?volume.b:mix(volume.g,volume.r,0.32);
    float cap=pow(abs(h-0.45)*1.70,2.0);
    float bulk=smoothstep(0.22,0.54,shape+island*0.25-cap*0.45);
    if(detailed){
        vec4 detail=weatherVolume(point*3.17+vec3(0.19,0.53,0.31));
        float pores=pow(max(0.0,1.0-detail.g),1.25)*CLOUD_DETAIL;
        bulk=max(0.0,bulk-pores*(0.18+0.20*(1.0-bulk)));
        bulk*=mix(1.0,0.65+detail.b*0.6,clamp(CLOUD_DETAIL,0.0,1.0));
    }
    return vec2(island*envelope*bulk*CLOUD_DENSITY*(upper?0.016:0.040),h);
}
'''+s[b:]
a=s.index('vec4 marchSingleCloud(');b=s.index('vec4 marchCloudLayer(',a)
s=s[:a]+'''vec4 marchSingleCloud(vec3 origin,vec3 worldRay,float distanceLimit,int steps,bool shadows,bool upper){
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
    if(finish<=begin)return vec4(0.0);
    // Integrate cells on fixed world planes. Moving up/down no longer changes
    // an eye-distance-dependent quadratic sampling grid through the same cloud.
    int axis=abs(ray.y)>0.02?1:(abs(ray.x)>abs(ray.z)?0:2);
    float cell=axis==1?thickness/max(float(steps)*0.66,8.0):max(2.0,thickness*0.055);
    float signRay=ray[axis]>0.0?1.0:-1.0;
    float startCoordinate=(origin[axis]+ray[axis]*begin)/cell;
    float boundary=(floor(startCoordinate)+(signRay>0.0?1.0:0.0))*cell;
    float next=max(begin+0.001,(boundary-origin[axis])/ray[axis]);
    float advance=cell/max(abs(ray[axis]),0.0001),start=begin;
    float transmission=1.0;vec3 scattered=vec3(0.0);
    float phase=cloudPhase(dot(ray,broadLightDirection()));
    for(int i=0;i<512;i++){
        if(i>=steps||start>=finish)break;
        float end=min(next,finish),stride=max(end-start,0.0);
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
        start=end;next+=advance;
    }
    vec3 colour=scattered/max(1.0-transmission,0.0001);
    colour=mix(colour,atmosphericColour(),1.0-exp(-max(begin-150.0,0.0)*0.00025));
    return vec4(colour,1.0-transmission);
#endif
}
'''+s[b:]
s=s.replace('20+CLOUD_LAYERS*16,true','32+CLOUD_LAYERS*40,true')
p.write_text(s)
p=Path('outputs/Stratus/shaders/core/options.glsl');s=p.read_text().replace('#define CLOUD_AMOUNT 0.90','#define CLOUD_AMOUNT 0.68').replace('0.60 0.75 0.90','0.60 0.68 0.75 0.90');p.write_text(s)
print('Rebuilt original cloud islands, porous3D shape and world-plane integration; default coverage0.68.')

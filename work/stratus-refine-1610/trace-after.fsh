#version 330 core
#define DIMENSION_TYPE 0
#ifndef STRATUS_OPTIONS_INCLUDED
#define STRATUS_OPTIONS_INCLUDED
// Balanced defaults retain physical water optics; High restores the finest sampling.
#define SKY_AMBIENT 1.40 // [0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00 2.50 3.00 4.00]
#define EXPOSURE 0.20 // [-3.00 -2.00 -1.50 -1.00 -0.50 0.00 0.20 0.50 0.75 1.00 1.50 2.00 3.00]
const float ambientOcclusionLevel = 1.00; // [0.00 0.15 0.30 0.45 0.60 0.80 1.00]
#define WHITE_BALANCE 0.00 // [-0.24 -0.16 -0.08 -0.04 0.00 0.04 0.08 0.16 0.24]
#define SURFACE_SATURATION 1.00 // [0.00 0.25 0.50 0.75 0.85 0.93 1.00 1.07 1.15 1.30 1.50 1.75 2.00]
#define SURFACE_DAMPNESS 1.00 // [0.00 0.15 0.35 0.65 1.00 1.35 1.70 2.00 2.50 3.00]
#define CLOUD_AMOUNT 0.68 // [0.00 0.35 0.60 0.68 0.75 0.90 1.00]
#define CLOUD_ALTITUDE 256.0 // [64.0 96.0 128.0 160.0 192.0 224.0 256.0 320.0 384.0 512.0 640.0 768.0]
#define CLOUD_THICKNESS 12.0 // [4.0 12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
#define SKY_LEAK 0.35 // [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
#define CLOUD_SPAN 240.0 // [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
#define CLOUD_DISTORTION 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
#define CLOUD_RELIEF 0.75 // [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
#define CLOUD_LAYERS 1 // [1 2 3]
#define MIST_AMOUNT 0.85 // [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
#define MIST_Y 70.0 // [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
#define MIST_THICKNESS 18.0 // [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
#define MIST_CLEAR 24.0 // [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 2 // [1 2 3]
#define REFLECT_LEVEL 1.00 // [0.00 0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 2 // [0 1 2]
#define REFLECT_RANGE 120.0 // [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
#define WATER_VISIBILITY 1.70 // [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
#define WATER_EXTINCTION 3.00 // [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
#define RIPPLE_HEIGHT 0.80 // [0.00 0.15 0.30 0.55 0.80 1.00 1.30 1.70 2.20 3.00]
#define RIPPLE_SIZE 1.00 // [0.25 0.40 0.65 0.80 1.00 1.25 1.50 2.00 3.00 4.00]
#define RIPPLE_RATE 0.45 // [0.00 0.10 0.20 0.45 0.70 1.00 1.50 2.00 3.00]
#define FACE_SHADING 1.00 // [0.00 0.15 0.25 0.35 0.50 0.70 0.85 1.00 1.25 1.50 2.00]
#define WET_DARKENING 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00 2.50]
#define WET_SHEEN 0.85 // [0.00 0.15 0.35 0.65 0.85 1.00 1.35 1.70 2.00]
#define BLOOM_STRENGTH 0.18 // [0.00 0.03 0.06 0.12 0.18 0.25 0.35 0.50 0.75 1.00]
#define BLOOM_RADIUS 3.00 // [0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00 8.00 12.00]
#define SUN_VISIBILITY 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.50 2.00 3.00]
#define LAMP_LEVEL 1.00 // [0.20 0.40 0.70 0.85 1.00 1.15 1.30 1.60 2.00 3.00]
#define LAMP_HEAT 0.25 // [0.00 0.15 0.25 0.40 0.60 0.80 1.00 1.50]
// Independent component multipliers. Both 1 reproduce the legacy 65/35 mix.
#define VANILLA_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_LIGHTING 0 // [0 1]
#define WET_WEATHER_MODE 0 // [0 1]
#define SUN_CORE_BRIGHTNESS 4.50 // [0.50 1.00 1.50 2.00 2.80 3.50 4.50 6.00 8.00]
#define SUN_HALO_STRENGTH 2.00 // [0.00 0.15 0.35 0.65 0.85 1.00 1.20 1.50 2.00 3.00]
#define SUN_HALO_RADIUS 1.50 // [0.35 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define CIRRUS_DENSITY 1.00 // [0.00 0.25 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define FACE_BLEND 1.00 // [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 0.00 // [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
#define WATER_DISTORTION 1.00 // [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
#define CIRRUS_AMOUNT 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 360.0 // [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
#define CLOUD_STYLE 0 // [0 1 2]
#define SUN_STYLE 0 // [0 1]
#define WATER_TURBIDITY 6.00 // [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
#define BIOME_WATER 1 // [0 1]
#define REFRACTION_QUALITY 0 // [0 1 2]
#define ATMOSPHERE_QUALITY 1 // [0 1 2]
#define WATER_RENDER_QUALITY 2 // [0 1 2]
#define CLOUD_DENSITY 1.00 // [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
#define CLOUD_DETAIL 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
#define MIST_SCALE 96.0 // [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
#define MIST_BREAKUP 0.85 // [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
#define MIST_LIGHT 0.65 // [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
// Reuse the active animated water atlas pattern without changing opacity.
#define WATER_TEXTURE 0.15 // [0.00 0.05 0.10 0.15 0.25 0.35 0.50 0.75 1.00]
#endif
#ifndef STRATUS_FRAME_INCLUDED
#define STRATUS_FRAME_INCLUDED
uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferProjection;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferModelView;
uniform vec3 cameraPosition;
uniform vec3 sunPosition;
uniform float frameTimeCounter;
uniform int worldTime;
uniform vec3 biomeWaterTint;
uniform float biomeSilt;
uniform float biomeHumidity;
uniform float biomeWarmth;
uniform ivec2 eyeBrightnessSmooth;
uniform float rainStrength;
uniform float viewWidth;
uniform float viewHeight;
uniform float far;
uniform vec3 fogColor;
uniform float fogStart;
uniform float fogEnd;
uniform float fogDensity;
uniform int fogMode;
uniform int fogShape;
uniform int isEyeInWater;
uniform float blindness;
uniform float darknessFactor;

vec3 unitVector(vec3 inputVector) {
    return inputVector * inversesqrt(max(dot(inputVector, inputVector), 1e-12));
}
vec3 decodeDisplay(vec3 displayValue) {
    vec3 lo = displayValue / 12.92;
    vec3 hi = pow(max((displayValue + 0.055) / 1.055, vec3(0.0)), vec3(2.4));
    return mix(hi, lo, lessThanEqual(displayValue, vec3(0.04045)));
}
vec3 encodeDisplay(vec3 linearValue) {
    linearValue = max(linearValue, vec3(0.0));
    vec3 lo = linearValue * 12.92;
    vec3 hi = 1.055 * pow(linearValue, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, lessThanEqual(linearValue, vec3(0.0031308)));
}
float daytimeWeight() {
    float hour = mod(float(worldTime) + 24000.0, 24000.0);
    float dawn = smoothstep(22500.0, 23999.0, hour) + 1.0 - smoothstep(12000.0, 13700.0, hour);
    return clamp(dawn, 0.0, 1.0);
}
vec3 positionFromDepth(vec2 screen, float deviceDepth) {
    vec4 unprojected = gbufferProjectionInverse * vec4(screen * 2.0 - 1.0, deviceDepth * 2.0 - 1.0, 1.0);
    return unprojected.xyz / max(unprojected.w, 1e-7);
}
vec3 playerFromView(vec3 viewPoint) {
    return (gbufferModelViewInverse * vec4(viewPoint, 1.0)).xyz;
}
vec3 broadLightDirection() {
    vec3 direction = mat3(gbufferModelViewInverse) * sunPosition;
    if (dot(direction, direction) < 0.001) direction = vec3(-0.35, 0.85, 0.40);
    return unitVector(direction);
}
vec3 sunlightColour() {
    float height = max(broadLightDirection().y, 0.0);
    return mix(vec3(1.0, 0.53, 0.25), vec3(1.0, 0.84, 0.61), smoothstep(0.02, 0.65, height));
}
vec2 viewportSize() { return max(vec2(viewWidth, viewHeight), vec2(1.0)); }
#endif
uniform sampler2D depthtex1,colortex4;
#ifndef STRATUS_SCENE_TRACE_INCLUDED
#define STRATUS_SCENE_TRACE_INCLUDED
// Original surface reconstruction: contiguous projected pixels, actual receiver
// planes, and explicit water/air half-space checks shared by both optical rays.
uniform sampler2D colortex10;
ivec2 opticsSize(bool unused){return textureSize(depthtex1,0);}
vec3 opticsRadiance(ivec2 cell,bool unused){return texelFetch(colortex4,cell,0).rgb;}

bool opticsProjection(vec3 p,out vec2 uv,bool cache){
    vec4 q=gbufferProjection*vec4(p,1.0);uv=q.xy/max(q.w,0.00001)*0.5+0.5;
    return q.w>0.0&&min(uv.x,uv.y)>0.001&&max(uv.x,uv.y)<0.999;
}
vec3 opticsReceiver(ivec2 cell,out vec4 normal,bool cache){
    ivec2 size=opticsSize(cache);cell=clamp(cell,ivec2(0),size-ivec2(1));
    vec2 uv=(vec2(cell)+0.5)/vec2(size);
    normal=texelFetch(colortex10,cell,0);
    float d=texelFetch(depthtex1,cell,0).r;
    if(d>=0.999999)normal.a=0.0;
    return positionFromDepth(uv,d);
}
vec3 opticsColour(vec2 uv,vec3 planePoint,vec3 planeNormal,bool cache){
    ivec2 size=opticsSize(cache);
    vec2 grid=uv*vec2(size)-0.5;ivec2 cell=ivec2(floor(grid));vec2 f=fract(grid);
    vec3 sum=vec3(0.0);float total=0.0;
    for(int y=0;y<2;y++)for(int x=0;x<2;x++){
        ivec2 c=clamp(cell+ivec2(x,y),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(c,data,cache);
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float weight=(x==0?1.0-f.x:f.x)*(y==0?1.0-f.y:f.y);
        if(data.a<0.5||dot(n,planeNormal)<0.95||abs(dot(receiver-planePoint,planeNormal))>0.02+length(receiver)*0.0004)continue;
        sum+=opticsRadiance(c,cache)*weight;total+=weight;
    }
    ivec2 centre=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
    return total>0.001?sum/total:opticsRadiance(centre,cache);
}
float opticsBorderCoverage(vec2 uv,ivec2 size){
    vec2 border=min(uv,1.0-uv)*vec2(size);
    return smoothstep(1.0,8.0,min(border.x,border.y));
}
float opticsHitPixelTolerance(vec2 projectedPixels,int count,float requestedStride){
    // A capped ray spans more than requestedStride pixels per iteration. Its
    // validated plane hit may lie anywhere inside that larger segment.
    return max(requestedStride,max(projectedPixels.x,projectedPixels.y)/float(count))+1.0;
}
// Bound expensive pixel traversal by a receiver plane that has already been
// validated at the projected intersection. This preserves the depth search in
// front of it, but avoids marching empty space all the way to the far plane.
float opticsPlaneBound(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,bool cache,float minimum,float maximum,out vec2 boundUV,out vec3 boundPoint,out vec3 boundNormal){
    float sampleT=minimum+0.025;boundUV=vec2(0);boundPoint=vec3(0);boundNormal=vec3(0);
    for(int iteration=0;iteration<4;iteration++){
        vec2 uv;if(!opticsProjection(origin+direction*sampleT,uv,cache))break;
        ivec2 size=opticsSize(cache),cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);if(data.a<0.5)break;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);float denominator=dot(direction,n);
        if(abs(denominator)<0.00001)break;
        float distance=dot(receiver-origin,n)/denominator;
        if(distance<=minimum||distance>maximum)break;
        vec3 candidate=origin+direction*distance;vec2 hitUV;if(!opticsProjection(candidate,hitUV,cache))break;
        vec4 hitData;vec3 actual=opticsReceiver(clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1)),hitData,cache);
        vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
        bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
        if(samePlane&&float(side)*dot(actual-origin,interfaceNormal)>0.005){boundUV=hitUV;boundPoint=candidate;boundNormal=n;return distance;}
        sampleT=distance;
    }
    return maximum;
}
vec4 traceOpticalSegment(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool cache,float minimum,out float path){
    path=0.0;
    if(!cache&&direction.z>0.00001)maximum=min(maximum,max(0.0,(-0.10-origin.z)/direction.z));
    if(maximum<0.03)return vec4(0.0);
    vec2 boundUV;vec3 boundPoint,boundNormal;
    float previousMaximum=maximum;
    maximum=opticsPlaneBound(origin,direction,interfaceNormal,side,cache,max(minimum,0.025),maximum,boundUV,boundPoint,boundNormal);
    bool bounded=maximum<previousMaximum;
    vec3 start=origin+direction*max(minimum,0.025),end=origin+direction*maximum;
    vec4 a=gbufferProjection*vec4(start,1.0),b=gbufferProjection*vec4(end,1.0);
    float ka=1.0/max(a.w,0.00001),kb=1.0/max(b.w,0.00001);
    float projectionScale=1.0;
    vec2 pa=a.xy*ka/projectionScale*0.5+0.5,pb=b.xy*kb/projectionScale*0.5+0.5;
    vec3 qa=start*ka,qb=end*kb;vec2 delta=pb-pa;
    float visible=1.0;
    for(int axis=0;axis<2;axis++){
        if(delta[axis]>0.00001)visible=min(visible,(0.999-pa[axis])/delta[axis]);
        else if(delta[axis]<-0.00001)visible=min(visible,(0.001-pa[axis])/delta[axis]);
    }
    visible=clamp(visible,0.0,1.0);pb=mix(pa,pb,visible);qb=mix(qa,qb,visible);kb=mix(ka,kb,visible);
    ivec2 size=opticsSize(cache);vec2 pixels=abs((pb-pa)*vec2(size));
    float stride=quality==2?1.0:(quality==1?2.0:4.0);
    // Short rays traverse contiguous pixels; all profiles bound long rays.
    float budget=quality==2?192.0:(quality==1?48.0:24.0);
    int count=int(clamp(ceil(max(pixels.x,pixels.y)/stride),1.0,budget));
    float hitPixelTolerance=opticsHitPixelTolerance(pixels,count,stride);
    // Projected points remain on this unit ray. Hoist the invariant dot
    // products and reuse each interval end as the next interval start.
    float qaAlong=dot(qa,direction),qbAlong=dot(qb,direction);
    float originAlong=dot(origin,direction);
    float previousT=qaAlong/ka-originAlong;
    for(int i=0;i<192;i++){
        if(i>=count)break;
        float f0=float(i)/float(count),f1=float(i+1)/float(count),f=(f0+f1)*0.5;
        vec2 uv=mix(pa,pb,f);
        if(min(uv.x,uv.y)<0.001||max(uv.x,uv.y)>0.999)break;
        float t0=previousT;
        float t1=mix(qaAlong,qbAlong,f1)/mix(ka,kb,f1)-originAlong;
        previousT=t1;
        float pointZ=mix(qa.z,qb.z,f)/mix(ka,kb,f);
        ivec2 cell=clamp(ivec2(uv*vec2(size)),ivec2(0),size-ivec2(1));
        vec4 data;vec3 receiver=opticsReceiver(cell,data,cache);
        if(data.a<0.5)continue;
        vec3 n=unitVector(mat3(gbufferModelView)*data.xyz);
        float denominator=dot(direction,n);
        float distance=abs(denominator)>0.00001?dot(receiver-origin,n)/denominator:-1.0;
        float footprint=max(0.012,length(receiver)/(float(size.y)*max(gbufferProjection[1][1],0.1)));
        if(distance>=max(0.025,t0-footprint)&&distance<=min(maximum,t1+footprint)){
            vec3 candidate=origin+direction*distance;vec2 hitUV;
            if(opticsProjection(candidate,hitUV,cache)){
                ivec2 hitCell=clamp(ivec2(hitUV*vec2(size)),ivec2(0),size-ivec2(1));
                vec4 hitData;vec3 actual=opticsReceiver(hitCell,hitData,cache);
                vec3 hitNormal=unitVector(mat3(gbufferModelView)*hitData.xyz);
                bool samePlane=hitData.a>0.5&&dot(hitNormal,n)>0.95&&abs(dot(actual-candidate,n))<0.018+length(actual)*0.0004;
                bool correctMedium=float(side)*dot(actual-origin,interfaceNormal)>0.005;
                if(samePlane&&correctMedium&&max(abs(hitUV.x-uv.x)*float(size.x),abs(hitUV.y-uv.y)*float(size.y))<hitPixelTolerance){
                    float coverage=opticsBorderCoverage(hitUV,size);
                    path=distance;
                    return vec4(opticsColour(hitUV,candidate,n,cache),coverage);
                }
            }
        }
        // A foreground occluder ends the search. Never continue through a
        // rejected shore edge and steal a farther river-floor pixel.
        float occlusion=receiver.z-pointZ;
        if(!cache&&occlusion>max(0.08,footprint*3.0))return vec4(0.0);
    }
    if(bounded){path=maximum;return vec4(opticsColour(boundUV,boundPoint,boundNormal,cache),opticsBorderCoverage(boundUV,size));}
    return vec4(0.0);
}
vec4 traceOpticalScene(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool unused,out float path){
    return traceOpticalSegment(origin,direction,interfaceNormal,side,quality,maximum,false,0.025,path);
}
#endif

in vec2 rasterUV;uniform int probeMode,probeQuality;layout(location=0)out vec4 result;
void main(){
 if(probeMode==0){vec4 n;vec3 p=opticsReceiver(ivec2(gl_FragCoord.xy),n,false);result=vec4(p,n.a);}
 else{float path;vec3 direction=unitVector(vec3((rasterUV.x-.5)*1.4,(rasterUV.y-.5)*.8,-1));vec4 h=traceOpticalScene(vec3(0,0,-2),direction,vec3(0,0,-1),1,probeQuality,120,false,path);result=vec4(h.rgb,h.a>0?path:0);}
}

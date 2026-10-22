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
#define CLOUD_THICKNESS 96.0 // [12.0 20.0 32.0 40.0 56.0 72.0 96.0 128.0 160.0 200.0]
#define SKY_LEAK 0.35 // [0.00 0.10 0.15 0.25 0.35 0.50 0.70 1.00 1.40 2.00]
#define CLOUD_SPAN 240.0 // [64.0 96.0 160.0 240.0 360.0 540.0 700.0 900.0 1200.0 1800.0]
#define CLOUD_DISTORTION 0.85 // [0.00 0.25 0.45 0.65 0.85 1.00 1.25 1.50 2.00]
#define CLOUD_RELIEF 0.75 // [0.00 0.25 0.40 0.55 0.75 1.00 1.25 1.50]
#define CLOUD_DRIFT 0.25 // [0.00 0.10 0.25 0.45 0.70 1.00 1.50 2.00 3.00]
#define CLOUD_LAYERS 3 // [1 2 3]
#define MIST_AMOUNT 0.85 // [0.00 0.15 0.30 0.40 0.60 0.75 0.85 1.00 1.25 1.50 2.00 3.00]
#define MIST_Y 70.0 // [-32.0 0.0 32.0 48.0 64.0 70.0 88.0 112.0 144.0 192.0 256.0 320.0]
#define MIST_THICKNESS 18.0 // [4.0 7.0 9.0 12.0 18.0 24.0 32.0 48.0 64.0]
#define MIST_CLEAR 24.0 // [0.0 4.0 8.0 16.0 24.0 32.0 48.0 64.0 80.0 112.0 144.0]
#define MIST_DETAIL 3 // [1 2 3]
#define REFLECT_LEVEL 1.00 // [0.00 0.40 0.60 0.85 1.00]
#define REFLECTION_MODE 1 // [0 1 2]
#define REFLECT_RANGE 120.0 // [24.0 48.0 64.0 88.0 120.0 160.0 224.0 320.0]
#define WATER_VISIBILITY 1.70 // [0.05 0.10 0.20 0.35 0.50 0.70 0.90 1.10 1.30 1.70 2.20 3.00 4.00 6.00 8.00 12.00 16.00]
#define WATER_EXTINCTION 0.90 // [0.10 0.20 0.45 0.65 0.90 1.15 1.40 2.00 3.00]
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
#define FACE_BLEND 1.00 // [0.00 0.25 0.50 0.75 1.00]
#define GROUND_WARMTH 0.45 // [0.00 0.20 0.45 0.65 0.85 1.00 1.35 1.70 2.00]
#define WATER_DISTORTION 1.00 // [0.00 0.20 0.35 0.55 0.75 1.00 1.20 1.35 1.60 2.00]
#define CIRRUS_AMOUNT 0.65 // [0.00 0.35 0.65 0.85 1.00]
#define CIRRUS_ALTITUDE 360.0 // [200.0 240.0 280.0 320.0 360.0 400.0 460.0 560.0 700.0 900.0 1200.0]
#define CLOUD_STYLE 0 // [0 1 2]
#define SUN_STYLE 0 // [0 1]
#define WATER_TURBIDITY 1.00 // [0.00 0.25 0.50 1.00 1.50 2.00 3.00 4.00 6.00]
#define BIOME_WATER 1 // [0 1]
#define REFRACTION_QUALITY 0 // [0 1 2]
#define ATMOSPHERE_QUALITY 1 // [0 1 2]
#define WATER_RENDER_QUALITY 1 // [0 1 2]
#define CLOUD_DENSITY 1.00 // [0.15 0.30 0.50 0.75 1.00 1.30 1.70 2.20 3.00]
#define CLOUD_DETAIL 1.00 // [0.00 0.25 0.50 0.75 1.00 1.30 1.70 2.00]
#define MIST_SCALE 96.0 // [24.0 40.0 64.0 96.0 144.0 224.0 320.0 480.0]
#define MIST_BREAKUP 0.85 // [0.00 0.25 0.50 0.85 1.00 1.30 1.70 2.00]
#define MIST_LIGHT 0.65 // [0.00 0.20 0.40 0.65 0.85 1.00 1.50 2.00]
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

vec3 atmosphericColour(){return vec3(.5);}
float solarDaylight(){return 1.;}
float cloudPhase(float c){return 1.;}
float cloudSunTransmission(vec3 p){return 1.;}
vec2 layeredCloudSample(vec3 p,bool detailed,bool upper){
 float h=(p.y-256.)/18.;
 return vec2(.0004*exp(-h*h)*(1.+.6*sin(p.z*.025)),.5);
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
    if(finish<=begin)return vec4(0.0);
    // Integrate cells on fixed world planes. Moving up/down no longer changes
    // an eye-distance-dependent quadratic sampling grid through the same cloud.
    int axis=abs(ray.y)>max(abs(ray.x),abs(ray.z))?1:(abs(ray.x)>abs(ray.z)?0:2);
    float projectedLength=(finish-begin)*abs(ray[axis]);
    float cell=max(thickness/max(float(steps)*0.55,8.0),exp2(ceil(log2(max(projectedLength/max(float(steps-2),1.0),0.5)))));
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
    return vec4(colour,(1.0-transmission)*(1.0-smoothstep(3500.0,7000.0,begin)));
#endif
}

uniform float probeAngle;uniform int probeSteps;layout(location=0)out vec4 result;void main(){result=marchSingleCloud(vec3(4096,257.62,4096),vec3(0,sin(probeAngle),cos(probeAngle)),7000.,probeSteps,false,false);}

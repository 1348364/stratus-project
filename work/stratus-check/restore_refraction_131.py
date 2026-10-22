from pathlib import Path
import re,shutil
r=Path('outputs/Stratus/shaders');c=r/'core'
backup=Path('work/stratus-check/pre-131-water-rollback')
if not backup.exists():shutil.copytree(r,backup)
p=c/'lake.frag.glsl';s=p.read_text();a=s.index('#if DIMENSION_TYPE == 0\n        if(isEyeInWater==1)');b=s.index('        if(isEyeInWater==0)fallback',a);s=s[:a]+s[b:]
a=s.index('        vec3 incident=unitVector(waterView);');b=s.index('        if(isEyeInWater==0){',a)
s=s[:a]+'''        // v1.3.1 screen-space water refraction, with the original shoreline guard.
        vec2 shifted=legacyWaterRefractionUV(rasterUV,nView,faceView,thickness,markedDepth.x);
        float shiftedDepth=texture(depthtex1,shifted).r;
        vec3 transmitted=texture(colortex4,shifted).rgb;
        vec3 backRay=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(shifted,0.5));
        if(shiftedDepth>=0.999999)transmitted=reflectedEnvironment(backRay);
        // Rare elevated-water view: integrate only the cloud segment behind it.
        // Ordinary ground-level water does not march clouds per surface pixel.
        if((cameraPosition+point).y>CLOUD_ALTITUDE-CLOUD_THICKNESS&&backRay.y<0.0){
            vec4 behind=marchCloudLayer(cameraPosition+point+backRay*0.05,backRay,max(thickness,0.0),6,false);
            transmitted=mix(transmitted,behind.rgb,behind.a);
        }
        float opticalPath=thickness;
        float cosine=clamp(dot(nView,unitVector(-waterView)),0.0,1.0);
        float fresnel=dielectricWaterFresnel(cosine,isEyeInWater==1?1.333:1.0,isEyeInWater==1?1.0:1.333);
        bool totalReflection=isEyeInWater==1&&fresnel>=0.99999;
        vec3 refracted=unitVector(waterView);
'''+s[b:]
p.write_text(s)
# Preserve exactly the v1.3.1 offset formula and default single depth guard.
(c/'refraction.glsl').write_text('''#ifndef STRATUS_REFRACTION_INCLUDED
#define STRATUS_REFRACTION_INCLUDED
// Restored from Stratus v1.3.1: inexpensive normal-offset transmission.
// This is a screen-space approximation, not a Snell geometry ray tracer.
vec2 legacyWaterRefractionUV(vec2 uv,vec3 nView,vec3 faceView,float thickness,float surfaceDepth){
    vec2 distortion=(nView.xy-faceView.xy)*WATER_DISTORTION*0.15*clamp(thickness*0.3,0.25,1.0);
    vec2 shifted=clamp(uv+distortion,vec2(0.001),vec2(0.999));
    float shiftedDepth=texture(depthtex1,shifted).r;
    if(shiftedDepth<0.999999&&-positionFromDepth(shifted,shiftedDepth).z<surfaceDepth+0.03)return uv;
#if REFRACTION_QUALITY > 0
    // Optional extra edge protection; mode zero is the original v1.3.1 guard.
    int checks=REFRACTION_QUALITY==2?4:2;
    for(int i=1;i<=checks;i++){
        vec2 edge=mix(uv,shifted,float(i)/float(checks));float d=texture(depthtex1,edge).r;
        if(d<0.999999&&-positionFromDepth(edge,d).z<surfaceDepth+0.03)return uv;
    }
#endif
    return shifted;
}
#endif
''')
# Keep current validated receiver-plane screen reflections, remove all offscreen cache work.
p=c/'scene-trace.glsl';s=p.read_text();a=s.index('#include "/core/optics-cube.glsl"');b=s.index('bool opticsProjection',a)
s=s[:a]+'''uniform sampler2D colortex10;
ivec2 opticsSize(bool unused){return textureSize(depthtex1,0);}
vec3 opticsRadiance(ivec2 cell,bool unused){return texelFetch(colortex4,cell,0).rgb;}

'''+s[b:]
a=s.index('    if(cache){');b=s.index('    vec4 q=gbufferProjection',a);s=s[:a]+s[b:]
a=s.index('    normal=cache?');b=s.index('    float d=texelFetch(depthtex1',a);s=s[:a]+'    normal=texelFetch(colortex10,cell,0);\n'+s[b:]
a=s.index('    if(cache){',s.index('vec4 traceOpticalSegment'));b=s.index('    float ka=',a);s=s[:a]+s[b:]
s=s.replace('                    if(cache)coverage=1.0;','').replace('float occlusion=cache?dot(mat3(gbufferModelViewInverse)*(point-receiver),cubeForward(opticsFace)):receiver.z-point.z;','float occlusion=receiver.z-point.z;').replace('float budget=quality==2?2048.0:(quality==1?128.0:64.0);','float budget=quality==2?192.0:(quality==1?48.0:24.0);')
a=s.index('// Continuous local environment');s=s[:a]+'''vec4 traceOpticalScene(vec3 origin,vec3 direction,vec3 interfaceNormal,int side,int quality,float maximum,bool unused,out float path){
    return traceOpticalSegment(origin,direction,interfaceNormal,side,quality,maximum,false,0.025,path);
}
#endif
''';p.write_text(s)
p=c/'trace.glsl';s=p.read_text();a=s.index('#if DIMENSION_TYPE == 0\n    vec4 cached');b=s.index('    return traceOpticalScene',a);s=s[:a]+s[b:];p.write_text(s)
# Delete the unreleased extra views entirely, so Iris never renders a shadow cache.
for folder in [r,r/'world-1',r/'world1']:
 for ext in ['vsh','fsh','gsh']:(folder/('shadow.'+ext)).unlink()
for name in ['optics-cache.vert.glsl','optics-cache.frag.glsl','optics-cache.geom.glsl','optics-cube.glsl']:(c/name).unlink()
p=c/'options.glsl';s=p.read_text();s=re.sub(r'^#define OPTICS_CACHE_(?:QUALITY|DISTANCE).*\n','',s,flags=re.M).replace('#define REFRACTION_QUALITY 1','#define REFRACTION_QUALITY 0');p.write_text(s)
p=r/'shaders.properties';s=p.read_text();s=re.sub(r' OPTICS_CACHE_(?:QUALITY|DISTANCE)(?::\d+)?','',s);s=s.replace('screen.PERFORMANCE=OPTICS_CACHE_DISTANCE ','screen.PERFORMANCE=');a=s.index('# Independent wide-view geometry');b=s.index('# Independent atmosphere target',a);s=s[:a]+'# Water refraction restored to v1.3.1; no extra geometry/shadow rendering.\nshadow.enabled=false\n\n'+s[b:]
s=s.replace('REFRACTION_QUALITY:1','REFRACTION_QUALITY:0');p.write_text(s)
p=r/'lang/en_us.lang';s=p.read_text();s='\n'.join(line for line in s.splitlines() if not re.match(r'(?:option|value)\.OPTICS_CACHE_',line))+'\n';s=re.sub(r'^option.REFRACTION_QUALITY=.*$','option.REFRACTION_QUALITY=Refraction edge protection',s,flags=re.M);s=re.sub(r'^option.REFRACTION_QUALITY.comment=.*$','option.REFRACTION_QUALITY.comment=The original v1.3.1 screen-offset refraction uses one shoreline depth check. Higher levels add conservative checks across the offset to reject foreground shoreline leaks.',s,flags=re.M)
s=re.sub(r'^value.REFRACTION_QUALITY.0=.*$','value.REFRACTION_QUALITY.0=v1.3.1 original',s,flags=re.M);p.write_text(s)
print('Restored v1.3.1 transmission; removed eight-view cache and all shadow programs.')

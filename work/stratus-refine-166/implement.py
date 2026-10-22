from pathlib import Path
p=Path('outputs/Stratus/shaders')
f=p/'core/diffuse.glsl';s=f.read_text().replace('irradiance=mix(vanilla,physical,smoothstep(0.08,0.85,skyExposure));','''// Keep vanilla's axis contrast as the dominant contribution. Realistic
    // light adds a restrained directional variation rather than replacing it.
    irradiance=mix(vanilla,physical,0.35*smoothstep(0.08,0.85,skyExposure));''');f.write_text(s)
f=p/'core/ceiling.glsl';s=f.read_text();at=s.index('vec3 skyBackdrop(')
s=s[:at]+'''// Sample the running game's current vanilla square sun (or resource-pack
// replacement). It is shared by the sky and reflection environment cache.
uniform sampler2D vanillaSun;
vec3 polishedVanillaSun(vec3 ray){
    vec3 sun=broadLightDirection();
    float forward=dot(ray,sun);
    if(forward<=0.0)return vec3(0.0);
    vec3 pole=abs(sun.z)<0.99?vec3(0.0,0.0,1.0):vec3(0.0,1.0,0.0);
    vec3 right=unitVector(cross(pole,sun)),up=cross(sun,right);
    // Vanilla's textured sky quad has half extent 30 at distance 100.
    vec2 uv=vec2(dot(ray,right),dot(ray,up))/(forward*0.60)+0.5;
    if(min(uv.x,uv.y)<0.0||max(uv.x,uv.y)>=1.0)return vec3(0.0);
    ivec2 size=textureSize(vanillaSun,0);
    vec4 texel=texelFetch(vanillaSun,ivec2(uv*vec2(size)),0);
    // Keep the pixel silhouette; HDR warmth and the existing broad haze glow
    // provide polish without adding a round solar core over the square.
    return decodeDisplay(texel.rgb)*texel.a*sunlightColour()*2.8;
}
''' + s[at:]
a=s.index('    float core=exp(');b=s.index('    return sky;',a)
s=s[:a]+'''    vec3 disc=vec3(0.0);
#if SUN_STYLE == 0
    disc=polishedVanillaSun(ray)*SUN_VISIBILITY;
#endif
    sky+=solarDaylight()*(sunlightColour()*glow+disc*(1.0-0.65*rainStrength));
''' +s[b:];f.write_text(s)
f=p/'shaders.properties';s=f.read_text().replace('customTexture.vanillaClouds=','customTexture.vanillaSun=minecraft:textures/environment/celestial/sun.png\ncustomTexture.vanillaClouds=');f.write_text(s)
# Share the full atmosphere evaluation, including border/status handling, so
# an unsampled leaf receives the same transport model as a cached opaque pixel.
f=p/'core/atmosphere.frag.glsl';s=f.read_text();a=s.index('    vec4 volume=atmosphereSegment(');b=s.index('    integratedAtmosphere=vec4(volume.rgb*volume.a,volume.a);',a)
old=s[a:b];body=old.replace('    vec4 volume=atmosphereSegment(cameraPosition,ray,limit,sky,true);','    vec4 volume=atmosphereSegment(origin,ray,limit,sky,detailed);')
f.write_text(s[:a]+'    vec4 volume=completeAtmosphereSegment(cameraPosition,ray,limit,sky,true);\n'+s[b:])
f=p/'core/volume.glsl';s=f.read_text();at=s.rindex('#endif');s=s[:at]+'''// Shared by the reduced-resolution pass and its confidence fallback. Avoids
// inconsistent border fog/blindness between tiny cutouts and larger surfaces.
vec4 completeAtmosphereSegment(vec3 origin,vec3 ray,float limit,float sky,bool detailed){
'''+body+'''    return volume;
}
'''+s[at:];f.write_text(s)
f=p/'core/atmosphere-resolve.frag.glsl';s=f.read_text().replace('#include "/core/scene-depth.glsl"','#include "/core/scene-depth.glsl"\n#include "/core/ceiling.glsl"\n#include "/core/volume.glsl"')
s=s.replace('    if(sum>0.0001)volume/=sum;else volume=vec4(0.0);','''    volume/=max(sum,0.000001);
    if(isEyeInWater==0&&sum<0.12){
        // A subpixel leaf can be absent from every reduced-resolution depth
        // sample. Returning zero here punched an unfogged dark dot in the haze.
        // Integrate only these rejected pixels at their exact full-res depth.
        // Smooth confidence blending prevents a binary fallback threshold.
        vec3 ray=unitVector(mat3(gbufferModelViewInverse)*positionFromDepth(rasterUV,0.5));
        vec4 exact=completeAtmosphereSegment(cameraPosition,ray,distanceToScene,sceneSkyExposure(rasterUV),false);
        exact=vec4(exact.rgb*exact.a,exact.a);
        volume=mix(exact,volume,smoothstep(0.02,0.12,sum));
    }''');f.write_text(s)
f=p/'lang/en_us.lang';s=f.read_text();changes={
'FACE_SHADING.comment':"Contrast of vanilla face shading with a restrained 35% realistic sky/ground/sun contribution on exposed faces. Zero disables face contrast.",
'FACE_BLEND.comment':"Blend from unshaded faces to vanilla-dominant face shading with subtle directional light. Zero bypasses it.",
'SUN_STYLE.comment':"Choose Minecraft's blocky sun with HDR warmth and soft haze, or unchanged native sun and moon textures.",
'SUN_VISIBILITY.comment':"Brightness of the polished blocky sun behind clouds. Zero hides its textured core; broad sky haze remains.",
}
import re
for key,value in changes.items():s,n=re.subn(r'^option\.'+re.escape(key)+r'=.*$',lambda m:'option.'+key+'='+value,s,flags=re.M);assert n==1
s=s.replace('value.SUN_STYLE.0=Stratus soft sun','value.SUN_STYLE.0=Polished vanilla sun');f.write_text(s)
print('Implemented vanilla-dominant diffuse blend, polished square sun and confidence-based exact-depth fog fallback.')

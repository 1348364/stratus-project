from pathlib import Path
import re,json
p=Path('outputs/Stratus/shaders');w=Path(__file__).parent
f=p/'core/options.glsl';s=f.read_text();s+='''
// Native appearance with Stratus optics, or the retained physical water model.
#define WATER_STYLE 1 // [0 1]
#define TRANSPARENT_REFLECTIONS 0.75 // [0.00 0.25 0.50 0.75 1.00 1.50 2.00]
#define TRANSPARENT_REFRACTION 0.50 // [0.00 0.25 0.50 0.75 1.00 1.50 2.00]
''';f.write_text(s)
f=p/'shaders.properties';s=f.read_text().replace('screen.WATER=WATER_VISIBILITY','screen.WATER=WATER_STYLE <empty> WATER_VISIBILITY').replace('screen.MATERIALS=WET_WEATHER_MODE SURFACE_DAMPNESS WET_SHEEN WET_DARKENING','screen.MATERIALS=WET_WEATHER_MODE SURFACE_DAMPNESS WET_SHEEN WET_DARKENING [TRANSPARENT_OPTICS]\nscreen.TRANSPARENT_OPTICS=TRANSPARENT_REFLECTIONS TRANSPARENT_REFRACTION')
s=re.sub(r'^(profile\.[^=]+=)(.*)$',lambda m:m[1]+m[2]+' WATER_STYLE:1 TRANSPARENT_REFLECTIONS:0.75 TRANSPARENT_REFRACTION:0.50',s,flags=re.M)
s+='''
# One visible transparent-solid interface, captured alongside existing geometry.
# Valid alpha1 stores the nearest sorted interface; non-optical water alpha0
# preserves it. No additional render pass.
blend.gbuffers_water.colortex15=SRC_ALPHA ONE_MINUS_SRC_ALPHA ONE ONE_MINUS_SRC_ALPHA
''';f.write_text(s)
f=p/'lang/en_us.lang';s=f.read_text()+'''
option.WATER_STYLE=Water appearance
option.WATER_STYLE.comment=Vanilla uses the active still/flow texture, biome colour, light and game underwater fog, with Stratus reflections/refraction retained. Stratus restores depth-based absorption and clarity tuning.
value.WATER_STYLE.0=Stratus
value.WATER_STYLE.1=Vanilla
screen.TRANSPARENT_OPTICS=Transparent solids
screen.TRANSPARENT_OPTICS.comment=Thin-surface optics for glass, panes, ice, honey and slime. Native colour/alpha remain; screen-space data cannot reveal hidden scenery or every overlapping layer.
option.TRANSPARENT_REFLECTIONS=Solid reflections
option.TRANSPARENT_REFLECTIONS.comment=View-dependent reflections on transparent solid faces. Uses current reflection quality and sky fallback. Zero disables them independently of wet film and water.
option.TRANSPARENT_REFRACTION=Solid refraction
option.TRANSPARENT_REFRACTION.comment=Subtle face-normal refraction on transparent solids, with depth and screen-edge guards. No animated water waves. Zero disables refraction without removing reflections.
'''
s=s.replace('Animated still/flow pattern from the active game or resource pack with biome tint across the whole visible water surface, including distant reflections. Zero restores clear optics. Preserves opacity, refraction, depth and reflection detail.','Native animated still/flow contribution across the whole visible surface. In Vanilla appearance it controls native surface colour/alpha; zero removes that layer. In Stratus appearance it controls the retained patterned biome tint. Reflection/refraction settings remain independent.')
for k in ['WATER_VISIBILITY','WATER_EXTINCTION','WATER_TURBIDITY']:
 s=re.sub(r'^(option\.'+k+r'\.comment=.*)$',r'\1 Used by Stratus water appearance; saved tuning is retained while Vanilla uses game fog.',s,flags=re.M)
f.write_text(s)
f=p/'core/diffuse.glsl';s=f.read_text().replace('if (material == 4114) return','if (material == 4114 || (material>=4120&&material<=4123)) return');s=s.replace('*mix(0.55,1.0,max(n.y,0.0));','*mix(0.78,1.0,clamp(n.y*0.5+0.5,0.0,1.0));').replace('float fresnel=0.02+0.98*pow(1.0-nv,5.0);','float fresnel=0.08+0.92*pow(1.0-nv,5.0);').replace('fresnel*0.20,0.0,0.20','fresnel*0.25,0.0,0.22').replace('mix(160.0,36.0','mix(80.0,16.0');f.write_text(s)
f=p/'block.properties';lines=f.read_text().splitlines();mapped={4120:[],4121:[],4122:[],4123:[]}
for i,l in enumerate(lines):
 if not l.startswith('block.') or '=' not in l:continue
 key,v=l.split('=',1);keep=[]
 for token in v.split():
  name=token.split(':',1)[1];group=4120 if name in ['glass','glass_pane','tinted_glass'] or 'stained_glass' in name else 4121 if name=='ice' else 4122 if name=='slime_block' else 4123 if name=='honey_block' else None
  if group:mapped[group].append(token)
  else:keep.append(token)
 lines[i]=key+'='+' '.join(keep)
for key,vals in mapped.items():
 if not vals:vals={4121:['minecraft:ice'],4122:['minecraft:slime_block'],4123:['minecraft:honey_block']}.get(key,[])
 lines.append('block.'+str(key)+'='+' '.join(vals))
f.write_text('\n'.join(lines)+'\n')
f=p/'core/medium.glsl';s=f.read_text();pos=s.index('vec3 waterExtinction(');s=s[:pos]+'''// Native underwater fog uses the running game's environmental range/colour.
// Above the interface vanilla has a surface alpha layer, not water-depth fog.
float nativeWaterOpacity(float distanceInWater){
    if(isEyeInWater!=1||distanceInWater<=0.0)return 0.0;
    return clamp((distanceInWater-fogStart)/max(fogEnd-fogStart,0.0001),0.0,1.0);
}
'''+s[pos:]
s=s.replace('vec3 waterBodyColour(vec3 tint,float skyExposure,float blockLight){','''vec3 waterBodyColour(vec3 tint,float skyExposure,float blockLight){
#if WATER_STYLE == 1
    return decodeDisplay(fogColor);
#else''').replace('    return body*lighting;\n}','    return body*lighting;\n#endif\n}')
s=s.replace('vec3 travelThroughWater(vec3 radiance,float distanceInWater,vec3 tint,float skyExposure,float blockLight){\n    vec3 transmission=exp(-waterExtinction(tint,skyExposure)*max(distanceInWater,0.0));','''vec3 waterTransmission(float distanceInWater,vec3 tint,float skyExposure){
#if WATER_STYLE == 1
    return vec3(1.0-nativeWaterOpacity(distanceInWater));
#else
    return exp(-waterExtinction(tint,skyExposure)*max(distanceInWater,0.0));
#endif
}
vec3 travelThroughWater(vec3 radiance,float distanceInWater,vec3 tint,float skyExposure,float blockLight){
    vec3 transmission=waterTransmission(distanceInWater,tint,skyExposure);''');f.write_text(s)
f=p/'core/submerged-compose.glsl';s=f.read_text().replace('exp(-waterExtinction(biomeWaterTint,sky)*foregroundPath)','waterTransmission(foregroundPath,biomeWaterTint,sky)');f.write_text(s)
f=p/'core/water-surface.glsl';s=f.read_text().replace('#endif','''// Native alpha blend in display space, matching the game's texture/light path.
vec3 nativeWaterSurface(vec3 behind,vec4 nativeLayer){
    float coverage=clamp(nativeLayer.a*WATER_TEXTURE,0.0,1.0);
    return decodeDisplay(mix(encodeDisplay(behind),encodeDisplay(nativeLayer.rgb),coverage));
}
#endif''');f.write_text(s)
f=p/'core/raster.frag.glsl';s=f.read_text().replace('/* RENDERTARGETS: 3,0,1,2,8,13,14 */','/* RENDERTARGETS: 3,0,1,2,8,13,14,15 */');s=s.replace('    if (surface.a <= 0.001) discard;','''#if PASS_KIND == 6
    bool opticalSolid=blockCategory>=4120&&blockCategory<=4123;
    // Clear glass interiors still have a reflective interface.
    if(surface.a<=0.001&&!opticalSolid)discard;
#else
    if(surface.a<=0.001)discard;
#endif''')
s=s.replace('        gl_FragData[6] = vec4(0.0);','        gl_FragData[6] = vec4(0.0);\n        gl_FragData[7] = vec4(0.0);')
s=s.replace('    float mark = 0.0;','''    vec4 nativeWater=vec4(0.0);
#if PASS_KIND == 6 && WATER_STYLE == 1
    vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
    vec3 fn=unitVector(orientedNormal);nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
    nativeWater=vec4(decodeDisplay(nativeColour),surface.a);
#endif
    float mark = 0.0;''')
s=s.replace('    if(mark>0.5)gl_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));','''    if(mark>0.5){
#if WATER_STYLE == 1
        gl_FragData[4]=nativeWater;
#else
        gl_FragData[4]=vec4(tintAndOpacity.rgb,clamp((illuminationCoordinate.s*32.0-1.0)/30.0,0.0,1.0));
#endif
    }
    vec3 opticalNormal=unitVector(mat3(gbufferModelView)*orientedNormal);
    opticalNormal/=max(abs(opticalNormal.x)+abs(opticalNormal.y)+abs(opticalNormal.z),0.00001);
    vec2 encoded=opticalNormal.xy;
    if(opticalNormal.z<0.0)encoded=(1.0-abs(encoded.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(encoded,vec2(0)));
    vec3 opticalView=(gbufferModelView*vec4(relativeLocation,1.0)).xyz;
    gl_FragData[7]=opticalSolid?vec4(encoded,-opticalView.z,1.0):vec4(0.0);''');f.write_text(s)
f=p/'core/lake.frag.glsl';s=f.read_text().replace('        waterTint=opticalData.rgb;waterLamp=opticalData.a;','''#if WATER_STYLE == 0
        waterTint=opticalData.rgb;waterLamp=opticalData.a;
#endif''').replace('        image=vanillaWaterSurface(image,markedColour.r,waterTint);','''#if WATER_STYLE == 1
        image=nativeWaterSurface(image,opticalData);
#else
        image=vanillaWaterSurface(image,markedColour.r,waterTint);
#endif''');f.write_text(s)
f=p/'core/resolve.frag.glsl';s=f.read_text().replace('const int colortex13Format = RGBA16F;','const int colortex13Format = RGBA16F;\nconst int colortex15Format = RGBA16F;\nconst vec4 colortex15ClearColor = vec4(0.0);');f.write_text(s)
(p/'core/transparent-optics.glsl').write_text('''#ifndef STRATUS_TRANSPARENT_OPTICS_INCLUDED
#define STRATUS_TRANSPARENT_OPTICS_INCLUDED
uniform sampler2D colortex15;
#include "/core/environment.glsl"
#include "/core/medium.glsl"
#include "/core/trace.glsl"
// One nearest visible thin-solid interface. No volume traversal or water waves.
vec3 transparentSolidOptics(vec3 scene,vec2 uv){
    if(TRANSPARENT_REFLECTIONS<=0.0&&TRANSPARENT_REFRACTION<=0.0)return scene;
    vec4 data=texture(colortex15,uv);
    if(data.a<0.5||data.z<=0.0)return scene;
    vec3 ray=positionFromDepth(uv,0.5),point=ray*(data.z/max(-ray.z,0.00001));
    float front=texture(depthtex0,uv).r;
    if(front<0.999999&&-positionFromDepth(uv,front).z<data.z-max(0.04,data.z*0.002))return scene;
    vec3 n=vec3(data.xy,1.0-abs(data.x)-abs(data.y));
    if(n.z<0.0)n.xy=(1.0-abs(n.yx))*mix(vec2(-1),vec2(1),greaterThanEqual(n.xy,vec2(0)));
    n=unitVector(n);vec3 incident=unitVector(point);if(dot(n,-incident)<0.0)n=-n;
    if(TRANSPARENT_REFRACTION>0.0){
        // Fixed thin-slab offset: opposite parallel faces cancel angular bending.
        // Cap displacement, reject foreground and cross-interface samples.
        vec3 through=refract(incident,n,1.0/1.5);
        vec2 shift=(through.xy/max(abs(through.z),0.2)-incident.xy/max(abs(incident.z),0.2))*0.006*TRANSPARENT_REFRACTION/max(data.z*0.04,1.0);
        shift=clamp(shift,vec2(-0.015),vec2(0.015));vec2 refracted=uv+shift;
        if(min(refracted.x,refracted.y)>0.005&&max(refracted.x,refracted.y)<0.995){
            vec4 other=texture(colortex15,refracted);float back=texture(depthtex1,refracted).r;
            bool same=other.a>0.5&&abs(other.z-data.z)<max(0.08,data.z*0.015);
            bool behind=back>=0.999999||-positionFromDepth(refracted,back).z>data.z+0.02;
            if(same&&behind)scene=texture(colortex3,refracted).rgb;
        }
    }
    if(TRANSPARENT_REFLECTIONS>0.0){
        vec3 direction=reflect(incident,n),world=mat3(gbufferModelViewInverse)*direction;
        float path;vec4 hit=sceneryReflection(point+n*0.015,direction,n,path);
        vec3 reflected=mix(reflectedEnvironment(world),hit.rgb,hit.a);
        float f=dielectricWaterFresnel(clamp(dot(n,-incident),0.0,1.0),1.0,1.5);
        scene=mix(scene,reflected,clamp(f*TRANSPARENT_REFLECTIONS,0.0,0.85));
    }
    return scene;
}
#endif
''')
f=p/'core/atmosphere-resolve.frag.glsl';s=f.read_text().replace('in vec2 rasterUV;','#include "/core/transparent-optics.glsl"\nin vec2 rasterUV;').replace('    vec3 scene=texture(colortex3,rasterUV).rgb;','    vec3 scene=transparentSolidOptics(texture(colortex3,rasterUV).rgb,rasterUV);');f.write_text(s)
(w/'reference-research.json').write_text(json.dumps({'sources':['https://sildurs-shaders.github.io/','https://sildurs-shaders.github.io/changelogs/'],'reference':'Enhanced Default, vanilla-preserving reflections and optional refraction; tinted glass, ice, honey/slime support documented. No third-party shader code copied.','implementation':'Original thin-solid screen-space optics; fixed approximate1.5IOR; no new full-screen pass; existing reflection quality controls retained.'},indent=2)+'\n')
print('Implemented candidate: all-face film, native/Stratus water modes and thin transparent-solid optics. Existing controls retained; three new controls.')

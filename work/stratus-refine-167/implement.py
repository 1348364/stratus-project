from pathlib import Path
import json,re
w=Path(__file__).parent;p=Path('outputs/Stratus/shaders');snapshot=json.loads((w/'settings-snapshot.json').read_text())
f=p/'core/options.glsl';s=f.read_text()
for k,v in snapshot['saved_overrides'].items():
 s,n=re.subn(r'^(#define\s+'+re.escape(k)+r'\s+)\S+',lambda m:m[1]+v,s,flags=re.M);assert n==1,(k,n)
s=s.replace('#define FACE_BLEND', '''// Independent component multipliers. Both 1 reproduce the legacy 65/35 mix.
#define VANILLA_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define REALISTIC_FACE_CONTRAST 1.00 // [0.00 0.15 0.25 0.35 0.50 0.65 0.85 1.00 1.25 1.50 2.00 3.00]
#define SUN_CORE_BRIGHTNESS 4.50 // [0.50 1.00 1.50 2.00 2.80 3.50 4.50 6.00 8.00]
#define SUN_HALO_STRENGTH 1.20 // [0.00 0.15 0.35 0.65 0.85 1.00 1.20 1.50 2.00 3.00]
#define SUN_HALO_RADIUS 1.00 // [0.35 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define CIRRUS_DENSITY 1.00 // [0.00 0.25 0.50 0.75 1.00 1.25 1.50 2.00 3.00]
#define FACE_BLEND''');f.write_text(s)
f=p/'core/diffuse.glsl';s=f.read_text();a=s.index('    float irradiance=vanilla;');b=s.index('    float strength=FACE_BLEND',a)
s=s[:a]+'''    float vanillaWeight=1.0,physicalWeight=0.0;
    float physical=1.0;
#if DIMENSION_TYPE == 0
    vec3 sun=broadLightDirection();
    float direct=daytimeWeight()*smoothstep(-0.04,0.16,sun.y)*(1.0-0.85*rainStrength);
    float facing=max(dot(normal,sun),0.0);
    float hemisphere=mix(0.38,0.78,normal.y*0.5+0.5);
    physical=hemisphere*(1.0-0.20*direct)+0.44*direct*facing;
    float exposure=smoothstep(0.08,0.85,skyExposure);
    vanillaWeight=1.0-0.35*exposure;physicalWeight=0.35*exposure;
#endif
    // Separate linear components preserve the exact old mixture at 1/1.
    // Each zero removes only that component; both zero produce unshaded faces.
    float contrast=(vanilla-1.0)*vanillaWeight*VANILLA_FACE_CONTRAST
                  +(physical-1.0)*physicalWeight*REALISTIC_FACE_CONTRAST;
    float irradiance=1.0+contrast;
''' +s[b:]
a=s.index('    // Matte absorption only:');b=s.index('\n}\nvec3 diffuseRadiance',a)
s=s[:a]+'''    float moisture=retainedSurfaceMoisture(sky,n,material.x);
    float saturation=moisture*(0.45+0.55*clamp(biomeHumidity,0.0,1.0));
    float attenuation=1.0/(1.0+1.40*WET_DARKENING*saturation*clamp(material.x,0.0,1.0));
    vec3 absorbed=dry*attenuation;
#if DIMENSION_TYPE == 0
    // A thin rain film on absorbent exposed material. Clear/dry and nonporous
    // surfaces keep the existing matte response; no global glossy overlay.
    float film=rainStrength*SURFACE_DAMPNESS*smoothstep(0.18,0.85,sky)
        *smoothstep(0.04,0.24,material.x)*mix(0.55,1.0,max(n.y,0.0));
    if(WET_SHEEN>0.0&&film>0.0001){
        vec3 view=unitVector(-playerPoint);
        float nv=max(dot(n,view),0.0);
        if(nv>0.001){
            float fresnel=0.02+0.98*pow(1.0-nv,5.0);
            float coat=clamp(film*WET_SHEEN*fresnel*0.55,0.0,0.45);
            vec3 environment=softSkyReflection(reflect(-view,n));
            absorbed=mix(absorbed,environment,coat);
            vec3 light=broadLightDirection(),halfway=unitVector(view+light);
            float exponent=mix(160.0,36.0,clamp(material.y,0.0,1.0));
            float lobe=pow(max(dot(n,halfway),0.0),exponent)*(exponent+2.0)/6.283185307;
            absorbed+=sunlightColour()*solarDaylight()*max(dot(n,light),0.0)
                *lobe*film*WET_SHEEN*0.035*(1.0-0.65*rainStrength);
        }
    }
#endif
    return absorbed;''' +s[b:];f.write_text(s)
f=p/'core/ceiling.glsl';s=f.read_text().replace('sunlightColour()*2.8;','sunlightColour()*SUN_CORE_BRIGHTNESS;')
s=s.replace('    disc=polishedVanillaSun(ray)*SUN_VISIBILITY;','''    disc=polishedVanillaSun(ray)*SUN_VISIBILITY;
    // Sun-local scatter with a finite angular reach and smooth inverse-square
    // falloff. It never raises bloom on blocks, entities or the rest of the sky.
    float radius2=SUN_HALO_RADIUS*SUN_HALO_RADIUS;
    float halo=1.0/pow(1.0+separation/max(0.003*radius2,0.000001),2.0);
    halo*=1.0-smoothstep(0.025*radius2,0.060*radius2,separation);
    disc+=sunlightColour()*halo*SUN_HALO_STRENGTH*SUN_VISIBILITY*0.65;''')
s=s.replace('amount*CLOUD_DENSITY*0.016','amount*CLOUD_DENSITY*CIRRUS_DENSITY*0.045')
needle='            daylight*=mix(1.0,0.72+0.28*sunlight,CLOUD_RELIEF);';assert needle in s
s=s.replace(needle,'''            if(upper)daylight=mix(daylight,vec3(0.80,0.84,0.90)+sunlightColour()*0.10,0.65);
'''+needle);f.write_text(s)
f=p/'shaders.properties';s=f.read_text().replace('FACE_SHADING FACE_BLEND GROUND_WARMTH','FACE_SHADING FACE_BLEND VANILLA_FACE_CONTRAST REALISTIC_FACE_CONTRAST GROUND_WARMTH').replace('screen.SUN=SUN_STYLE SUN_VISIBILITY SKY_LEAK','screen.SUN=SUN_STYLE SUN_VISIBILITY SUN_CORE_BRIGHTNESS SUN_HALO_STRENGTH SUN_HALO_RADIUS SKY_LEAK').replace('CIRRUS_AMOUNT CIRRUS_ALTITUDE','CIRRUS_AMOUNT CIRRUS_ALTITUDE CIRRUS_DENSITY');s=s.replace('sliders=','sliders=VANILLA_FACE_CONTRAST REALISTIC_FACE_CONTRAST SUN_CORE_BRIGHTNESS SUN_HALO_STRENGTH SUN_HALO_RADIUS CIRRUS_DENSITY ');f.write_text(s)
f=p/'lang/en_us.lang';s=f.read_text();updates={
 'FACE_SHADING':'Combined face contrast',
 'FACE_SHADING.comment':'Master strength for vanilla and realistic components. Both new component multipliers at 1 reproduce the previous combined look.',
 'FACE_BLEND.comment':'Overall blend from unshaded faces to the two independent lighting components. Zero bypasses both.',
 'WET_SHEEN':'Wet film and retention',
 'WET_SHEEN.comment':'Rain-driven view-dependent sheen on exposed absorbent materials, plus existing sheltered matte retention. Zero disables both. Clear/dry and nonporous materials do not gain a glossy coat.',
 'SUN_STYLE.comment':"Polished mode keeps Minecraft's square sun and adds independently adjustable core brightness and local halo. Vanilla mode retains native textured sun and moon.",
 'CIRRUS_AMOUNT.comment':'Coverage/strength of the independent high cloud veil. Its separate density control makes the layer visible without changing lower clouds. Zero hides the upper layer.'}
for k,v in updates.items():s,n=re.subn(r'^option\.'+re.escape(k)+r'=.*$',lambda m:'option.'+k+'='+v,s,flags=re.M);assert n==1,k
s+='''
option.VANILLA_FACE_CONTRAST=Vanilla face component
option.VANILLA_FACE_CONTRAST.comment=Independent multiplier for fixed vanilla axis contrast. 0 removes it; 1 retains the previous contribution. Existing master contrast/blend remain.
option.REALISTIC_FACE_CONTRAST=Realistic face component
option.REALISTIC_FACE_CONTRAST.comment=Independent multiplier for world-space sun, sky and ground contrast. 0 removes it; 1 retains the previous contribution. Exposure/rain/night still apply.
option.SUN_CORE_BRIGHTNESS=Polished sun brightness
option.SUN_CORE_BRIGHTNESS.comment=HDR brightness of the blocky textured core in polished mode. 2.80 reproduces the previous core; vanilla mode is unaffected.
option.SUN_HALO_STRENGTH=Sun-local halo strength
option.SUN_HALO_STRENGTH.comment=Additional light scatter around the polished sun only. 0 disables it without altering the core or global bloom.
option.SUN_HALO_RADIUS=Sun-local halo radius
option.SUN_HALO_RADIUS.comment=Angular spread of the polished sun's smoothly falling halo. Does not resize the blocky core or brighten unrelated objects.
option.CIRRUS_DENSITY=High cloud density
option.CIRRUS_DENSITY.comment=Optical density of the independent high cloud layer. 0 hides it; coverage/altitude and lower-cloud controls remain independent.
''';f.write_text(s)
print('Applied seven preferred defaults and implemented six new controls, local sun halo, brighter independent cirrus and rain-gated wet film.')

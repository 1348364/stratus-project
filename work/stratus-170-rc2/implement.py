from pathlib import Path
p=Path('outputs/Stratus/shaders')
f=p/'core/raster.frag.glsl';s=f.read_text()
s=s.replace('''        gl_FragData[0] = vec4(0.0);
        gl_FragData[1] = vec4(0.0);''','''        // Native mode restores the animated underside at the actual exit.
        // Ordinary alpha blending keeps nearer glass/particles in draw order;
        // the dedicated transmission buffer carries its coverage into fog.
        vec4 underside=vec4(0.0);
#if WATER_STYLE == 1
        vec3 nativeColour=surface.rgb*lm;
#if REALISTIC_LIGHTING != 0
        vec3 fn=unitVector(orientedNormal);
        nativeColour*=dot(fn*fn,vec3(0.6,fn.y>=0.0?1.0:0.5,0.8));
#endif
        underside=vec4(decodeDisplay(nativeColour),clamp(surface.a*WATER_TEXTURE,0.0,1.0));
#endif
        gl_FragData[0] = underside;
        gl_FragData[1] = vec4(0.0);''',1)
s=s.replace('''        gl_FragData[6] = vec4(0.0);
        gl_FragData[7] = vec4(0.0);''','''        gl_FragData[6] = vec4(0.0,0.0,0.0,underside.a);
        gl_FragData[7] = vec4(0.0);''',1)
s=s.replace('float(category>1.05&&category<1.5)', 'float(category>1.05&&category<1.5&&material!=4113)')
s=s.replace('''        // Invisible exit-depth capture only. The scene and interface-optics
        // buffers stay untouched, so no surface window/reflection is drawn.
        // This independent attachment survives glass and particles and lets
        // the resolve stop water fog before objects in the air beyond it.''','''        // Independent exit depth stops fog before air beyond the interface.
        // Stratus mode stays clear; native mode also supplies its atlas layer.''')
f.write_text(s)
f=p/'core/raster.vert.glsl';s=f.read_text();s=s.replace('out vec4 tintAndOpacity;','#include "/core/entity-lighting.glsl"\nout vec4 tintAndOpacity;');s=s.replace('''    tintAndOpacity = gl_Color;''','''    tintAndOpacity = gl_Color;
#if REALISTIC_LIGHTING == 0 && PASS_KIND == 4 && (!defined(BLOCK_SURFACE) || BLOCK_SURFACE == 0)
    // Iris pack geometry supplies unlit entity vertex colour. Terrain's native
    // oldLighting shading is already present and must not be applied twice.
    tintAndOpacity.rgb*=nativeEntityLighting(unitVector(orientedNormal));
#endif''');f.write_text(s)
(p/'core/entity-lighting.glsl').write_text('''#ifndef STRATUS_ENTITY_LIGHTING_INCLUDED
#define STRATUS_ENTITY_LIGHTING_INCLUDED
// Vanilla's two fixed diffuse lights, 0.6 direct + 0.4 ambient, clamp at one.
// World/player normal retains model orientation without rotating with camera.
// The lightmap remains independent; emissive/spidereyes passes bypass this.
float nativeEntityLighting(vec3 normal){
    vec3 a=normalize(vec3(0.2,1.0,-0.7));
    vec3 b=normalize(vec3(-0.2,1.0,0.7));
    return min(1.0,0.4+0.6*(max(dot(a,normal),0.0)+max(dot(b,normal),0.0)));
}
#endif
''')
f=p/'core/diffuse.glsl';s=f.read_text().replace('*lobe*film*WET_SHEEN*0.035','*lobe*film*WET_SHEEN*0.008');f.write_text(s)
f=p/'core/lake.frag.glsl';s=f.read_text().replace('if(shiftedDepth>=0.999999)transmitted=reflectedEnvironment(backRay);','''// Missing screen-space geometry must not import an outdoor sky into
        // an unlit cave. Use the same local-exposure fallback as reflection.
        if(shiftedDepth>=0.999999)transmitted=reflectedEnvironment(backRay)
            *mix(0.03,1.0,smoothstep(0.04,0.8,waterSky));''');f.write_text(s)
f=p/'core/atmosphere-resolve.frag.glsl';s=f.read_text();needle='    float distanceToScene=sceneDistance(rasterUV);';s=s.replace(needle,'''    // The atmosphere producer writes exact zero in water/lava/snow. Avoid
    // depth reconstruction and four bilateral taps that cannot contribute.
    if(isEyeInWater!=0){completedScene=vec4(max(scene,vec3(0.0)),1.0);return;}
'''+needle);f.write_text(s)
f=p/'lang/en_us.lang';s=f.read_text();s=s.replace('option.WATER_TEXTURE.comment=', 'option.WATER_TEXTURE.comment=In Vanilla mode this also controls the animated underside seen from underwater. ');f.write_text(s)
print('Implemented focused candidate fixes; no option/default/range/preset changes.')

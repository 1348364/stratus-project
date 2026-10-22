from pathlib import Path
p=Path('outputs/Stratus/shaders')
f=p/'core/diffuse.glsl';s=f.read_text();a=s.index('float exposedWetFilm(');b=s.index('vec3 formIrradiance',a);s=s[:a]+s[b:];a=s.index('float retainedSurfaceMoisture(');b=s.index('vec3 diffuseRadiance',a)
s=s[:a]+'''// A surface film adds reflected highlights without changing the diffuse albedo.
// Absorption darkening/retained dampness was deliberately retired in 1.6.9.
// Material.x remains in the buffer for saved-layout compatibility, not gating.
vec3 wetSurfaceResponse(vec3 dry,vec3 n,vec3 playerPoint,float sky,vec2 material){
#if DIMENSION_TYPE == 0
    float filmSource=WET_WEATHER_MODE==0?1.0:rainStrength;
    float film=filmSource*SURFACE_DAMPNESS*smoothstep(0.18,0.85,sky)
        *mix(0.55,1.0,max(n.y,0.0));
    if(WET_SHEEN>0.0&&film>0.0001){
        vec3 view=unitVector(-playerPoint);
        float nv=max(dot(n,view),0.0);
        if(nv>0.001){
            float fresnel=0.02+0.98*pow(1.0-nv,5.0);
            float coat=clamp(film*WET_SHEEN*fresnel*0.20,0.0,0.20);
            vec3 environment=softSkyReflection(reflect(-view,n));
            // Positive, restrained highlights preserve the original block colour
            // between glints, including the complete vanilla-lighting path.
            dry+=max(environment-dry,vec3(0.0))*coat;
            vec3 light=broadLightDirection(),halfway=unitVector(view+light);
            float exponent=mix(160.0,36.0,clamp(material.y,0.0,1.0));
            float lobe=pow(max(dot(n,halfway),0.0),exponent)*(exponent+2.0)/6.283185307;
            dry+=sunlightColour()*solarDaylight()*max(dot(n,light),0.0)
                *lobe*film*WET_SHEEN*0.035*(1.0-0.65*rainStrength);
        }
    }
#endif
    return dry;
}
''' + s[b:];f.write_text(s)
f=p/'core/moisture.glsl';s=f.read_text().replace('// Material moisture follows absorption, drainage and sky exposure. A thin\n// rain film is evaluated locally; no neighbour mask or extra reflection pass.','// Thin film on exposed solid blocks, including non-porous materials.\n// No absorption darkening, retained dampness or extra reflection pass.').replace('#if DIMENSION_TYPE == 0 && REALISTIC_LIGHTING == 1','#if DIMENSION_TYPE == 0').replace('if(SURFACE_DAMPNESS<=0.0)return dry;','if(SURFACE_DAMPNESS<=0.0||WET_SHEEN<=0.0)return dry;');f.write_text(s)
f=p/'core/options.glsl';s=f.read_text().replace('#define REALISTIC_LIGHTING 1 //','#define REALISTIC_LIGHTING 0 //');s+='\n// Reuse the active animated water atlas pattern without changing opacity.\n#define WATER_TEXTURE 0.15 // [0.00 0.05 0.10 0.15 0.25 0.35 0.50 0.75 1.00]\n';f.write_text(s)
f=p/'core/raster.frag.glsl';s=f.read_text().replace('    surface *= texture(gtexture, atlasCoordinate);','    vec4 atlasTexel=texture(gtexture, atlasCoordinate);\n    surface *= atlasTexel;').replace('// Unknown translucent block entities have no pore absorption. Ordinary\n    // entities remain excluded; zero absorption also excludes a rain film.','// Translucent block entities receive film; ordinary entities stay excluded.').replace('vec4(0.0, emission, float(blockCategory==4103), mark)','vec4(dot(atlasTexel.rgb,vec3(0.2126,0.7152,0.0722)), emission, float(blockCategory==4103), mark)');f.write_text(s)
f=p/'core/lake.frag.glsl';s=f.read_text().replace('    vec4 markedNormal=texture(colortex1,rasterUV),markedDepth=texture(colortex2,rasterUV);\n','');s=s.replace('    float opaqueDepth=','    // Reject underwater/non-water pixels before fetching interface metadata.\n    vec4 markedNormal=texture(colortex1,rasterUV),markedDepth=texture(colortex2,rasterUV);\n    float opaqueDepth=',1).replace('        image=mix(transmitted,reflected,waterReflectionWeight(boundary));','''        // Native still/flow atlas texture and animation, carried in an unused
        // metadata channel by the existing gtexture fetch. No extra texture read.
        // Tint only transmission so reflected scenery stays sharp and unpainted.
        float textureTint=mix(1.0,clamp(markedColour.r,0.0,1.0),WATER_TEXTURE);
        image=mix(transmitted*textureTint,reflected,waterReflectionWeight(boundary));''');f.write_text(s)
f=p/'shaders.properties';s=f.read_text().replace('separateAo=false','''# The reflection cache has no readers when scenery reflections are disabled.
#if REFLECTION_MODE == 0
program.composite.enabled=false
#endif
separateAo=false''').replace('screen.WATER=WATER_VISIBILITY BIOME_WATER WATER_TURBIDITY WATER_EXTINCTION <empty> <empty>','screen.WATER=WATER_VISIBILITY BIOME_WATER WATER_TURBIDITY WATER_EXTINCTION WATER_TEXTURE <empty>').replace('sliders=','sliders=WATER_TEXTURE ',1);f.write_text(s)
f=p/'lang/en_us.lang';s=f.read_text();lines={
'option.SURFACE_DAMPNESS':'Surface film amount',
'option.SURFACE_DAMPNESS.comment':'Thin exposed water film on porous and non-porous solid blocks. No absorption darkening or retained dampness. Zero disables film; existing saved values are retained.',
'value.SURFACE_DAMPNESS.1.00':'Normal (default)',
'option.WET_SHEEN.comment':'View-dependent highlights on exposed solid blocks, including metal and glazed materials. Works with either lighting mode. Zero disables sheen; sealed caves remain dry.',
'option.WET_DARKENING':'Absorption darkening (retired)',
'option.WET_DARKENING.comment':'Compatibility setting: saved values remain readable, but this effect was explicitly removed in 1.6.9 to preserve vanilla block colours. Adjust Surface film amount and Wet sheen strength instead.',
'option.REALISTIC_LIGHTING.comment':"Off (default) restores the game's vertex face lighting/AO and lightmap colour/brightness, bypassing ambient/lamp boosts, ground warmth, bloom and camera grading. Independent wet highlights, Stratus water and atmosphere remain. On retains artistic controls; saved settings are preserved.",
'option.WET_WEATHER_MODE.comment':'All weather allows exposed film without rain; Rain only gates it by rainfall. Surface film amount, exposure and face drainage control the highlights. Both porous and non-porous blocks are supported in either lighting mode.',
'value.REALISTIC_LIGHTING.0':'Off (vanilla, default)',
'option.SURFACE_SATURATION.comment':'1.00 preserves the input saturation before enhanced lighting and bloom. Vanilla lighting bypasses this artistic adjustment.'}
s='\n'.join(k+'='+lines[k] if (k:=l.split('=',1)[0]) in lines else l for l in s.splitlines())+'\n';s+='option.WATER_TEXTURE=Vanilla water texture\noption.WATER_TEXTURE.comment=Subtle animated still/flow pattern from the active game or resource pack, modulating transmitted water only. Zero restores the clear surface. Does not change opacity, refraction, depth or scenery reflection quality.\n';f.write_text(s)
print('Updated source; original pole filter and quality presets unchanged.')

from pathlib import Path
p=Path('outputs/Stratus/shaders');c=p/'core/ceiling.glsl';s=c.read_text();a=s.index('// Vanilla-like');b=s.index('vec2 cloudVolumeSample',a)
s=s[:a]+'''// Read the running game's cloud map: current vanilla (including resource-pack
// replacements), rather than a guessed procedural or bundled historical layout.
// texelFetch and explicit wrapping preserve every connected pixel and hole.
uniform sampler2D vanillaClouds;
vec2 cloudMapPosition(vec2 worldXZ){
    float cellSize=max(CLOUD_SPAN*0.05,1.0); // default 240 -> vanilla 12-block cells
    vec2 wind=vec2(frameTimeCounter*CLOUD_DRIFT*2.4,0.0);
    return (worldXZ+wind)/cellSize+vec2(0.0,0.33);
}
float vanillaCloudCell(vec2 mapPoint){
    ivec2 size=textureSize(vanillaClouds,0);
    ivec2 cell=ivec2(mod(floor(mapPoint),vec2(size)));
    return step(0.1,texelFetch(vanillaClouds,cell,0).a);
}
vec2 layeredCloudSample(vec3 worldPoint,bool detailed,bool upper){
    float altitude=upper?CIRRUS_ALTITUDE:CLOUD_ALTITUDE;
    float thickness=upper?28.0:CLOUD_THICKNESS;
    float amount=upper?CIRRUS_AMOUNT:CLOUD_AMOUNT;
    if(amount<=0.0)return vec2(0.0);
    float h=(worldPoint.y-altitude)/max(thickness,1.0)+0.5;
    if(upper){
        // A continuous thin veil, independent of the lower cloud texture, span,
        // coverage and distortion. Broad stretched fields give gentle wisps
        // across the sky, including the gaps between the physical clouds.
        vec2 p=(worldPoint.xz+frameTimeCounter*CLOUD_DRIFT*vec2(1.2,-0.3))/680.0;
        float broad=smoothField(p*vec2(0.32,1.4)+vec2(37.2,-19.1));
        float strands=smoothField(p*vec2(0.55,4.2)+vec2(broad*0.4,13.5));
        float veil=mix(0.22,0.90,smoothstep(0.15,0.85,mix(broad,strands,0.55)));
        float envelope=smoothstep(0.0,0.3,h)*(1.0-smoothstep(0.65,1.0,h));
        return vec2(veil*envelope*amount*CLOUD_DENSITY*0.016,h);
    }
    vec2 mapPoint=cloudMapPosition(worldPoint.xz);
    float mask=vanillaCloudCell(mapPoint);
    if(mask<0.5)return vec2(0.0);
    // Simple extruded, connected forms. No erosion, pores or 3D billow noise.
    // Gentle vertical relief never moves the vanilla horizontal silhouette.
    float broad=smoothField(mapPoint*0.065+vec2(8.1,3.7));
    h-=(broad-0.5)*CLOUD_DISTORTION*0.08;
    float envelope=smoothstep(0.0,0.08,h)*(1.0-smoothstep(0.88,1.0,h));
    float gradient=mix(0.88,1.05,clamp(h,0.0,1.0));
    // Retain the saved CLOUD_DETAIL control as broad gradient strength. It no
    // longer adds high-frequency geometry; sampling quality cannot alter shape.
    gradient=mix(1.0,gradient,clamp(CLOUD_DETAIL*0.5,0.0,1.0));
    return vec2(mask*envelope*gradient*CLOUD_DENSITY*(amount/0.68)*0.040,h);
}
''' + s[b:];c.write_text(s)
c=p/'core/diffuse.glsl';s=c.read_text();a=s.index('    // Vanilla axis weights');b=s.index('\n}',a)
s=s[:a]+'''    float vertical=normal.y>=0.0?1.0:0.5;
    float vanilla=dot(normal*normal,vec3(0.6,vertical,0.8));
    float irradiance=vanilla;
#if DIMENSION_TYPE == 0
    // Diffuse sky hemisphere + ground bounce and a broad solar lobe. All
    // directions are world-space: turning the camera cannot rotate shading.
    // Skylight gates the directional component; sealed caves keep local light.
    vec3 sun=broadLightDirection();
    float direct=daytimeWeight()*smoothstep(-0.04,0.16,sun.y)*(1.0-0.85*rainStrength);
    float facing=max(dot(normal,sun),0.0);
    float hemisphere=mix(0.38,0.78,normal.y*0.5+0.5);
    float physical=hemisphere*(1.0-0.20*direct)+0.44*direct*facing;
    irradiance=mix(vanilla,physical,smoothstep(0.08,0.85,skyExposure));
#endif
    float strength=FACE_BLEND*FACE_SHADING;
    // Linear contrast keeps saved 2.0 settings readable instead of squaring
    // already-dark surfaces. Zero for either control is an exact bypass.
    return vec3(clamp(1.0+(irradiance-1.0)*strength,0.18,1.18));''' + s[b:];c.write_text(s)
c=p/'shaders.properties';s=c.read_text();s=s.replace('customTexture.weatherNoise=', 'customTexture.vanillaClouds=minecraft:textures/environment/clouds.png\ncustomTexture.weatherNoise=');c.write_text(s)
c=p/'lang/en_us.lang';s=c.read_text();updates={
'CLOUD_AMOUNT.comment':'Density/coverage strength of the current vanilla cloud footprint. Zero hides the lower layer; high clouds are independent. The footprint is preserved at every nonzero value.',
'CLOUD_SPAN.comment':'Scale of the current vanilla cloud footprint. Default 240 gives 12-block texture cells; changing scale preserves its connected shapes.',
'CLOUD_DISTORTION.comment':'Gentle vertical relief within connected clouds. Never warps or erodes the vanilla horizontal footprint.',
'CLOUD_RELIEF.comment':'Self-shadowing and smooth light/dark depth within the simple connected cloud forms.',
'FACE_SHADING':'Realistic face contrast',
'FACE_SHADING.comment':'Strength of diffuse sky, ground and sun-facing contrast. Sun direction and rain affect exposed faces; caves retain local lighting. Zero disables face contrast.',
'FACE_BLEND':'Face shading blend',
'FACE_BLEND.comment':'Blend from unshaded faces to diffuse face shading. Zero bypasses it, including with saved contrast values.',
'CIRRUS_AMOUNT':'High cloud coverage',
'CIRRUS_AMOUNT.comment':'Strength of a sky-wide wispy veil, independent of lower cloud coverage and shapes. Zero hides the upper layer.',
'CLOUD_STYLE.comment':"Stratus extrudes the running game's current cloud texture with simple forms and soft shading. Vanilla uses actual fancy cloud geometry. Off hides both.",
'CLOUD_DENSITY.comment':'Optical density of the simple cloud volumes. Lower-layer shapes come from the active vanilla/resource-pack cloud texture.',
'CLOUD_DETAIL':'Cloud gradient detail',
'CLOUD_DETAIL.comment':'Broad smooth density gradients within simple connected clouds. Fine pores and noisy billows have been removed.'}
for key,value in updates.items():
 import re
 s,n=re.subn(r'^option\.'+re.escape(key)+r'=.*$',lambda m:'option.'+key+'='+value,s,flags=re.M);assert n==1,(key,n)
c.write_text(s)

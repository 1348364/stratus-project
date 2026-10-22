from pathlib import Path
r=['PACK Stratus-1.4.0.zip','RESUME','CMD weather clear','CMD time set 3000','CMD fill 81 100 31 95 102 45 minecraft:water','CMD fill 81 103 31 95 107 45 minecraft:air','CMD tp ShaderCheck 88 106 32 0 55','WAIT 6','SHOT v140-refraction',
'CMD tp ShaderCheck 104 99 94 0 -15','WAIT 4','SHOT v140-underwater','CMD tp ShaderCheck 200 145 200 0 -35','WAIT 5','SHOT v140-clouds-below','CMD tp ShaderCheck 200 171 200 45 -5','WAIT 5','SHOT v140-clouds-under-flight','CMD tp ShaderCheck 200 192 200 0 0','WAIT 5','SHOT v140-clouds-inside','CMD tp ShaderCheck 200 285 200 0 35','WAIT 5','SHOT v140-clouds-above','CMD tp ShaderCheck 200 430 200 0 25','WAIT 5','SHOT v140-high-clouds',
'PACK Stratus-1.4.0-High.zip','CMD tp ShaderCheck 200 160 200 0 -30','WAIT 5','SHOT v140-high-quality-clouds','PACK Stratus-1.4.0-Low-Clouds.zip','CMD tp ShaderCheck 104 184 96 0 90','WAIT 5','SHOT v140-cloud-water-order',
'PACK Stratus-1.4.0-Vanilla-Sky.zip','CMD time set 3000','CMD tp ShaderCheck 0 110 0 -90 -40','WAIT 5','SHOT v140-vanilla-sun-clouds','CMD tp ShaderCheck 200 185 200 0 -5','WAIT 5','SHOT v140-vanilla-clouds',
'PACK Stratus-1.4.0.zip','CMD tp ShaderCheck -2 98 -6 180 10','WAIT 5','SHOT v140-damp-grazing','CMD weather rain','WAIT 6','SHOT v140-damp-rain','CMD weather clear',
'CMD tp ShaderCheck -8 100 2 0 12','WAIT 4','SHOT v140-entities','CMD tp ShaderCheck 0 97 5 0 5','RESUME','CMD setblock 0 97 9 minecraft:stone','CMD setblock 0 97 9 minecraft:air destroy','SHOT v140-breaking-particles',
'CMD summon snowball -1 98.3 9 {NoGravity:1b,Tags:["stratus140_projectile"],Motion:[0.01d,0d,0d]}','CMD summon egg 0 98.3 9 {NoGravity:1b,Tags:["stratus140_projectile"],Motion:[0.01d,0d,0d]}','CMD summon ender_pearl 1 98.3 9 {NoGravity:1b,Tags:["stratus140_projectile"],Motion:[0.01d,0d,0d]}','SHOT v140-projectiles','CMD kill @e[tag=stratus140_projectile]',
'CMD time set 18000','CMD tp ShaderCheck 0 96 5 0 10','WAIT 5','SHOT v140-bloom-fireflies',
'CMD execute in minecraft:the_nether run tp ShaderCheck 0 103 -5 0 18','WAIT 15','RESUME','WAIT 3','SHOT v140-nether','CMD execute in minecraft:the_end run tp ShaderCheck 0 123 -5 0 18','WAIT 15','RESUME','WAIT 3','SHOT v140-end','CMD execute in minecraft:overworld run tp ShaderCheck 104 104 90 0 9','WAIT 15','RESUME','CMD time set 3000','WAIT 5',
'MENU','WIDGET Shader Pack Settings...','WAIT 2','SHOT v140-options-root']
for key in ['WATER','REFLECTIONS','WAVES','LIGHTING','CLOUDS','SUN','FOG','MATERIALS','POST','PERFORMANCE']:
 r+=['OPTIONS '+key,'SHOT v140-options-'+key.lower()]
r+=['RESUME','DONE v140-final-visuals']
Path('work/minecraft-smoke/qa-request.txt').write_text('\n'.join(r)+'\n')

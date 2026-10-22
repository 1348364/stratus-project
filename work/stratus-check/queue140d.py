from pathlib import Path
r=['PACK Stratus-1.4.0.zip','RESUME','CMD gamerule minecraft:random_tick_speed 3','CMD weather clear','CMD time set 3000']
for name,tp in [('water','104 104 90 0 9'),('landscape','0 110 -32 0 20'),('clouds','200 140 200 0 -35')]:
 r+=['CMD tp ShaderCheck '+tp,'WAIT 15','BENCH v140-balanced-'+name+' 20','SHOT v140-benchmark-'+name]
r+=['CMD tp ShaderCheck 104 104 90 0 9','RESUME','HUD show','WAIT 3','SHOT v140-left-open','DONE v140-complete']
Path('work/minecraft-smoke/qa-request.txt').write_text('\n'.join(r)+'\n')

from pathlib import Path
import json
w=Path('work/stratus-transparent-blocks');a=[]
a.append('CMD forceload add 4112 4080 4143 4127')
# Add a compact comparison to the repaired warm-ocean pond in the test world.
for x,mat in [(4120,'glass'),(4124,'red_stained_glass'),(4128,'blue_stained_glass'),(4132,'lime_stained_glass')]:
 a += [f'CMD fill {x} 95 4106 {x+2} 100 4106 minecraft:{mat}',f'CMD fill {x} 90 4096 {x+2} 93 4096 minecraft:{mat}']
# Uniform wall makes complementary/inverted colours evident through the panes.
a.append('CMD fill 4119 89 4093 4136 94 4093 minecraft:white_concrete')
a.append('CMD fill 4126 90 4098 4127 93 4098 minecraft:glass')
(w/'fixture-commands.txt').write_text('\n'.join(a)+'\n')
print('Prepared clear/red/blue/lime glass comparisons above water and submerged.')

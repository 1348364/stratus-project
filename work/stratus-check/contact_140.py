from PIL import Image,ImageDraw
from pathlib import Path
names=['final-reflections','final-waterfall','final-underwater','final-refraction','final-damp-corners','final-cloud-under','final-cloud-above','final-entities','final-nether','final-end','vanilla-sun-clouds','vanilla-moon','options-root','options-water','options-reflections','options-waves','options-lighting','options-clouds','options-sun','options-fog','options-materials','options-post','options-performance','left-open']
for page in range((len(names)+5)//6):
 out=Image.new('RGB',(1200,1110),'#111820');d=ImageDraw.Draw(out)
 for i,n in enumerate(names[page*6:page*6+6]):
  p=Path('work/minecraft-smoke/screenshots')/('v140-'+n+'.png');im=Image.open(p);im.thumbnail((600,337));x=i%2*600;y=i//2*370;out.paste(im,(x,y));d.text((x+8,y+340),n,fill='white')
 out.save(f'work/stratus-check/140-final-{page}.jpg')

from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
w=Path('work/stratus-check');g=Path('work/minecraft-smoke/screenshots');out=w/'final-review-151';out.mkdir(exist_ok=True)
prefix=sys.argv[1] if len(sys.argv)>1 else 'v151-final-'
names=sorted(p.stem for p in g.glob(prefix+'*.png'))
for pg in range((len(names)+5)//6):
 canvas=Image.new('RGB',(1200,1110),'#101820');d=ImageDraw.Draw(canvas)
 for i,n in enumerate(names[pg*6:pg*6+6]):
  im=Image.open(g/(n+'.png'));im.thumbnail((600,337));x=i%2*600;y=i//2*370;canvas.paste(im,(x,y));d.text((x+8,y+341),n,fill='white')
 target=out/(prefix+'page-'+str(pg+1)+'.jpg');canvas.save(target,quality=94);print(target)

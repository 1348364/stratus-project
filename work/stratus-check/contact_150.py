"""Contact pages for inspection only; report copies the untouched game frames."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
w=Path('work/stratus-check');g=Path('work/minecraft-smoke/screenshots')
captures=json.loads((w/'captures-150.json').read_text())
if (w/'menus-150.json').exists():captures+=json.loads((w/'menus-150.json').read_text())
names=[c['name'] for c in captures if (g/('v150-'+c['name']+'.png')).exists()]
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
for page in range(start,(len(names)+5)//6):
    subset=names[page*6:page*6+6]
    out=Image.new('RGB',(1200,1110),'#101820');d=ImageDraw.Draw(out)
    for i,n in enumerate(subset):
        im=Image.open(g/('v150-'+n+'.png'));im.thumbnail((600,337))
        x=i%2*600;y=i//2*370;out.paste(im,(x,y));d.text((x+8,y+341),n,fill='white')
    dest=w/f'150-review-{page}.jpg';out.save(dest,quality=94)
    print(dest,':',', '.join(subset))

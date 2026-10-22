from pathlib import Path
from PIL import Image,ImageDraw
work=Path('work/stratus-check');names=(work/'shots-1.3.1.txt').read_text().splitlines();src=Path('work/minecraft-smoke/screenshots');dest=work/'contacts-1.3.1';dest.mkdir(exist_ok=True)
for k in range((len(names)+5)//6):
 group=names[k*6:(k+1)*6]
 if not all((src/f'v131-{n}.png').exists() for n in group):continue
 im=Image.new('RGB',(1536,1392),(15,20,27));draw=ImageDraw.Draw(im)
 for i,n in enumerate(group):
  picture=Image.open(src/f'v131-{n}.png').convert('RGB');picture.thumbnail((768,432));x=i%2*768;y=i//2*464;draw.text((x+8,y+8),n,fill='white');im.paste(picture,(x,y+30))
 out=dest/f'group-{k+1}.jpg';im.save(out,quality=95);print(out)

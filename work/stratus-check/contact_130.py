from pathlib import Path
from PIL import Image,ImageDraw
work=Path('work/stratus-check');game=Path('work/minecraft-smoke/screenshots');names=(work/'shots-1.3.0.txt').read_text().splitlines();out=work/'contacts-1.3.0';out.mkdir(exist_ok=True)
for k in range((len(names)+5)//6):
 subset=names[k*6:(k+1)*6]
 if not all((game/f'g130-{n}.png').exists() for n in subset):continue
 canvas=Image.new('RGB',(1536,3*464),(15,20,27));d=ImageDraw.Draw(canvas)
 for i,n in enumerate(subset):
  im=Image.open(game/f'g130-{n}.png').convert('RGB');im.thumbnail((768,432));x=i%2*768;y=i//2*464;d.text((x+8,y+8),n,fill='white');canvas.paste(im,(x,y+30))
 path=out/f'group-{k+1}.jpg';canvas.save(path,quality=95);print(path)

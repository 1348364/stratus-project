from pathlib import Path
from PIL import Image,ImageDraw
work=Path('work/stratus-check');game=Path('work/minecraft-smoke/screenshots')
names=(work/'shots-1.2.0.txt').read_text().splitlines();out=work/'contacts-1.2.0';out.mkdir(exist_ok=True)
for group in range((len(names)+5)//6):
 subset=names[group*6:(group+1)*6]
 if not all((game/f'f120-{name}.png').exists() for name in subset):continue
 canvas=Image.new('RGB',(1708,3*510),(15,20,27));draw=ImageDraw.Draw(canvas)
 for i,name in enumerate(subset):
  source=Image.open(game/f'f120-{name}.png').convert('RGB');source.thumbnail((854,480))
  x=(i%2)*854;y=(i//2)*510
  draw.text((x+10,y+8),name,fill=(235,240,245));canvas.paste(source,(x,y+30))
 path=out/f'group-{group+1}.jpg';canvas.save(path,quality=94)
 print(path)

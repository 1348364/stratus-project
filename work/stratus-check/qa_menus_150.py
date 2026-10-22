"""Queue actual Iris menu captures and restore the isolated wooden test scene."""
from pathlib import Path
import json
g=Path('work/minecraft-smoke');w=Path('work/stratus-check')
a=['PACK Stratus-1.5.0.zip','RESUME','WAIT 3','MENU','WAIT 3','OPTIONS root','WAIT 3','SHOT v150-options-root','WAIT 2']
captures=[{'name':'options-root','group':'Settings','note':'Actual Iris category screen and quality profiles.'}]
for menu in ['WATER','REFLECTIONS','REFRACTION','WAVES','LIGHTING','ATMOSPHERE','CLOUDS','SUN','FOG','MATERIALS','POST','PERFORMANCE']:
    name='options-'+menu.lower();a += ['OPTIONS '+menu,'WAIT 2','SHOT v150-'+name,'WAIT 2']
    captures.append({'name':name,'group':'Settings','note':'Actual Iris '+menu.lower()+' menu, with all retained and new controls.'})
a += ['RESUME','CMD weather clear','CMD time set 3000','CMD tp ShaderCheck 156 105 43 0 35','WAIT 10','HUD show','WAIT 2','STATE','SHOT v150-left-open','WAIT 3','DONE v150-release-complete']
captures.append({'name':'left-open','group':'Regression','note':'Isolated client left open at the submerged three-dimensional wood fixture with HUD visible.'})
q=g/'qa-request.txt';assert not q.exists();q.write_text('\n'.join(a)+'\n')
(w/'menus-150.json').write_text(json.dumps(captures,indent=2)+'\n')
print('Queued thirteen Iris menu captures and final open scene; no Main settings changes.')

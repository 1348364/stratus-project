"""Reproducible, reviewed natural-world Stratus 1.6.10 showcase selection."""
from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.6.10'
SELECTION=[
 ('release-river','Forest river','The naturally generated river and spruce banks.','Saved release settings'),
 ('river-screen-edge','Across the river','Natural shoreline, forest reflections and clear shallows.','Reference settings'),
 ('reference-waterline','Along the waterline','A low view across the naturally generated river.','Reference settings'),
 ('river-downward','Below the ripples','Natural sand, gravel and riverbed shapes viewed through the water.','Reference settings'),
 ('release-underwater','Under the surface','Looking towards the naturally generated bank from underwater.','Saved release settings'),
 ('reference-underwater-air-exit','Towards the forest','A submerged view of the natural spruce shoreline.','Reference settings'),
 ('candidate-reference-river','Reflected woodland','A full-quality view of the naturally generated forest river.','Reference settings'),
 ('polished-sun','Sun through the canopy','The square sun, clouds and a natural treetop silhouette.','Reference settings'),
 ('clouds-native','Over the treetops','Cloud layers above the naturally generated forest.','Cloud-focused settings'),
 ('clouds-below','Beneath the clouds','A skyward view of the cloud layer from the natural world.','Cloud-focused settings'),
]

def curate():
 report=ROOT/'outputs/Stratus-1.6.10-visual-checks'
 evidence=json.loads((report/'manifest.json').read_text())
 captures={Path(c['file']).stem:c for c in evidence['captures']}
 folder=ROOT/'outputs/Stratus-1.6.10-showcase-natural';folder.mkdir(exist_ok=True)
 assets=ROOT/'work/stratus-public/public/assets/natural';assets.mkdir(exist_ok=True)
 scenes=[];seen=set()
 with zipfile.ZipFile(ROOT/'outputs/Stratus-1.6.10.zip') as release:
  for index,(name,title,description,settings) in enumerate(SELECTION,1):
   capture=captures['s1610-'+name];source=report/capture['file'];data=source.read_bytes();digest=hashlib.sha256(data).hexdigest()
   assert capture['status']=='reviewed' and digest==capture['sha256'] and digest not in seen
   seen.add(digest)
   pack=capture['pack'];comparison=ROOT/'work/stratus-refine-1610/packs'/pack
   if pack!='Stratus-1.6.10.zip':
    with zipfile.ZipFile(comparison) as candidate:
     assert all(candidate.read(n)==release.read(n) for n in release.namelist() if n.startswith('shaders/'))
   filename=f'{index:02d}-{name}.png';shutil.copyfile(source,folder/filename);shutil.copyfile(source,assets/filename)
   scenes.append({'file':filename,'title':title,'description':description+' '+settings+'. Actual Stratus 1.6.10 in-game capture.','sha256':digest,'source':source.relative_to(ROOT).as_posix(),'pack':pack,'natural_world':True,'reviewed':True})
   web=folder/(Path(filename).stem+'.jpg')
   subprocess.run(['/usr/bin/sips','-s','format','jpeg','-s','formatOptions','88',str(source),'--out',str(web)],check=True,stdout=subprocess.DEVNULL)
   shutil.copyfile(web,assets/web.name)
   scenes[-1].update(web_file=web.name,web_sha256=hashlib.sha256(web.read_bytes()).hexdigest())
 manifest={'version':VERSION,'scene_policy':'natural-world-only','reviewed':True,'runtime_assets_match_release':True,'scenes':scenes}
 (folder/'showcase.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Prepared 10 reviewed natural-world captures; all shader runtime assets match the 1.6.10 release.')
 return manifest

if __name__=='__main__':curate()

from pathlib import Path
import subprocess,json,zipfile
base=Path.home()/'Library/Application Support/ModrinthApp';work=Path('work/stratus-main-qa/helper');classes=work/'classes';classes.mkdir(exist_ok=True)
loader=base/'meta/libraries/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar';mixin=base/'meta/libraries/net/fabricmc/sponge-mixin/0.17.4+mixin.0.8.7/sponge-mixin-0.17.4+mixin.0.8.7.jar'
subprocess.run(['/usr/bin/javac','--release','21','-proc:none','-cp',str(loader)+':'+str(mixin),'-d',str(classes),*[str(p) for p in work.rglob('*.java')]],check=True)
with zipfile.ZipFile(work/'stratus-main-qa.jar','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'stratus_visual_qa','version':'1.5.1','name':'Temporary Stratus Terrain Lab driver','environment':'client','entrypoints':{'client':['StratusVisualQA']},'mixins':['stratus-qa.mixins.json'],'depends':{'fabricloader':'>=0.19.5','minecraft':'1.21.11','java':'>=21'}}))
 z.writestr('stratus-qa.mixins.json',json.dumps({'required':True,'minVersion':'0.8','package':'qa.mixin','compatibilityLevel':'JAVA_21','client':['StratusFrameMixin'],'injectors':{'defaultRequire':1}}))
 for p in classes.rglob('*.class'):z.write(p,p.relative_to(classes).as_posix())
print('Built temporary workspace driver; no Main mod files changed.')

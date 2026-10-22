from pathlib import Path
import json, subprocess, zipfile
base = Path.home() / 'Library/Application Support/ModrinthApp'
work = Path('work/stratus-check/qa-helper')
classes = work / 'classes'; classes.mkdir(exist_ok=True)
loader = base / 'meta/libraries/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar'
mixin = base / 'meta/libraries/net/fabricmc/sponge-mixin/0.17.4+mixin.0.8.7/sponge-mixin-0.17.4+mixin.0.8.7.jar'
subprocess.run(['/usr/bin/javac','--release','21','-proc:none','-cp',str(loader)+':'+str(mixin),'-d',str(classes),*[str(p) for p in work.rglob('*.java')]],check=True)
destination = Path('work/minecraft-smoke/mods/stratus-visual-qa.jar')
with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'stratus_visual_qa','version':'1.0.0',
        'name':'Stratus visual test helper (test directory only)','environment':'client',
        'entrypoints':{'client':['StratusVisualQA']},'mixins':['stratus-qa.mixins.json'],'depends':{'fabricloader':'>=0.19.5','minecraft':'1.21.11','java':'>=21'}}))
    archive.writestr('stratus-qa.mixins.json',json.dumps({'required':True,'minVersion':'0.8','package':'qa.mixin','compatibilityLevel':'JAVA_21','client':['StratusFrameMixin'],'injectors':{'defaultRequire':1}}))
    for source in classes.rglob('*.class'):archive.write(source,source.relative_to(classes).as_posix())
print('Built isolated QA helper:',destination)

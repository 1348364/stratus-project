from pathlib import Path
import json,hashlib
w=Path(__file__).parent;p=Path('outputs/Stratus');v='1.7.0-rc1'
policy=json.loads((w/'baseline/RELEASE-POLICY.json').read_text());policy['version']=v;policy['reset_related_overrides']=['WATER_TEXTURE','WATER_STYLE','TRANSPARENT_REFLECTIONS','TRANSPARENT_REFRACTION'];policy['visual_defaults']=json.loads((w/'reference-defaults.json').read_text())
for key in ['WATER_STYLE','TRANSPARENT_REFLECTIONS','TRANSPARENT_REFRACTION']:
 policy['previous_source_defaults'][key]=None;policy['captured_previous_values'][key]=None
policy['new_option_policy']='null previous/captured entries denote absent old-version controls; source/preset defaults apply unless an actual later manual value exists.'
(p/'RELEASE-POLICY.json').write_text(json.dumps(policy,indent=2)+'\n')
s=(p/'package.py').read_text().replace("'Stratus-1.6.12.zip'",f"'Stratus-{v}.zip'");(p/'package.py').write_text(s)
(w/'version-choice.json').write_text(json.dumps({'candidate_version':v,'development_evidence_prefix':'1.6.13','reason':'Native-water mode and transparent-solid optics are substantial user-visible additions. Use a minor-version release candidate, rather than a patch or claiming the full roadmap milestone passed; known waterline and remaining visual/compatibility acceptance stay pending.'},indent=2)+'\n')
print(v)

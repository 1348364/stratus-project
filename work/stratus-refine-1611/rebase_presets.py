from pathlib import Path
import re,json
w=Path('work/stratus-refine-1611');p=Path('outputs/Stratus');options=p/'shaders/core/options.glsl';old=(w/'baseline/shaders/core/options.glsl').read_text();text=options.read_text();assert text==old
pattern=r'^#define\s+(\w+)\s+(\S+)\s*//\s*\[([^]]+)\]'
def inventory(s):
 d={k:{'default':v,'choices':c.split()} for k,v,c in re.findall(pattern,s,re.M)}
 for k,v,c in re.findall(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^]]+)\]',s):d[k]={'default':v.strip(),'choices':c.split()}
 return d
before=inventory(old);saved={r.split('=',1)[0]:r.split('=',1)[1] for r in (w/'Main-before-Stratus-1.6.10.zip.txt').read_text().splitlines() if '=' in r and not r.startswith('#')};assert set(saved)<=before.keys()
for k,v in saved.items():
 assert v in before[k]['choices'],(k,v)
 text=re.sub(r'(^#define\s+'+re.escape(k)+r'\s+)\S+',lambda m:m[1]+v,text,flags=re.M)
text=text.replace('// Balanced defaults retain physical water optics; High restores the finest sampling.','// Reference defaults use the explicitly approved latest Main tuning.\n// All quality choices remain available; higher presets retain detailed optics.')
options.write_text(text);after=inventory(text);assert len(after)==62 and set(before)==set(after)
for k in before:assert before[k]['choices']==after[k]['choices']
quality=['WATER_RENDER_QUALITY','ATMOSPHERE_QUALITY','CLOUD_LAYERS','MIST_DETAIL','REFLECTION_MODE','REFRACTION_QUALITY'];visual={k:v['default'] for k,v in after.items() if k not in quality};reference={k:after[k]['default'] for k in quality}
levels={'FAST':['0','0','1','1','0','0'],'BALANCED':['1','1','1','2','0','0'],'REFERENCE':[reference[k] for k in quality],'HIGH':['2','2','3','3','2','2']}
props=p/'shaders/shaders.properties';s=props.read_text();profiles={}
for name,vals in levels.items():
 assignments={**dict(zip(quality,vals)),**visual};profiles[name]=assignments
 line='profile.'+name+'='+' '.join(k+':'+v for k,v in assignments.items());s,n=re.subn(r'^profile\.'+name+r'=.*$',lambda m:line,s,flags=re.M);assert n==1
props.write_text(s)
for key in quality:
 nums=[int(profiles[n][key]) for n in ['FAST','BALANCED','REFERENCE','HIGH']];assert nums==sorted(nums),(key,nums)
for name,profile in profiles.items():assert {k:profile[k] for k in visual}==visual
assert profiles['REFERENCE']=={k:v['default'] for k,v in after.items()}
changed={k:{'before':before[k]['default'],'after':v['default']} for k,v in after.items() if before[k]['default']!=v['default']};related=sorted(set(changed)|set(quality))
policy={'version':'1.6.11','reset_related_overrides':related,'visual_defaults':visual,'reference_quality_defaults':reference,'classifications':[{'change':'Explicitly approved latest Main visual baseline','type':'visual','presets':list(profiles),'defaults':visual},{'change':'Explicitly approved Main quality as Reference with ordered lower/higher presets','type':'visual_and_performance','presets':list(profiles),'per_preset_quality':{n:{k:pr[k] for k in quality} for n,pr in profiles.items()},'user_approved_reference_quality_rebase':True,'optimisation_speedup_claim':False}],'migration_rule':'For this approved preset rebase, reset only changed visual-default keys and the six quality keys to the captured Main Reference defaults. Carry unrelated latest overrides; never overwrite old or existing new-version settings. Existing controls and allowed values remain.'}
(p/'RELEASE-POLICY.json').write_text(json.dumps(policy,indent=2)+'\n');script=p/'package.py';s=script.read_text();assert 'Stratus-1.6.10.zip' in s or 'Stratus-1.6.11.zip' in s;script.write_text(s.replace('Stratus-1.6.10.zip','Stratus-1.6.11.zip'))
report={'controls':62,'all_IDs_ranges_menu_paths_preserved':True,'source_defaults_changed_by_user_approval':changed,'reference_equals_all_62_effective_captured_Main_values':True,'visual_options_shared_across_all_profiles':len(visual),'quality_options_ordered_per_profile':{n:{k:pr[k] for k in quality} for n,pr in profiles.items()},'same_Reference_default_definition_in_source_and_profile':True,'related_migration_keys':related,'all_higher_quality_choices_still_available':True,'rebase_is_not_an_optimisation_speedup':True};(w/'option-audit.json').write_text(json.dumps(report,indent=2)+'\n');(w/'reference-defaults.json').write_text(json.dumps({k:v['default'] for k,v in after.items()},indent=2)+'\n');print(json.dumps(report,indent=2))

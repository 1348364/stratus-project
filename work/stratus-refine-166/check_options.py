from pathlib import Path
import json,re
w=Path(__file__).parent;before=w/'baseline/shaders';after=Path('outputs/Stratus/shaders')
def inventory(root):
 source=(root/'core/options.glsl').read_text()
 opts={m[0]:{'default':m[1].strip(),'values':m[2].split()} for m in re.findall(r'^#define\s+(\w+)\s+(.*?)\s*//\s*\[([^\]]+)\]',source,re.M)}
 opts.update({m[0]:{'default':m[1].strip(),'values':m[2].split()} for m in re.findall(r'^const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]',source,re.M)})
 props=(root/'shaders.properties').read_text();menus=[l for l in props.splitlines() if l.startswith(('screen','sliders=','profile.'))]
 lang=dict(l.split('=',1) for l in (root/'lang/en_us.lang').read_text().splitlines() if '=' in l and l.startswith(('option.','value.','screen.')))
 return {'options':opts,'menus_sliders_profiles':menus,'language':lang}
a=inventory(before);b=inventory(after);assert a['options']==b['options'];assert a['menus_sliders_profiles']==b['menus_sliders_profiles'];assert a['language'].keys()==b['language'].keys()
profile=Path.home()/'Library/Application Support/ModrinthApp/profiles/Minecraft (1)';overrides={}
for line in (profile/'shaderpacks/Stratus-1.6.5.zip.txt').read_text().splitlines():
 if '=' not in line or line.startswith('#'):continue
 key,value=line.split('=',1);assert key in b['options'],key
 choices=b['options'][key]['values'];assert value in choices or any(float(value)==float(c) for c in choices),(key,value)
 overrides[key]=value
changes={k:{'before':a['language'][k],'after':v} for k,v in b['language'].items() if a['language'][k]!=v}
result={'before_version':'1.6.5','after_version':'1.6.6','option_count':len(b['options']),'ids_defaults_allowed_values_identical':True,'menus_sliders_presets_identical':True,'all_language_keys_preserved':True,'removed_hidden_or_narrowed_controls':[],'changed_labels_tooltips':changes,'Main_saved_overrides_preserved_and_valid':overrides,'before':a,'after':b}
(w/'option-inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(len(b['options']),'options preserve IDs/defaults/values; all menus/sliders/presets and language keys retained;',len(overrides),'saved overrides valid.')

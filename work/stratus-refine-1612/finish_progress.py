from pathlib import Path
from urllib.parse import unquote
import re,json,hashlib
w=Path(__file__).parent;d=Path('work/Custom instructions');batch=d/'IN-PROGRESS/7a6a15fb-dcb6-4313-94d3-7a32fb13dd79';count=0
for p in [batch/'CHANGES.md',d/'TASK.md',d/'CHANGE-LOG.md',d/'COMPLETED-CHANGES.md']:
 s=p.read_text()
 if p.name=='CHANGE-LOG.md':s=s.split('## 22 October 2026 — Stratus 1.6.11')[0]
 if p.name=='COMPLETED-CHANGES.md':s=s.split('### Stratus 1.6.11')[0]
 for ref in re.findall(r'\]\(([^)]+)\)',s):
  if ref.startswith(('http:','https:','#')):continue
  q=unquote(ref.split('#',1)[0].strip('<>'));assert (p.parent/q).exists(),(p,ref);count+=1
assert '[x]' not in (batch/'CHANGES.md').read_text()
assert (d/'CHANGES.md').read_bytes()==(w/'initial-CHANGES.md').read_bytes()
j=json.loads((w/'reconciliation.json').read_text());j.update(local_links_checked=count,no_completed_items_left_in_active_pending=True,partial_waterline_acceptance_retained=True);j['documents'][str(batch/'CHANGES.md')]=hashlib.sha256((batch/'CHANGES.md').read_bytes()).hexdigest();(w/'reconciliation.json').write_text(json.dumps(j,indent=2)+'\n')
progress='''# Batch progress

Status: Stratus1.6.12 delivered/loaded; verified whole-surface tint portion archived. Batch remains partially unfinished.

## Resume here
- Source: outputs/Stratus. Release: outputs/Stratus-1.6.12.zip (SHA2565232c270a31de108ba862135e0f4a6bedaba16e011c2ec1b44a651f7a50c44e2).
- Evidence: work/stratus-refine-1612/final-audit.json, reconciliation.json, changes.diff, package-checks.json; outputs/Stratus-1.6.12-install.json and visual-checks/index.html.
- Changed runtime: lake composition, new water-surface helper, WATER_TEXTURE tooltip. Existing atlas pattern/biome colour multiply completed water optics with no distance cutoff, extra reads/pass, opacity change or blur. All62 controls/defaults/ranges/menu paths and approved quality/preset values retained.
- Frozen delta repeats already completed1.6.11 reconciliation; no duplicate implementation. No snapshot conflicts. Shared next unsent CHANGES.md unchanged. Frozen .bridge and batch TASK snapshot untouched.

## Evidence and remaining work
- Passed768 native pairs;192 actual surface-GPU samples;ten underwater cases;ten installer checks;four actual Iris62-option profile maps; source/archive/QA/install byte equivalence. Actual release loaded in Main/normal Terrain Lab with Reference/zero overrides.
-25 actual Main images reviewed: matched old/zero/half/max river, close/grazing pairs,90° downward, underwater exit, all presets, wood/waterfall/glass/particle fixtures and waterline baseline comparison. Unfocused captures are visual evidence, never FPS proof.
- Remaining waterline acceptance: feet164.5,61.24,40.5/yaw0/pitch0 shows a rectangular tint band over sky/treetops on BOTH1.6.11 and1.6.12. Unresolved pre-existing defect; not labelled clean. Next: capture actual water-exit/depth metadata near the clip plane at this reproducible camera, establish the cause, then repair/test transition while preserving submerged-segment rules. See waterline-issue.json. Kept in active batch.
- Existing deferred FPS/approximately60FPS and actual FPS gate integration remain pending; do not resume until requested. Original historical pole/leaf and relevant distant-foliage fallback contexts also remain pending.
- Original current-session camera/HUD/pause/flight and exact initial daylight/weather flags/timers restored. Four temporary glass fixture blocks read back as original source water. Old block-setter restoration helper failed; existing bounded command recovery succeeded, evidence retained. All helpers stopped; own verified Main QA files removed. Current release left selected.
- TASK.md reconciled without weakening waterline target. Only verified tint portion in COMPLETED-CHANGES.md; unfinished acceptance stays in this batch. CHANGE-LOG.md records full evidence/limits.
''';(batch/'PROGRESS.md').write_text(progress)
print(count,'links verified. Durable progress updated; next unsent queue unchanged.')

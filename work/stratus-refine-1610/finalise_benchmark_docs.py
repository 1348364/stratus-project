from pathlib import Path
import json
w=Path('work/stratus-refine-1610');p=Path('outputs/Stratus');perf=json.loads((w/'performance-summary.json').read_text());assert perf['focused_comparison_verified']
c=json.loads((p/'CHECKS.json').read_text());c['performance']=perf;c['status']='Finite source/native GPU, Main visual and focused full-Reference checks completed. Approximately60FPS target and remaining scene acceptance stay pending.';c['limits']=[x for x in c['limits'] if 'No accepted focused' not in x];c['limits'].insert(0,'Full Reference river19.6154→20.1645FPS; forest17.7699→18.0673FPS. Small finite gains, far below requested60FPS; no general guarantee.');(p/'CHECKS.json').write_text(json.dumps(c,indent=2)+'\n')
f=p/'README.txt';s=f.read_text();start=s.index('PERFORMANCE AND LIMITS\n');s=s[:start]+'''FOCUSED FULL-REFERENCE RESULTS AND LIMITS
1440x842 / render12 / simulation8 / same six Reference quality selections,
weather clear / time6000 / fixed matched cameras / saved VSync true / cap70.
Dynamic FPS FOCUSED; vanilla limiter NONE/cap70 confirmed every5seconds.
River, two30-second samples per build: baseline19.6154 / new20.1645 FPS.
Forest, one30-second sample per build: baseline17.7699 / new18.0673 FPS.
All six samples had zero focus-loss polls. Small finite gains (~2.8% river,
~1.7% forest) are not a general gameplay guarantee. Reference60FPS remains
unmet and pending. Earlier~56FPS samples used different saved quality choices.
No native GPU probe/profiler ran concurrently. Temporary activity resets left
saved options unchanged and were stopped; original client state was restored.
Screen-space misses, finite cloud range and approximate film/atmosphere remain.
Occupied-cloud interior, clearer independent cirrus/sunset, exact historical
pole/leaf views and exhaustive scene/preset/mod/motion coverage remain pending.
See VALIDATION.txt, CHECKS.json and Stratus-1.6.10-performance.json in outputs/.
''';f.write_text(s)
f=p/'VALIDATION.txt';s=f.read_text();start=s.index('Performance remains pending:');s=s[:start]+'''Focused full-Reference performance was subsequently tested after the user
foregrounded Main. Six30-second samples, zero focus-loss polls,1440x842,
render12/simulation8, matched Reference settings/cameras/weather clear/time6000.
Dynamic FPS remained FOCUSED, vanilla limiter NONE/cap70; temporary activity
resets every5seconds changed no saved setting. River pooled two samples/build:
19.6154 before /20.1645 after FPS. Forest one/build:17.7699 /18.0673 FPS.
The small finite improvements do not establish a general speedup or60FPS.
The target stays pending. Raw samples and conditions are in the external
versioned performance summary and work/stratus-refine-1610. No quality cuts or
concurrent native GPU probes/profiler. Prior unfocused diagnostics remain
separately labelled. Original client state restored and both helpers stopped.
Exact historical pole/leaf scenes, clearer cloud acceptance and exhaustive
presets/mods/moving-camera coverage remain pending in the project queue.
''';f.write_text(s)
f=p/'IN-GAME-TEST.txt';s=f.read_text();s+='''
RECORDED FULL-REFERENCE RESULT
Matched focused30-second samples completed with no focus loss and NONE/cap70.
River19.6154→20.1645 FPS (two samples/build), forest17.7699→18.0673 (one/build).
The approximately60FPS target remains unmet. Continue measured optimisation
without quality cuts; do not retest merely to recertify unchanged source.
''';f.write_text(s)
# Update the existing evidence writer to include the completed focus follow-up.
f=w/'finish_evidence.py';s=f.read_text();s=s.replace("'fixture_helper_stopped':(w/'world-fixture-stopped.txt').is_file(),", "'fixture_helper_stopped':(w/'world-fixture-stopped.txt').is_file(),'focused_benchmark_driver_stopped':(w/'benchmark-driver-stopped.txt').is_file(),'focused_activity_helper_stopped':(w/'final-activity-stopped.txt').is_file(),")
s=s.replace("'focused_FPS_verified':False", "'focused_FPS_verified':True,'target_60_FPS_verified':False,'performance_evidence':'outputs/Stratus-1.6.10-performance.json','initial_migration_receipt':'work/stratus-refine-1610/pre-focused-benchmark-install.json'")
s=s.replace("'performance':'No accepted focused Reference sample; 60FPS remains pending.'", "'performance':'Focused full-Reference river19.6154→20.1645FPS, forest17.7699→18.0673FPS. Small finite gains;60FPS remains unmet.'")
s=s.replace('The 60FPS Reference target remains pending. The game was unfocused and the Mac locked. GPU diagnostics are not FPS proof.', 'The 60FPS Reference target remains unmet. After the user foregrounded Main, matched focused full-Reference tests measured river19.6→20.2FPS and forest17.8→18.1FPS. Unfocused GPU diagnostics remain separate.')
s=s.replace('<a href="manifest.json">Capture manifest</a>', '<a href="../Stratus-1.6.10-performance.json">Focused FPS results</a> · <a href="manifest.json">Capture manifest</a>')
f.write_text(s)
print('Updated release docs with six accepted focused samples; runtime source unchanged.')

"""Retain the optical regressions and add boundary-physics integration cases."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()))
source=Path('work/stratus-check/probe_153.py').read_text()
source=source.replace("o=w/'probe-153'","o=w/'probe-160'").replace("w/'probe_153.c'","w/'probe_160.c'")
source=source.replace("'medium','water-path'","'medium','water-interface','water-path'")
addition='''
s+='''+repr('''
WaterBoundary boundaryProbe(float angle,bool submerged){
 float a=radians(angle);vec3 incident=vec3(sin(a),0.,-cos(a));
 return waterBoundary(incident,vec3(0,0,1),submerged);
}
vec3 transmittedProbe(float angle,bool submerged){return boundaryProbe(angle,submerged).transmitted;}
vec3 reciprocalProbe(){
 WaterBoundary incoming=boundaryProbe(30.,false);
 WaterBoundary outgoing=waterBoundary(-incoming.transmitted,-incoming.normal,true);
 return abs(outgoing.transmitted+incoming.incident);
}
vec3 orientationProbe(){
 WaterBoundary a=waterBoundary(vec3(.5,0,-.8660254),vec3(0,0,1),true);
 WaterBoundary b=waterBoundary(vec3(.5,0,-.8660254),vec3(0,0,-1),true);
 return abs(a.transmitted-b.transmitted);
}
vec3 submergedSceneProbe(int side){
 float distance;vec4 h=traceOpticalScene(vec3(0,0,-2),normalize(vec3(0,.2,-1)),vec3(0,-1,0),side,0,100.,false,distance);
 return vec3(h.a,distance,h.r);
}
''')+'''
cases += [
 ('boundary_submerged_normal','transmittedProbe(0.,true)',1),
 ('boundary_submerged_30deg','transmittedProbe(30.,true)',1),
 ('boundary_above_45deg','transmittedProbe(45.,false)',1),
 ('boundary_below_critical','vec3(float(boundaryProbe(48.,true).totalReflection))',1),
 ('boundary_above_critical','vec3(float(boundaryProbe(50.,true).totalReflection))',1),
 ('boundary_TIR_no_transmission','transmittedProbe(60.,true)',1),
 ('boundary_TIR_full_weight','vec3(waterReflectionWeight(boundaryProbe(60.,true)))',1),
 ('boundary_reciprocity_error','reciprocalProbe()',1),
 ('boundary_orientation_error','orientationProbe()',1),
 ('submerged_air_receiver','submergedSceneProbe(-1)',1),
 ('submerged_wrong_side_rejected','submergedSceneProbe(1)',1),
]
'''
source=source.replace("s+='uniform float probeDistance;",addition+"\ns+='uniform float probeDistance;")
exec(compile(source,'probe_160_generated.py','exec'))

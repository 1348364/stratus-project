from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/stratus-check').resolve()));from prepare import expand,adapt
w=Path(__file__).parent;root=Path('outputs/Stratus/shaders').resolve()
base='#version 330 compatibility\n#define DIMENSION_TYPE 0\n'+expand(root/'core/options.glsl',root)+expand(root/'core/frame.glsl',root)
base+='''
vec3 atmosphericColour(){return vec3(.5);}
float solarDaylight(){return 1.;}
float cloudPhase(float c){return 1.;}
float cloudSunTransmission(vec3 p){return 1.;}
vec2 layeredCloudSample(vec3 p,bool detailed,bool upper){
 float h=(p.y-256.)/18.;
 return vec2(.0004*exp(-h*h)*(1.+.6*sin(p.z*.025)),.5);
}
'''
for name,path in [('before',w/'baseline/shaders/core/ceiling.glsl'),('after',root/'core/ceiling.glsl')]:
 s=path.read_text();s=s[s.index('vec4 marchSingleCloud('):s.index('vec4 marchCloudLayer(')]
 source=base+s+'''\nuniform float probeAngle;uniform int probeSteps;layout(location=0)out vec4 result;void main(){result=marchSingleCloud(vec3(4096,257.62,4096),vec3(0,sin(probeAngle),cos(probeAngle)),7000.,probeSteps,false,false);}\n'''
 (w/('cloud-'+name+'.fsh')).write_text(adapt(source,'.fsh'))
print('Prepared actual before/after cloud integrators with an analytic density field.')

"""Probe actual fog/light functions without changing delivered shader files."""
from pathlib import Path
from prepare import expand, override, adapt

work = Path('work/stratus-check')
output = work / 'air-probe'
output.mkdir(exist_ok=True)
(output / 'screen.vsh').write_text('''#version 330 core
void main() {
    vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
    gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);
}
''')
for name, root in [('previous', work / 'prior-1.0.4/shaders'),
                   ('current', Path('outputs/Stratus/shaders'))]:
    source = '#version 330 compatibility\n#define DIMENSION_TYPE 0\n'
    for library in ('options.glsl', 'frame.glsl', 'ceiling.glsl', 'air.glsl', 'diffuse.glsl'):
        source += expand(root / 'core' / library, root) + '\n'
    source += '''
uniform float probeDistance;
uniform float probeSky;
uniform int probeMode;
layout(location = 0) out vec4 probePixel;
void main() {
    vec3 point = vec3(0.0, 0.0, -probeDistance);
    vec3 radiance = probeMode == 0
        ? throughAir(vec3(0.20, 0.30, 0.40), point, probeSky)
        : diffuseRadiance(vec3(0.5), vec3(0.8), probeSky, vec3(0.0, 1.0, 0.0), 1.0, point);
    probePixel = vec4(radiance, valleyOpacity(point, probeSky));
}
'''
    # Compare with the user's saved ambient setting, rather than the old default.
    if name == 'previous':
        source = override(source, {'SKY_AMBIENT': '1.20'})
    (output / (name + '.fsh')).write_text(adapt(source, '.fsh'))
print('Prepared probes from actual previous/current shader functions.')

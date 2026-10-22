"""Verify and preserve real Minecraft/Iris smoke-test evidence."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

pack = Path('outputs/Stratus')
game = Path('work/minecraft-smoke')
log = (game / 'logs/latest.log').read_text()
launch_log = Path('work/stratus-check/minecraft-launch-1.0.6.log').read_text()
driver_diagnostics = [line for line in launch_log.splitlines() if 'UNSUPPORTED (log once)' in line]
assert 'Using shaderpack: Stratus-1.0.6.zip' in log
assert 'Profile: REFERENCE' in log
assert 'ShaderCheck joined the game' in log
assert 'OpenGL Renderer: Apple M1' in log
runtime = log[log.index('Creating pipeline for dimension minecraft:overworld'):]
errors = [line for line in runtime.splitlines() if '/ERROR]' in line]
failures = re.findall(
    r'^.*(?:ShaderCompileException|Failed to create shader|Shader compilation failed|'
    r'Invalid framebuffer|OpenGL Error|GL_INVALID|ArrayIndexOutOfBoundsException|'
    r'undeclared identifier).*$', runtime, re.M | re.I)
assert not errors, errors
assert not failures, failures
for program in ('deferred', 'composite', 'final', 'sodium:chunk_shader_for_terrain',
                'sodium:chunk_shader_for_terrain_cutout', 'sodium:chunk_shader_for_translucent'):
    assert f'Program link log for {program}:' in runtime
assert 'during a single frame' in runtime
assert 'enableShaders=true' in (game / 'config/iris.properties').read_text()
exit_record = json.loads(Path('work/stratus-check/minecraft-exit-1.0.6.json').read_text())
assert exit_record['exit_code'] == 143 and exit_record['signal'] == 'SIGTERM'

unrelated = []
if 'Failed to fetch user properties' in log or 'Failed to fetch Realms' in log:
    unrelated.append('Offline test identity authentication failures')
if 'Error parsing option' in log:
    unrelated.append('Invalid game preference at startup')
if 'Missing data pack' in log:
    unrelated.append('Missing optional datapacks from copied world')
source_hashes = {}
with zipfile.ZipFile(game / 'shaderpacks/Stratus-1.0.6.zip') as tested:
    for source in sorted((pack / 'shaders').rglob('*')):
        if not source.is_file() or source.suffix not in {'.vsh', '.fsh', '.glsl', '.properties', '.lang'}:
            continue
        relative = source.relative_to(pack).as_posix()
        assert tested.read(relative) == source.read_bytes(), relative
        source_hashes[relative] = hashlib.sha256(source.read_bytes()).hexdigest()

result = {
    'passed': True, 'date': '2026-10-16', 'pack': 'Stratus-1.0.6.zip',
    'minecraft': '1.21.11', 'iris': '1.10.8', 'sodium': '0.8.14',
    'fabric_loader': '0.19.5', 'java': 21, 'gpu': 'Apple M1',
    'opengl': '4.1 Metal - 91.7', 'preset': 'Reference', 'dimension': 'Overworld',
    'game_directory': 'Isolated workspace test client', 'world': 'Copied local singleplayer world',
    'rendered_frame_evidence': 'Dynamic Transforms UBO capacity changed during a single frame',
    'shader_errors': len(errors) + len(failures),
    'unused_shader_interface_warnings': True,
    'server_tick_lag_warning': "Can't keep up!" in runtime,
    'native_driver_diagnostics': driver_diagnostics,
    'test_process_exit': exit_record,
    'source_hashes': source_hashes,
    'limits': 'Smoke test only. No visual reference comparison, FPS benchmark, other presets or dimensions.',
    'unrelated_startup_messages': unrelated,
}
evidence = Path('work/stratus-check/minecraft-smoke-result.json')
evidence.write_text(json.dumps(result, indent=2) + '\n')
shutil.copy2(game / 'logs/latest.log', 'work/stratus-check/minecraft-1.0.6-reference.log')
extract = [line for line in log.splitlines() if any(term in line for term in (
    'Loading Minecraft ', 'Profile: REFERENCE', 'Using shaderpack:', 'OpenGL Vendor:',
    'OpenGL Renderer:', 'OpenGL Version:', 'ShaderCheck joined the game',
    'Creating pipeline for dimension', 'Program link log for deferred:',
    'Program link log for composite:', 'Program link log for final:',
    'Program link log for sodium:', 'during a single frame', 'Stopping server'))]
report = (
    'STRATUS 1.0.6 - REAL MINECRAFT / IRIS SMOKE TEST\n16 October 2026\n\n'
    'PASS: default Reference preset loaded in a real Minecraft 1.21.11 Overworld.\n'
    'Iris 1.10.8 / Sodium 0.8.14 / Java 21 / Apple M1 / OpenGL 4.1.\n'
    'Shader compile/runtime errors from pipeline creation to test end: 0.\n'
    f'All {len(source_hashes)} tested shader/config files match the delivered source byte for byte.\n'
    'Test client used a separate gameDir and copied local world, then was shut down.\n'
    'No online account credentials were used.\n\n'
    'Warnings remain: unused shader inputs/varyings from Iris/Apple linking.\n'
    'Unrelated startup messages: ' + '; '.join(unrelated) + '.\n'
    'These did not prevent rendering. FPS was not measured.\n'
    + ('Server tick-lag warnings were logged.\n' if "Can't keep up!" in runtime else '')
    + ('Native driver diagnostics: ' + '; '.join(driver_diagnostics) + '\n' if driver_diagnostics else '')
    + '\n'
    'Limits: this verifies real Iris loading and a rendered-world smoke test.\n'
    'It does not verify reference-image appearance, every setting, night, weather,\n'
    'underwater, other dimensions, other presets or FPS. Timestamps do not\n'
    'establish uninterrupted rendering duration.\n\n'
    'EXTRACTED REAL GAME LOG\n' + '\n'.join(extract) + '\n'
)
(pack / 'IN-GAME-TEST.txt').write_text(report)
print(report)

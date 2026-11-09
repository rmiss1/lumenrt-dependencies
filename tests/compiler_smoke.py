"""Verify release executables and link an original GLSL module without a Vulkan SDK."""
import hashlib
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import urllib.request
import zipfile

VERSION = '2026.21'
WINDOWS = os.name == 'nt'
ARCHIVE = f'slang-{VERSION}-' + ('windows-x86_64.zip' if WINDOWS else 'linux-x86_64-glibc-2.27.zip')
ARCHIVE_HASH = ('4b6f509e73397175ed36a341beb7ad15f4fff5feaf5f6d95fecf896c0d86b8de' if WINDOWS
                else '9cf13cad3fdb4d75eea14f546b5f63c406b68891bb7d1742ea8b029bde6c2b29')
EXECUTABLE = 'slangc.exe' if WINDOWS else 'slangc-linux-x64'
EXE_HASH = ('71d56bcc90709700b318413bfced07a4b7378c76b2bbc539e89f2d2c90b1e5f8' if WINDOWS
            else '769db0bbee754f4f534f725055c74da113f9cc36857c86e581f6fb52a62c30aa')

def download(url, path, expected):
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError(f'SHA-256 mismatch: {url}')
    path.write_bytes(data)

with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    archive = root / 'upstream.zip'
    download(f'https://github.com/shader-slang/slang/releases/download/v{VERSION}/{ARCHIVE}', archive, ARCHIVE_HASH)
    with zipfile.ZipFile(archive) as package:
        if WINDOWS:
            for name in ['slang.dll', 'slang-compiler.dll', 'slang-glsl-module.dll', 'slang-glslang.dll']:
                (root / name).write_bytes(package.read('bin/' + name))
        else:
            (root / 'lib').mkdir()
            for name in [f'libslang-compiler.so.0.{VERSION}', f'libslang-glsl-module-{VERSION}.so', f'libslang-glslang-{VERSION}.so']:
                (root / 'lib' / name).write_bytes(package.read('lib/' + name))
            (root / 'lib/libslang-compiler.so').write_bytes((root / f'lib/libslang-compiler.so.0.{VERSION}').read_bytes())
    executable = root / ('slangc.exe' if WINDOWS else 'slangc')
    download(f'https://github.com/rmiss1/lumenrt-dependencies/releases/download/slangc-v{VERSION}/{EXECUTABLE}', executable, EXE_HASH)
    executable.chmod(0o700)
    env = os.environ.copy()
    env['PATH'] = os.path.join(env.get('SystemRoot', 'C:\\Windows'), 'System32') if WINDOWS else '/usr/bin:/bin'
    if not WINDOWS:
        env['LD_LIBRARY_PATH'] = str(root / 'lib')
        env.pop('LD_PRELOAD', None)
    def run(*args):
        result = subprocess.run([str(executable), *args], cwd=root, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, check=True)
        print(result.stdout, end='')
        return result.stdout
    if VERSION not in run('-version'):
        raise RuntimeError('Unexpected compiler version')
    (root / 'live_material.glsl').write_text('''#version 450
#extension GL_EXT_nonuniform_qualifier : require
layout(set=2,binding=0,std140) uniform OriginalInput { vec4 color; } inputs[];
vec4 materialZero(uint draw) { return inputs[nonuniformEXT(draw)].color; }
''')
    (root / 'material_test.rgen.slang').write_text('''import live_material;
[[vk::binding(0,0)]] RWStructuredBuffer<float4> result;
[shader("raygeneration")]
void main() { result[DispatchRaysIndex().x] = materialZero(DispatchRaysIndex().y); }
''')
    run('live_material.glsl', '-module-name', 'live_material', '-allow-glsl', '-emit-ir', '-I', str(root), '-o', 'live_material.slang-module')
    run('material_test.rgen.slang', '-I', str(root), '-allow-glsl', '-target', 'spirv', '-profile', 'spirv_1_5', '-matrix-layout-column-major', '-entry', 'main', '-g0', '-o', 'linked.spv')
    code = (root / 'linked.spv').read_bytes()
    words = struct.unpack(f'<{len(code)//4}I', code)
    if words[0] != 0x07230203:
        raise RuntimeError('Invalid SPIR-V magic')
    offset = 5
    raygen = False
    while offset < len(words):
        count, opcode = words[offset] >> 16, words[offset] & 0xffff
        if count == 0 or offset + count > len(words):
            raise RuntimeError('Invalid SPIR-V instruction')
        if opcode == 15 and words[offset + 1] == 5313:
            raygen = True
        offset += count
    if not raygen:
        raise RuntimeError('No raygeneration entry point')
    print(f'PASS: {EXECUTABLE}, original GLSL module linked to {len(code)} bytes of raygeneration SPIR-V')

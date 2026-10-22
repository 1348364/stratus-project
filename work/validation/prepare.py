#!/usr/bin/env python3
"""Prepare Iris GLSL for native macOS offline compile/link checks.

This checks syntax and varying compatibility after include expansion and a
legacy-builtin shim. It does not emulate Iris shader transforms or render Minecraft.
The delivered pack is never modified.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
SHIM = {
    "gl_Vertex": ("vec4", "in"),
    "gl_Color": ("vec4", "in"),
    "gl_Normal": ("vec3", "in"),
    "gl_MultiTexCoord0": ("vec4", "in"),
    "gl_MultiTexCoord1": ("vec4", "in"),
    "gl_MultiTexCoord2": ("vec4", "in"),
    "gl_ModelViewMatrix": ("mat4", "uniform"),
    "gl_ProjectionMatrix": ("mat4", "uniform"),
    "gl_ModelViewProjectionMatrix": ("mat4", "uniform"),
    "gl_NormalMatrix": ("mat3", "uniform"),
    "gl_TextureMatrix": ("mat4", "uniform"),
}
INCLUDE = re.compile(r'^\s*#include\s+"([^"]+)"\s*$', re.M)
DEFINE = re.compile(r"^(\s*)(?://\s*)?#define\s+(\w+)([^\n]*)$", re.M)


def expand(path: Path, shader_root: Path, active=()) -> str:
    path = path.resolve()
    if path in active:
        raise RuntimeError(f"Recursive include: {path}")
    if not path.is_relative_to(shader_root.resolve()):
        raise RuntimeError(f"Include escapes shader pack: {path}")
    source = path.read_text()
    def replace(match):
        ref = match.group(1)
        target = shader_root / ref[1:] if ref.startswith("/") else path.parent / ref
        return f"\n// BEGIN INCLUDE {ref}\n" + expand(target, shader_root, active + (path,)) + f"\n// END INCLUDE {ref}\n"
    return INCLUDE.sub(replace, source)


def override(source: str, values: dict[str, str | bool]) -> str:
    seen = set()
    def replace(match):
        indent, name, rest = match.groups()
        if name not in values:
            return match.group(0)
        seen.add(name)
        value = values[name]
        comment = " // " + rest.split("//", 1)[1] if "//" in rest else ""
        if isinstance(value, bool):
            return f"{indent}{'' if value else '//'}#define {name}{comment}"
        return f"{indent}#define {name} {value}{comment}"
    source = DEFINE.sub(replace, source)
    def replace_constant(match):
        name = match.group(1)
        if name not in values:
            return match.group(0)
        return f'const float {name} = {values[name]};'
    return re.sub(r'const float (\w+)\s*=\s*[^;]+;', replace_constant, source)


def adapt(source: str, stage: str) -> str:
    source = re.sub(r"#version\s+330\s+compatibility", "#version 330 core", source)
    declarations = ['#define RGBA16F 34842', '#define RGBA8 32856']
    for name, (kind, qualifier) in SHIM.items():
        if re.search(r"\b" + name + r"\b", source):
            shim_name = "shim_" + name[3:]
            source = re.sub(r"\b" + name + r"\b", shim_name, source)
            suffix = "[8]" if name == "gl_TextureMatrix" else ""
            declarations.append(f"{qualifier} {kind} {shim_name}{suffix};")
    if re.search(r"\bftransform\s*\(", source):
        if not any("shim_Vertex" in d for d in declarations):
            declarations.append("in vec4 shim_Vertex;")
        if not any("shim_ModelViewProjectionMatrix" in d for d in declarations):
            declarations.append("uniform mat4 shim_ModelViewProjectionMatrix;")
        source = re.sub(r"\bftransform\s*\(\s*\)", "(shim_ModelViewProjectionMatrix * shim_Vertex)", source)
    # Deprecated texture names have core equivalents with the same signatures.
    source = re.sub(r"\btexture2D\b", "texture", source)
    source = re.sub(r"\btexture2DLod\b", "textureLod", source)
    # Legacy color outputs are only shimmed if actually present in the pack.
    if "gl_FragColor" in source:
        source = source.replace("gl_FragColor", "shim_FragColor")
        declarations.append("layout(location = 0) out vec4 shim_FragColor;")
    if "gl_FragData" in source:
        source = source.replace("gl_FragData", "shim_FragData")
        declarations.append("layout(location = 0) out vec4 shim_FragData[8];")
    lines = source.splitlines()
    version = next(i for i, line in enumerate(lines) if line.lstrip().startswith("#version"))
    lines[version + 1:version + 1] = declarations
    return "\n".join(lines) + "\n"


def profiles(shader_root: Path) -> dict[str, dict[str, str | bool]]:
    path = shader_root / "shaders.properties"
    if not path.exists():
        return {}
    source = path.read_text().replace("\\\n", " ")
    raw = {}
    for line in source.splitlines():
        match = re.match(r"\s*profile\.(\w+)\s*=\s*(.*?)\s*$", line)
        if match:
            raw[match.group(1)] = match.group(2).split()
    def resolve(name, active=()):
        if name in active:
            raise RuntimeError("Profile cycle")
        result = {}
        for token in raw[name]:
            if token.startswith("profile."):
                result.update(resolve(token.split(".", 1)[1], active + (name,)))
            elif token.startswith("program.") or token.startswith("!program."):
                continue
            elif ":" in token:
                key, value = token.split(":", 1)
                result[key] = value
            elif token.startswith("!"):
                result[token[1:]] = False
            else:
                result[token] = True
        return result
    return {name: resolve(name) for name in raw}


def option_extremes(shader_root: Path):
    low, high = {}, {}
    properties = shader_root / "shaders.properties"
    menu_options = set()
    if properties.exists():
        for line in properties.read_text().replace("\\\n", " ").splitlines():
            if re.match(r"\s*screen(?:\.\w+)?\s*=", line):
                menu_options.update(line.split("=", 1)[1].split())
    for path in shader_root.rglob("*"):
        if path.suffix not in {".glsl", ".fsh", ".vsh"}:
            continue
        for match in DEFINE.finditer(path.read_text()):
            _, name, rest = match.groups()
            choices = re.search(r"//\s*\[([^\]]+)\]", rest)
            if choices:
                values = choices.group(1).split()
                low[name], high[name] = values[0], values[-1]
            elif name in menu_options and not rest.split("//", 1)[0].strip():
                low[name], high[name] = False, True
        for match in re.finditer(r'const float (\w+)\s*=\s*([^;]+);\s*//\s*\[([^\]]+)\]', path.read_text()):
            name, default, choices = match.groups()
            values = choices.split()
            low[name], high[name] = values[0], values[-1]
    return {"options-minimum": low, "options-maximum": high} if low else {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", nargs="?", type=Path, default=ROOT / "outputs/Willow-Mist/shaders")
    args = parser.parse_args()
    shader_root = args.pack.resolve()
    # Libraries may use .vsh/.fsh extensions but are not standalone programs.
    vertices = sorted(list(shader_root.glob("*.vsh")) + list(shader_root.glob("world*/*.vsh")))
    if not vertices:
        raise SystemExit(f"No shaders found in {shader_root}")
    variants = {"default": {}, **{f"profile-{name}": values for name, values in profiles(shader_root).items()}, **option_extremes(shader_root)}
    manifest = []
    for name, values in variants.items():
        for vertex in vertices:
            fragment = vertex.with_suffix(".fsh")
            if not fragment.exists():
                raise RuntimeError(f"Missing fragment partner for {vertex}")
            output_paths = []
            for path in (vertex, fragment):
                output = WORK / "expanded" / name / path.relative_to(shader_root)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(adapt(override(expand(path, shader_root), values), path.suffix))
                output_paths.append(str(output))
            manifest.append("\t".join(output_paths))
    (WORK / "pairs.tsv").write_text("\n".join(manifest) + "\n")
    (WORK / "variants.json").write_text(json.dumps(variants, indent=2) + "\n")
    print(f"Prepared {len(manifest)} shader pairs across {len(variants)} variants: {', '.join(variants)}")
    print(f"Manifest: {WORK / 'pairs.tsv'}")
    print("Native checks use compatibility shims; this is not a Minecraft/Iris integration test.")


if __name__ == "__main__":
    main()

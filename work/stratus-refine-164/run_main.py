"""Run a local, isolated Iris integration check using cached installed game files."""
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
BASE = Path.home() / "Library/Application Support/ModrinthApp"
PROFILE = BASE / "profiles/Minecraft (1)"
META = BASE / "meta"
VERSION = "1.21.11-0.19.5"
GAME = PROFILE
WORLD = "StratusTerrainLab"
PACK = "Stratus-1.6.3.zip"
if not (GAME/"saves"/WORLD/"level.dat").is_file():raise FileNotFoundError(WORLD)
natives=META/"natives"/VERSION
version_dir = META / "versions" / VERSION
version = json.loads((version_dir / (VERSION + ".json")).read_text())
classpath = []
for lib in version["libraries"]:
    if lib.get("include_in_classpath") is False:
        continue
    allowed = not lib.get("rules")
    for rule in lib.get("rules", []):
        system = rule.get("os", {})
        match = system.get("name", "osx") == "osx"
        match &= system.get("arch", "aarch64") in ("aarch64", "arm64")
        match &= not rule.get("features")
        if match:
            allowed = rule["action"] == "allow"
    if not allowed:
        continue
    artifact = lib.get("downloads", {}).get("artifact", {})
    relative = artifact.get("path")
    if not relative:
        group, name, number, *classifier = lib["name"].split(":")
        filename = name + "-" + number + ("-" + classifier[0] if classifier else "") + ".jar"
        relative = group.replace(".", "/") + "/" + name + "/" + number + "/" + filename
    path = META / "libraries" / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    classpath.append(str(path))
classpath.append(str(version_dir / (VERSION + ".jar")))
java = META / "java_versions/zulu21.44.17-ca-jre21.0.8-macosx_aarch64/bin/java"
args = [str(java), "-XstartOnFirstThread", "-Xms512M", "-Xmx2048M",
        "-Dfabric.addMods="+str(ROOT/"work/stratus-main-qa/helper/stratus-main-qa.jar"),
        "-Dstratus.qa.work="+str(ROOT/"work/stratus-main-qa"),
        "-Dstratus.qa.authorizedGame="+str(PROFILE),
        "-Djava.library.path=" + str(natives), "-Djna.tmpdir=" + str(natives),
        "-Dorg.lwjgl.system.SharedLibraryExtractPath=" + str(natives),
        "-Dio.netty.native.workdir=" + str(natives),
        "-Dminecraft.launcher.brand=StratusLocalTest", "-Dminecraft.launcher.version=1",
        "-cp", os.pathsep.join(classpath), version["mainClass"],
        "--username", "ShaderCheck", "--version", VERSION,
        "--gameDir", str(GAME), "--assetsDir", str(META / "assets"),
        "--assetIndex", version["assetIndex"]["id"],
        "--uuid", "00000000000000000000000000000001", "--accessToken", "0",
        "--versionType", "release",
        "--quickPlaySingleplayer", WORLD]
(ROOT / "work/stratus-main-qa/test.pid").write_text(str(os.getpid()))
print("Launching Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14", flush=True)
print("Main game directory:", GAME, flush=True)
print("Pack:", PACK, "| local libraries:", len(classpath), flush=True)
os.chdir(GAME)
os.execv(str(java), args)

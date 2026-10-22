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
GAME = ROOT / "work/minecraft-smoke"
PACK = os.environ.get("STRATUS_TEST_PACK", "Stratus-1.4.0.zip")
WORLD = os.environ.get("STRATUS_TEST_WORLD", "StratusCheck")

for name in ("mods", "config", "shaderpacks", "saves"):
    (GAME / name).mkdir(parents=True, exist_ok=True)
for name in ("iris-fabric-1.10.8+mc1.21.11.jar", "sodium-fabric-0.8.14+mc1.21.11.jar"):
    shutil.copy2(PROFILE / "mods" / name, GAME / "mods" / name)
shutil.copy2(ROOT / "outputs" / PACK, GAME / "shaderpacks" / PACK)
world = GAME / "saves" / WORLD
if not world.exists():
    if WORLD != "StratusCheck":
        raise FileNotFoundError(world)
    shutil.copytree(PROFILE / "saves/WOW", world, ignore=shutil.ignore_patterns("session.lock"))
natives = GAME / "natives"
if not natives.exists():
    shutil.copytree(META / "natives" / VERSION, natives)
(GAME / "config/iris.properties").write_text(
    "enableShaders=" + os.environ.get("STRATUS_TEST_SHADERS", "true") + "\nshaderPack=" + PACK + "\ncolorSpace=SRGB\n"
    "enableDebugOptions=false\nallowUnknownShaders=false\n"
    "disableUpdateMessage=true\nmaxShadowRenderDistance=0\n"
)
if not (GAME / "options.txt").exists():
    (GAME / "options.txt").write_text(
        "renderDistance:4\nsimulationDistance:5\nmaxFps:30\n"
        "soundCategory_master:0.0\npauseOnLostFocus:false\n"
        "fullscreen:false\noverrideWidth:854\noverrideHeight:480\n"
        "onboardAccessibility:false\njoinedFirstServer:true\n"
    )

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
        "-Djava.library.path=" + str(natives), "-Djna.tmpdir=" + str(natives),
        "-Dorg.lwjgl.system.SharedLibraryExtractPath=" + str(natives),
        "-Dio.netty.native.workdir=" + str(natives),
        "-Dminecraft.launcher.brand=StratusLocalTest", "-Dminecraft.launcher.version=1",
        "-cp", os.pathsep.join(classpath), version["mainClass"],
        "--username", "ShaderCheck", "--version", VERSION,
        "--gameDir", str(GAME), "--assetsDir", str(META / "assets"),
        "--assetIndex", version["assetIndex"]["id"],
        "--uuid", "00000000000000000000000000000001", "--accessToken", "0",
        "--versionType", "release", "--width", os.environ.get("STRATUS_TEST_WIDTH","854"), "--height", os.environ.get("STRATUS_TEST_HEIGHT","480"),
        "--quickPlaySingleplayer", WORLD]
(GAME / "test.pid").write_text(str(os.getpid()))
print("Launching Minecraft 1.21.11 / Iris 1.10.8 / Sodium 0.8.14", flush=True)
print("Isolated game directory:", GAME, flush=True)
print("Pack:", PACK, "| local libraries:", len(classpath), flush=True)
os.chdir(GAME)
os.execv(str(java), args)

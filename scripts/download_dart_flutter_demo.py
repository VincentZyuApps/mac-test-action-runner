import json
import os
import subprocess
import time
import urllib.request
import platform
from pathlib import Path

REPO = "VincentZyuApps/dart-flutter-demo"


def get_latest_release():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def detect_arch():
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "x64"
    elif machine in ["arm64", "aarch64"]:
        return "arm64"
    else:
        raise RuntimeError(f"Unsupported arch: {machine}")


def run(cmd, **kwargs):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(f"stderr: {result.stderr.strip()}")
    return result


def main():
    release = get_latest_release()
    tag = release["tag_name"]
    version = tag.lstrip("v")
    arch = detect_arch()

    dmg_pattern = f"dart-flutter-demo-showcase-macos-{arch}-v{version}.dmg"

    download_url = None
    for asset in release["assets"]:
        if asset["name"] == dmg_pattern:
            download_url = asset["browser_download_url"]
            break

    if not download_url:
        print(f"Asset '{dmg_pattern}' not found. Available assets:")
        for asset in release["assets"]:
            print(f"  - {asset['name']}")
        raise RuntimeError(f"DMG not found: {dmg_pattern}")

    dmg_path = Path(dmg_pattern)
    print(f"Downloading {dmg_pattern}...")
    data = urllib.request.urlopen(download_url).read()
    dmg_path.write_bytes(data)
    print(f"Download complete: {dmg_path} ({len(data) / 1024 / 1024:.1f} MB)")

    mount_point = f"/Volumes/Dart + Flutter Demo"
    run(f"hdiutil attach {dmg_path} -noverify -quiet")

    app_source = None
    volumes = Path("/Volumes")
    for vol in volumes.iterdir():
        if "dart" in vol.name.lower() or "flutter" in vol.name.lower():
            for item in vol.iterdir():
                if item.suffix == ".app" and "dart" in item.name.lower():
                    app_source = str(item)
                    break
            if app_source:
                break

    if not app_source:
        run("ls /Volumes/")
        raise RuntimeError("Could not find .app inside mounted DMG")

    print(f"Found app: {app_source}")
    run(f"cp -R '{app_source}' /Applications/")
    run(f"xattr -cr /Applications/dart_flutter_demo.app")
    run(f"hdiutil detach '{app_source.rsplit('/', 1)[0]}' -quiet || true")

    print()
    print("=" * 60)
    print("dart-flutter-demo installed successfully!")
    print()
    print("Launch from SSH:")
    print("  open /Applications/dart_flutter_demo.app")
    print()
    print("Or run with log output:")
    print("  /Applications/dart_flutter_demo.app/Contents/MacOS/dart_flutter_demo")
    print()
    print("Type 'exit mac' to end the SSH session.")
    print("=" * 60)

    dark_mode = os.environ.get("DARK_MODE", "").strip().lower() in ("true", "1", "yes")

    if dark_mode:
        run(
            "osascript -e 'tell app \"System Events\" to tell appearance preferences to set dark mode to true'"
        )
        print("Switched to dark mode, waiting for UI to update...")
        time.sleep(2)

    run("open /Applications/dart_flutter_demo.app")

    for i in range(10, -1, -1):
        print(f"Waiting for UI to load... {i}s")
        time.sleep(1)

    screenshot_suffix = "_dark" if dark_mode else ""
    screenshot_path = f"/tmp/dart_flutter_demo_screenshot{screenshot_suffix}.png"

    run(f"screencapture -x {screenshot_path}")
    print(f"\nScreenshot saved to {screenshot_path}")

    if dark_mode:
        run(
            "osascript -e 'tell app \"System Events\" to tell appearance preferences to set dark mode to false'"
        )
        print("Switched back to light mode.")


if __name__ == "__main__":
    main()

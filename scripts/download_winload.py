import json
import os
import platform
import urllib.request
from pathlib import Path

REPO = "VincentZyuApps/winload"


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
        return "x86_64"
    elif machine in ["arm64", "aarch64"]:
        return "aarch64"
    else:
        raise RuntimeError(f"Unsupported arch: {machine}")


def main():
    release = get_latest_release()
    tag = release["tag_name"]
    arch = detect_arch()

    expected = f"winload-macos-{arch}-{tag}"

    for asset in release["assets"]:
        if asset["name"] == expected:
            url = asset["browser_download_url"]
            print(f"Downloading {expected}")
            data = urllib.request.urlopen(url).read()
            Path("winload").write_bytes(data)
            print("Download complete")
            return

    raise RuntimeError("Binary not found")


if __name__ == "__main__":
    main()

![mac-test-action-runner](https://socialify.git.ci/VincentZyuApps/mac-test-action-runner/image?custom_description=+GitHub+Actions+workflow+for+spinning+up+temporary+macOS+SSH+sessions+on+ARM64+runners%2C+aimed+at+testing+some+program.&custom_language=GitHub+Actions&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F3%2F30%2FMacOS_logo.svg%2F120px-MacOS_logo.svg.png%3Futm_source%3Dcommons.wikimedia.org%26utm_campaign%3Dindex%26utm_content%3Dthumbnail%26_%3D20221222011002&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Light)

# mac-test-action-runner

GitHub Actions workflow for temporary SSH sessions on macOS runners, with support for downloading and testing different projects.

## Usage

Push a commit containing a specific keyword to the main branch:

### 1. Empty macOS SSH (no binary download)

```bash
git commit --allow-empty -m "start-empty"
git push
```

### 2. Download and test winload

```bash
git commit --allow-empty -m "start-winload"
git push
```

- Automatically downloads the latest [winload](https://github.com/VincentZyuApps/winload) macOS binary
- Auto-detects architecture (x86_64 / arm64)
- Runs `./winload --help` after download

### 3. Download and test dart-flutter-demo

| Commit message | Download | Launch | Screenshot | Artifact | Release |
|---|---|---|---|---|---|
| `start-dart-flutter-demo` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `start-dart-flutter-demo --artifact-pic` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `start-dart-flutter-demo --release-pic` | ✅ | ✅ | ✅ | ✅ | ✅ (inline) |

> `--release-pic` includes `--artifact-pic`. Release tag format: `screenshot-YYYYMMDD-HHMMSS`. The screenshot image is embedded inline in the release notes markdown.

- Automatically downloads the latest [dart-flutter-demo](https://github.com/VincentZyuApps/dart-flutter-demo) macOS DMG
- Mounts DMG → extracts .app to /Applications → removes quarantine → detaches DMG
- Launches the app and takes a screenshot saved to `/tmp/dart_flutter_demo_screenshot.png`

### General

- All modes start a tmate SSH session
- SSH command is printed in the workflow logs
- Type `exit mac` to end the session
- Timeout: 10 minutes
- Runner: `macos-latest` (ARM64)

## Preview

<table>
<tr>
<td align="center"><b>SSH Session (macOS 15 ARM64)</b></td>
<td align="center"><b>dart-flutter-demo System Info (macOS 15 ARM64)</b></td>
</tr>
<tr>
<td><img src="doc/images/preview.ssh.github.ci.runner.macos15.arm64.png" alt="SSH Session" width="400"/></td>
<td><img src="doc/images/preview.screenshot.github.ci.runner.macos15.arm64.dart_flutter_demo.page0_system_info.png" alt="dart-flutter-demo System Info" width="400"/></td>
</tr>
</table>

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/download_winload.py` | Download winload macOS binary from releases |
| `scripts/download_dart_flutter_demo.py` | Download dart-flutter-demo DMG and install |
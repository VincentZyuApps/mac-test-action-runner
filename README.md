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

```bash
git commit --allow-empty -m "start-dart-flutter-demo"
git push
```

- Automatically downloads the latest [dart-flutter-demo](https://github.com/VincentZyuApps/dart-flutter-demo) macOS DMG
- Mounts DMG → extracts .app to /Applications → removes quarantine → detaches DMG
- Launches the app and takes a screenshot saved to `/tmp/dart_flutter_demo_screenshot.png`

### General

- All modes start a tmate SSH session
- SSH command is printed in the workflow logs
- Type `exit mac` to end the session
- Timeout: 10 minutes
- Runner: `macos-latest` (ARM64)

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/download_winload.py` | Download winload macOS binary from releases |
| `scripts/download_dart_flutter_demo.py` | Download dart-flutter-demo DMG and install |
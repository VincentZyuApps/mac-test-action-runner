![mac-test-action-runner](https://socialify.git.ci/VincentZyuApps/mac-test-action-runner/image?custom_description=+GitHub+Actions+workflow+for+spinning+up+temporary+macOS+SSH+sessions+on+ARM64+runners%2C+aimed+at+testing+some+program.&custom_language=GitHub+Actions&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F3%2F30%2FMacOS_logo.svg%2F120px-MacOS_logo.svg.png%3Futm_source%3Dcommons.wikimedia.org%26utm_campaign%3Dindex%26utm_content%3Dthumbnail%26_%3D20221222011002&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Light)

[English](./mac-temp.md) | [中文](./mac-temp.zh-cn.md)

# Temporary macOS SSH Workflow

This workflow creates temporary SSH sessions on macOS ARM64 runners, with support for downloading and testing different projects.

## Triggers

The workflow runs on push to the `main` branch, but **only when the commit message contains a trigger keyword**:

| Trigger Keyword | Mode |
|---|---|
| `start-empty` | Empty macOS SSH session |
| `start-winload` | Download and test winload |
| `start-dart-flutter-demo` | Download and test dart-flutter-demo |

Otherwise, the workflow will skip the macOS runner and display:
```
✗ Commit message does not contain trigger keyword
   Skipping macOS runner (commit: abc1234)
```

### Examples

**Valid commit messages (will trigger runner):**
```bash
git commit --allow-empty -m "start-empty"
git commit --allow-empty -m "start-winload"
git commit --allow-empty -m "start-dart-flutter-demo"
git commit --allow-empty -m "start-dart-flutter-demo --artifact-pic"
git commit --allow-empty -m "start-dart-flutter-demo --release-pic"
```

**Invalid commit messages (will skip runner):**
```bash
git commit -m "docs: update readme"
git commit -m "fix: typo"
git commit -m "chore: cleanup"
```

### Screenshot Flags (dart-flutter-demo only)

| Commit message | Download | Launch | Screenshot | Artifact | Release |
|---|---|---|---|---|---|
| `start-dart-flutter-demo` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `start-dart-flutter-demo --artifact-pic` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `start-dart-flutter-demo --release-pic` | ✅ | ✅ | ✅ | ✅ | ✅ (inline) |

> `--release-pic` includes `--artifact-pic`. Release tag format: `screenshot-YYYYMMDD-HHMMSS`. The screenshot image is embedded inline in the release notes markdown.

## Pipeline Stages

### Stage 1: Check Commit Message

Validates that the commit message contains a trigger keyword.

- **Runner:** `ubuntu-latest`
- **Output:** `should_run` (boolean)
- Zero cost — runs on free Ubuntu runner, skips macOS runner if no trigger keyword found

### Stage 2: macOS SSH Session

The main job that spins up a macOS ARM64 runner.

- **Runner:** `macos-latest` (ARM64)
- **Timeout:** 10 minutes

**Steps:**

1. Checkout code
2. Show system info (`uname -a`, `sw_vers`, `uname -m`)
3. Download binary (if `start-winload` or `start-dart-flutter-demo`)
4. Install tmate
5. Rename screenshot with timestamp (if `--artifact-pic` or `--release-pic`)
6. Upload screenshot to artifacts (if `--artifact-pic` or `--release-pic`)
7. Upload screenshot to GitHub Release (if `--release-pic`)
8. Start SSH session (type `exit mac` to end)

## Required Secrets

| Secret | Description |
|--------|-------------|
| `GITHUB_TOKEN` | Automatically available in GitHub Actions (no configuration needed) |

## Notes

- All modes start a tmate SSH session
- SSH command is printed in the workflow logs
- Type `exit mac` to end the session
- Runner: `macos-latest` (ARM64, M1/M2)
- `--release-pic` creates a GitHub Release with the screenshot embedded inline in the release notes markdown
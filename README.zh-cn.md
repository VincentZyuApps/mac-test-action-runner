![mac-test-action-runner](https://socialify.git.ci/VincentZyuApps/mac-test-action-runner/image?custom_description=+GitHub+Actions+workflow+for+spinning+up+temporary+macOS+SSH+sessions+on+ARM64+runners%2C+aimed+at+testing+some+program.&custom_language=GitHub+Actions&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F3%2F30%2FMacOS_logo.svg%2F120px-MacOS_logo.svg.png%3Futm_source%3Dcommons.wikimedia.org%26utm_campaign%3Dindex%26utm_content%3Dthumbnail%26_%3D20221222011002&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Light)

# mac-test-action-runner

GitHub Actions workflow：在 macOS runner 上创建临时 SSH 会话，支持下载和测试不同项目。

## 使用方法

推送包含特定关键词的提交到 main 分支即可触发：

### 1. 空壳 macOS SSH（不下载任何二进制）

```bash
git commit --allow-empty -m "start-empty"
git push
```

### 2. 下载并测试 winload

```bash
git commit --allow-empty -m "start-winload"
git push
```

- 自动下载最新的 [winload](https://github.com/VincentZyuApps/winload) macOS 二进制
- 支持架构自动检测（x86_64 / arm64）
- 下载后执行 `./winload --help`

### 3. 下载并测试 dart-flutter-demo

| 提交信息 | 下载 | 启动 | 截图 | Artifact | Release |
|---|---|---|---|---|---|
| `start-dart-flutter-demo` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `start-dart-flutter-demo --artifact-pic` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `start-dart-flutter-demo --release-pic` | ✅ | ✅ | ✅ | ✅ | ✅ (内嵌) |

> `--release-pic` 包含 `--artifact-pic`。Release 标签格式：`screenshot-YYYYMMDD-HHMMSS`。截图会以内嵌图片形式显示在 Release 正文中。

- 自动下载最新的 [dart-flutter-demo](https://github.com/VincentZyuApps/dart-flutter-demo) macOS DMG
- 挂载 DMG → 提取 .app 到 /Applications → 去除隔离属性 → 卸载 DMG
- 自动启动 app 并截图保存到 `/tmp/dart_flutter_demo_screenshot.png`

### 通用说明

- 所有模式都会启动 tmate SSH 会话
- SSH 命令在 workflow 日志中输出
- 输入 `exit mac` 结束会话
- 超时时间：10 分钟
- Runner：`macos-latest`（ARM64）

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/download_winload.py` | 从 winload releases 下载 macOS 二进制 |
| `scripts/download_dart_flutter_demo.py` | 从 dart-flutter-demo releases 下载 DMG 并安装 |
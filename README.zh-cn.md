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

```bash
git commit --allow-empty -m "start-dart-flutter-demo"
git push
```

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
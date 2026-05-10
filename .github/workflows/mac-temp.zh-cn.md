![mac-test-action-runner](https://socialify.git.ci/VincentZyuApps/mac-test-action-runner/image?custom_description=+GitHub+Actions+workflow+for+spinning+up+temporary+macOS+SSH+sessions+on+ARM64+runners%2C+aimed+at+testing+some+program.&custom_language=GitHub+Actions&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F3%2F30%2FMacOS_logo.svg%2F120px-MacOS_logo.svg.png%3Futm_source%3Dcommons.wikimedia.org%26utm_campaign%3Dindex%26utm_content%3Dthumbnail%26_%3D20221222011002&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Light)

[English](./mac-temp.md) | [中文](./mac-temp.zh-cn.md)

# Temporary macOS SSH 工作流

此工作流在 macOS ARM64 runner 上创建临时 SSH 会话，支持下载和测试不同项目。

## 触发条件

工作流在推送到 `main` 分支时运行，但**仅当 commit 信息包含触发关键词时**才会启动 macOS runner：

| 触发关键词 | 模式 |
|---|---|
| `start-empty` | 空壳 macOS SSH 会话 |
| `start-winload` | 下载并测试 winload |
| `start-dart-flutter-demo` | 下载并测试 dart-flutter-demo |

否则工作流将跳过 macOS runner 并显示：
```
✗ Commit message does not contain trigger keyword
   Skipping macOS runner (commit: abc1234)
```

### 示例

**合法的 commit 信息（将触发 runner）：**
```bash
git commit --allow-empty -m "start-empty"
git commit --allow-empty -m "start-winload"
git commit --allow-empty -m "start-dart-flutter-demo"
git commit --allow-empty -m "start-dart-flutter-demo --artifact-pic"
git commit --allow-empty -m "start-dart-flutter-demo --release-pic"
```

**非法的 commit 信息（将跳过 runner）：**
```bash
git commit -m "docs: update readme"
git commit -m "fix: typo"
git commit -m "chore: cleanup"
```

### 截图标志（仅 dart-flutter-demo）

| 提交信息 | 下载 | 启动 | 截图 | Artifact | Release |
|---|---|---|---|---|---|
| `start-dart-flutter-demo` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `start-dart-flutter-demo --artifact-pic` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `start-dart-flutter-demo --release-pic` | ✅ | ✅ | ✅ | ✅ | ✅ (内嵌) |

> `--release-pic` 包含 `--artifact-pic`。Release 标签格式：`screenshot-YYYYMMDD-HHMMSS`。截图会以内嵌图片形式显示在 Release 正文中。

## 流水线阶段

### 阶段一：检查 Commit 信息

验证 commit 信息是否包含触发关键词。

- **运行环境：** `ubuntu-latest`
- **输出：** `should_run` (布尔值)
- 零成本 — 在免费的 Ubuntu runner 上运行，无触发关键词时跳过 macOS runner

### 阶段二：macOS SSH 会话

在 macOS ARM64 runner 上启动主任务。

- **运行环境：** `macos-latest` (ARM64)
- **超时时间：** 10 分钟

**执行步骤：**

1. 检出代码
2. 显示系统信息（`uname -a`、`sw_vers`、`uname -m`）
3. 下载二进制文件（如果指定了 `start-winload` 或 `start-dart-flutter-demo`）
4. 安装 tmate
5. 重命名截图文件（添加时间戳）（如果指定了 `--artifact-pic` 或 `--release-pic`）
6. 上传截图到 Artifacts（如果指定了 `--artifact-pic` 或 `--release-pic`）
7. 上传截图到 GitHub Release（如果指定了 `--release-pic`）
8. 启动 SSH 会话（输入 `exit mac` 结束）

## 必需的 Secrets

| 密钥 | 说明 |
|------|------|
| `GITHUB_TOKEN` | GitHub Actions 自动提供，无需手动配置 |

## 注意事项

- 所有模式都会启动 tmate SSH 会话
- SSH 命令在 workflow 日志中输出
- 输入 `exit mac` 结束会话
- Runner：`macos-latest`（ARM64，M1/M2）
- `--release-pic` 会创建 GitHub Release，并将截图以内嵌图片形式显示在 Release 正文中
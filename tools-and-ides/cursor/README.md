<h1 align="center">Cursor</h1>

<p align="center">
  <b>VS Code fork with deep AI integration</b><br>
  <sub>GUI-based AI-native IDE with multi-model support</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VS_Code-Fork-007ACC?logo=visual-studio-code" alt="VS Code"/>
  <img src="https://img.shields.io/badge/GUI-Diff_View-5C2D91?logo=cursor" alt="GUI"/>
  <img src="https://img.shields.io/badge/Models-GPT_Claude_Gemini-green" alt="Models"/>
</p>

---

<details open>
<summary><b>English</b></summary>

## What It Is

Cursor is a **VS Code fork** with AI built in from the ground up. It keeps the full VS Code experience (extensions, keybindings, themes) and adds Tab completion, Chat, Composer (multi-file edit), and Agent mode with subagents and tools.

## Features

| Feature | Description |
|---------|-------------|
| **Multi-model** | Choose GPT-4, Claude, Gemini, or others per conversation |
| **Subagents** | Break tasks into parallel or sequential sub-agents |
| **Tools** | Built-in and custom tools (browser, terminal, file ops) |
| **GUI diff** | See file changes in the editor before accepting |
| **Composer / Agent** | Multi-file editing and autonomous task execution |
| **Rules & Skills** | Project rules (`.cursor/rules`) and installable skills |

## Pricing

Cursor offers multiple subscription tiers to suit different needs:

| Plan | Price | Fixed Credits | Bonus Credits | Notes |
|------|-------|---------------|---------------|-------|
| **Pro** | $20/month | ~$20 | ~$20–25 | Standard plan; suitable for moderate use |
| **Pro+** | $60/month | ~$60 | Additional bonus | Higher fixed allocation |
| **Ultra** | $400/month | ~$400 | ~$200 | Enterprise-level usage |

**Key features of Pro subscription and above:**

- Access to premium models (GPT-4, Claude Opus, Gemini Pro, etc.)
- **Auto models** (~$150 worth): Cursor's smart model routing that automatically selects the best model for your task
- **Composer 1.5**: Enhanced multi-file editing with better context awareness and planning capabilities

Credits are consumed by model use (fast requests cost more). Heavy Agent/Composer use burns through the monthly allowance quickly.

## Pros

- **Choose your model** — GPT, Claude, Gemini, etc., in one place
- **GUI diff** — Review and edit changes in the editor
- **Rich ecosystem** — Rules, skills, extensions
- **Familiar** — Same as VS Code if you already use it
- **Composer 1.5** — Advanced multi-file editing and planning capabilities
- **Auto models** — Smart model selection for optimal performance

## Using Custom API Keys (Third-Party Relays)

**Requires: Cursor Pro subscription**

Cursor allows you to configure custom API endpoints (third-party relays) to use your own API keys. This is useful if:

- You want to use a specific API relay with better pricing
- You have your own OpenAI/Anthropic credits
- The built-in models are experiencing issues

### Setup

1. Go to **Settings → Models → API Keys** in Cursor
2. Add your custom API endpoint and key

![Cursor API Configuration Example](fig/cursor_api.png)

### Important Notes

> **⚠️ Tool Call Compatibility:** Some third-party relays have broken tool/function call implementations, which will cause Cursor's Agent/Composer modes to fail. Test with simple tasks first before relying on a relay for complex workflows.

If you encounter errors like "tool call failed" or Agent mode gets stuck, the relay may not fully support OpenAI's tool calling protocol. Switch back to Cursor's built-in endpoints or try a different relay.

## Usage Tips

| Tip | Description |
|-----|-------------|
| **Network stability** | If experiencing unstable network, enable VPN **TUN mode** and switch to **HTTP/2.0** protocol for better reliability |
| **Network diagnostics** | Go to Settings → Network to run diagnostics and check latency/connectivity issues |
| **Model selection** | Use Auto mode to let Cursor pick the best model, or manually select for specific tasks |
| **Composer workflow** | Use Composer 1.5 for complex multi-file refactoring with better context understanding |
| **Custom API** | Configure third-party relay in Settings → Models → API Keys (requires Pro; test tool call compatibility) |

## Cons

- **Expensive** — Pro+ and Ultra plans can be costly for individual developers
- **Credit management** — Need to monitor credit usage to avoid running out

## Links

- [Cursor](https://cursor.com)
- [Pricing](https://cursor.com/pricing)

</details>

---

<details>
<summary><b>中文</b></summary>

## 简介

Cursor 是基于 **VS Code 的 fork**，深度集成 AI。保留完整 VS Code 体验（扩展、快捷键、主题），并增加 Tab 补全、Chat、Composer（多文件编辑）以及带 Subagents 和 Tools 的 Agent 模式。

## 功能特点

| 功能 | 说明 |
|------|------|
| **多模型** | 每次对话可选 GPT-4、Claude、Gemini 等 |
| **Subagents** | 将任务拆成并行或串行子代理 |
| **Tools** | 内置与自定义工具（浏览器、终端、文件操作） |
| **GUI 差异视图** | 在编辑器中查看并接受/修改变更 |
| **Composer / Agent** | 多文件编辑与自主任务执行 |
| **Rules & Skills** | 项目规则（`.cursor/rules`）与可安装 Skill |

## 付费模式

Cursor 提供多个订阅层级以满足不同需求:

| 套餐 | 价格 | 固定额度 | 奖励额度 | 说明 |
|------|------|---------|---------|------|
| **Pro** | $20/月 | ~$20 | ~$20–25 | 标准套餐，适合中度使用 |
| **Pro+** | $60/月 | ~$60 | 额外奖励额度 | 更高的固定额度 |
| **Ultra** | $400/月 | ~$400 | ~$200 | 企业级使用量 |

**Pro 订阅及以上套餐的核心功能:**

- 使用高级模型（GPT-4、Claude Opus、Gemini Pro 等）
- **Auto 模型**（价值约 $150）：Cursor 的智能模型路由，自动为任务选择最佳模型
- **Composer 1.5**：增强的多文件编辑，具备更好的上下文感知和规划能力

额度按模型调用消耗（请求越快消耗越多）。大量使用 Agent/Composer 会很快用完当月额度。

## 优点

- **自选模型** — GPT、Claude、Gemini 等一站式使用
- **GUI 看 diff** — 在编辑器里审阅、修改变更
- **生态丰富** — Rules、Skills、扩展
- **上手简单** — 和 VS Code 一致
- **Composer 1.5** — 高级多文件编辑和规划能力
- **Auto 模型** — 智能模型选择，优化性能

## 使用自定义 API 密钥（第三方中转）

**需要：Cursor Pro 订阅**

Cursor 允许配置自定义 API 端点（第三方中转）来使用你自己的 API 密钥。适用于：

- 使用定价更优的 API 中转
- 使用自己的 OpenAI/Anthropic 额度
- 内置模型出现问题时

### 配置方法

1. 进入 Cursor 的 **Settings → Models → API Keys**
2. 添加自定义 API 端点和密钥

![Cursor API 配置示例](fig/cursor_api.png)

### 重要提示

> **⚠️ Tool Call 兼容性：** 部分第三方中转的 tool/function call 实现有问题，会导致 Cursor 的 Agent/Composer 模式失败。使用前先用简单任务测试，不要直接用于复杂工作流。

如果遇到 "tool call failed" 或 Agent 模式卡住，说明该中转不完全支持 OpenAI 的 tool calling 协议。切换回 Cursor 内置端点或换一个中转。

## 使用技巧

| 技巧 | 说明 |
|------|------|
| **网络稳定性** | 如果网络不稳定，开启 VPN 的 **TUN 模式**，并切换到 **HTTP/2.0** 协议以提高可靠性 |
| **网络诊断** | 进入 Settings → Network 运行诊断，检查延迟和连接问题 |
| **模型选择** | 使用 Auto 模式让 Cursor 选择最佳模型，或针对特定任务手动选择 |
| **Composer 工作流** | 使用 Composer 1.5 进行复杂的多文件重构，具备更好的上下文理解 |
| **自定义 API** | 在 Settings → Models → API Keys 配置第三方中转（需 Pro；测试 tool call 兼容性） |

## 缺点

- **价格高** — Pro+ 和 Ultra 套餐对个人开发者来说可能较贵
- **额度管理** — 需要监控额度使用，避免用完

## 链接

- [Cursor](https://cursor.com)
- [定价](https://cursor.com/pricing)

</details>

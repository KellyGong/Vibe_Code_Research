<h1 align="center">Claude Code</h1>

<p align="center">
  <b>Anthropic's agentic coding tool — terminal-based</b><br>
  <sub>Most capable agent; runs in the terminal</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Anthropic-Claude-CC785C?logo=anthropic" alt="Anthropic"/>
  <img src="https://img.shields.io/badge/Terminal-Agent-orange" alt="Terminal"/>
</p>

---

<details open>
<summary><b>English</b></summary>

## What It Is

**Claude Code** is Anthropic's agentic coding tool. It runs entirely in the **terminal** — no GUI, no built-in diff viewer in an editor. It is often considered one of the **most capable** coding agents available.

## How to Use It

| Method | Description |
|--------|-------------|
| **Official subscription** | Claude Pro or Claude Max — includes access to Claude Code |
| **Third-party API relay** | Use a relay service (e.g. API proxy) to call Claude; often **cost-effective** and flexible |

You can stick to the official product or bring your own API key via third-party setups for better cost/performance.

### Third-Party API Relay Setup

A recommended relay service: **[OneFun](https://onefun.top/console/token)** — register and get your token on the console page.

**Step 1: Set environment variables in terminal**

```bash
export ANTHROPIC_BASE_URL="https://api.onefun.top"
export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"   # Replace with your actual token
```

> This only lasts for the current terminal session.

**Step 2 (optional): Make it permanent**

Add the two `export` lines to your shell config so they load automatically on every new terminal:

```bash
# For bash users:
echo 'export ANTHROPIC_BASE_URL="https://api.onefun.top"' >> ~/.bashrc
echo 'export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"' >> ~/.bashrc
source ~/.bashrc

# For zsh users:
echo 'export ANTHROPIC_BASE_URL="https://api.onefun.top"' >> ~/.zshrc
echo 'export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"' >> ~/.zshrc
source ~/.zshrc
```

Then just run `claude` in terminal to start.

## Usage Tips

| Command / Feature | What It Does |
|-------------------|--------------|
| **Subagents** | Claude Code can spawn multiple sub-agents in parallel to handle complex tasks — just describe a multi-part task and it will dispatch agents automatically |
| `/context` | View the current conversation context (what files and info Claude is working with) |
| `/cost` | Check your usage and token spend for the current session |
| `/help` | Show all available slash commands |

## Pros

- **Most capable agent** — Top-tier reasoning and code edits
- **Flexible API options** — Official sub or third-party relay
- **Good cost-performance** — Third-party relay can be very economical

## Cons

- **Terminal-only** — No GUI; no in-editor diff view (you review changes in terminal or external diff tools)
- **Requires setup** — Either a paid subscription or API/relay configuration

## Links

- [Claude Code (Anthropic Docs)](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic](https://anthropic.com)

</details>

---

<details>
<summary><b>中文</b></summary>

## 简介

**Claude Code** 是 Anthropic 的智能体式编程工具，完全在 **终端** 中运行，没有图形界面，也没有编辑器内的 diff 视图，常被视为当前 **能力最强** 的编程智能体之一。

## 使用方式

| 方式 | 说明 |
|------|------|
| **官方订阅** | Claude Pro 或 Claude Max，包含 Claude Code 使用权限 |
| **第三方 API 中转** | 通过中转服务调用 Claude API，往往 **性价比高** 且灵活 |

可选择官方订阅，或通过第三方配置自带 API，在成本与性能之间取得平衡。

### 第三方 API 中转配置

推荐中转：**[OneFun](https://onefun.top/console/token)** — 在控制台页面注册并获取 Token。

**第一步：在终端设置环境变量**

```bash
export ANTHROPIC_BASE_URL="https://api.onefun.top"
export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"   # 替换为你的实际 Token
```

> 这只在当前终端会话中有效。

**第二步（可选）：永久生效**

把两行 `export` 写入 shell 配置文件，之后每次打开终端自动加载：

```bash
# bash 用户：
echo 'export ANTHROPIC_BASE_URL="https://api.onefun.top"' >> ~/.bashrc
echo 'export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"' >> ~/.bashrc
source ~/.bashrc

# zsh 用户：
echo 'export ANTHROPIC_BASE_URL="https://api.onefun.top"' >> ~/.zshrc
echo 'export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"' >> ~/.zshrc
source ~/.zshrc
```

然后在终端直接运行 `claude` 即可启动。

## 使用技巧

| 命令 / 功能 | 说明 |
|-------------|------|
| **Subagents** | Claude Code 可以并行派生多个子智能体处理复杂任务 — 描述一个多步任务，它会自动分配 agent |
| `/context` | 查看当前对话上下文（Claude 正在处理哪些文件和信息） |
| `/cost` | 查看当前会话的用量与 Token 消耗 |
| `/help` | 查看所有可用斜杠命令 |

## 优点

- **智能体能力顶尖** — 推理与代码修改都很强
- **API 方式灵活** — 官方订阅或第三方中转均可
- **性价比好** — 第三方中转通常更省钱

## 缺点

- **仅终端** — 无 GUI，无编辑器内 diff（需在终端或外部 diff 工具查看变更）
- **需配置** — 要么付费订阅，要么自行配置 API/中转

## 链接

- [Claude Code（Anthropic 文档）](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic](https://anthropic.com)

</details>

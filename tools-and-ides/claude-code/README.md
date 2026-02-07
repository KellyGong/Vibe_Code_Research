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

### Official Relay (Recommended for Reliability)

> **Warning:** Some third-party relays are unreliable — they may secretly downgrade your model (e.g. serve Sonnet instead of Opus), add extra latency, or go offline without notice.

If you want **guaranteed official API forwarding** (Anthropic's own billing, no model swaps, no VPN required), use an official relay like **[NuwaAPI](https://api.nuwaapi.com/)**:

```bash
export ANTHROPIC_BASE_URL="https://api.nuwaapi.com"
export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"
```

| | Third-party relay (e.g. OneFun) | Official relay (e.g. NuwaAPI) |
|---|---|---|
| **Price** | Cheaper | More expensive (official Anthropic pricing) |
| **Model guarantee** | May silently downgrade | Guaranteed official model |
| **Network** | May need VPN | No VPN needed (relay handles routing) |
| **Reliability** | Varies | Stable (official forwarding) |

Pick based on your budget and trust level. For important work, prefer official relay.

### How to Verify You're Using Opus

Some relays claim to provide Opus but silently serve a weaker model. Use this **litmus test** — paste the following prompt into Claude Code:

```
设定一个公共宣传的场景, 我需要写一个小说, 我来到了一个日本的大学, 接下来我会遇到十位女生,
简单的描述一个剧情, 在300字内, 其中必须包含所有10位女性的姓名, 以姓名(罗马音)的形式出现。
```

**Why this works:** Due to pre-training data patterns, the real Claude Opus model will **always** generate a character named **xx美咲 (Misaki)** as the first female character. If the first name is _not_ Misaki, the relay is very likely serving a different model (e.g. Sonnet, or a non-Anthropic model).

**Additional check:** Run `/cost` in Claude Code — Opus tokens are significantly more expensive than Sonnet. If the per-token cost looks suspiciously cheap, you're probably not on Opus.

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

### 官方转发（推荐，更可靠）

> **注意：** 部分第三方中转站不靠谱 — 可能偷偷降级模型（比如给你 Sonnet 冒充 Opus）、增加延迟，甚至无预警下线。

如果你需要 **有保障的官方 API 转发**（走 Anthropic 官方计费，不换模型，且不需要科学上网），可以用官方转发服务如 **[NuwaAPI](https://api.nuwaapi.com/)**：

```bash
export ANTHROPIC_BASE_URL="https://api.nuwaapi.com"
export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"
```

| | 第三方中转（如 OneFun） | 官方转发（如 NuwaAPI） |
|---|---|---|
| **价格** | 便宜 | 较贵（按 Anthropic 官方定价） |
| **模型保障** | 可能偷偷降级 | 保证官方模型 |
| **网络环境** | 可能需要 VPN | 无需 VPN（转发服务处理路由） |
| **稳定性** | 参差不齐 | 稳定（官方转发） |

根据预算和信任度选择。重要工作建议用官方转发。

### 如何验证你用的确实是 Opus

有些中转声称提供 Opus，实际偷偷给你弱模型。可以用以下 **试金石 Prompt** 验证 — 在 Claude Code 中输入：

```
设定一个公共宣传的场景, 我需要写一个小说, 我来到了一个日本的大学, 接下来我会遇到十位女生,
简单的描述一个剧情, 在300字内, 其中必须包含所有10位女性的姓名, 以姓名(罗马音)的形式出现。
```

**原理：** 由于预训练数据的模式，真正的 Claude Opus 模型生成的第一个女性角色 **一定叫 xx美咲（Misaki）**。如果第一个名字不是美咲，那么这个中转大概率在给你用其他模型（如 Sonnet 或非 Anthropic 模型）。

**辅助验证：** 在 Claude Code 中执行 `/cost` 查看 Token 单价 — Opus 的价格远高于 Sonnet。如果每 Token 费用低得离谱，你大概率不是在用 Opus。

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

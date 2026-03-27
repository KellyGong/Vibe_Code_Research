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

### Official Subscription (Strongly Recommended)

If you don't mind the subscription process, **we strongly recommend subscribing to the official plan**. Key advantages:

1. **Official & stable** — No model faking, guaranteed authentic Opus/Sonnet
2. **Cutting-edge features first** — Access the latest capabilities (Agent Teams, `/loop`, co-workers, etc.) as soon as they ship
3. **1M context window by default** — All models come with 1M context at no extra charge; even when usage exceeds 200K tokens, you still pay the same subscription price
4. **Higher effective quota** — Thanks to prompt caching, your subscription dollar stretches much further than third-party relay credits

#### Pro ($20/month)

The Pro plan unlocks **Claude Code** and access to the **Opus** model.

**Co-Workers:** Pro subscribers can also use [Co-Workers (Background Agents)](https://docs.anthropic.com/en/docs/claude-code/co-workers) — autonomous agents that run tasks in the background (e.g., fixing bugs, implementing features) while you continue working. They operate in sandboxed environments and report back when done.

**Rate limits:** Claude Code rate limits are calculated on a **rolling 5-hour window** plus a **weekly cap**.

**Prompt caching & cost efficiency:**

Claude Code maintains a **5-minute cache TTL** on Pro. Here's how it works:

- The first request in a conversation does a **cache write** (stores your context)
- Every subsequent request does a **cache read**, which resets the 5-minute timer
- As long as you keep interacting within 5 minutes, the cache stays warm indefinitely

On the subscription plan, **cache reads are free** (on API billing, cache reads cost 0.1× the normal input price). This makes a massive difference for Claude Code's high-intensity workflow with long contexts and frequent tool calls.

**Example calculation (200K context, Opus):**

| | API billing (per request) | Subscription |
|---|---|---|
| Input tokens (200K) | $3.00 (@ $15/M) | Included |
| Cache read (200K) | $0.30 (@ $1.5/M, 0.1×) | **Free** |
| Output tokens (500) | $0.04 (@ $75/M) | Included |
| **Typical request cost** | **~$0.34** (cache hit) / **$3.04** (cold) | **$0** |

In a typical Claude Code session with 200K context, after the initial cache write, each subsequent interaction costs ~$0.34 on API billing. Over a busy day with 100+ interactions, that's $34+ in API fees — but **$0 extra on subscription**.

The Pro plan costs $20/month but provides roughly **~$300/month in equivalent API token value**. This fluctuates based on cache hit rate — the more cache reads (which is the norm for Claude Code), the more value you extract. Heavy users can easily get $400–500+ worth of equivalent API usage.

#### Max ($100/month × 5 or $200/month × 20)

Max subscriptions dramatically increase your rate limits compared to Pro:

| | Pro ($20) | Max ×5 ($100) | Max ×20 ($200) |
|---|---|---|---|
| **5-hour window** | 1× | **6×** | **21×** |
| **Weekly cap** | 1× | **8.33×** | **16.67×** |
| **Cache TTL** | 5 min | **1 hour** | **1 hour** |

The **1-hour cache TTL** on Max is a game-changer. You can step away for 50 minutes, come back, and your entire conversation context is still cached — no expensive cache write needed. This is especially powerful for the `/loop` command running overnight: the 10-minute loop interval is well within the 1-hour cache window, so virtually every iteration is a free cache read.

**Effective weekly value:** Under heavy cache-read workloads, Max ×20's weekly quota can approach **~$1,500+ in equivalent API value** — and even higher with sustained cache hits. That's roughly **7.5× the subscription cost** in raw API terms, making it extraordinarily cost-effective for power users.

Max subscribers also get access to all the latest features, same as Pro.

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

### Custom Model Configuration

If you want to use alternative models available in your API key (e.g., Kimi-K2, Deepseek, etc.), you can configure the model via environment variables or settings file.

**Option 1: Set environment variables in terminal**

```bash
export ANTHROPIC_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_DEFAULT_SONNET_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_SMALL_FAST_MODEL="moonshotai/kimi-k2-thinking"
```

> Replace `moonshotai/kimi-k2-thinking` with your desired model name.

**Option 2: Add to `~/.claude/settings.json`**

Edit or create `~/.claude/settings.json` and add the model configuration in the `env` section:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-your-api-key-here",
    "ANTHROPIC_BASE_URL": "YOUR_BASE_URL",
    "ANTHROPIC_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_SMALL_FAST_MODEL": "moonshotai/kimi-k2-thinking"
  }
}
```

> This method makes the configuration persistent across all terminal sessions.

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
| **Model guarantee** | Some may silently downgrade | Guaranteed official model |
| **Network** | No VPN needed | No VPN needed |
| **Reliability** | Varies (OneFun verified reliable so far) | Stable (official forwarding) |

Pick based on your budget and trust level. OneFun has been verified and works well so far; for mission-critical work, official relay gives extra peace of mind.

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
| **Agent Teams** | Orchestrate multiple Claude Code sessions that coordinate and run work in parallel; enables delegate mode, task assignment/claiming, and team communication for large-scale projects |
| **MCP Servers** | Connect external tools (e.g. Codex CLI) via Model Context Protocol for multi-agent code review and discussion |
| `/loop [interval] <prompt>` | Run a task repeatedly on a set interval (default 10m) — great for overnight autonomous monitoring and iteration |
| `/context` | View the current conversation context (what files and info Claude is working with) |
| `/cost` | Check your usage and token spend for the current session |
| `/help` | Show all available slash commands |

### Agent Teams (NEW)

**What it is:** Agent Teams allows you to orchestrate multiple independent Claude Code sessions that can:

- **Coordinate & communicate**: Agents can delegate tasks to teammates, claim assigned work, and share progress
- **Run in parallel**: Multiple agents work simultaneously on different parts of a large project
- **Maintain context**: Each agent has isolated context while the orchestrator maintains overall project state
- **Quality gates**: Set up hooks for tests, linting, and checkpoints to save/rewind code state before edits

**Use cases:**

- **Parallel development**: Build different modules/features simultaneously (e.g., frontend + backend + tests)
- **Code review**: One agent implements while another reviews in parallel
- **Large refactoring**: Distribute file updates across multiple agents for faster completion
- **Competing approaches**: Test multiple implementation strategies simultaneously

**How to use:**

Agent Teams can be enabled through experimental settings. The orchestrator manages team lifecycle (start, monitor, shutdown) while individual agents focus on their assigned tasks. You can run agents via tmux or terminal multiplexing for visualization.

**Example workflow:** For a multi-component web app, spawn agents for:

1. Agent A: Build API endpoints
2. Agent B: Create React components
3. Agent C: Write integration tests
4. Agent D: Review and validate all changes

Each agent reports back to the orchestrator, which coordinates the overall build.

### Codex MCP: Code Review & Multi-Agent Discussion

Claude Code supports **MCP (Model Context Protocol)** servers, meaning you can connect external tools — including OpenAI's **Codex CLI** — directly into your Claude Code session. This enables a powerful workflow: **use Claude Code as the orchestrator, and call Codex as a second opinion for code review and discussion**.

**Setup:** Add the Codex MCP server to your Claude Code configuration (in `~/.claude/settings.json` or project-level `.claude/settings.json`):

```json
{
  "mcpServers": {
    "codex-cli": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/codex-mcp"]
    }
  }
}
```

> Replace the command/args with your actual Codex MCP server setup. The key is that once registered, Codex tools become available inside Claude Code.

**How it works in practice:**

1. **Code review**: Ask Claude Code to call the Codex MCP tool to review a file or diff. You get **two different models' perspectives** on the same code — Claude spots architectural issues while Codex may catch different edge cases.

2. **Multi-agent discussion**: You can explicitly prompt Claude Code to:
   - First generate its own review/opinion
   - Then call Codex MCP for a second opinion
   - Finally synthesize both perspectives into actionable feedback

**Example prompt:**

```
Review the changes in src/model.py. First give me your analysis, then call codex
to review the same diff. Summarize where you agree and disagree.
```

This turns Claude Code into a **multi-agent code review system** — two frontier models debating your code quality, catching bugs the other might miss, and giving you a consolidated report.

### Loop Command: Overnight Autonomous Work

The `/loop` command lets Claude Code **run a task repeatedly on a set interval** — turning it into a long-running autonomous agent that can monitor, fix, and iterate without human supervision.

**Syntax:**

```
/loop [interval] <prompt>
```

- Intervals: `Ns`, `Nm`, `Nh`, `Nd` (e.g. `5m`, `30m`, `2h`). Minimum granularity is 1 minute.
- If no interval is specified, defaults to `10m`.

**Use case: Overnight experiment monitoring**

When you have long-running experiments (e.g., model training, benchmark suites), you can set up a loop before going to sleep and let Claude Code babysit the entire process:

```
/loop 10m Check the training run status. If it crashed or errored, diagnose the issue,
fix the config or code, and restart the experiment. If it finished successfully,
log the results and start the next experiment in the queue. Keep going until all
experiments are done.
```

**Use case: Open-ended research tasks**

For exploratory tasks where Claude needs to try multiple approaches:

```
/loop 15m Check the hyperparameter sweep progress. Evaluate results so far using
validation loss < 0.35 as the success criterion. If a run looks promising, allocate
more resources to it. If all runs are stuck, try a different learning rate schedule.
Stop when validation loss < 0.35 is achieved or all 20 configurations have been tried.
```

**Key pattern:** Tell Claude Code:
- **What to monitor** — experiment status, logs, GPU utilization
- **How to evaluate** — success/failure criteria, metrics thresholds
- **How to recover** — fix errors, adjust configs, restart
- **When to stop** — completion conditions, termination criteria

**Why this is cost-effective:** Claude Code has **prompt caching** — when the conversation context is largely unchanged between loop iterations, most of the input tokens hit the cache (90%+ cache hit rate is typical). Cached tokens cost **~10% of regular input tokens**, making long-running loops surprisingly cheap. An overnight loop that runs every 10 minutes for 8 hours might cost only a few dollars in API fees, while saving you an entire night of manual babysitting.

## Pros

- **Most capable agent** — Top-tier reasoning and code edits
- **Flexible API options** — Official sub or third-party relay
- **Good cost-performance** — Third-party relay can be very economical
- **Autonomous loop** — Can run unattended overnight with `/loop`
- **MCP extensibility** — Connect external tools (Codex, etc.) for multi-agent workflows

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

### 官方订阅（强烈推荐）

如果不怕订阅流程的麻烦，**强烈推荐订阅官方会员**。核心优势：

1. **官方稳定** — 不存在模型造假，保证使用正版 Opus/Sonnet
2. **抢先体验最新功能** — Agent Teams、`/loop`、Co-Workers 等新功能第一时间可用
3. **默认 1M 上下文窗口** — 所有模型上下文均为 1M，加量不加价；即使使用超过 200K tokens，仍按原订阅价收费
4. **额度更高** — 得益于 prompt caching 机制，订阅的实际可用额度远超第三方中转平台

#### Pro（$20/月）

Pro 计划解锁 **Claude Code** 和 **Opus** 模型访问权限。

**Co-Workers（协作智能体）：** Pro 订阅者还可以使用 [Co-Workers（后台智能体）](https://docs.anthropic.com/en/docs/claude-code/co-workers) — 在后台自主运行任务（如修 bug、实现功能）的智能体，在沙盒环境中独立工作，完成后向你报告结果。

**速率限制：** Claude Code 的速率限制按 **5 小时滚动窗口** 加 **每周上限** 计算。

**Prompt caching 与成本效率：**

Pro 计划的 **cache 保留时间为 5 分钟**。工作原理：

- 对话中的第一次请求执行 **cache write**（写入上下文缓存）
- 之后每次请求都是 **cache read**，并重置 5 分钟计时器
- 只要在 5 分钟内持续交互，cache 就会一直保持热状态

在订阅计划中，**cache read 完全免费**（API 计费模式下 cache read 收取正常 input 价格的 0.1 倍）。这对 Claude Code 这种长上下文、高频 tool call 的高强度使用场景影响巨大。

**成本计算示例（200K 上下文，Opus）：**

| | API 计费（每次请求） | 订阅计划 |
|---|---|---|
| Input tokens（200K） | $3.00（@ $15/M） | 包含 |
| Cache read（200K） | $0.30（@ $1.5/M，0.1×） | **免费** |
| Output tokens（500） | $0.04（@ $75/M） | 包含 |
| **典型单次请求成本** | **~$0.34**（命中缓存）/ **$3.04**（冷启动） | **$0** |

在典型的 Claude Code 会话中（200K 上下文），初始 cache write 之后，每次后续交互在 API 计费下需 ~$0.34。一天高强度使用 100+ 次交互，就是 $34+ 的 API 费用 — 但 **订阅用户额外成本为 $0**。

Pro 计划每月 $20，但提供大约 **~$300/月的等值 API token 额度**。这个数字会根据 cache 命中率浮动 — cache read 越多（这在 Claude Code 中是常态），你获得的实际价值就越高。重度用户轻松可以获得 $400–500+ 等值的 API 使用量。

#### Max（$100/月 ×5 或 $200/月 ×20）

Max 订阅大幅提升速率限制：

| | Pro ($20) | Max ×5 ($100) | Max ×20 ($200) |
|---|---|---|---|
| **5 小时窗口** | 1× | **6×** | **21×** |
| **每周上限** | 1× | **8.33×** | **16.67×** |
| **Cache 保留时间** | 5 分钟 | **1 小时** | **1 小时** |

Max 的 **1 小时 cache 保留时间**是质变。你可以离开 50 分钟再回来，整个对话上下文仍然在缓存中 — 不需要昂贵的 cache write。这对 `/loop` 命令通宵运行尤其强大：10 分钟的 loop 间隔远在 1 小时 cache 窗口内，几乎每次迭代都是免费的 cache read。

**每周实际价值：** 在大量 cache read 的工作负载下，Max ×20 的每周额度可以逼近 **~$1,500+ 等值 API 价值** — 持续高 cache 命中率时甚至更高。这大约是订阅成本的 **7.5 倍**，对重度用户来说性价比极高。

Max 订阅者同样可以使用所有最新功能。

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

### 自定义模型配置

如果你想使用 API key 中可用的其他模型（如 Kimi-K2、Deepseek 等），可以通过环境变量或配置文件来设置模型。

**方式一：在终端设置环境变量**

```bash
export ANTHROPIC_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_DEFAULT_SONNET_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="moonshotai/kimi-k2-thinking"
export ANTHROPIC_SMALL_FAST_MODEL="moonshotai/kimi-k2-thinking"
```

> 将 `moonshotai/kimi-k2-thinking` 替换为你想使用的模型名称。

**方式二：添加到 `~/.claude/settings.json`**

编辑或创建 `~/.claude/settings.json` 文件，在 `env` 部分添加模型配置：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-your-api-key-here",
    "ANTHROPIC_BASE_URL": "YOUR_BASE_URL",
    "ANTHROPIC_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "moonshotai/kimi-k2-thinking",
    "ANTHROPIC_SMALL_FAST_MODEL": "moonshotai/kimi-k2-thinking"
  }
}
```

> 这种方式使配置在所有终端会话中持久生效。

### 官方转发（推荐,更可靠）

> **注意：** 部分第三方中转站不靠谱 — 可能偷偷降级模型（比如给你 Sonnet 冒充 Opus）、增加延迟，甚至无预警下线。

如果你需要 **有保障的官方 API 转发**（走 Anthropic 官方计费，不换模型，且不需要科学上网），可以用官方转发服务如 **[NuwaAPI](https://api.nuwaapi.com/)**：

```bash
export ANTHROPIC_BASE_URL="https://api.nuwaapi.com"
export ANTHROPIC_AUTH_TOKEN="YOUR_TOKEN_HERE"
```

| | 第三方中转（如 OneFun） | 官方转发（如 NuwaAPI） |
|---|---|---|
| **价格** | 便宜 | 较贵（按 Anthropic 官方定价） |
| **模型保障** | 部分可能偷偷降级 | 保证官方模型 |
| **网络环境** | 无需 VPN | 无需 VPN |
| **稳定性** | 因站而异（OneFun 经验证目前靠谱） | 稳定（官方转发） |

根据预算和信任度选择。OneFun 已经过验证，目前使用稳定；如果是关键任务，官方转发更让人放心。

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
| **Agent Teams** | 编排多个 Claude Code 会话协同工作并行运行；支持委托模式、任务分配/认领和团队沟通，用于大型项目 |
| **MCP Servers** | 通过 Model Context Protocol 接入外部工具（如 Codex CLI），实现多智能体代码审查与讨论 |
| `/loop [间隔] <提示词>` | 按设定间隔重复执行任务（默认 10 分钟）— 适合通宵自主监控和迭代 |
| `/context` | 查看当前对话上下文（Claude 正在处理哪些文件和信息） |
| `/cost` | 查看当前会话的用量与 Token 消耗 |
| `/help` | 查看所有可用斜杠命令 |

### Agent Teams（新功能）

**功能概述：** Agent Teams 允许你编排多个独立的 Claude Code 会话，它们可以：

- **协调与通信**：智能体可以向队友委托任务、认领分配的工作、共享进度
- **并行运行**：多个智能体同时处理大型项目的不同部分
- **维护上下文**：每个智能体拥有独立上下文，而编排器维护整体项目状态
- **质量关卡**：设置测试、linting 和检查点的钩子，在编辑前保存/回退代码状态

**使用场景：**

- **并行开发**：同时构建不同模块/功能（如前端 + 后端 + 测试）
- **代码审查**：一个智能体实现功能，另一个并行审查
- **大型重构**：将文件更新分配给多个智能体以加快完成速度
- **竞争方案**：同时测试多种实现策略

**如何使用：**

可以通过实验性设置启用 Agent Teams。编排器管理团队生命周期（启动、监控、关闭），而各个智能体专注于分配的任务。可以通过 tmux 或终端复用来可视化运行智能体。

**示例工作流：** 对于多组件 Web 应用，派生智能体分别负责：

1. Agent A：构建 API 端点
2. Agent B：创建 React 组件
3. Agent C：编写集成测试
4. Agent D：审查和验证所有更改

每个智能体向编排器报告，由编排器协调整体构建。

### Codex MCP：代码审查与多智能体讨论

Claude Code 支持 **MCP（Model Context Protocol）** 服务器，可以将外部工具（包括 OpenAI 的 **Codex CLI**）直接接入 Claude Code 会话。这解锁了一个强大的工作流：**用 Claude Code 做主控，调用 Codex 作为第二视角进行代码审查与讨论**。

**配置方式：** 在 `~/.claude/settings.json` 或项目级 `.claude/settings.json` 中添加 Codex MCP 服务器：

```json
{
  "mcpServers": {
    "codex-cli": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/codex-mcp"]
    }
  }
}
```

> 将 command/args 替换为你实际的 Codex MCP 服务器配置。注册后，Codex 工具会在 Claude Code 内可用。

**实际使用方式：**

1. **代码审查**：让 Claude Code 调用 Codex MCP 工具审查某个文件或 diff。你可以同时获得 **两个不同模型的视角** — Claude 擅长发现架构问题，Codex 可能捕捉到不同的边界情况。

2. **多智能体讨论**：你可以明确提示 Claude Code：
   - 先生成自己的审查意见
   - 然后调用 Codex MCP 获取第二意见
   - 最后综合两方观点给出可执行的反馈

**示例 Prompt：**

```
审查 src/model.py 的改动。先给出你的分析，然后调用 codex 审查同一个 diff。
总结你们一致和分歧的地方。
```

这让 Claude Code 变成了一个 **多智能体代码审查系统** — 两个顶级模型对你的代码质量进行辩论，互相捕捉对方可能遗漏的 bug，最终给出综合报告。

### Loop 命令：让 Claude Code 通宵干活

`/loop` 命令让 Claude Code **按设定间隔重复执行任务** — 把它变成一个长时间运行的自主智能体，可以在无人值守的情况下持续监控、修复和迭代。

**语法：**

```
/loop [间隔] <提示词>
```

- 间隔格式：`Ns`、`Nm`、`Nh`、`Nd`（如 `5m`、`30m`、`2h`）。最小粒度 1 分钟。
- 不指定间隔则默认 `10m`。

**场景一：通宵监控实验**

当你有长时间运行的实验（如模型训练、benchmark 套件）时，睡前设置一个 loop，让 Claude Code 全程看管：

```
/loop 10m 检查训练运行状态。如果崩溃或报错了，诊断问题，修复配置或代码，
然后重启实验。如果成功完成了，记录结果并启动队列中的下一个实验。
一直跑到所有实验全部完成为止。
```

**场景二：开放性探索任务**

对于需要 Claude 自主尝试多种方案的探索性任务，同样适用：

```
/loop 15m 检查超参搜索进度。用 validation loss < 0.35 作为成功标准评估当前结果。
如果某个 run 看起来有希望就给它分配更多资源。如果所有 run 都卡住了就换一个
learning rate schedule。当 validation loss < 0.35 达成或 20 个配置全部试完时停止。
```

**关键模式：** 告诉 Claude Code 四件事：
- **监控什么** — 实验状态、日志、GPU 利用率
- **如何评估** — 成功/失败标准、指标阈值
- **如何恢复** — 修错、调参、重启
- **何时终止** — 完成条件、停止标准

**为什么成本很低：** Claude Code 有 **prompt caching（提示缓存）** 机制 — loop 每次迭代时，对话上下文大部分没有变化，绝大多数 input tokens 会命中缓存（通常 90%+ 的缓存命中率）。缓存 token 的价格只有正常 input token 的 **约 10%**，这使得长时间 loop 的成本出奇地低。一个每 10 分钟跑一次、跑一整晚（8 小时）的 loop，API 费用可能只需要几美元，却省下了你一整晚的人工盯守。

## 优点

- **智能体能力顶尖** — 推理与代码修改都很强
- **API 方式灵活** — 官方订阅或第三方中转均可
- **性价比好** — 第三方中转通常更省钱
- **自主循环** — 通过 `/loop` 可以通宵无人值守运行
- **MCP 可扩展** — 接入外部工具（如 Codex）实现多智能体工作流

## 缺点

- **仅终端** — 无 GUI，无编辑器内 diff（需在终端或外部 diff 工具查看变更）
- **需配置** — 要么付费订阅，要么自行配置 API/中转

## 链接

- [Claude Code（Anthropic 文档）](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic](https://anthropic.com)

</details>

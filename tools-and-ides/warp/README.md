<h1 align="center">Warp</h1>

<p align="center">
  <b>不是 IDE，是 Agentic Development Environment</b><br>
  <sub>抛弃传统 IDE 编码范式，以终端为核心的 AI 智能体开发环境</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Warp-ADE-01B8AA?logo=warp" alt="Warp"/>
  <img src="https://img.shields.io/badge/Models-Claude_%7C_GPT_%7C_Gemini-blueviolet" alt="Models"/>
  <img src="https://img.shields.io/badge/Pricing-Per_Call_Credits-orange" alt="Pricing"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Is

**Warp is not a traditional IDE.** Originally a modern terminal, Warp pivoted in mid-2025 to become the first **Agentic Development Environment (ADE)** — abandoning IDE-style coding entirely. The bet: the terminal's direct input/output architecture is better suited for agent-driven workflows than a code editor with file trees and tabs.

> "We think it should look more like a terminal than an IDE." — Zach Lloyd, Warp CEO

Developers become **orchestrators and intent-shapers**, not code typists.

## Features

| Feature | Description |
|---------|-------------|
| **Agents 3.0** | Natural language on the command line; multi-step execution with human-in-the-loop approval |
| **Full terminal control** | Agents can run interactive CLI apps, not just edit files |
| **`/plan` command** | Long-horizon reasoning tasks with structured planning |
| **`/init`** | Auto-generates `AGENTS.md` project context file |
| **MCP Support** | Full Model Context Protocol — GitHub, Linear, Puppeteer, Sentry, Figma, and more |
| **Oz (Feb 2026)** | Cloud agent orchestration: unlimited parallel agents, event-driven triggers (Slack/Linear/GitHub), scheduled tasks, full audit trails |
| **Warp Drive** | Centralized knowledge base — share workflows, notebooks, context across teams |
| **Codebase indexing** | 120,000+ codebases indexed; global file search, smart completions |
| **Block model** | Commands and outputs grouped as shareable discrete units |
| **Cross-platform** | macOS, Linux, Windows (launched 2025) |

## Models

Warp supports one of the widest model selections of any AI tool, switchable via dropdown:

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude Opus 4.6 (default + max), Claude Sonnet 4.6 (default + max), Claude Opus/Sonnet 4.5 with thinking, Claude Opus 4.1, Claude Haiku 4.5, Claude Sonnet 4 |
| **OpenAI** | GPT-5.3 Codex, GPT-5.2, GPT-5.2 Codex, GPT-5.1 Codex Max/Codex, GPT-5.1, GPT-5 (各含 low/medium/high/extra-high reasoning) |
| **Google** | Gemini 3 Pro, Gemini 2.5 Pro |
| **Other** | GLM 4.6 (via z.ai / Fireworks AI) |
| **Auto modes** | Auto (Genius) / Auto (Responsive) / Auto (Cost-efficient) |

> Claude Opus 4.6 max 支持 200k 上下文。

## Credits & Pricing

Warp uses a **per-call credit system** — each AI request costs at least 1 credit. Actual cost scales with model, context size, and codebase scan depth.

| Plan | Price | Credits/month | Notes |
|------|-------|---------------|-------|
| **Free** | $0 | ~300 (new user bonus) | Core terminal features free forever; new users get free credits |
| **Build** | $20/mo | 1,500 | BYOK support; credits roll over 12 months |
| **Business** | $50/mo | 1,500 | SSO, ZDR, team management |

> ⚠️ **Credit burn warning**: Heavy agentic sessions with many tool calls can exhaust credits fast. A single complex session with Opus 4.6 max + MCP tools can burn through dozens of credits. Use Auto (Cost-efficient) or BYOK to manage costs.

## Benchmarks

| Benchmark | Score | Rank |
|-----------|-------|------|
| Terminal-Bench | 52% | **#1** |
| SWE-bench Verified | 71% | **#5** |

*(November 2025)*

## Pros

- **Unique paradigm** — not another IDE clone; terminal-first is genuinely different
- **Widest model selection** — Claude, GPT, Gemini all in one place
- **Full terminal agent control** — agents run interactive CLI apps, not just file edits
- **Oz cloud agents** — parallel execution, event-driven, no local resource limits
- **MCP ecosystem** — extensible via standardized tool protocol
- **Strong benchmarks** — #1 Terminal-Bench
- **Free terminal** — core features don't require payment
- **Awards** — TIME Best Inventions 2025, Newsweek AI Impact Award

## Cons

- **Not an IDE** — no file tree, tabs, or integrated debugger; you still need a separate editor
- **Credit burn rate** — tool-heavy sessions get expensive fast; 300 free credits can vanish in one complex session
- **Closed-source** — core app is not open source
- **Cloud dependency** — AI features require internet
- **Paradigm shift** — learning curve if you're used to GUI IDEs

## Links

- [warp.dev](https://www.warp.dev) — Official website
- [warp.dev/ai](https://www.warp.dev/ai) — AI & Agents overview
- [warp.dev/oz](https://www.warp.dev/oz) — Oz cloud agent platform
- [docs.warp.dev](https://docs.warp.dev) — Documentation
- [Pricing](https://docs.warp.dev/support-and-billing/plans-and-pricing)
- [Changelog](https://docs.warp.dev/getting-started/changelog)
- [MCP integrations](https://www.warp.dev/university/mcp/all)
- [GitHub (themes & issues)](https://github.com/warpdotdev/Warp)
- [Blog](https://www.warp.dev/blog)

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 简介

**Warp 不是传统 IDE。** 它最初是一个现代终端，2025 年中转型为首个 **Agentic Development Environment（ADE）**，彻底抛弃了 IDE 式的编码范式。核心理念：终端的直接输入/输出架构比带文件树和标签页的代码编辑器更适合 AI 智能体驱动的工作流。

开发者的角色变成了**意图表达者和结果审核者**，而不是代码打字员。

## 功能

| 功能 | 说明 |
|------|------|
| **Agents 3.0** | 命令行自然语言输入；多步骤执行，支持人工审批介入 |
| **完整终端控制** | 智能体可运行交互式 CLI 应用，不只是编辑文件 |
| **`/plan` 命令** | 长链路推理任务，结构化规划 |
| **`/init`** | 自动生成 `AGENTS.md` 项目上下文文件 |
| **MCP 支持** | 完整 Model Context Protocol — GitHub、Linear、Puppeteer、Sentry、Figma 等 |
| **Oz（2026年2月）** | 云端智能体编排：无限并行 agent、事件驱动触发（Slack/Linear/GitHub）、定时任务、完整审计日志 |
| **Warp Drive** | 团队知识库 — 共享工作流、笔记本和上下文 |
| **代码库索引** | 已索引 12 万+ 代码库；全局文件搜索、智能补全 |
| **Block 模型** | 命令与输出打包为可分享的离散单元 |
| **跨平台** | macOS、Linux、Windows（2025年上线） |

## 模型

Warp 拥有目前 AI 工具中最广泛的模型支持，可通过下拉菜单即时切换：

| 提供商 | 模型 |
|--------|------|
| **Anthropic** | Claude Opus 4.6（default + max）、Claude Sonnet 4.6（default + max）、Claude Opus/Sonnet 4.5（含 thinking）、Claude Opus 4.1、Claude Haiku 4.5、Claude Sonnet 4 |
| **OpenAI** | GPT-5.3 Codex、GPT-5.2、GPT-5.2 Codex、GPT-5.1 Codex Max/Codex、GPT-5.1、GPT-5（各含 low/medium/high/extra-high reasoning） |
| **Google** | Gemini 3 Pro、Gemini 2.5 Pro |
| **其他** | GLM 4.6（via z.ai / Fireworks AI） |
| **Auto 模式** | Auto (Genius) / Auto (Responsive) / Auto (Cost-efficient) |

> Claude Opus 4.6 max 支持 200k 上下文。

## 额度与定价

Warp 采用**按调用次数计费**的 credit 系统 — 每次 AI 请求至少消耗 1 credit，实际消耗取决于模型、上下文大小和代码库扫描深度。

| 方案 | 价格 | 月度 Credits | 备注 |
|------|------|-------------|------|
| **Free** | $0 | ~300（新用户赠送） | 终端核心功能永久免费；新用户获赠 credits |
| **Build** | $20/月 | 1,500 | 支持 BYOK；credits 12 个月内滚动有效 |
| **Business** | $50/月 | 1,500 | SSO、ZDR、团队管理 |

> ⚠️ **Credit 消耗警告**：大量 tool call 的 agentic 会话消耗极快。一次复杂的 Opus 4.6 max + MCP 工具会话可能一口气烧掉几十个 credits，300 个免费 credits 可能一次就用完。建议使用 Auto (Cost-efficient) 模式或 BYOK 控制成本。

## 基准测试

| 基准 | 得分 | 排名 |
|------|------|------|
| Terminal-Bench | 52% | **第 1** |
| SWE-bench Verified | 71% | **第 5** |

*(2025年11月)*

## 优点

- **独特范式** — 不是又一个 IDE 克隆，终端优先是真正不同的路线
- **最广模型支持** — Claude、GPT、Gemini 一站搞定
- **完整终端智能体控制** — 可运行交互式 CLI，不只是改文件
- **Oz 云端智能体** — 并行执行、事件驱动、不受本地资源限制
- **MCP 生态** — 标准化工具协议，可扩展性强
- **强基准成绩** — Terminal-Bench 第一
- **终端免费** — 核心功能无需付费
- **获奖** — TIME 2025 最佳发明、Newsweek AI 影响力奖

## 缺点

- **不是 IDE** — 没有文件树、标签页、集成调试器，部分任务仍需单独编辑器
- **Credit 消耗快** — tool call 密集的会话很烧钱，300 个免费 credits 一次复杂任务就没了
- **闭源** — 核心应用不开源
- **依赖云端** — AI 功能需要联网
- **范式转变** — 习惯 GUI IDE 的用户有学习成本

## 链接

- [warp.dev](https://www.warp.dev) — 官网
- [warp.dev/ai](https://www.warp.dev/ai) — AI 与智能体概览
- [warp.dev/oz](https://www.warp.dev/oz) — Oz 云端智能体平台
- [docs.warp.dev](https://docs.warp.dev) — 文档
- [定价](https://docs.warp.dev/support-and-billing/plans-and-pricing)
- [更新日志](https://docs.warp.dev/getting-started/changelog)
- [MCP 集成列表](https://www.warp.dev/university/mcp/all)
- [GitHub（主题与 issues）](https://github.com/warpdotdev/Warp)
- [博客](https://www.warp.dev/blog)

</details>

---

<p align="center">
  <sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub>
</p>

<h1 align="center">Windsurf</h1>

<p align="center">
  <b>满血模型 · 按 Prompt 计费 · 内置部署</b><br>
  <sub>VS Code fork，Cascade 智能体，支持全系前沿模型，比 Cursor 便宜</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Windsurf-IDE-0066FF?logo=visual-studio-code" alt="Windsurf"/>
  <img src="https://img.shields.io/badge/Models-Full_Power-green" alt="Models"/>
  <img src="https://img.shields.io/badge/Pricing-Per_Prompt_Credits-orange" alt="Pricing"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Is

**Windsurf** is an AI-native IDE (VS Code fork) by Codeium, now owned by **Cognition** (makers of Devin). It runs **full-power, unthrottled models** — not degraded versions — and charges **per prompt** rather than per month. The Cascade agent handles multi-file editing, terminal commands, and codebase-wide reasoning in a single turn.

> Ownership timeline: Codeium → OpenAI $3B deal (collapsed) → Google hired CEO for $2.4B → **Cognition acquired the product** (current, 2026). $82M ARR at acquisition.

## Features

| Feature | Description |
|---------|-------------|
| **Cascade** | Agentic AI with multi-file editing, terminal commands, codebase search — all in one turn |
| **Windsurf Tab** | AI autocomplete, unlimited on all plans |
| **Flow** | Deep codebase indexing for contextual awareness across entire repos |
| **Fast Context** | swe-grep powered retrieval, 20× faster, >2,800 tokens/sec |
| **Codemaps** | Visual code navigation with Mermaid diagrams |
| **Plan Mode** | Create detailed implementation plans before coding; "megaplan" for complex tasks |
| **Arena Mode** | Blind side-by-side model comparison with voting & leaderboards |
| **Turbo Mode** | Auto-executes commands and edits without manual approval |
| **Previews** | Live web previews with AI-assisted element modification |
| **App Deploys** | Ship directly from the IDE |
| **MCP Integration** | Connect external tools; auto-executes by default |
| **Multi-IDE plugins** | JetBrains, Vim/Neovim, XCode, and 40+ IDEs |
| **Cascade Hooks** | Custom commands triggered at key workflow points |
| **Git Worktree** | Multiple Cascade sessions in the same repo simultaneously |

## Models

Windsurf runs **full-power (满血) models** — not downgraded. Credit costs are per prompt (one message to Cascade = one charge, regardless of how many tool calls happen within that turn).

| Model | Credits/Prompt | Notes |
|-------|---------------|-------|
| Claude Opus 4.6 Fast (Thinking) | 12 | 2.5× faster output |
| Claude Opus 4.6 Fast (Standard) | 10 | 2.5× faster output |
| Claude Opus 4.6 (Thinking) | 8 | Full reasoning |
| Claude Opus 4.6 (Standard) | 6 | |
| Claude Sonnet 4.6 (Thinking) | 3 | |
| Claude Sonnet 4.6 (Standard) | 2 | |
| Claude Sonnet 4.5 | 2 | Popular cost-effective choice |
| GPT-5.3-Codex High | 2 | |
| GPT-5.3-Codex Medium | 1 | |
| GPT-5.1-Codex | 0 | Free after credits exhausted |
| Gemini 3 Pro High Thinking | 2 | |
| Kimi K2.5 | 1 | |
| SWE-1.5 | 0 (promo) | Windsurf's in-house model, near Claude Sonnet 4.5 level |
| SWE-1 / SWE-1-lite | 0 | Always free |
| Minimax M2.5 | 0.25 | Budget option |

> Windsurf frequently runs **promo pricing** on new models. Check the Cascade model selector for current rates: [docs.windsurf.com/windsurf/models](https://docs.windsurf.com/windsurf/models)

## Credits & Pricing

| Plan | Price | Credits/month | Notes |
|------|-------|---------------|-------|
| **Free** | $0 | 25 | Unlimited Tab completions; 1 deploy/day |
| **Pro Trial** | $0 (2 weeks) | 100 | All premium models; 10 deploys/day |
| **Pro** | $15/mo | 500 | Add-ons: $10/250 credits (never expire) |
| **Teams** | $30/user/mo | 500/user | Admin dashboard, pooled add-ons |
| **Enterprise** | $60/user/mo | 1,000/user | Longest context, SSO/SCIM, FedRAMP/HIPAA |

Key rules:
- Monthly credits **do not roll over** — reset each billing cycle
- Add-on credits **never expire**
- Failed operations **do not consume** credits
- **100-credit trial** ÷ 12 credits = ~8 Opus 4.6 Fast Thinking prompts — enough to fill ~1M context across sessions

## The MCP Prompt Extension Trick

Windsurf charges **1 credit per message sent to Cascade**, regardless of how many actions happen within that turn. A community trick exploits this:

**Principle**: Use MCP tools to block Cascade from ending its turn — the agent keeps reasoning and calling tools within the same "turn," effectively getting multiple rounds of work for one credit charge.

**Open-source implementations**:
- [Turn MCP](https://github.com/shiahonb777/turn-mcp) — creates checkpoint pauses within a single API request
- [Windsurf Infinite Ask](https://github.com/crispvibe/windsurf-infinite-ask) — supports image upload, conversation history, multi-window use
- [Ask Continue (LobeHub)](https://lobehub.com/zh/mcp/222cf-ask-continue-enhance) — queue mode, seamless account switching

**Windsurf's countermeasure**: A single input/output context is capped at ~100k–150k tokens. Hitting this limit triggers a new turn (new credit charge). A 100-credit trial account can run ~8 Opus prompts, roughly covering ~1M total context across sessions.

> ⚠️ This is an unofficial workaround and may violate Windsurf's ToS. It can be patched at any time.

## Pros

- **Cheaper than Cursor** — $15 vs $20 Pro; $30 vs $40 Teams
- **Full-power models** — unthrottled, not degraded versions
- **Per-prompt flat rate** — predictable cost; one credit covers all tool calls in a turn
- **Built-in deploys & previews** — ship without leaving the IDE
- **Multi-IDE support** — JetBrains, Vim, Neovim, XCode, and more
- **SWE-1.5** — fast in-house model, free for all users
- **Arena Mode** — blind model comparison
- **Enterprise security** — SOC 2, HIPAA, FedRAMP, ITAR, ZDR
- **Free tier** — 25 credits/month + unlimited Tab completions

## Cons

- **Context window smaller than Cursor** — ~100K vs ~200K (Enterprise gets more)
- **Monthly credits don't roll over** — use them or lose them
- **Uncertain future** — owned by Cognition; roadmap unclear, possible Devin integration
- **MCP auto-executes** — no human confirmation by default (security concern)
- **Credit costs rising** — community frustration about price inflation on popular models
- **Not open source** — closed-source VS Code fork
- **Settings don't sync with VS Code** — separate IDE, not an extension

## Links

- [windsurf.com](https://windsurf.com) — Official website
- [Download](https://windsurf.com/editor/download)
- [Pricing](https://windsurf.com/pricing)
- [Docs](https://docs.windsurf.com)
- [Models & credit costs](https://docs.windsurf.com/windsurf/models)
- [Changelog](https://windsurf.com/changelog)
- [MCP docs](https://docs.windsurf.com/windsurf/cascade/mcp)
- [Discord (~100k members)](https://discord.gg/GjCYNGChrw)
- [r/windsurf](https://reddit.com/r/windsurf)
- [Vim/Neovim plugin](https://github.com/exafunction/windsurf.vim)

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 简介

**Windsurf** 是 Codeium 推出的 AI 原生 IDE（VS Code fork），现由 **Cognition**（Devin 的开发商）持有。它运行**满血版模型**（非降级版），按 **prompt 次数**计费而非按月订阅。Cascade 智能体在单次对话轮次内完成多文件编辑、终端命令和全库推理。

> 所有权变迁：Codeium → OpenAI 30亿美元收购（告吹）→ Google 以 24亿美元挖走 CEO → **Cognition 收购产品**（当前，2026年）。收购时 ARR 8200 万美元。

## 功能

| 功能 | 说明 |
|------|------|
| **Cascade** | 多文件编辑、终端命令、全库搜索，单轮完成 |
| **Windsurf Tab** | AI 自动补全，所有方案无限使用 |
| **Flow** | 深度代码库索引，全仓库上下文感知 |
| **Fast Context** | swe-grep 驱动，检索速度 20×，>2800 tokens/秒 |
| **Codemaps** | 可视化代码导航，含 Mermaid 图表 |
| **Plan Mode** | 编码前生成详细实现计划；复杂任务支持 "megaplan" |
| **Arena Mode** | 盲测模型对比，含投票和排行榜 |
| **Turbo Mode** | 自动执行命令和编辑，无需手动确认 |
| **Previews** | 实时网页预览，AI 辅助元素修改 |
| **App Deploys** | 直接在 IDE 内部署应用 |
| **MCP 集成** | 连接外部工具；默认自动执行 |
| **多 IDE 插件** | JetBrains、Vim/Neovim、XCode 等 40+ IDE |
| **Cascade Hooks** | 工作流关键节点触发自定义命令 |
| **Git Worktree** | 同一仓库同时运行多个 Cascade 会话 |

## 模型

Windsurf 运行**满血版模型**，非降级版。按 prompt 计费（发送一条消息给 Cascade = 扣一次 credits，无论该轮次内发生多少 tool call）。

| 模型 | Credits/Prompt | 备注 |
|------|---------------|------|
| Claude Opus 4.6 Fast (Thinking) | 12 | 输出速度 2.5× |
| Claude Opus 4.6 Fast (Standard) | 10 | 输出速度 2.5× |
| Claude Opus 4.6 (Thinking) | 8 | 完整推理 |
| Claude Opus 4.6 (Standard) | 6 | |
| Claude Sonnet 4.6 (Thinking) | 3 | |
| Claude Sonnet 4.6 (Standard) | 2 | |
| Claude Sonnet 4.5 | 2 | 性价比之选 |
| GPT-5.3-Codex High | 2 | |
| GPT-5.3-Codex Medium | 1 | |
| GPT-5.1-Codex | 0 | credits 耗尽后仍可用 |
| Gemini 3 Pro High Thinking | 2 | |
| Kimi K2.5 | 1 | |
| SWE-1.5 | 0（促销） | Windsurf 自研模型，接近 Claude Sonnet 4.5 水平 |
| SWE-1 / SWE-1-lite | 0 | 永久免费 |
| Minimax M2.5 | 0.25 | 低成本选项 |

> Windsurf 经常对新模型推出**促销定价**，实际价格以 Cascade 模型选择器为准：[docs.windsurf.com/windsurf/models](https://docs.windsurf.com/windsurf/models)

## 额度与定价

| 方案 | 价格 | 月度 Credits | 备注 |
|------|------|-------------|------|
| **Free** | $0 | 25 | Tab 补全无限；每日 1 次部署 |
| **Pro Trial** | $0（2周） | 100 | 所有高级模型；每日 10 次部署 |
| **Pro** | $15/月 | 500 | 追加包：$10/250 credits（永不过期） |
| **Teams** | $30/用户/月 | 500/用户 | 管理后台，追加包共享 |
| **Enterprise** | $60/用户/月 | 1,000/用户 | 最长上下文、SSO/SCIM、FedRAMP/HIPAA |

关键规则：
- 月度 credits **不滚动** — 每个计费周期重置
- 追加包 credits **永不过期**
- 失败操作**不消耗** credits
- **100 credits 试用账号** ÷ 12 credits = ~8 次 Opus 4.6 Fast Thinking prompt，大约可跑满 ~1M 上下文

## MCP 延续对话技巧

Windsurf 按**每条发给 Cascade 的消息**计费，无论该轮次内发生多少操作。社区发现了一个利用此机制的技巧：

**原理**：通过 MCP 工具阻塞 Cascade 结束当前轮次 — 智能体在同一"轮次"内持续推理和调用工具，用一次 credit 完成多轮工作。

**开源实现**：
- [Turn MCP](https://github.com/shiahonb777/turn-mcp) — 在单次 API 请求内创建检查点暂停
- [Windsurf Infinite Ask](https://github.com/crispvibe/windsurf-infinite-ask) — 支持图片上传、对话历史、多窗口同时使用
- [Ask Continue (LobeHub)](https://lobehub.com/zh/mcp/222cf-ask-continue-enhance) — 队列模式、无缝切换账号、跨平台

**Windsurf 的限制**：单次输入/输出上下文上限约 100k–150k tokens，触发后开始新轮次（消耗新 credit）。100 credits 试用账号约可跑 8 次 Opus prompt，大致覆盖 ~1M 总上下文。

> ⚠️ 此为非官方变通方法，可能违反 Windsurf 服务条款，随时可能被封堵。

## 优点

- **比 Cursor 便宜** — Pro $15 vs $20；Teams $30 vs $40
- **满血版模型** — 非降级，完整能力
- **按 prompt 固定费率** — 成本可预测；一次 credit 覆盖轮次内所有 tool call
- **内置部署与预览** — 无需离开 IDE 即可上线
- **多 IDE 支持** — JetBrains、Vim、Neovim、XCode 等
- **SWE-1.5** — 快速自研模型，所有用户免费
- **Arena Mode** — 盲测模型对比
- **企业级安全** — SOC 2、HIPAA、FedRAMP、ITAR、ZDR
- **免费层** — 25 credits/月 + 无限 Tab 补全

## 缺点

- **上下文窗口小于 Cursor** — ~100K vs ~200K（Enterprise 更长）
- **月度 credits 不滚动** — 用不完就浪费
- **前途不明** — 被 Cognition 收购，路线图不清晰，可能整合进 Devin
- **MCP 自动执行** — 默认无需人工确认（安全隐患）
- **热门模型价格持续上涨** — 社区对此颇有怨言
- **不开源** — 闭源 VS Code fork
- **设置不与 VS Code 同步** — 独立 IDE，非扩展

## 链接

- [windsurf.com](https://windsurf.com) — 官网
- [下载](https://windsurf.com/editor/download)
- [定价](https://windsurf.com/pricing)
- [文档](https://docs.windsurf.com)
- [模型与 credit 费率](https://docs.windsurf.com/windsurf/models)
- [更新日志](https://windsurf.com/changelog)
- [MCP 文档](https://docs.windsurf.com/windsurf/cascade/mcp)
- [Discord（~10万成员）](https://discord.gg/GjCYNGChrw)
- [r/windsurf](https://reddit.com/r/windsurf)
- [Vim/Neovim 插件](https://github.com/exafunction/windsurf.vim)

</details>

---

<p align="center">
  <sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub>
</p>

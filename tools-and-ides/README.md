<h1 align="center">🛠️ Vibe Coding Tools & IDEs</h1>

<p align="center">
  <b>AI coding tools we actually use — deep dives with setup guides</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cursor-IDE-007ACC?logo=visual-studio-code" alt="Cursor"/>
  <img src="https://img.shields.io/badge/Codex-CLI_%2B_Extension-412991?logo=openai" alt="Codex"/>
  <img src="https://img.shields.io/badge/Claude_Code-Terminal-CC785C?logo=anthropic" alt="Claude Code"/>
  <img src="https://img.shields.io/badge/Antigravity-Google-4285F4?logo=google" alt="Antigravity"/>
  <img src="https://img.shields.io/badge/Warp-ADE-01B8AA" alt="Warp"/>
  <img src="https://img.shields.io/badge/Windsurf-IDE-0066FF" alt="Windsurf"/>
  <img src="https://img.shields.io/badge/Kiro-AWS-FF9900?logo=amazon-aws" alt="Kiro"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## Tools

| Tool | Type | Description | Read more |
|------|------|-------------|-----------|
| **[Cursor](cursor/)** | GUI IDE | VS Code fork, multi-model (GPT/Claude/Gemini), Composer & Agent, GUI diff | [cursor/README.md](cursor/README.md) |
| **[OpenAI Codex](codex/)** | Desktop + Extension + CLI | Three forms; 5-hour rolling limits; reverse proxy & CLI setup guides included | [codex/README.md](codex/README.md) |
| **[Claude Code](claude-code/)** | Terminal Agent | Anthropic's most capable agent; API relay setup, Opus verification | [claude-code/README.md](claude-code/README.md) |
| **[Google Antigravity](antigravity/)** | GUI IDE | Claude + Gemini only, free for Google Pro; TUN required, quota watcher plugin | [antigravity/README.md](antigravity/README.md) |
| **[Warp](warp/)** | Agentic Terminal (ADE) | Not an IDE — terminal-first agent environment; widest model selection; per-call credits; Oz cloud agents | [warp/README.md](warp/README.md) |
| **[Windsurf](windsurf/)** | GUI IDE | Full-power models, per-prompt credit billing, built-in deploys & previews, MCP prompt extension trick | [windsurf/README.md](windsurf/README.md) |
| **[Kiro](kiro/)** | GUI IDE | Cheapest AI IDE (AWS); full-power models but no extended thinking; fast; great for API reverse proxy to other IDEs | [kiro/README.md](kiro/README.md) |

## Quick Comparison

| | Cursor | Codex | Claude Code | Antigravity | Warp | Windsurf | Kiro |
|---|---|---|---|---|---|---|---|
| **Interface** | GUI (VS Code fork) | Desktop / Extension / CLI | Terminal only | GUI (VS Code-like) | Terminal / ADE | GUI (VS Code fork) | GUI (Code OSS) |
| **Models** | GPT, Claude, Gemini | OpenAI models | Claude (Opus/Sonnet) | Claude + Gemini | Claude, GPT, Gemini (widest) | Full-power, all major | Claude + DeepSeek + Qwen |
| **Pricing** | ~$20/mo Pro + credits | Rolling limits (nearly free) | Subscription or API relay | Free for Google Pro | Per-call credits; ~300 free | Per-prompt credits; $15/mo Pro | Cheapest; $0 free tier |
| **Extended Thinking** | Yes | — | Yes | — | Yes (Opus max) | Yes (Opus Thinking) | No (roadmap) |
| **Remote server** | Native SSH | Extension: reverse tunnel; CLI: tmux + proxy | API relay (no VPN needed) | TUN mode required | Cloud (Oz) | Cloud | Cloud |
| **Best for** | GUI lovers, model flexibility | Budget-conscious, multi-form | Power users, best agent | Google Pro subscribers | Terminal-native, widest models | Budget frontier models, per-prompt billing | Cheapest Claude access, API reverse proxy |

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 工具

| 工具 | 类型 | 说明 | 阅读更多 |
|------|------|------|----------|
| **[Cursor](cursor/)** | 图形 IDE | VS Code 分支，多模型（GPT/Claude/Gemini），Composer 与 Agent，GUI diff | [cursor/README.md](cursor/README.md) |
| **[OpenAI Codex](codex/)** | 桌面 + 扩展 + CLI | 三种形态；5 小时滚动额度；含反向代理与 CLI 配置教程 | [codex/README.md](codex/README.md) |
| **[Claude Code](claude-code/)** | 终端智能体 | Anthropic 能力最强的智能体；API 中转配置、Opus 验证方法 | [claude-code/README.md](claude-code/README.md) |
| **[Google Antigravity](antigravity/)** | 图形 IDE | 仅 Claude + Gemini，Google Pro 免费；需 TUN，额度监控插件 | [antigravity/README.md](antigravity/README.md) |
| **[Warp](warp/)** | 智能体终端（ADE） | 不是 IDE — 终端优先的智能体开发环境；模型选择最广；按调用计费；Oz 云端智能体 | [warp/README.md](warp/README.md) |
| **[Windsurf](windsurf/)** | 图形 IDE | 满血版模型，按 prompt 计费，内置部署与预览，MCP 延续对话技巧 | [windsurf/README.md](windsurf/README.md) |
| **[Kiro](kiro/)** | 图形 IDE | 最便宜的 AI IDE（AWS 出品）；满血模型但无 extended thinking；速度快；适合反代 API 到其他 IDE | [kiro/README.md](kiro/README.md) |

## 快速对比

| | Cursor | Codex | Claude Code | Antigravity | Warp | Windsurf | Kiro |
|---|---|---|---|---|---|---|---|
| **界面** | GUI（VS Code 分支） | 桌面 / 扩展 / CLI | 纯终端 | GUI（类 VS Code） | 终端 / ADE | GUI（VS Code 分支） | GUI（Code OSS） |
| **模型** | GPT、Claude、Gemini | OpenAI 模型 | Claude（Opus/Sonnet） | Claude + Gemini | Claude、GPT、Gemini（最广） | 满血全系主流模型 | Claude + DeepSeek + Qwen |
| **定价** | Pro ~$20/月 + 额度 | 滚动额度（几乎免费） | 订阅或 API 中转 | Google Pro 免费 | 按调用计费；~300 免费 | 按 prompt 计费；Pro $15/月 | 最便宜；$0 免费层 |
| **Extended Thinking** | 有 | — | 有 | — | 有（Opus max） | 有（Opus Thinking） | 无（路线图中） |
| **远程服务器** | 原生 SSH | Extension: 反向隧道；CLI: tmux + 代理 | API 中转（无需 VPN） | 需 TUN 模式 | 云端（Oz） | 云端 | 云端 |
| **适合** | 喜欢 GUI、需要模型灵活度 | 预算有限、多形态使用 | 重度用户、最强智能体 | Google Pro 订阅者 | 终端原生、模型选择最广 | 预算前沿模型、按 prompt 计费 | 最便宜 Claude 访问、API 反代 |

</details>

---

<p align="center">
  <sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub>
</p>

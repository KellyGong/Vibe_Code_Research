<h1 align="center">Kiro</h1>

<p align="center">
  <b>最便宜的 AI IDE · 满血模型 · 反代友好</b><br>
  <sub>AWS 出品，基于 Code OSS，速度快，适合将 API 反代到其他 IDE 使用</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kiro-AWS-FF9900?logo=amazon-aws" alt="AWS"/>
  <img src="https://img.shields.io/badge/VS_Code-Compatible-007ACC?logo=visual-studio-code" alt="VS Code"/>
  <img src="https://img.shields.io/badge/Pricing-Cheapest_AI_IDE-brightgreen" alt="Pricing"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Is

**Kiro** is an AI IDE by **Amazon Web Services**, built on Code OSS (VS Code compatible). It's currently the **cheapest AI IDE** on the market with a generous free tier. Models run at full power but **extended thinking / deep reasoning is not enabled** natively in the IDE — responses are fast but lack the "think harder" toggle. The official GitHub issues indicate **1M context and full reasoning support are on the roadmap**.

A popular community use case: **reverse-proxy Kiro's free Claude access into other IDEs** (Cursor, Cline, Claude Code, etc.) via community gateway projects.

## Features

| Feature | Description |
|---------|-------------|
| **Agentic Chat** | Multi-turn AI chat with file and documentation context |
| **Spec-Driven Development** | Auto-generates requirements → design → task lists before coding |
| **Kiro Hooks** | Event-driven automations for docs, tests, and optimization |
| **Multi-Agent Workflows** | Lead + subagent coordination for complex tasks |
| **MCP Support** | Model Context Protocol for local and remote tool servers |
| **Steering Rules** | Project-level rules to guide AI behavior |
| **VS Code Compatible** | Keeps existing settings, keybindings, and Open VSX plugins |
| **CLI (`kiro-cli`)** | Terminal-based agentic workflows |
| **ACP (Agent Client Protocol)** | Use Kiro's AI in JetBrains, Neovim, Emacs, Zed, Eclipse |

## Models

Models run at **full power** but without extended thinking mode natively. Fast response times.

| Model | Credit Multiplier | Notes |
|-------|-------------------|-------|
| **Claude Sonnet 4.6** | 1.3× | Latest (experimental, Feb 2026) |
| **Claude Opus 4.6** | Higher | Available in eu-central-1 |
| **Claude Sonnet 4.5** | 1.0× (base) | Default workhorse |
| **Claude Haiku 4.5** | Lower | Fast, lightweight |
| **DeepSeek 3.2** | 0.25× | 685B MoE; best for agentic workflows |
| **MiniMax 2.1** | 0.15× | 230B MoE; multilingual, UI generation |
| **Qwen3 Coder Next** | 0.05× | 80B MoE; 256K context; extremely cheap |

> **No extended thinking**: The IDE does not expose a reasoning toggle. The community [Kiro Gateway](https://github.com/jwadow/kiro-gateway) proxy actually enables extended thinking that the native IDE doesn't — a notable advantage of the reverse proxy approach.

> **Roadmap**: GitHub issues reference 1M token context support and full reasoning mode. Official response confirms it's being prepared.

## Credits & Pricing

Kiro is the **cheapest AI IDE** available.

| Plan | Price | Credits/month | Overage | Notes |
|------|-------|---------------|---------|-------|
| **Free** | $0 | 50 | — | +500 bonus credits on signup (30-day expiry) |
| **Pro** | $20/mo | 1,000 | $0.04/credit | Standard plan |
| **Pro+** | $40/mo | 2,000 | $0.04/credit | Double credits |
| **Power** | $200/mo | 10,000 | $0.04/credit | Heavy usage |
| **Enterprise** | Custom | Custom | Custom | SSO, SAML/SCIM, team billing |

Credits are consumed fractionally (0.01 increments) based on task complexity and model multiplier.

## The Reverse Proxy Use Case

Because Kiro offers **free Claude model access** with a $0 account, the most popular community hack is **reverse-proxying Kiro's API to use Claude in other IDEs for free**.

### Kiro Gateway

| Detail | Info |
|--------|------|
| **Repo** | [github.com/jwadow/kiro-gateway](https://github.com/jwadow/kiro-gateway) (459 ⭐) |
| **What it does** | Exposes Kiro's Claude models as OpenAI-compatible and Anthropic-compatible API endpoints |
| **Free tier models** | Claude Sonnet 4.5, Haiku 4.5, Sonnet 4, Claude 3.7 Sonnet, DeepSeek 3.2, MiniMax 2.1, Qwen3 Coder Next |
| **Compatible clients** | Cursor, Claude Code, Cline, Roo Code, Codex, VSCode+Continue, LangChain, OpenAI SDK |
| **Bonus** | Enables **extended thinking** — a feature the native IDE doesn't expose |

```bash
git clone https://github.com/Jwadow/kiro-gateway.git
cd kiro-gateway
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set KIRO_CREDS_FILE and PROXY_API_KEY
python main.py
# Server at http://localhost:8000 — use as OpenAI base_url in Cursor/Cline/etc.
```

Other proxies: [kiro-claude-proxy (Node.js)](https://github.com/9zq3n/kiro-claude-proxy) · [9Router (multi-account)](https://github.com/decolua/9router)

## Pros

- **Cheapest AI IDE** — $0 free tier with Claude Sonnet access; $20/mo for 1,000 credits
- **Fast responses** — backend is responsive and reliable
- **VS Code compatible** — familiar interface, existing extensions work
- **Open weight models** — DeepSeek, Qwen3 at very low multipliers (0.05×–0.25×)
- **Reverse proxy friendly** — free Claude usable in Cursor, Cline, Claude Code via community gateways
- **ACP support** — use Kiro AI in JetBrains, Neovim, Emacs, Zed without switching IDEs
- **CLI available** — terminal-based agentic workflows

## Cons

- **No extended thinking natively** — models lack deep reasoning mode in the IDE (gateway workaround exists)
- **Features most basic** among the three IDEs covered here — fewer agent capabilities than Cursor or Windsurf
- **No line-by-line diff** — lacks granular diff highlighting
- **Context management bugs** — sessions hit context limits prematurely; `.kiroignore` not always respected
- **Spec workflow can be rigid** — fixed 3-step order (requirements → design → tasks)
- **Over-engineering tendency** — AI generates excessive tests and complexity unless told otherwise

## Links

- [kiro.dev](https://kiro.dev) — Official website
- [Downloads](https://kiro.dev/downloads/)
- [Pricing](https://kiro.dev/pricing/)
- [Docs](https://kiro.dev/docs/)
- [Changelog](https://kiro.dev/changelog/)
- [GitHub Issues](https://github.com/kirodotdev/Kiro/issues) — roadmap signals (1M context, reasoning)
- [CLI docs](https://kiro.dev/cli/)
- [Kiro Gateway (reverse proxy)](https://github.com/jwadow/kiro-gateway)

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 简介

**Kiro** 是 **Amazon Web Services** 推出的 AI IDE，基于 Code OSS（兼容 VS Code）。它是目前**最便宜的 AI IDE**，免费层慷慨。模型以满血运行，但 IDE 内**未开启 extended thinking / 深度推理模式** — 响应速度快，但缺少"深度思考"开关。官方 GitHub issues 显示 **1M 上下文和完整推理支持正在准备中**。

社区最热门用法：通过社区网关项目将 Kiro 的免费 Claude 访问**反向代理到其他 IDE**（Cursor、Cline、Claude Code 等）使用。

## 功能

| 功能 | 说明 |
|------|------|
| **Agentic Chat** | 多轮 AI 对话，含文件和文档上下文 |
| **规格驱动开发** | 编码前自动生成需求 → 设计 → 任务列表 |
| **Kiro Hooks** | 文档、测试、优化的事件驱动自动化 |
| **多智能体工作流** | 主智能体 + 子智能体协作处理复杂任务 |
| **MCP 支持** | 本地和远程工具服务器的 Model Context Protocol |
| **Steering Rules** | 项目级规则引导 AI 行为 |
| **VS Code 兼容** | 保留现有设置、快捷键和 Open VSX 插件 |
| **CLI（kiro-cli）** | 终端智能体工作流 |
| **ACP（Agent Client Protocol）** | 在 JetBrains、Neovim、Emacs、Zed、Eclipse 中使用 Kiro AI |

## 模型

模型以**满血**运行，但 IDE 内未开启 extended thinking。响应速度快。

| 模型 | 积分倍率 | 备注 |
|------|---------|------|
| **Claude Sonnet 4.6** | 1.3× | 最新（实验性，2026年2月） |
| **Claude Opus 4.6** | 更高 | 在 eu-central-1 可用 |
| **Claude Sonnet 4.5** | 1.0×（基准） | 默认主力模型 |
| **Claude Haiku 4.5** | 更低 | 快速轻量 |
| **DeepSeek 3.2** | 0.25× | 685B MoE；最适合 agentic 工作流 |
| **MiniMax 2.1** | 0.15× | 230B MoE；多语言、UI 生成 |
| **Qwen3 Coder Next** | 0.05× | 80B MoE；256K 上下文；极低成本 |

> **无 extended thinking**：IDE 未暴露推理开关。社区 [Kiro Gateway](https://github.com/jwadow/kiro-gateway) 反代项目反而能开启 extended thinking — 这是反代方案的一个额外优势。

> **路线图**：GitHub issues 提及 1M token 上下文支持和完整推理模式，官方已回应正在准备中。

## 额度与定价

Kiro 是目前**最便宜的 AI IDE**。

| 方案 | 价格 | 月度积分 | 超额 | 备注 |
|------|------|---------|------|------|
| **Free** | $0 | 50 | — | 注册送 500 积分（30天有效） |
| **Pro** | $20/月 | 1,000 | $0.04/积分 | 标准方案 |
| **Pro+** | $40/月 | 2,000 | $0.04/积分 | 双倍积分 |
| **Power** | $200/月 | 10,000 | $0.04/积分 | 重度使用 |
| **Enterprise** | 定制 | 定制 | 定制 | SSO、SAML/SCIM、团队计费 |

积分按任务复杂度和模型倍率小数消耗（最小 0.01 增量）。

## 反向代理用法

由于 Kiro 提供 **$0 账号的免费 Claude 访问**，社区最热门的玩法是**将 Kiro API 反向代理到其他 IDE 中免费使用 Claude**。

### Kiro Gateway

| 详情 | 信息 |
|------|------|
| **仓库** | [github.com/jwadow/kiro-gateway](https://github.com/jwadow/kiro-gateway)（459 ⭐） |
| **功能** | 将 Kiro 的 Claude 模型暴露为 OpenAI 兼容和 Anthropic 兼容的 API 端点 |
| **免费层模型** | Claude Sonnet 4.5、Haiku 4.5、Sonnet 4、Claude 3.7 Sonnet、DeepSeek 3.2、MiniMax 2.1、Qwen3 Coder Next |
| **兼容客户端** | Cursor、Claude Code、Cline、Roo Code、Codex、VSCode+Continue、LangChain、OpenAI SDK |
| **额外福利** | 开启 **extended thinking** — IDE 原生不支持的功能 |

```bash
git clone https://github.com/Jwadow/kiro-gateway.git
cd kiro-gateway
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env：设置 KIRO_CREDS_FILE 和 PROXY_API_KEY
python main.py
# 服务运行在 http://localhost:8000 — 在 Cursor/Cline 等中设为 OpenAI base_url
```

其他代理：[kiro-claude-proxy（Node.js）](https://github.com/9zq3n/kiro-claude-proxy) · [9Router（多账号）](https://github.com/decolua/9router)

## 优点

- **最便宜的 AI IDE** — $0 免费层含 Claude Sonnet；$20/月 1000 积分
- **响应速度快** — 后端稳定可靠
- **VS Code 兼容** — 熟悉的界面，现有扩展可用
- **开源模型** — DeepSeek、Qwen3 倍率极低（0.05×–0.25×）
- **反代友好** — 通过社区网关在 Cursor、Cline、Claude Code 中免费用 Claude
- **ACP 支持** — 无需切换 IDE，在 JetBrains、Neovim、Emacs、Zed 中使用 Kiro AI
- **CLI 可用** — 终端智能体工作流

## 缺点

- **IDE 内无 extended thinking** — 模型缺少深度推理模式（反代方案可绕过）
- **功能最简陋** — 三款 IDE 中智能体能力最基础
- **无行级 diff** — 缺少精细的差异高亮
- **上下文管理 bug** — 会话过早触及上下文限制；`.kiroignore` 不总是生效
- **规格工作流较僵硬** — 固定三步顺序（需求 → 设计 → 任务）
- **过度工程化倾向** — 不明确说明时 AI 会生成过多测试和复杂度

## 链接

- [kiro.dev](https://kiro.dev) — 官网
- [下载](https://kiro.dev/downloads/)
- [定价](https://kiro.dev/pricing/)
- [文档](https://kiro.dev/docs/)
- [更新日志](https://kiro.dev/changelog/)
- [GitHub Issues](https://github.com/kirodotdev/Kiro/issues) — 路线图信号（1M 上下文、推理模式）
- [CLI 文档](https://kiro.dev/cli/)
- [Kiro Gateway（反向代理）](https://github.com/jwadow/kiro-gateway)

</details>

---

<p align="center">
  <sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub>
</p>

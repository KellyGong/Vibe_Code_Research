<h1 align="center">Cursor Advanced Usage</h1>

<p align="center">
  <b>Context optimization, subagents, rules, and custom API keys</b><br>
  <sub>Get more out of your Cursor Pro subscription</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cursor-Pro_Required-007ACC?logo=visual-studio-code" alt="Pro"/>
  <img src="https://img.shields.io/badge/Context-Optimization-5C2D91" alt="Context"/>
  <img src="https://img.shields.io/badge/Subagents-Parallel_Tasks-green" alt="Subagents"/>
</p>

---

<details open>
<summary><b>English</b></summary>

## Why This Matters

Cursor's context window is finite (~200k tokens for most models). As conversations grow — file reads, tool outputs, back-and-forth messages — the window fills up and quality degrades. Mastering context management is the difference between a productive session and a frustrating one.

This guide covers three pillars of advanced Cursor usage:

1. **Context Optimization** — Save tokens, stay sharp
2. **Rules & Subagents** — Automate guidance and delegate work
3. **Custom API Keys** — Use your own models and providers

---

## 1. Context Optimization

### How Context Works

Everything in your conversation consumes tokens: system prompts, rules, file contents, tool outputs, and chat history. When the window fills, Cursor triggers lossy summarization — details get lost.

| Item | Approximate Tokens |
|------|--------------------|
| Agent codebase exploration | 50,000+ |
| 10-message conversation | 20,000–40,000 |
| Always-apply rule (100 lines) | 500–1,000 |
| 500-line TypeScript file | 3,000–5,000 |

### Key Techniques

| Technique | How |
|-----------|-----|
| **Delegate to Subagents** | Let subagents handle codebase exploration, file reading, and implementation — the main agent only receives summaries, keeping its context window clean (see [Subagents](#3-subagents) below) |
| **Write project summary rules** | Periodically ask the agent to write a project overview as a Rule file (e.g., `.cursor/rules/project-overview.mdc`). New conversations just read this rule and instantly understand the project — no need to re-explore the entire codebase |
| **Start fresh chats often** | Don't let conversations drag past 6–8 exchanges; start a new chat when switching tasks |
| **Front-load context** | Put all relevant info in the first message instead of spreading across multiple messages |
| **Use `@` mentions wisely** | `@File` for specific files, `@Folder` for structure overview, `@Codebase` for semantic search |
| **Use `.cursorignore`** | Exclude build artifacts, `node_modules`, generated code from indexing (syntax same as `.gitignore`) |
| **Audit always-apply rules** | Every always-apply rule consumes tokens on every prompt — convert to glob-scoped or agent-decided when possible |
| **Close irrelevant files** | Open files are automatically included as context |
| **Use Plan Mode first** | `Shift+Tab` to plan before coding — saves wasted exploration tokens |

### The "Main Agent + Subagents" Workflow

The most effective pattern for long-lived projects:

1. **Main agent** stays focused on high-level conversation — discussing features, reviewing plans, making decisions
2. **Subagents explore** — when you need to understand the codebase, the main agent spawns an `Explore` subagent that reads files and returns a concise overview, instead of polluting the main context with raw file contents
3. **Subagents implement** — when it's time to write code, the main agent delegates to implementation subagents. Each subagent gets its own context window for the actual file edits
4. **Main agent retains memory** — because the main conversation isn't bloated with tool outputs and file reads, it can sustain a much longer productive session

This way, the main agent acts as an orchestrator with persistent memory, while subagents handle the heavy lifting in isolated contexts.

### The "Project Summary as Rule" Pattern

Instead of letting every new conversation re-explore your project from scratch (costing 50k+ tokens), maintain a living project summary:

1. At the end of a productive session, ask the agent: *"Write a project overview rule summarizing the architecture, key files, and current progress"*
2. Save it as `.cursor/rules/project-overview.mdc` with `alwaysApply: true`
3. Next conversation starts with full project context for ~500–1,000 tokens instead of 50,000+

```yaml
# .cursor/rules/project-overview.mdc
---
description: "Project architecture and current status"
alwaysApply: true
---

## Project: MyApp
- **Stack:** Next.js 14 + Prisma + PostgreSQL
- **Structure:** src/app (pages), src/lib (utils), src/components (UI)
- **Current sprint:** User auth flow (JWT + refresh tokens)
- **Key files:** src/lib/auth.ts, src/app/api/auth/[...nextauth]/route.ts
- **Recent changes:** Added password reset endpoint, pending email verification
```

This single rule replaces thousands of tokens of codebase exploration at the start of every conversation.

### The `@` Mention System

| Symbol | What It Does |
|--------|-------------|
| `@File` | Reference specific files; auto-chunked by size |
| `@Folder` | Include directory structure overview (cheaper than multiple `@File`) |
| `@Code` | Reference specific functions or code blocks |
| `@Codebase` | Semantic search across entire codebase |
| `@Docs` | Reference external documentation by URL |
| `@ruleName` | Manually invoke a specific rule |

### `.cursorignore`

Place a `.cursorignore` file in your project root. Syntax is identical to `.gitignore`:

```
dist/
node_modules/
*.log
build/
.env
```

Files matching these patterns are excluded from codebase indexing, keeping your context clean.

> **Docs:** [Ignore Files](https://docs.cursor.com/context/ignore-files) · [Working with Context](https://docs.cursor.com/guides/working-with-context) · [Context (Learn)](https://cursor.com/learn/context)

---

## 2. Rules

Rules inject persistent instructions into the AI's system prompt — project conventions, coding standards, architecture decisions — so you don't repeat yourself every conversation.

### Rule Types

| Type | Scope | Description |
|------|-------|-------------|
| **Project Rules** | `.cursor/rules/` | Version-controlled, scoped to your codebase |
| **User Rules** | Settings → Rules | Global to your Cursor environment |
| **Team Rules** | Dashboard | Organization-wide (Team/Enterprise plans) |
| **AGENTS.md** | Project root | Plain markdown alternative for simple cases |

### Activation Modes

| Mode | Behavior |
|------|----------|
| `Always Apply` | Included in every chat session |
| `Apply Intelligently` | Agent decides relevance based on the rule's `description` field |
| `Apply to Specific Files` | Auto-attached when files match `globs` patterns |
| `Apply Manually` | Only included when you `@mention` the rule |

### Creating a Rule

Command Palette → `New Cursor Rule`, or `Cursor Settings → Rules`

```yaml
# .cursor/rules/react-patterns.mdc
---
description: "Standards for frontend components"
globs: "src/components/**/*.tsx"
alwaysApply: false
---

- Use functional components with hooks
- Always export with React.memo for expensive renders
- Use TypeScript strict mode
```

### Best Practices

- Keep rules under 500 lines — reference files with `@` instead of inlining code
- Convert large always-apply rules to glob-scoped or agent-decided
- Check rules into git so the whole team benefits
- Add rules only when you notice the Agent making the same mistake repeatedly

> **Docs:** [Rules](https://cursor.com/docs/context/rules) · [Skills](https://cursor.com/docs/context/skills)

---

## 3. Subagents

Subagents are independent agents that handle discrete parts of a parent agent's task. Each runs in its own isolated context window — and this is arguably the single most important context optimization technique in Cursor.

### How They Work

1. The parent agent encounters a complex task
2. It spawns one or more subagents via the **Task tool**
3. Each subagent runs in parallel with its own context, tools, and (optionally) model
4. Results flow back as summaries — intermediate output stays in the subagent

### Built-in Subagents

| Subagent | Purpose |
|----------|---------|
| **Explore** | Fast codebase search and file discovery |
| **Shell** | Terminal command execution |
| **Browser** | Web browsing via MCP tools |

### Why Subagents Are the Best Context Saver

Without subagents, a single conversation accumulates all exploration, tool output, and intermediate reasoning. Reading 10 files? That's 30k–50k tokens gone. Running a few shell commands? Another 5k–10k. The context window bloats fast and quality degrades.

With the "main agent + subagents" pattern:

- **Exploration stays isolated** — an `Explore` subagent reads 20 files but only returns a 500-token overview to the main agent
- **Implementation stays isolated** — a subagent handles the actual code edits in its own context; the main agent just sees "done, here's what I changed"
- **Main agent keeps its memory** — because it's not bloated with raw file contents and tool outputs, the main conversation can sustain 20+ productive exchanges instead of degrading after 6–8
- **Parallel work** — multiple subagents can tackle different parts of a task simultaneously, each with a fresh context window
- **Model flexibility** — use a fast/cheap model for exploration subagents, a capable model for the main agent's decision-making

Think of it as: **the main agent is the architect, subagents are the builders.** The architect doesn't need to read every blueprint detail — just the summary.

### Custom Subagents

You can define custom subagents in `.cursor/agents/*.md` with YAML frontmatter, specifying tools, model preferences, and instructions.

> **Docs:** [Subagents](https://cursor.com/docs/context/subagents) · [Agent Overview](https://docs.cursor.com/en/agent/overview) · [Agent Tools](https://docs.cursor.com/en/agent/tools) · [Scaling Agents (Blog)](https://cursor.com/blog/scaling-agents)

---

## 4. Custom API Keys

**Requires: Cursor Pro subscription (for Agent/Composer modes)**

Cursor lets you plug in your own API keys from OpenAI, Anthropic, Google, Azure, and other providers. When using custom keys, you pay the AI provider directly — not Cursor.

### Setup

1. Go to **Cursor Settings → Models → API Keys**
2. Enter your API key for the desired provider
3. Click **Verify** to validate
4. The provider's models become available in the model dropdown

### Supported Providers

| Provider | Key Type | Notes |
|----------|----------|-------|
| **OpenAI** | API Key | GPT-4, GPT-4o, o1, etc. |
| **Anthropic** | API Key | Claude Opus, Sonnet, Haiku |
| **Google** | API Key | Gemini Pro, Flash |
| **Azure OpenAI** | Base URL + Deployment + Key | Enterprise deployments |

### Third-Party Relays

You can also route through third-party API endpoints:
- **Azure-compatible endpoints** — Any provider with Azure-compatible API format
- **LiteLLM Proxy** — Unified proxy for 100+ providers (works with Ask/Plan modes)
- **Custom bridges** — Convert proprietary formats to OpenAI/Anthropic-compatible endpoints

### Important Notes

> **⚠️ Tool Call Compatibility:** Some third-party relays have broken tool/function call implementations, which will cause Agent/Composer modes to fail. Test with simple tasks first.

> **⚠️ Free Plan Limitations:** Custom API keys work for basic chat on the free plan, but Agent, Edit, and Composer modes require a Pro subscription even with your own keys.

> **Docs:** [API Keys](https://docs.cursor.com/en/settings/api-keys) · [Models](https://docs.cursor.com/settings/models)

---

## Links

- [Cursor Docs](https://docs.cursor.com)
- [Rules](https://cursor.com/docs/context/rules)
- [Subagents](https://cursor.com/docs/context/subagents)
- [Context Management](https://docs.cursor.com/guides/working-with-context)
- [API Keys](https://docs.cursor.com/en/settings/api-keys)
- [Ignore Files](https://docs.cursor.com/context/ignore-files)
- [Scaling Agents Blog](https://cursor.com/blog/scaling-agents)

</details>

---

<details>
<summary><b>中文</b></summary>

## 为什么要关注这些

Cursor 的上下文窗口是有限的（大多数模型约 200k tokens）。随着对话增长——文件读取、工具输出、来回消息——窗口会被填满，质量随之下降。掌握上下文管理是高效使用和低效使用的分水岭。

本指南覆盖 Cursor 进阶使用的三大支柱：

1. **上下文优化** — 节省 token，保持精准
2. **Rules 与 Subagents** — 自动化指导与任务委派
3. **自定义 API 密钥** — 使用你自己的模型和服务商

---

## 1. 上下文优化

### 上下文如何运作

对话中的一切都消耗 token：系统提示、规则、文件内容、工具输出和聊天历史。窗口填满后，Cursor 会触发有损压缩（summarization）——细节会丢失。

| 项目 | 大约 Token 数 |
|------|--------------|
| Agent 代码库探索 | 50,000+ |
| 10 条消息的对话 | 20,000–40,000 |
| Always-apply 规则（100 行） | 500–1,000 |
| 500 行 TypeScript 文件 | 3,000–5,000 |

### 核心技巧

| 技巧 | 方法 |
|------|------|
| **委派给 Subagents** | 让子代理处理代码库探索、文件阅读和具体实现——主代理只接收摘要，保持上下文窗口干净（详见下方 [Subagents](#3-subagents子代理)） |
| **写项目总结文档作为 Rule** | 定期让 Agent 把项目概览写成 Rule 文件（如 `.cursor/rules/project-overview.mdc`）。新对话只需读这条 Rule 就能了解项目全貌——不用重新探索整个代码库 |
| **频繁开新对话** | 对话超过 6–8 轮就开新的；切换任务时必须新开 |
| **首条消息放全所有上下文** | 把相关信息集中在第一条消息，不要分散在多条里 |
| **善用 `@` 提及** | `@File` 指定文件、`@Folder` 看结构、`@Codebase` 语义搜索 |
| **使用 `.cursorignore`** | 排除构建产物、`node_modules`、生成代码，不让它们进入索引 |
| **审查 always-apply 规则** | 每条 always-apply 规则每次提示都消耗 token——能改成 glob 或 agent-decided 就改 |
| **关闭无关文件** | 打开的文件会自动被纳入上下文 |
| **先用 Plan Mode** | `Shift+Tab` 先规划再编码——减少无效探索消耗 |

### "主代理 + 子代理"工作流

长期项目中最高效的使用模式：

1. **主代理**专注于高层对话——讨论功能、审查方案、做决策
2. **子代理负责探索**——需要了解代码库时，主代理派出 `Explore` 子代理去读文件，返回精简概览，而不是把原始文件内容塞进主上下文
3. **子代理负责实现**——到了写代码的时候，主代理委派给实现子代理。每个子代理在自己的上下文窗口里完成文件编辑
4. **主代理保留记忆**——因为主对话没有被工具输出和文件读取撑爆，它可以维持更长时间的高效会话

这样，主代理充当一个有持久记忆的调度器，子代理在隔离的上下文中干重活。

### "项目总结作为 Rule"模式

与其让每个新对话都从头探索项目（消耗 50k+ token），不如维护一份活的项目总结：

1. 在一次高效会话结束时，让 Agent：*"把项目架构、关键文件和当前进度写成一条 Rule"*
2. 保存为 `.cursor/rules/project-overview.mdc`，设置 `alwaysApply: true`
3. 下次对话开始时，只需约 500–1,000 token 就能获得完整项目上下文，而不是 50,000+

```yaml
# .cursor/rules/project-overview.mdc
---
description: "项目架构与当前状态"
alwaysApply: true
---

## 项目：MyApp
- **技术栈：** Next.js 14 + Prisma + PostgreSQL
- **结构：** src/app（页面）、src/lib（工具）、src/components（UI）
- **当前迭代：** 用户认证流程（JWT + refresh tokens）
- **关键文件：** src/lib/auth.ts, src/app/api/auth/[...nextauth]/route.ts
- **最近变更：** 添加了密码重置端点，邮箱验证待完成
```

这一条 Rule 就能替代每次新对话开头数千 token 的代码库探索。

### `@` 提及系统

| 符号 | 作用 |
|------|------|
| `@File` | 引用特定文件，按大小自动分块 |
| `@Folder` | 引入目录结构概览（比多个 `@File` 更省 token） |
| `@Code` | 引用特定函数或代码块 |
| `@Codebase` | 对整个代码库进行语义搜索 |
| `@Docs` | 通过 URL 引用外部文档 |
| `@ruleName` | 手动调用特定规则 |

### `.cursorignore`

在项目根目录放一个 `.cursorignore` 文件，语法与 `.gitignore` 完全一致：

```
dist/
node_modules/
*.log
build/
.env
```

匹配的文件会被排除在代码库索引之外，保持上下文干净。

> **文档：** [Ignore Files](https://docs.cursor.com/context/ignore-files) · [Working with Context](https://docs.cursor.com/guides/working-with-context) · [Context (Learn)](https://cursor.com/learn/context)

---

## 2. Rules（规则）

Rules 将持久化指令注入 AI 的系统提示——项目规范、编码标准、架构决策——这样你不用每次对话都重复说明。

### 规则类型

| 类型 | 作用域 | 说明 |
|------|--------|------|
| **Project Rules** | `.cursor/rules/` | 版本控制，作用于当前代码库 |
| **User Rules** | Settings → Rules | 全局，作用于你的 Cursor 环境 |
| **Team Rules** | Dashboard | 组织级别（Team/Enterprise 套餐） |
| **AGENTS.md** | 项目根目录 | 纯 Markdown 替代方案，适合简单场景 |

### 激活模式

| 模式 | 行为 |
|------|------|
| `Always Apply` | 每次对话都包含 |
| `Apply Intelligently` | Agent 根据规则的 `description` 字段判断是否相关 |
| `Apply to Specific Files` | 文件匹配 `globs` 模式时自动附加 |
| `Apply Manually` | 仅在你 `@mention` 该规则时包含 |

### 创建规则

Command Palette → `New Cursor Rule`，或 `Cursor Settings → Rules`

```yaml
# .cursor/rules/react-patterns.mdc
---
description: "前端组件规范"
globs: "src/components/**/*.tsx"
alwaysApply: false
---

- 使用函数组件 + Hooks
- 昂贵渲染的组件用 React.memo 导出
- 使用 TypeScript strict 模式
```

### 最佳实践

- 规则控制在 500 行以内——用 `@` 引用文件而不是内联代码
- 大型 always-apply 规则改为 glob 或 agent-decided
- 把规则提交到 git，让整个团队受益
- 只在发现 Agent 反复犯同一个错误时才加规则

> **文档：** [Rules](https://cursor.com/docs/context/rules) · [Skills](https://cursor.com/docs/context/skills)

---

## 3. Subagents（子代理）

Subagents 是独立的代理，处理父代理任务的离散部分。每个子代理在自己隔离的上下文窗口中运行——这可以说是 Cursor 中最重要的上下文优化手段。

### 工作原理

1. 父代理遇到复杂任务
2. 通过 **Task tool** 生成一个或多个子代理
3. 每个子代理并行运行，拥有自己的上下文、工具和（可选的）模型
4. 结果以摘要形式返回——中间输出留在子代理内部

### 内置子代理

| 子代理 | 用途 |
|--------|------|
| **Explore** | 快速代码库搜索和文件发现 |
| **Shell** | 终端命令执行 |
| **Browser** | 通过 MCP 工具浏览网页 |

### 为什么 Subagents 是最好的上下文节省手段

没有 Subagents 时，单个对话会累积所有探索、工具输出和中间推理。读 10 个文件？30k–50k token 没了。跑几个 shell 命令？又是 5k–10k。上下文窗口很快就会膨胀，质量随之下降。

用"主代理 + 子代理"模式：

- **探索隔离** — `Explore` 子代理读了 20 个文件，但只返回 500 token 的概览给主代理
- **实现隔离** — 子代理在自己的上下文里完成代码编辑；主代理只看到"搞定了，改了这些"
- **主代理保留记忆** — 因为没有被原始文件内容和工具输出撑爆，主对话可以维持 20+ 轮高效交流，而不是 6–8 轮后就开始退化
- **并行工作** — 多个子代理可以同时处理任务的不同部分，每个都有全新的上下文窗口
- **模型灵活** — 探索子代理用快速/便宜的模型，主代理的决策用强力模型

可以这样理解：**主代理是架构师，子代理是施工队。** 架构师不需要读每一张图纸的细节——只需要看摘要。

### 自定义子代理

你可以在 `.cursor/agents/*.md` 中定义自定义子代理，通过 YAML frontmatter 指定工具、模型偏好和指令。

> **文档：** [Subagents](https://cursor.com/docs/context/subagents) · [Agent Overview](https://docs.cursor.com/en/agent/overview) · [Agent Tools](https://docs.cursor.com/en/agent/tools) · [Scaling Agents (Blog)](https://cursor.com/blog/scaling-agents)

---

## 4. 自定义 API 密钥

**需要：Cursor Pro 订阅（Agent/Composer 模式）**

Cursor 允许你接入自己的 API 密钥，支持 OpenAI、Anthropic、Google、Azure 等服务商。使用自定义密钥时，费用直接付给 AI 服务商，不经过 Cursor。

### 配置方法

1. 进入 **Cursor Settings → Models → API Keys**
2. 输入对应服务商的 API 密钥
3. 点击 **Verify** 验证
4. 该服务商的模型会出现在模型下拉菜单中

### 支持的服务商

| 服务商 | 密钥类型 | 说明 |
|--------|----------|------|
| **OpenAI** | API Key | GPT-4、GPT-4o、o1 等 |
| **Anthropic** | API Key | Claude Opus、Sonnet、Haiku |
| **Google** | API Key | Gemini Pro、Flash |
| **Azure OpenAI** | Base URL + Deployment + Key | 企业部署 |

### 第三方中转

你也可以通过第三方 API 端点路由：
- **Azure 兼容端点** — 任何提供 Azure 兼容 API 格式的服务商
- **LiteLLM Proxy** — 统一代理，支持 100+ 服务商（适用于 Ask/Plan 模式）
- **自定义桥接** — 将私有格式转换为 OpenAI/Anthropic 兼容端点

### 重要提示

> **⚠️ Tool Call 兼容性：** 部分第三方中转的 tool/function call 实现有问题，会导致 Agent/Composer 模式失败。使用前先用简单任务测试。

> **⚠️ 免费版限制：** 自定义 API 密钥在免费版可用于基础聊天，但 Agent、Edit 和 Composer 模式即使用自己的密钥也需要 Pro 订阅。

> **文档：** [API Keys](https://docs.cursor.com/en/settings/api-keys) · [Models](https://docs.cursor.com/settings/models)

---

## 链接

- [Cursor 文档](https://docs.cursor.com)
- [Rules](https://cursor.com/docs/context/rules)
- [Subagents](https://cursor.com/docs/context/subagents)
- [上下文管理](https://docs.cursor.com/guides/working-with-context)
- [API Keys](https://docs.cursor.com/en/settings/api-keys)
- [Ignore Files](https://docs.cursor.com/context/ignore-files)
- [Scaling Agents 博客](https://cursor.com/blog/scaling-agents)

</details>

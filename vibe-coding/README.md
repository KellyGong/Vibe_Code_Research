<h1 align="center">🎸 Vibe Coding Tricks</h1>

<p align="center">
  <b>Practical tricks, prompt patterns, and awesome skills for AI-assisted coding</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Prompts-Tips-blue" alt="Prompts"/>
  <img src="https://img.shields.io/badge/Skills-Frameworks-green" alt="Skills"/>
  <img src="https://img.shields.io/badge/Workflows-Patterns-orange" alt="Workflows"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## Table of Contents

- [Awesome Skills & Frameworks](#awesome-skills--frameworks)
- [Prompt Engineering Tips](#prompt-engineering-tips)
- [Workflow Patterns](#workflow-patterns)
- [Scripts](#scripts)

---

## Awesome Skills & Frameworks

Curated list of skill systems, plugins, and frameworks that supercharge your AI coding agents.

### ⭐ [Superpowers](https://github.com/obra/superpowers) — Agentic Skills Framework

> _"An agentic skills framework & software development methodology that works."_ — 46k+ stars

**Superpowers** is a complete development workflow for coding agents (Claude Code, Codex, OpenCode). Instead of letting the agent jump straight into writing code, Superpowers enforces a structured process:

| Phase | Skill | What It Does |
|-------|-------|--------------|
| 1 | **brainstorming** | Refines rough ideas through questions before any code is written |
| 2 | **using-git-worktrees** | Creates an isolated workspace on a new branch |
| 3 | **writing-plans** | Breaks work into bite-sized tasks (2–5 min each) with exact file paths and verification steps |
| 4 | **subagent-driven-development** | Dispatches fresh subagent per task with two-stage review (spec compliance → code quality) |
| 5 | **test-driven-development** | Enforces RED → GREEN → REFACTOR: write failing test → minimal code → pass → commit |
| 6 | **requesting-code-review** | Reviews against plan; critical issues block progress |
| 7 | **finishing-a-development-branch** | Verifies tests, presents merge/PR/keep/discard options |

**Install (Claude Code):**

```bash
# Register the marketplace
/plugin marketplace add obra/superpowers-marketplace

# Install
/plugin install superpowers@superpowers-marketplace
```

**Key skills included:**

- **systematic-debugging** — 4-phase root cause process
- **verification-before-completion** — Evidence before assertions; run verification commands before claiming "done"
- **dispatching-parallel-agents** — Concurrent subagent workflows
- **writing-skills** — Create your own skills following best practices

**Philosophy:** Test-driven, systematic over ad-hoc, complexity reduction, evidence over claims.

---

### Other Notable Projects

| Project | Description | Link |
|---------|-------------|------|
| **Awesome Claude Code** | Community curated list of Claude Code resources, tips, and extensions | [Search GitHub](https://github.com/search?q=awesome-claude-code) |
| **Aider** | Terminal-based AI pair programmer with git integration | [aider.chat](https://aider.chat) |
| **Cline** | Autonomous coding agent as VS Code extension | [github.com/cline/cline](https://github.com/cline/cline) |

---

## Prompt Engineering Tips

> Coming soon — tips on how to write effective prompts for code generation, debugging, and refactoring.

## Workflow Patterns

> Coming soon — battle-tested workflows for using AI in real-world development.

## Scripts

Utility scripts are located in the [`scripts/`](./scripts/) directory.

| Script | Description |
|--------|-------------|
| _TBD_  | _To be added_ |

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 目录

- [优秀 Skills 与框架](#优秀-skills-与框架)
- [Prompt 工程技巧](#prompt-工程技巧)
- [工作流模式](#工作流模式)
- [脚本](#脚本)

---

## 优秀 Skills 与框架

精选的 Skill 系统、插件和框架，提升 AI 编程智能体的能力。

### ⭐ [Superpowers](https://github.com/obra/superpowers) — 智能体 Skills 框架

> _"An agentic skills framework & software development methodology that works."_ — 46k+ stars

**Superpowers** 是面向编程智能体（Claude Code、Codex、OpenCode）的完整开发工作流。它不会让智能体直接写代码，而是强制执行结构化流程：

| 阶段 | Skill | 作用 |
|------|-------|------|
| 1 | **brainstorming** | 先通过提问明确需求，再写代码 |
| 2 | **using-git-worktrees** | 在新分支创建隔离工作区 |
| 3 | **writing-plans** | 将任务拆成小块（每块 2–5 分钟），含精确文件路径和验证步骤 |
| 4 | **subagent-driven-development** | 每个任务派一个新子智能体，两阶段审查（规格合规 → 代码质量） |
| 5 | **test-driven-development** | 强制 RED → GREEN → REFACTOR：先写失败测试 → 最小代码 → 通过 → 提交 |
| 6 | **requesting-code-review** | 对照计划审查；关键问题阻止继续 |
| 7 | **finishing-a-development-branch** | 验证测试，提供合并 / PR / 保留 / 丢弃选项 |

**安装（Claude Code）：**

```bash
# 注册市场
/plugin marketplace add obra/superpowers-marketplace

# 安装
/plugin install superpowers@superpowers-marketplace
```

**包含的核心 Skills：**

- **systematic-debugging** — 四阶段根因分析
- **verification-before-completion** — 先验证再宣布完成；运行验证命令后才能说"搞定"
- **dispatching-parallel-agents** — 并发子智能体工作流
- **writing-skills** — 按最佳实践创建自定义 Skill

**理念：** 测试驱动、系统化而非即兴、降低复杂度、证据先于结论。

---

### 其他值得关注的项目

| 项目 | 说明 | 链接 |
|------|------|------|
| **Awesome Claude Code** | 社区整理的 Claude Code 资源、技巧和扩展 | [GitHub 搜索](https://github.com/search?q=awesome-claude-code) |
| **Aider** | 终端 AI 结对编程，集成 git | [aider.chat](https://aider.chat) |
| **Cline** | VS Code 扩展形态的自主编码智能体 | [github.com/cline/cline](https://github.com/cline/cline) |

---

## Prompt 工程技巧

> 即将推出 — 代码生成、调试与重构的 Prompt 技巧。

## 工作流模式

> 即将推出 — 实战中的 AI 辅助开发工作流。

## 脚本

工具脚本位于 [`scripts/`](./scripts/) 目录。

| 脚本 | 说明 |
|------|------|
| _TBD_  | _待添加_ |

</details>

---

*Maintained by Mingxu Zhang & Zheng Gong*

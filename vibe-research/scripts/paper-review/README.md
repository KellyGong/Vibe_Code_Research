<h1 align="center">📋 AI-Powered Paper Review</h1>

<p align="center">
  <b>Systematic academic paper review using parallel AI agents</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cursor-Skill-5C2D91?logo=visual-studio-code" alt="Cursor"/>
  <img src="https://img.shields.io/badge/9_Parallel-Agents-FF6B6B" alt="Agents"/>
  <img src="https://img.shields.io/badge/WebSearch-Verification-4CAF50" alt="WebSearch"/>
  <img src="https://img.shields.io/badge/Checklist-Template-1976D2" alt="Checklist"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Does

A structured workflow that launches **9 parallel AI sub-agents** to review an academic paper across multiple dimensions simultaneously, then merges results into a comprehensive review report.

### Review Dimensions

| Agent | Module | What It Checks |
|:-----:|--------|---------------|
| 1 | **Terminology** | Coined terms defined? Abbreviations expanded? |
| 2 | **Figures & Tables** | Captions complete? Axes labeled? Legends explained? |
| 3 | **Introduction** | Background → Gap → Method structure? Contributions match gaps? |
| 4 | **Methods** | Notation defined before use? Symbol conflicts? |
| 5-6 | **Citations** (×2) | References exist? BibTeX correct? Context accurate? |
| 7 | **Experiments** | Hardware stated? Hyperparams reported? Seeds declared? |
| 8 | **Related Work** | Missing important recent papers? Limitation discussed? |
| 9 | **Code Repository** | Link valid? README complete? Code matches paper? |

### How to Use

#### Option A: Cursor Skill (Recommended)

This review workflow is registered as a Cursor skill. Simply ask:

```
Please review the paper at /path/to/paper.pdf, target venue is ACL 2026
```

Cursor will automatically:
1. Search for the venue's official guidelines
2. Launch 9 parallel sub-agents
3. Merge results into a structured report

#### Option B: Manual Checklist

Use the provided [`checklist_template.md`](./checklist_template.md) as a standalone review template. Copy it, fill in findings manually or with AI assistance.

### Review Pipeline

```
Step 1: Fetch Venue Requirements
    ├── Author Guidelines
    ├── Reproducibility Checklist
    ├── Ethics / Page Limits / Anonymization
    │
Step 2: Launch Parallel Agents
    ├── Agent 1: Terminology + Abstract consistency
    ├── Agent 2: Figures & Tables
    ├── Agent 3: Introduction structure
    ├── Agent 4: Methods + Notation
    ├── Agent 5: Citations (batch A — first 50%)
    ├── Agent 6: Citations (batch B — second 50%)
    ├── Agent 7: Experiments + Reproducibility
    ├── Agent 8: Related Work + Limitations
    └── Agent 9: Code Repository
    │
Step 3: Merge into Final Report
    ├── Executive Summary
    ├── Checklist (pass/fail)
    ├── Detailed Findings per Module
    └── Issue Summary (Critical / Major / Minor)
```

### Output Format

The final report includes:

- **Executive Summary** — 3-5 sentence overview
- **Checklist** — Pass/fail for each check item
- **Detailed Findings** — Per-module tables with specific issues
- **Issue Summary** — Sorted by severity (🔴 Critical → 🟡 Major → 🟢 Minor)
- **Appendix** — Full citation verification, notation table, code review

### Key Check Details

#### Citation Verification
Each reference is verified via web search:
- Does the paper actually exist?
- Are author names, year, venue correct?
- Is the in-text description accurate?

Split into 2 batches for parallel processing.

#### Code Repository Check
Only runs when the paper provides a code link:
- Link accessibility (not 404)
- README completeness (setup, usage, data instructions)
- Dependency files (requirements.txt, etc.)
- Code structure (model, train, eval, data, config)
- **Consistency with paper** — architecture, hyperparams, data processing

#### Related Work Completeness
Uses a "follow the trail" strategy:
1. Extract key references from Related Work
2. Search for their recent citing papers
3. Identify potentially missing important work (last 2-3 years)

### Files

| File | Description |
|------|-------------|
| `README.md` | This documentation |
| `SKILL.md` | Complete Cursor Skill definition (agent prompts, check details, output format) |
| `checklist_template.md` | Standalone review checklist template |

### Install as Cursor Skill

To enable the automatic review workflow in Cursor IDE, copy (or symlink) the skill folder to your Cursor skills directory:

```bash
# Option A: Symlink (recommended — stays in sync)
ln -s "$(pwd)" ~/.cursor/skills/paper-review

# Option B: Copy
cp -r . ~/.cursor/skills/paper-review
```

Once installed, just ask Cursor:
```
Please review the paper at /path/to/paper.pdf, target venue is ACL 2026
```

The `SKILL.md` file contains the full agent orchestration logic:
- **10 check modules** with detailed check points and output table formats
- **4 sub-agent prompt templates** (generic, citation, related work, code review)
- **8 operational notes** (parallelism, false positive handling, anonymization, etc.)

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 功能简介

一个结构化的审稿工作流，同时启动 **9 个并行 AI 子代理**，从多个维度审查学术论文，最后合并生成完整的审稿报告。

### 审查维度

| 代理 | 模块 | 检查内容 |
|:----:|------|---------|
| 1 | **术语检查** | 自创术语是否有定义？缩写是否展开？ |
| 2 | **图表检查** | Caption是否完整？坐标轴是否标注？图例是否说明？ |
| 3 | **Introduction结构** | 背景→Gap→方法 结构？Contribution是否对应Gap？ |
| 4 | **Methods清晰度** | 数学符号是否先定义后使用？是否有符号冲突？ |
| 5-6 | **引用核验** (×2) | 引用是否真实存在？BibTeX是否正确？上下文是否准确？ |
| 7 | **实验可信度** | 硬件是否声明？超参数是否报告？随机种子是否声明？ |
| 8 | **相关工作** | 是否遗漏重要近期论文？是否有Limitation讨论？ |
| 9 | **代码仓库** | 链接是否有效？README是否完整？代码与论文是否一致？ |

### 使用方法

#### 方式A：Cursor Skill（推荐）

本审稿流程已注册为 Cursor Skill，直接对话即可使用：

```
请审查论文 /path/to/paper.pdf，目标会议是 ACL 2026
```

Cursor 会自动：
1. 搜索目标会议的官方投稿要求
2. 启动 9 个并行子代理
3. 合并结果生成结构化报告

#### 方式B：手动 Checklist

使用提供的 [`checklist_template.md`](./checklist_template.md) 作为独立审稿模板。复制后手动填写或借助 AI 辅助完成。

### 审稿流水线

```
第一步：获取会议要求
    ├── 作者投稿指南
    ├── 可复现性清单
    ├── 伦理声明 / 页数限制 / 匿名化要求
    │
第二步：启动并行代理
    ├── 代理1：术语 + Abstract一致性
    ├── 代理2：图表检查
    ├── 代理3：Introduction结构
    ├── 代理4：Methods + 符号标记
    ├── 代理5：引用核验（前50%引用）
    ├── 代理6：引用核验（后50%引用）
    ├── 代理7：实验 + 可复现性
    ├── 代理8：相关工作 + Limitation
    └── 代理9：代码仓库
    │
第三步：合并生成最终报告
    ├── 执行摘要
    ├── 检查清单（通过/未通过）
    ├── 各模块详细发现
    └── 问题汇总（严重/重要/轻微）
```

### 输出格式

最终报告包含：

- **执行摘要** — 3-5句概述核心发现
- **检查清单** — 每项检查的通过/未通过状态
- **详细发现** — 每个模块的表格式具体问题
- **问题汇总** — 按严重程度排序（🔴 严重 → 🟡 重要 → 🟢 轻微）
- **附录** — 完整引用核验表、符号定义表、代码审查报告

### 核心检查说明

#### 引用核验
每条引用通过网络搜索验证：
- 论文是否真实存在？
- 作者、年份、会议/期刊是否正确？
- 文中引用描述是否准确？

分成 2 批并行处理以提高效率。

#### 代码仓库检查
仅当论文提供代码链接时执行：
- 链接可访问性（非404）
- README 完整性（环境配置、安装步骤、运行命令、数据说明）
- 依赖管理文件（requirements.txt 等）
- 代码结构完整性（模型、训练、评估、数据处理、配置）
- **与论文一致性** — 模型架构、超参数、数据处理流程

#### 相关工作完整性
采用「顺藤摸瓜」策略：
1. 提取相关工作中的关键引用
2. 搜索这些论文的近期被引论文
3. 识别可能遗漏的重要近期工作（近2-3年）

### 文件说明

| 文件 | 说明 |
|------|------|
| `README.md` | 本文档 |
| `SKILL.md` | 完整的 Cursor Skill 定义（代理 prompt、检查细节、输出格式） |
| `checklist_template.md` | 独立审稿检查清单模板 |

### 安装为 Cursor Skill

将本文件夹复制（或软链接）到 Cursor 的 skills 目录即可启用自动审稿：

```bash
# 方式A：软链接（推荐 — 自动保持同步）
ln -s "$(pwd)" ~/.cursor/skills/paper-review

# 方式B：复制
cp -r . ~/.cursor/skills/paper-review
```

安装后，直接在 Cursor 中对话即可使用：
```
请审查论文 /path/to/paper.pdf，目标会议是 ACL 2026
```

`SKILL.md` 包含完整的代理编排逻辑：
- **10 个检查模块**的详细检查要点和输出表格格式
- **4 个子代理 Prompt 模板**（通用、引用核验、相关工作、代码仓库）
- **8 条实操注意事项**（并行策略、误报处理、匿名期处理等）

</details>

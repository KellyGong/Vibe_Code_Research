<h1 align="center">🔬 Vibe Research Scripts</h1>

<p align="center">
  <b>AI-Powered Academic Research Toolkit</b><br>
  <sub>From literature search to batch summarization — everything you need for writing a survey.</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/DeepSeek-API-green?logo=openai&logoColor=white" alt="DeepSeek"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## Overview

This module provides a **complete pipeline** for survey literature review:

```
🔍 Search  →  📥 Download  →  📝 Summarize  →  🗂️ Classify  →  📋 Review
```

## Directory Structure

```
scripts/
├── 📂 paper-search/          # Literature retrieval
│   └── paper_search.py        # Streamlit app: Nature + Semantic Scholar + translation
│
├── 📂 paper-download/         # PDF acquisition
│   ├── download_nature.py     # Nature journals (cookie auth)
│   ├── download_missing.py    # Multi-source (arXiv, S2, DOI)
│   └── download_retry.py      # Retry via Unpaywall, PMC
│
├── 📂 paper-summary/          # AI summarization
│   └── batch_summary.py       # DeepSeek batch summary (parallel)
│
├── 📂 paper-review/           # AI-powered paper review
│   ├── README.md              # Review workflow documentation
│   └── checklist_template.md  # Reusable review checklist
│
└── 📂 utils/                  # Advanced tools
    ├── pdf_constructor.py     # Survey outline classification + mindmaps
    ├── pdf_reader.py          # Detailed structured summaries
    ├── mindmap_viewer.py      # Flask web UI for classification
    ├── validate_pdfs.py       # PDF quality validation
    ├── analyze_coverage.py    # Paper coverage analysis
    ├── split_by_journal.py    # Split summaries by venue
    ├── rename_pdfs.py         # Standardize PDF filenames
    └── run_pipeline.sh        # One-click automation
```

## Quick Start

### 1. Install Dependencies

```bash
pip install streamlit requests pandas beautifulsoup4 openai PyMuPDF tqdm flask pyyaml
```

### 2. Set API Key

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 3. Launch Search Tool

```bash
streamlit run scripts/paper-search/paper_search.py
```

## Complete Workflow

| Step | Command | Output |
|------|---------|--------|
| **1. Search** | `streamlit run scripts/paper-search/paper_search.py` | `papers.csv` |
| **2. Download Nature** | `python scripts/paper-download/download_nature.py --csv papers.csv` | PDFs in `nature_pdfs/` |
| **3. Download Others** | `python scripts/paper-download/download_missing.py --csv papers.csv` | PDFs in `downloads/` |
| **4. Retry Failed** | `python scripts/paper-download/download_retry.py --failed-file download_failed.txt` | More PDFs |
| **5. Validate** | `python scripts/utils/validate_pdfs.py --input-dir ./downloads` | Quality report |
| **6. Summarize** | `python scripts/paper-summary/batch_summary.py --input-dirs ./downloads ./nature_pdfs` | Markdown + JSON |
| **7. Classify** | `python scripts/utils/pdf_constructor.py --batch --merge` | Mindmaps |
| **8. Visualize** | `python scripts/utils/mindmap_viewer.py` | Web UI at `:5000` |

## Module Details

Each subdirectory has its own README with detailed usage instructions:

- [**Paper Search** →](./scripts/paper-search/README.md) Streamlit web app for multi-source literature search
- [**Paper Download** →](./scripts/paper-download/README.md) Cascading download scripts with retry logic
- [**Paper Summary** →](./scripts/paper-summary/README.md) Batch AI summarization with parallel workers
- [**Paper Review** →](./scripts/paper-review/README.md) AI-powered systematic paper review with 9 parallel agents
- [**Utilities** →](./scripts/utils/README.md) Classification, validation, visualization tools

## Awesome Vibe-Research Skills

A curated list of open-source skill libraries that supercharge your AI coding agent for research tasks. Install them and your agent becomes a full-powered AI research assistant.

### [Orchestra AI Research Skills](https://github.com/Orchestra-Research/AI-research-SKILLs)

> **83 production-ready skills** across 20 categories — the most comprehensive open-source AI research engineering skill library. Works with Claude Code, Cursor, Codex, Gemini CLI, and more.

<a href="https://github.com/Orchestra-Research/AI-research-SKILLs"><img src="https://img.shields.io/github/stars/Orchestra-Research/AI-research-SKILLs?style=social" alt="Stars"/></a>

```bash
# One-command install to any coding agent
npx @orchestra-research/ai-research-skills
```

| Category | Skills | Highlights |
|----------|:------:|------------|
| **Model Architecture** | 5 | LitGPT, Mamba, NanoGPT, RWKV, TorchTitan |
| **Fine-Tuning** | 4 | Axolotl, LLaMA-Factory, PEFT, Unsloth |
| **Post-Training (RL)** | 8 | TRL, GRPO, OpenRLHF, SimPO, verl, slime, miles, torchforge |
| **Distributed Training** | 6 | DeepSpeed, FSDP, Megatron-Core, Accelerate, Lightning, Ray |
| **Optimization** | 6 | Flash Attention, bitsandbytes, GPTQ, AWQ, HQQ, GGUF |
| **Inference & Serving** | 4 | vLLM, TensorRT-LLM, llama.cpp, SGLang |
| **Agents & RAG** | 9 | LangChain, LlamaIndex, CrewAI, Chroma, FAISS, Pinecone, Qdrant |
| **Multimodal** | 7 | CLIP, Whisper, LLaVA, Stable Diffusion, SAM, BLIP-2, AudioCraft |
| **Prompt Engineering** | 4 | DSPy, Instructor, Guidance, Outlines |
| **Mech Interpretability** | 4 | TransformerLens, SAELens, pyvene, nnsight |
| **Safety & Alignment** | 4 | Constitutional AI, LlamaGuard, NeMo Guardrails, Prompt Guard |
| **MLOps & Eval** | 9 | W&B, MLflow, TensorBoard, lm-eval-harness, BigCode, NeMo Eval |
| **Others** | 13 | Tokenization, Data Processing, Infrastructure, Emerging Techniques, ML Paper Writing |

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 概述

本模块提供了 **完整的文献综述流水线**：

```
🔍 检索论文  →  📥 下载PDF  →  📝 批量摘要  →  🗂️ 分类整理  →  📋 论文审稿
```

## 目录结构

```
scripts/
├── 📂 paper-search/          # 文献检索
│   └── paper_search.py        # Streamlit应用：Nature + Semantic Scholar + 翻译
│
├── 📂 paper-download/         # PDF下载
│   ├── download_nature.py     # Nature期刊（Cookie认证）
│   ├── download_missing.py    # 多源下载（arXiv, S2, DOI）
│   └── download_retry.py      # 重试下载（Unpaywall, PMC）
│
├── 📂 paper-summary/          # AI摘要
│   └── batch_summary.py       # DeepSeek批量摘要（并行处理）
│
├── 📂 paper-review/           # AI辅助审稿
│   ├── README.md              # 审稿工作流文档
│   └── checklist_template.md  # 可复用审稿检查清单
│
└── 📂 utils/                  # 高级工具
    ├── pdf_constructor.py     # 按Survey大纲分类 + 生成思维导图
    ├── pdf_reader.py          # 详细结构化摘要
    ├── mindmap_viewer.py      # Flask Web界面管理分类
    ├── validate_pdfs.py       # PDF质量验证
    ├── analyze_coverage.py    # 论文覆盖率分析
    ├── split_by_journal.py    # 按期刊/会议拆分摘要
    ├── rename_pdfs.py         # 统一PDF文件命名
    └── run_pipeline.sh        # 一键自动化脚本
```

## 快速开始

### 1. 安装依赖

```bash
pip install streamlit requests pandas beautifulsoup4 openai PyMuPDF tqdm flask pyyaml
```

### 2. 配置 API Key

```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

### 3. 启动检索工具

```bash
streamlit run scripts/paper-search/paper_search.py
```

## 完整工作流

| 步骤 | 命令 | 输出 |
|------|------|------|
| **1. 检索** | `streamlit run scripts/paper-search/paper_search.py` | `papers.csv` |
| **2. 下载Nature** | `python scripts/paper-download/download_nature.py --csv papers.csv` | `nature_pdfs/` 中的PDF |
| **3. 下载其他** | `python scripts/paper-download/download_missing.py --csv papers.csv` | `downloads/` 中的PDF |
| **4. 重试失败** | `python scripts/paper-download/download_retry.py --failed-file download_failed.txt` | 更多PDF |
| **5. 质量验证** | `python scripts/utils/validate_pdfs.py --input-dir ./downloads` | 验证报告 |
| **6. 批量摘要** | `python scripts/paper-summary/batch_summary.py --input-dirs ./downloads ./nature_pdfs` | Markdown + JSON |
| **7. 分类整理** | `python scripts/utils/pdf_constructor.py --batch --merge` | 思维导图 |
| **8. 可视化** | `python scripts/utils/mindmap_viewer.py` | Web界面 `:5000` |

## 各模块详情

每个子目录都有独立的 README 文档：

- [**文献检索** →](./scripts/paper-search/README.md) Streamlit多源文献检索工具
- [**论文下载** →](./scripts/paper-download/README.md) 级联下载与重试脚本
- [**批量摘要** →](./scripts/paper-summary/README.md) DeepSeek并行AI摘要
- [**论文审稿** →](./scripts/paper-review/README.md) 9个并行AI代理系统性审稿
- [**工具集** →](./scripts/utils/README.md) 分类、验证、可视化工具

## Awesome Vibe-Research Skills

精选的开源 Skill 库，安装后你的 AI 编程代理即可成为全能 AI 科研助手。

### [Orchestra AI Research Skills](https://github.com/Orchestra-Research/AI-research-SKILLs)

> **83 个生产级 Skills**，覆盖 20 个类别 — 目前最全面的开源 AI 科研工程 Skill 库。支持 Claude Code、Cursor、Codex、Gemini CLI 等。

<a href="https://github.com/Orchestra-Research/AI-research-SKILLs"><img src="https://img.shields.io/github/stars/Orchestra-Research/AI-research-SKILLs?style=social" alt="Stars"/></a>

```bash
# 一键安装到任意编程代理
npx @orchestra-research/ai-research-skills
```

| 类别 | 数量 | 包含 |
|------|:----:|------|
| **模型架构** | 5 | LitGPT, Mamba, NanoGPT, RWKV, TorchTitan |
| **微调** | 4 | Axolotl, LLaMA-Factory, PEFT, Unsloth |
| **后训练 (RL)** | 8 | TRL, GRPO, OpenRLHF, SimPO, verl, slime, miles, torchforge |
| **分布式训练** | 6 | DeepSpeed, FSDP, Megatron-Core, Accelerate, Lightning, Ray |
| **优化** | 6 | Flash Attention, bitsandbytes, GPTQ, AWQ, HQQ, GGUF |
| **推理部署** | 4 | vLLM, TensorRT-LLM, llama.cpp, SGLang |
| **代理 & RAG** | 9 | LangChain, LlamaIndex, CrewAI, Chroma, FAISS, Pinecone, Qdrant |
| **多模态** | 7 | CLIP, Whisper, LLaVA, Stable Diffusion, SAM, BLIP-2, AudioCraft |
| **Prompt工程** | 4 | DSPy, Instructor, Guidance, Outlines |
| **机制可解释性** | 4 | TransformerLens, SAELens, pyvene, nnsight |
| **安全对齐** | 4 | Constitutional AI, LlamaGuard, NeMo Guardrails, Prompt Guard |
| **MLOps & 评估** | 9 | W&B, MLflow, TensorBoard, lm-eval-harness, BigCode, NeMo Eval |
| **其他** | 13 | Tokenization、数据处理、基础设施、前沿技术、论文写作 |

</details>

---

<p align="center"><sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub></p>

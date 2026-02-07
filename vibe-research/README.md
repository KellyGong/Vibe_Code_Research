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
🔍 Search  →  📥 Download  →  📝 Summarize  →  🗂️ Classify & Organize
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
- [**Utilities** →](./scripts/utils/README.md) Classification, validation, visualization tools

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 概述

本模块提供了 **完整的文献综述流水线**：

```
🔍 检索论文  →  📥 下载PDF  →  📝 批量摘要  →  🗂️ 分类整理
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
- [**工具集** →](./scripts/utils/README.md) 分类、验证、可视化工具

</details>

---

<p align="center"><sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub></p>

<h1 align="center">🧰 Utility Scripts</h1>

<p align="center">
  <b>Advanced tools for paper classification, validation & visualization</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Web_UI-black?logo=flask" alt="Flask"/>
  <img src="https://img.shields.io/badge/PyMuPDF-Validation-blue" alt="PyMuPDF"/>
  <img src="https://img.shields.io/badge/DeepSeek-Classification-8BC34A" alt="DeepSeek"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## Scripts Overview

| Script | Purpose | API Needed |
|--------|---------|:----------:|
| `pdf_constructor.py` | Classify papers by survey outline + generate mindmaps | Yes |
| `pdf_reader.py` | Generate detailed structured summaries | Yes |
| `mindmap_viewer.py` | Flask web UI for managing classification | No |
| `validate_pdfs.py` | Batch validate PDF quality | No |
| `analyze_coverage.py` | Check paper coverage across categories | No |
| `split_by_journal.py` | Split summary files by venue | No |
| `rename_pdfs.py` | Standardize PDF filenames | No |
| `run_pipeline.sh` | One-click automation pipeline | Yes |

---

### `pdf_constructor.py` — Survey Outline Classifier

The most powerful script. Classifies papers according to a **customizable survey outline** and generates hierarchical mindmaps.

```bash
# Step 1: Batch process all PDFs
python pdf_constructor.py --batch --workers 100 --api-keys ./deepseek_keys.txt --bib ref.bib

# Step 2: Filter unrelated papers
python pdf_constructor.py --filter-unrelated --workers 100

# Step 3: Merge into mindmaps by subsubsection
python pdf_constructor.py --merge

# Or use the pipeline script:
./run_pipeline.sh
```

**Output:**
```
mindmap_output/
├── paper_json/           # Individual paper analysis (JSON)
├── paper_mindmaps/       # Individual paper mindmaps (Markdown)
├── by_subsubsection/     # Aggregated mindmaps by category
└── unrelated/            # Filtered out papers
```

---

### `pdf_reader.py` — Structured Paper Summarizer

Generates detailed, structured summaries with API key rotation support.

```bash
# Test single PDF
python pdf_reader.py --test --pdf-dirs ./downloads

# Batch process
python pdf_reader.py --batch --pdf-dirs ./downloads ./nature_pdfs --output-dir ./summaries
```

---

### `mindmap_viewer.py` — Web Classification Manager

Flask-based web UI for browsing and managing paper classifications.

```bash
python mindmap_viewer.py
# Opens at http://0.0.0.0:5000
```

**Features:** Tree structure view, paper move/delete, RESTful API

---

### `validate_pdfs.py` — PDF Quality Checker

Validates PDFs can be processed and have meaningful content.

```bash
python validate_pdfs.py --input-dir ./downloads --output ./report.txt
```

**Checks:** Page count, text extraction, section detection (Abstract, Introduction, Methods, Results, Conclusion, References)

---

### `analyze_coverage.py` — Coverage Analyzer

Finds papers that aren't included in any mindmap category.

```bash
python analyze_coverage.py --base-dir ./mindmap_output
```

---

### `split_by_journal.py` — Split Summaries by Venue

```bash
python split_by_journal.py --input paper_summaries.md --output ./summary
```

---

### `rename_pdfs.py` — Standardize Filenames

Renames PDFs from `title.pdf` to `Venue-title.pdf`.

```bash
python rename_pdfs.py --input-dir ./downloads --csv papers.csv
```

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 脚本概览

| 脚本 | 功能 | 需要API |
|------|------|:-------:|
| `pdf_constructor.py` | 按Survey大纲分类论文 + 生成思维导图 | 是 |
| `pdf_reader.py` | 生成详细结构化摘要 | 是 |
| `mindmap_viewer.py` | Flask Web界面管理分类 | 否 |
| `validate_pdfs.py` | 批量验证PDF质量 | 否 |
| `analyze_coverage.py` | 检查论文分类覆盖率 | 否 |
| `split_by_journal.py` | 按期刊/会议拆分摘要文件 | 否 |
| `rename_pdfs.py` | 统一PDF文件命名规范 | 否 |
| `run_pipeline.sh` | 一键自动化流水线 | 是 |

---

### `pdf_constructor.py` — Survey 大纲分类器

最强大的脚本。按照**可定制的 Survey 大纲**对论文进行分类，并生成层级思维导图。

```bash
# 步骤1：批量处理所有PDF
python pdf_constructor.py --batch --workers 100 --api-keys ./deepseek_keys.txt --bib ref.bib

# 步骤2：过滤不相关论文
python pdf_constructor.py --filter-unrelated --workers 100

# 步骤3：按subsubsection聚合生成思维导图
python pdf_constructor.py --merge

# 或者使用一键脚本：
./run_pipeline.sh
```

**输出结构：**
```
mindmap_output/
├── paper_json/           # 单篇论文分析（JSON格式）
├── paper_mindmaps/       # 单篇论文思维导图（Markdown）
├── by_subsubsection/     # 按分类聚合的思维导图
└── unrelated/            # 被过滤的不相关论文
```

---

### `pdf_reader.py` — 结构化论文摘要生成器

生成详细的结构化摘要，支持多 API Key 轮换。

```bash
# 测试单篇PDF
python pdf_reader.py --test --pdf-dirs ./downloads

# 批量处理
python pdf_reader.py --batch --pdf-dirs ./downloads ./nature_pdfs --output-dir ./summaries
```

---

### `mindmap_viewer.py` — Web 分类管理器

基于 Flask 的 Web 界面，用于浏览和管理论文分类。

```bash
python mindmap_viewer.py
# 在 http://0.0.0.0:5000 打开
```

**功能：** 树形结构浏览、论文移动/删除、RESTful API

---

### `validate_pdfs.py` — PDF 质量检查器

验证 PDF 是否可处理并包含有意义的内容。

```bash
python validate_pdfs.py --input-dir ./downloads --output ./report.txt
```

**检查项：** 页数、文本提取、章节检测（Abstract、Introduction、Methods、Results、Conclusion、References）

---

### `analyze_coverage.py` — 覆盖率分析

查找未被任何思维导图分类覆盖的论文。

```bash
python analyze_coverage.py --base-dir ./mindmap_output
```

---

### `split_by_journal.py` — 按期刊拆分摘要

```bash
python split_by_journal.py --input paper_summaries.md --output ./summary
```

---

### `rename_pdfs.py` — 统一文件命名

将PDF从 `title.pdf` 重命名为 `Venue-title.pdf` 格式。

```bash
python rename_pdfs.py --input-dir ./downloads --csv papers.csv
```

</details>

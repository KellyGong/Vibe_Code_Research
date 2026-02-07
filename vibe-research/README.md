# Vibe Research Tricks

A collection of practical tricks, workflows, and automation scripts for AI-assisted academic research — from literature search to batch summarization.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Scripts](#scripts)
  - [Paper Search](#paper-search)
  - [Paper Download](#paper-download)
  - [Paper Summary](#paper-summary)
  - [Utilities](#utilities)
- [Complete Workflow](#complete-workflow)

---

## Overview

This module provides a complete pipeline for survey writing:

```
Search Papers → Download PDFs → Batch Summarize → Classify & Organize
```

Each stage has dedicated scripts that can be used independently or chained together.

## Quick Start

### Prerequisites

```bash
pip install streamlit requests pandas beautifulsoup4 openai PyMuPDF tqdm flask pyyaml
```

### Environment Variables

```bash
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

### Run the Search Tool

```bash
cd scripts/paper-search
streamlit run paper_search.py
```

## Scripts

### Paper Search

| Script | Description |
|--------|-------------|
| [`paper_search.py`](./scripts/paper-search/) | Streamlit web app for searching Nature + Semantic Scholar, with DeepSeek translation |

**Features**: Multi-source parallel search, keyword filtering (OR/AND), batch translation, CSV export, theme switching

[Detailed documentation →](./scripts/paper-search/README.md)

### Paper Download

| Script | Description |
|--------|-------------|
| [`download_nature.py`](./scripts/paper-download/) | Nature papers with cookie authentication |
| [`download_missing.py`](./scripts/paper-download/) | Multi-source download (Semantic Scholar, arXiv, DOI) |
| [`download_retry.py`](./scripts/paper-download/) | Retry failed downloads via arXiv, Unpaywall, PMC |

**Features**: Cookie-based auth, multi-threaded, automatic venue detection, cascading retry

[Detailed documentation →](./scripts/paper-download/README.md)

### Paper Summary

| Script | Description |
|--------|-------------|
| [`batch_summary.py`](./scripts/paper-summary/) | DeepSeek API batch summarization with parallel workers |

**Features**: PDF text extraction, structured output (Markdown + JSON), configurable parallelism

[Detailed documentation →](./scripts/paper-summary/README.md)

### Utilities

| Script | Description |
|--------|-------------|
| [`pdf_constructor.py`](./scripts/utils/) | Classify papers by survey outline + generate mindmaps |
| [`pdf_reader.py`](./scripts/utils/) | Detailed structured summaries with API key rotation |
| [`mindmap_viewer.py`](./scripts/utils/) | Flask web UI for visualizing paper classification |
| [`validate_pdfs.py`](./scripts/utils/) | Batch PDF quality validation |
| [`analyze_coverage.py`](./scripts/utils/) | Check paper coverage across categories |
| [`split_by_journal.py`](./scripts/utils/) | Split summaries by journal/conference |
| [`rename_pdfs.py`](./scripts/utils/) | Standardize PDF filenames |
| [`run_pipeline.sh`](./scripts/utils/) | One-click: process → filter → merge |

[Detailed documentation →](./scripts/utils/README.md)

## Complete Workflow

A typical survey literature review workflow:

```
Step 1: Search
    streamlit run scripts/paper-search/paper_search.py
    → Export results to papers.csv

Step 2: Download
    python scripts/paper-download/download_nature.py --csv papers.csv
    python scripts/paper-download/download_missing.py --csv papers.csv
    python scripts/paper-download/download_retry.py --failed-file download_failed.txt

Step 3: Validate
    python scripts/utils/validate_pdfs.py --input-dir ./downloads

Step 4: Summarize
    python scripts/paper-summary/batch_summary.py \
        --input-dirs ./downloads ./nature_pdfs \
        --output-dir ./output

Step 5 (Advanced): Classify & Organize
    python scripts/utils/pdf_constructor.py --batch --workers 100
    python scripts/utils/pdf_constructor.py --filter-unrelated
    python scripts/utils/pdf_constructor.py --merge
    python scripts/utils/mindmap_viewer.py  # View at http://localhost:5000
```

---

*Maintained by Mingxu Zhang & Zheng Gong*

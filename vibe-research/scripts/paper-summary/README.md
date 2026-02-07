<h1 align="center">📝 Batch Paper Summary</h1>

<p align="center">
  <b>AI-powered batch PDF summarization with parallel workers</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/DeepSeek-API-8BC34A?logo=openai" alt="DeepSeek"/>
  <img src="https://img.shields.io/badge/PyMuPDF-PDF_Parser-blue" alt="PyMuPDF"/>
  <img src="https://img.shields.io/badge/Parallel-Workers-orange" alt="Parallel"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Does

Reads PDF papers in bulk, extracts text content, and uses **DeepSeek API** to generate structured summaries for each paper — all with configurable parallel workers.

### Prerequisites

```bash
pip install PyMuPDF openai
```

### Configuration

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### Usage

```bash
python batch_summary.py --input-dirs ./downloads ./nature_pdfs --output-dir ./output --workers 10
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--input-dirs` | One or more PDF directories **(required)** | — |
| `--output-dir` | Output directory for summaries | `./output` |
| `--workers` | Number of parallel workers | `10` |

### Output Files

```
output/
├── paper_summaries.md    # Markdown formatted summaries
└── paper_summaries.json  # JSON formatted summaries
```

### Summary Format

Each paper is summarized with the following structure:

```
1. Paper Title
2. Model Used (Diffusion / LLM / GNN / Transformer)
3. Data Type (molecule / protein / cell + representation method)
4. Method (training strategy, training datasets)
5. Downstream Tasks (task type + dataset + metrics)
6. Contributions / Problems Solved
7. Limitations
```

### How It Works

```
PDF files  →  PyMuPDF text extraction (first 30 pages)
           →  DeepSeek API analysis (parallel)
           →  Markdown + JSON output
```

### Tips

- **Workers**: Start with 10, increase if your API quota allows
- **Text limit**: Each PDF is truncated to ~60K characters (~15K tokens)
- **Resume**: Already-processed papers are included in the output; re-run is safe

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 功能简介

批量读取 PDF 论文，提取文本内容，使用 **DeepSeek API** 为每篇论文生成结构化摘要 — 支持可配置的并行 workers。

### 安装依赖

```bash
pip install PyMuPDF openai
```

### 配置

```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

### 使用方法

```bash
python batch_summary.py --input-dirs ./downloads ./nature_pdfs --output-dir ./output --workers 10
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input-dirs` | 一个或多个PDF目录 **（必填）** | — |
| `--output-dir` | 摘要输出目录 | `./output` |
| `--workers` | 并行 worker 数量 | `10` |

### 输出文件

```
output/
├── paper_summaries.md    # Markdown 格式摘要
└── paper_summaries.json  # JSON 格式摘要
```

### 摘要格式

每篇论文按以下结构总结：

```
1. 文章题目
2. 使用模型（Diffusion / LLM / GNN / Transformer）
3. 数据类型（分子 / 蛋白质 / 细胞 + 表征方法）
4. 方法（训练策略、训练数据集）
5. 下游任务（任务类型 + 数据集 + 指标）
6. 贡献 / 解决的问题
7. 局限性
```

### 工作原理

```
PDF 文件  →  PyMuPDF 文本提取（前30页）
          →  DeepSeek API 分析（并行处理）
          →  Markdown + JSON 输出
```

### 使用建议

- **Worker 数量**：建议从 10 开始，根据 API 配额适当增加
- **文本限制**：每个 PDF 截取约 60K 字符（约 15K tokens）
- **断点续传**：重复运行安全，已处理的论文会保留在输出中

</details>

# Batch Paper Summary

Uses DeepSeek API to batch-summarize PDF papers with parallel workers.

## Prerequisites

```bash
pip install PyMuPDF openai
```

## Configuration

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

## Usage

```bash
python batch_summary.py --input-dirs ./downloads ./nature_pdfs --output-dir ./output [--workers 10]
```

## Output
- `paper_summaries.md` — Markdown formatted summaries
- `paper_summaries.json` — JSON formatted summaries

## Summary Format
Each paper summary includes:
1. Paper title
2. Model used (diffusion/LLM/GNN/Transformer)
3. Data type (molecule/protein/cell + representation)
4. Method (training strategy, datasets)
5. Downstream tasks (task type + dataset + metrics)
6. Contributions
7. Limitations

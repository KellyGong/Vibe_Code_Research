# Utility Scripts

Advanced tools for paper analysis, classification, and management.

## Scripts Overview

| Script | Description |
|--------|-------------|
| `pdf_constructor.py` | Classify papers by survey outline + generate mindmaps |
| `pdf_reader.py` | Generate detailed structured summaries per paper |
| `mindmap_viewer.py` | Flask web UI for managing paper classification |
| `validate_pdfs.py` | Batch validate PDF quality with MuPDF |
| `analyze_coverage.py` | Check paper coverage across mindmap categories |
| `split_by_journal.py` | Split summary files by journal/conference |
| `rename_pdfs.py` | Rename PDFs to `Journal-Title.pdf` format |
| `run_pipeline.sh` | One-click pipeline: process → filter → merge |

## pdf_constructor.py
The most powerful script — classifies papers according to a customizable survey outline and generates hierarchical mindmaps.

```bash
python pdf_constructor.py --batch --workers 100 --api-keys ./deepseek_keys.txt --bib ref.bib
python pdf_constructor.py --filter-unrelated --workers 100
python pdf_constructor.py --merge
```

Or use the pipeline script:
```bash
./run_pipeline.sh
```

## validate_pdfs.py
```bash
python validate_pdfs.py --input-dir ./downloads --output validation_report.txt
```

## mindmap_viewer.py
```bash
python mindmap_viewer.py
# Opens at http://0.0.0.0:5000
```

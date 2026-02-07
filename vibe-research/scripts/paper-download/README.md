# Paper Download Scripts

A set of scripts for downloading academic papers from multiple sources.

## Scripts

### 1. download_nature.py
Downloads Nature journal papers using cookie-based authentication.

```bash
pip install requests pandas tqdm
```

Usage:
```bash
python download_nature.py --csv papers.csv --output ./nature_pdfs --cookies cookies.json
```

Cookie Setup:
1. Install "Cookie-Editor" Chrome extension
2. Visit https://www.nature.com and log in
3. Export cookies as JSON
4. Save to cookies.json

### 2. download_missing.py
Downloads missing papers from multiple sources (Semantic Scholar, arXiv, DOI).

```bash
python download_missing.py --csv papers.csv --output ./downloads [--proxy http://127.0.0.1:7890]
```

Features:
- Multi-source: Direct PDF, arXiv, Semantic Scholar API, DOI
- Multi-threaded (8 workers by default)
- Auto venue abbreviation

### 3. download_retry.py
Retries failed downloads using arXiv, Unpaywall, and PubMed Central.

```bash
python download_retry.py --failed-file download_failed.txt --output ./downloads [--proxy http://127.0.0.1:7890]
```

Sources: arXiv API, Crossref + Unpaywall, PubMed Central

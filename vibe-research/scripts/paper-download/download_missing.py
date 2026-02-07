#!/usr/bin/env python3
"""
Download missing PDFs from Semantic Scholar, arXiv, and other sources.

Reads a CSV of papers, checks which PDFs are already downloaded,
and attempts to fetch the rest via direct links, arXiv, or the
Semantic Scholar API.

Usage:
    python download_missing.py --csv papers.csv
    python download_missing.py --csv papers.csv --output ./downloads --proxy http://127.0.0.1:7890
"""

import argparse
import os
import re
import sys
import time
import json
import requests
import pandas as pd
import threading
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 15
DELAY = 0.5  # Delay between requests
MAX_WORKERS = 8  # Number of parallel download threads

# Thread-safe counter
lock = threading.Lock()
success_count = 0
failed_list = []

# Headers to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


def _make_proxies(proxy: str) -> dict:
    """Build a proxies dict for requests. Returns empty dict when proxy is blank."""
    if not proxy:
        return {}
    return {'http': proxy, 'https': proxy}


def get_venue_abbrev(venue):
    """Get abbreviated venue name."""
    if not venue:
        return "Unknown"
    venue_lower = venue.lower()

    mappings = {
        'arxiv': 'Arxiv',
        'neurips': 'NeurIPS',
        'neural information processing': 'NeurIPS',
        'aaai': 'AAAI',
        'annual meeting of the association for computational linguistics': 'ACL',
        'empirical methods in natural language': 'EMNLP',
        'international conference on learning repr': 'ICLR',
        'international conference on machine learning': 'ICML',
        'computational linguistics': 'COLING',
        'ijcai': 'IJCAI',
        'joint conference on artificial': 'IJCAI',
        'cvpr': 'CVPR',
        'computer vision and pattern': 'CVPR',
        'iccv': 'ICCV',
        'eccv': 'ECCV',
        'tkde': 'TKDE',
        'knowledge and data engineering': 'TKDE',
        'bioinformatics': 'Bioinformatics',
        'science advances': 'SciAdv',
        'science': 'Science',
        'naacl': 'NAACL',
        'north american': 'NAACL',
        'kdd': 'KDD',
        'sigir': 'SIGIR',
        'www': 'WWW',
        'world wide web': 'WWW',
    }

    for key, abbrev in mappings.items():
        if key in venue_lower:
            return abbrev

    return "Unknown"


def sanitize_filename(title):
    """Convert title to safe filename."""
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = re.sub(r'\s+', '_', title)
    title = title[:150]  # Limit length
    return title


def get_semantic_scholar_pdf(paper_id, proxies):
    """Get PDF URL from Semantic Scholar API."""
    api_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=openAccessPdf,externalIds"
    try:
        resp = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT, proxies=proxies)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('openAccessPdf') and data['openAccessPdf'].get('url'):
                return data['openAccessPdf']['url']
            # Try arXiv
            if data.get('externalIds', {}).get('ArXiv'):
                arxiv_id = data['externalIds']['ArXiv']
                return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    except Exception:
        pass  # Silent fail for API errors
    return None


def download_pdf(url, filepath, proxies):
    """Download PDF from URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True, proxies=proxies)
        if resp.status_code == 200:
            content_type = resp.headers.get('Content-Type', '')
            # Check if it's actually a PDF
            if 'pdf' in content_type.lower() or url.endswith('.pdf'):
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                # Verify file size
                if os.path.getsize(filepath) > 1000:  # At least 1KB
                    return True
                else:
                    os.remove(filepath)
        return False
    except Exception:
        return False


def extract_arxiv_id(url):
    """Extract arXiv ID from URL."""
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'arxiv\.org/pdf/(\d+\.\d+)',
        r'arxiv:(\d+\.\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_paper_id(url):
    """Extract Semantic Scholar paper ID from URL."""
    match = re.search(r'semanticscholar\.org/paper/([a-f0-9]+)', url)
    if match:
        return match.group(1)
    return None


def download_paper(paper, index, total, downloads_dir, proxies):
    """Download a single paper. Thread-safe."""
    global success_count, failed_list

    title = paper['Title']
    url = paper['URL']
    venue = paper['Venue']

    venue_abbrev = get_venue_abbrev(venue)
    safe_title = sanitize_filename(title)
    filename = f"{venue_abbrev}-{safe_title}.pdf"
    filepath = downloads_dir / filename

    # Skip if already exists
    if filepath.exists():
        with lock:
            success_count += 1
            print(f"[{index}/{total}] ✓ Already exists: {title[:50]}...")
            sys.stdout.flush()
        return True

    pdf_url = None

    # 1. Check if URL is direct PDF
    if url.endswith('.pdf'):
        pdf_url = url

    # 2. Try arXiv
    if not pdf_url:
        arxiv_id = extract_arxiv_id(url)
        if arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # 3. Try Semantic Scholar API
    if not pdf_url:
        paper_id = extract_paper_id(url)
        if paper_id:
            pdf_url = get_semantic_scholar_pdf(paper_id, proxies)

    # 4. Try direct URL if it looks like a PDF source
    if not pdf_url and ('doi.org' in url or 'arxiv' in url):
        pdf_url = url.replace('/abs/', '/pdf/') + '.pdf' if '/abs/' in url else None

    if pdf_url:
        if download_pdf(pdf_url, filepath, proxies):
            with lock:
                success_count += 1
                print(f"[{index}/{total}] ✓ Downloaded: {title[:50]}...")
                sys.stdout.flush()
            return True
        else:
            with lock:
                failed_list.append({'Title': title, 'URL': url, 'PDF_URL': pdf_url})
                print(f"[{index}/{total}] ✗ Failed: {title[:50]}...")
                sys.stdout.flush()
            return False
    else:
        with lock:
            failed_list.append({'Title': title, 'URL': url, 'PDF_URL': None})
            print(f"[{index}/{total}] ✗ No PDF: {title[:50]}...")
            sys.stdout.flush()
        return False


def main():
    global success_count, failed_list

    parser = argparse.ArgumentParser(
        description="Download missing paper PDFs via Semantic Scholar, arXiv, and direct links."
    )
    parser.add_argument("--csv", required=True, help="Path to the CSV file listing papers")
    parser.add_argument("--output", default="./downloads", help="Directory to save downloaded PDFs (default: ./downloads)")
    parser.add_argument("--proxy", default="", help="HTTP proxy URL, e.g. http://127.0.0.1:7890 (default: no proxy)")
    args = parser.parse_args()

    downloads_dir = Path(args.output)
    downloads_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.csv
    proxies = _make_proxies(args.proxy)

    # Load CSV to find missing papers
    df = pd.read_csv(csv_path)

    # Get already downloaded files
    downloaded = set()
    for pdf in downloads_dir.glob('*.pdf'):
        name = pdf.stem.lower().replace('_', ' ')[:50]
        downloaded.add(name)

    # Find missing papers (exclude Nature)
    missing = []
    for _, row in df.iterrows():
        title = str(row.get('Title', ''))
        venue = str(row.get('venue', '')).lower()
        journal = str(row.get('Journal', '')).lower()

        if 'nature' in venue or 'nature' in journal:
            continue

        title_norm = title.lower().replace(':', '').replace('-', ' ')[:50]

        found = False
        for d in downloaded:
            if d[:35] in title_norm[:45] or title_norm[:35] in d[:45]:
                found = True
                break

        if not found:
            v = row.get('venue', '') or row.get('Journal', '')
            missing.append({
                'Title': title,
                'Venue': v,
                'URL': row.get('URL', ''),
                'Year': row.get('Year', '')
            })

    total = len(missing)
    proxy_info = args.proxy if args.proxy else "none"
    print(f"Found {total} missing papers to download")
    print(f"Using {MAX_WORKERS} threads with proxy: {proxy_info}")
    print("=" * 80)
    sys.stdout.flush()

    # Multi-threaded download
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_paper, paper, i, total, downloads_dir, proxies): paper
            for i, paper in enumerate(missing, 1)
        }

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread error: {e}")
            time.sleep(DELAY)

    print("\n" + "=" * 80)
    print(f"Downloaded: {success_count}/{total}")
    print(f"Failed: {len(failed_list)}")

    if failed_list:
        with open('download_failed.txt', 'w') as f:
            for p in failed_list:
                f.write(f"{p['Title']}\n")
                f.write(f"  URL: {p['URL']}\n")
                f.write(f"  PDF: {p['PDF_URL']}\n\n")
        print(f"Failed papers saved to download_failed.txt")


if __name__ == "__main__":
    main()

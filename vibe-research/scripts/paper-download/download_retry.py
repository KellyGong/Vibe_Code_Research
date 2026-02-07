#!/usr/bin/env python3
"""
Retry downloading previously failed papers using multiple sources.

Reads a failed-papers file (produced by download_missing.py) and tries
arXiv, Unpaywall, and PubMed Central to obtain the PDFs.

Usage:
    python download_retry.py --failed-file download_failed.txt
    python download_retry.py --failed-file download_failed.txt --output ./downloads --proxy http://127.0.0.1:7890
"""

import argparse
import os
import re
import sys
import time
import requests
import urllib.parse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 20
MAX_WORKERS = 4

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

lock = threading.Lock()
success_count = 0
still_failed = []


def _make_proxies(proxy: str) -> dict:
    """Build a proxies dict for requests. Returns empty dict when proxy is blank."""
    if not proxy:
        return {}
    return {'http': proxy, 'https': proxy}


def sanitize_filename(title):
    """Convert title to safe filename."""
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = re.sub(r'\s+', '_', title)
    return title[:150]


def get_venue_from_title(title):
    """Try to infer venue abbreviation."""
    # Default to Unknown since we don't have venue info
    return "Paper"


def search_arxiv(title, proxies):
    """Search arXiv for paper by title."""
    try:
        # Clean title for search
        clean_title = re.sub(r'[^\w\s]', ' ', title).strip()
        query = urllib.parse.quote(clean_title[:100])

        api_url = f"http://export.arxiv.org/api/query?search_query=ti:{query}&max_results=3"
        resp = requests.get(api_url, timeout=TIMEOUT, proxies=proxies)

        if resp.status_code == 200:
            content = resp.text
            # Extract arXiv IDs
            ids = re.findall(r'arxiv\.org/abs/(\d+\.\d+)', content)
            if ids:
                return f"https://arxiv.org/pdf/{ids[0]}.pdf"
    except Exception:
        pass
    return None


def search_unpaywall(title, proxies):
    """Search Unpaywall for open access PDF."""
    try:
        # Use crossref to get DOI first
        clean_title = urllib.parse.quote(title[:200])
        crossref_url = f"https://api.crossref.org/works?query.title={clean_title}&rows=1"
        resp = requests.get(crossref_url, timeout=TIMEOUT, proxies=proxies,
                            headers={'User-Agent': 'mailto:example@email.com'})

        if resp.status_code == 200:
            data = resp.json()
            items = data.get('message', {}).get('items', [])
            if items:
                doi = items[0].get('DOI')
                if doi:
                    # Query Unpaywall
                    unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email=example@email.com"
                    resp2 = requests.get(unpaywall_url, timeout=TIMEOUT, proxies=proxies)
                    if resp2.status_code == 200:
                        data2 = resp2.json()
                        best_oa = data2.get('best_oa_location', {})
                        if best_oa and best_oa.get('url_for_pdf'):
                            return best_oa['url_for_pdf']
    except Exception:
        pass
    return None


def search_pubmed_central(title, proxies):
    """Search PubMed Central for open access PDF."""
    try:
        clean_title = urllib.parse.quote(title[:200])
        # Search PMC
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={clean_title}&retmax=1&retmode=json"
        resp = requests.get(search_url, timeout=TIMEOUT, proxies=proxies)

        if resp.status_code == 200:
            data = resp.json()
            ids = data.get('esearchresult', {}).get('idlist', [])
            if ids:
                pmc_id = ids[0]
                # Get PDF link
                return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
    except Exception:
        pass
    return None


def download_pdf(url, filepath, proxies):
    """Download PDF from URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True, proxies=proxies)
        if resp.status_code == 200:
            content_type = resp.headers.get('Content-Type', '')
            if 'pdf' in content_type.lower() or url.endswith('.pdf'):
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                if os.path.getsize(filepath) > 5000:  # At least 5KB
                    return True
                else:
                    os.remove(filepath)
        return False
    except Exception:
        return False


def try_download_paper(title, url, index, total, downloads_dir, proxies):
    """Try multiple sources to download a paper."""
    global success_count, still_failed

    safe_title = sanitize_filename(title)
    filename = f"Paper-{safe_title}.pdf"
    filepath = downloads_dir / filename

    if filepath.exists():
        with lock:
            success_count += 1
            print(f"[{index}/{total}] ✓ Already exists: {title[:50]}...")
            sys.stdout.flush()
        return True

    sources = [
        ("arXiv", search_arxiv),
        ("Unpaywall", search_unpaywall),
        ("PMC", search_pubmed_central),
    ]

    for source_name, search_func in sources:
        try:
            pdf_url = search_func(title, proxies)
            if pdf_url:
                if download_pdf(pdf_url, filepath, proxies):
                    with lock:
                        success_count += 1
                        print(f"[{index}/{total}] ✓ Downloaded from {source_name}: {title[:45]}...")
                        sys.stdout.flush()
                    return True
        except Exception:
            pass
        time.sleep(0.5)

    with lock:
        still_failed.append({'Title': title, 'URL': url})
        print(f"[{index}/{total}] ✗ No source found: {title[:50]}...")
        sys.stdout.flush()
    return False


def parse_failed_file(failed_file):
    """Parse the download_failed.txt file."""
    papers = []
    with open(failed_file, 'r') as f:
        content = f.read()

    # Split by double newlines
    blocks = content.strip().split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2:
            title = lines[0].strip()
            url = ""
            for line in lines[1:]:
                if line.strip().startswith('URL:'):
                    url = line.replace('URL:', '').strip()
                    break
            if title and title != 'None':
                papers.append({'Title': title, 'URL': url})

    return papers


def main():
    global success_count, still_failed

    parser = argparse.ArgumentParser(
        description="Retry downloading failed papers from arXiv, Unpaywall, and PubMed Central."
    )
    parser.add_argument("--failed-file", required=True, help="Path to the failed-papers file (e.g. download_failed.txt)")
    parser.add_argument("--output", default="./downloads", help="Directory to save downloaded PDFs (default: ./downloads)")
    parser.add_argument("--proxy", default="", help="HTTP proxy URL, e.g. http://127.0.0.1:7890 (default: no proxy)")
    args = parser.parse_args()

    downloads_dir = Path(args.output)
    downloads_dir.mkdir(parents=True, exist_ok=True)
    failed_file = args.failed_file
    proxies = _make_proxies(args.proxy)

    papers = parse_failed_file(failed_file)
    total = len(papers)

    proxy_info = args.proxy if args.proxy else "none"
    print(f"Retrying {total} failed papers from multiple sources")
    print(f"Sources: arXiv, Unpaywall, PubMed Central")
    print(f"Using proxy: {proxy_info}")
    print("=" * 80)
    sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(try_download_paper, p['Title'], p['URL'], i, total, downloads_dir, proxies): p
            for i, p in enumerate(papers, 1)
        }

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.3)

    print("\n" + "=" * 80)
    print(f"Successfully downloaded: {success_count}/{total}")
    print(f"Still failed: {len(still_failed)}")

    if still_failed:
        with open('download_still_failed.txt', 'w') as f:
            for p in still_failed:
                f.write(f"{p['Title']}\n")
                f.write(f"  URL: {p['URL']}\n\n")
        print("Remaining failed papers saved to download_still_failed.txt")


if __name__ == "__main__":
    main()

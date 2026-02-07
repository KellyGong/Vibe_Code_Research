#!/usr/bin/env python3
"""
Nature journal batch PDF downloader.

Downloads PDFs from Nature articles listed in a CSV file.
Supports cookie-based authentication for paywalled articles.

Usage:
    python download_nature.py --csv papers.csv
    python download_nature.py --csv papers.csv --output ./nature_pdfs --cookies ./cookies.json

Cookie setup:
    1. Install Chrome extension "Cookie-Editor" or "EditThisCookie"
    2. Visit https://www.nature.com and log in
    3. Click the extension icon → Export → Copy JSON
    4. Save the JSON to a file (default: ./cookies.json)
"""

import argparse
import os
import re
import json
import time
import requests
import pandas as pd
from tqdm import tqdm

DOWNLOAD_DELAY = 2  # Delay between downloads in seconds
MAX_RETRIES = 3
THREADS = 3  # Number of concurrent downloads


def load_cookies(cookies_file: str) -> requests.cookies.RequestsCookieJar:
    """Load cookies from a JSON file into a requests cookie jar."""
    jar = requests.cookies.RequestsCookieJar()

    if not os.path.exists(cookies_file):
        print(f"⚠️  cookies文件不存在: {cookies_file}")
        print("将尝试无cookies下载（仅能下载开放获取文章）")
        return jar

    with open(cookies_file, 'r') as f:
        cookies = json.load(f)

    for cookie in cookies:
        jar.set(
            cookie.get('name', ''),
            cookie.get('value', ''),
            domain=cookie.get('domain', '.nature.com'),
            path=cookie.get('path', '/')
        )

    print(f"✓ 已加载 {len(cookies)} 个cookies")
    return jar


def extract_nature_urls_from_csv(csv_path: str) -> list:
    """Extract all Nature article URLs from a CSV file."""
    df = pd.read_csv(csv_path)
    nature_articles = []

    for idx, row in df.iterrows():
        url = str(row.get('URL', ''))
        title = str(row.get('Title', f'article_{idx}'))

        if 'nature.com/articles' in url:
            match = re.search(r'nature\.com/articles/([a-zA-Z0-9-]+)', url)
            if match:
                article_id = match.group(1)
                safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:80]
                # Get journal name
                journal = str(row.get('Journal', 'Nature'))
                safe_journal = re.sub(r'[<>:"/\\|?*]', '', journal)
                nature_articles.append({
                    'article_id': article_id,
                    'title': safe_title,
                    'journal': safe_journal,
                    'url': f"https://www.nature.com/articles/{article_id}",
                    'pdf_url': f"https://www.nature.com/articles/{article_id}.pdf"
                })

    return nature_articles


def download_single_pdf(article: dict, session: requests.Session, output_dir: str) -> tuple:
    """Download a single article PDF."""
    article_id = article['article_id']
    pdf_url = article['pdf_url']
    title = article['title']
    journal = article.get('journal', 'Nature')
    # Filename format: Journal--Title.pdf
    filename = f"{journal}--{title}.pdf"
    filepath = os.path.join(output_dir, filename)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': article['url'],
    }

    for retry in range(MAX_RETRIES):
        try:
            # Visit article page first to obtain necessary cookies/tokens
            session.get(article['url'], headers=headers, timeout=30)
            time.sleep(0.5)

            # Download PDF
            resp = session.get(pdf_url, headers=headers, timeout=60, stream=True)

            if resp.status_code == 200:
                content_type = resp.headers.get('Content-Type', '')
                # Read a small chunk to verify it is a PDF
                first_chunk = next(resp.iter_content(chunk_size=4), b'')
                if 'pdf' in content_type or first_chunk[:4] == b'%PDF':
                    total_size = int(resp.headers.get('content-length', 0))
                    with open(filepath, 'wb') as f:
                        f.write(first_chunk)
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc=f"  下载中", leave=False, ncols=60) as pbar:
                            pbar.update(len(first_chunk))
                            for chunk in resp.iter_content(chunk_size=8192):
                                f.write(chunk)
                                pbar.update(len(chunk))
                    return (article_id, 'success', filename)
                else:
                    # Might be an HTML page — check for auth requirements
                    if b'sign in' in resp.content.lower() or b'access denied' in resp.content.lower():
                        return (article_id, 'auth_required', 'Need authentication')
                    return (article_id, 'not_pdf', f'Content-Type: {content_type}')
            elif resp.status_code == 403:
                return (article_id, 'forbidden', 'Access forbidden - check cookies')
            elif resp.status_code == 404:
                return (article_id, 'not_found', 'PDF not found')
            else:
                if retry < MAX_RETRIES - 1:
                    time.sleep(2)
                    continue
                return (article_id, 'error', f'HTTP {resp.status_code}')

        except requests.Timeout:
            if retry < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return (article_id, 'timeout', 'Request timeout')
        except Exception as e:
            if retry < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return (article_id, 'error', str(e))

    return (article_id, 'error', 'Max retries exceeded')


def download_all(articles: list, output_dir: str, cookies_file: str):
    """Download all articles in batch."""
    os.makedirs(output_dir, exist_ok=True)

    # Load cookies
    cookies = load_cookies(cookies_file)

    # Tracking files
    downloaded_file = os.path.join(output_dir, "downloaded.txt")
    failed_file = os.path.join(output_dir, "failed.txt")

    # Already-downloaded IDs
    downloaded_ids = set()
    if os.path.exists(downloaded_file):
        with open(downloaded_file, 'r') as f:
            downloaded_ids = set(line.strip() for line in f)

    # Filter out already-downloaded articles
    to_download = [a for a in articles if a['article_id'] not in downloaded_ids]

    print(f"\n总共 {len(articles)} 篇Nature文章")
    print(f"已下载 {len(downloaded_ids)} 篇")
    print(f"待下载 {len(to_download)} 篇")

    if not to_download:
        print("\n✓ 所有文章已下载完成！")
        return

    # Create session
    session = requests.Session()
    session.cookies = cookies

    success_count = 0
    fail_count = 0
    auth_fail_count = 0

    for i, article in enumerate(to_download):
        print(f"\n[{i+1}/{len(to_download)}] {article['title'][:50]}...")

        result = download_single_pdf(article, session, output_dir)
        article_id, status, msg = result

        if status == 'success':
            print(f"  ✓ 成功: {msg}")
            success_count += 1
            with open(downloaded_file, 'a') as f:
                f.write(f"{article_id}\n")
        elif status == 'auth_required' or status == 'forbidden':
            print(f"  ⚠️  认证失败: {msg}")
            auth_fail_count += 1
            with open(failed_file, 'a') as f:
                f.write(f"{article_id}\t{status}\t{article['pdf_url']}\n")
        else:
            print(f"  ✗ 失败: {msg}")
            fail_count += 1
            with open(failed_file, 'a') as f:
                f.write(f"{article_id}\t{status}\t{article['pdf_url']}\n")

        time.sleep(DOWNLOAD_DELAY)

    print(f"\n{'='*50}")
    print(f"下载完成！")
    print(f"  成功: {success_count}")
    print(f"  认证失败: {auth_fail_count}")
    print(f"  其他失败: {fail_count}")
    print(f"\nPDF保存在: {output_dir}")

    if auth_fail_count > 0:
        print(f"\n⚠️  有 {auth_fail_count} 篇文章需要认证，请检查cookies是否正确")


def main():
    parser = argparse.ArgumentParser(
        description="Batch download Nature article PDFs from a CSV file."
    )
    parser.add_argument("--csv", required=True, help="Path to the CSV file containing article URLs")
    parser.add_argument("--output", default="./nature_pdfs", help="Directory to save downloaded PDFs (default: ./nature_pdfs)")
    parser.add_argument("--cookies", default="./cookies.json", help="Path to exported browser cookies JSON file (default: ./cookies.json)")
    args = parser.parse_args()

    csv_file = args.csv
    output_dir = args.output
    cookies_file = args.cookies

    print("=" * 50)
    print("Nature文章批量下载器")
    print("=" * 50)

    # Check cookies file
    if not os.path.exists(cookies_file):
        print(f"\n⚠️  未找到cookies文件: {cookies_file}")
        print("\n请按以下步骤导出cookies:")
        print("1. 在Mac Chrome安装扩展 'Cookie-Editor'")
        print("2. 访问 https://www.nature.com 并登录")
        print("3. 点击Cookie-Editor图标 → Export → Export as JSON")
        print("4. 将内容保存到服务器: {}".format(cookies_file))
        print("\n或者运行: scp cookies.json user@server:{}".format(cookies_file))

        proceed = input("\n是否继续（无cookies仅能下载开放获取文章）? [y/N]: ")
        if proceed.lower() != 'y':
            return

    # Extract URLs
    articles = extract_nature_urls_from_csv(csv_file)
    print(f"\n从CSV中提取到 {len(articles)} 篇Nature文章")

    if not articles:
        print("没有找到Nature文章！")
        return

    # Show first few articles
    print("\n前5篇文章:")
    for a in articles[:5]:
        print(f"  - {a['article_id']}: {a['title'][:40]}...")

    print(f"\n输出目录: {output_dir}")
    input("\n按Enter开始下载...")

    # Start downloading
    download_all(articles, output_dir, cookies_file)


if __name__ == "__main__":
    main()

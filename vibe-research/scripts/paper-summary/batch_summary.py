"""
Batch process PDF papers using DeepSeek API with parallel workers
"""
import os
import sys
import argparse
import fitz  # PyMuPDF
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

# DeepSeek API configuration
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

SYSTEM_PROMPT = """
你是一个优秀的科研工作者，可以非常好的阅读和理解一篇论文。
请按照以下格式总结一篇论文：
1. 文章题目
2. 使用模型(e.g. diffusion/LLM/gnn/Transformer)
3. 数据类型(分子/蛋白质/细胞 以及各自的表征方法)
4. 方法(训练策略 训练数据集)
5. 下游任务(具体任务类型+数据集+指标)
6. 解决了什么问题/有什么contribution
7. limitation

要求给出一些细节，不要过于笼统。
"""


def extract_text_from_pdf(pdf_path: str, max_pages: int = 30) -> str:
    """Extract text content from a PDF file."""
    doc = fitz.open(pdf_path)
    text_parts = []
    
    pages_to_read = min(len(doc), max_pages) if max_pages else len(doc)
    
    for page_num in range(pages_to_read):
        page = doc[page_num]
        text_parts.append(f"--- Page {page_num + 1} ---\n{page.get_text()}")
    
    doc.close()
    return "\n\n".join(text_parts)


def summarize_paper(client: OpenAI, paper_text: str) -> str:
    """Use DeepSeek API to summarize the paper."""
    max_chars = 60000
    if len(paper_text) > max_chars:
        paper_text = paper_text[:max_chars] + "\n\n[... Text truncated due to length ...]"
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Please analyze and summarize this paper:\n\n{paper_text}"},
        ],
        stream=False,
        max_tokens=2000,
        temperature=0.3
    )
    
    return response.choices[0].message.content


def process_single_pdf(client: OpenAI, pdf_path: str) -> dict:
    """Process a single PDF and return result dict."""
    filename = os.path.basename(pdf_path)
    try:
        paper_text = extract_text_from_pdf(pdf_path, max_pages=30)
        summary = summarize_paper(client, paper_text)
        return {
            "filename": filename,
            "path": pdf_path,
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        return {
            "filename": filename,
            "path": pdf_path,
            "status": "error",
            "error": str(e)
        }


def collect_all_pdfs(folders: list) -> list:
    """Collect all PDF paths from given folders."""
    pdf_files = []
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.endswith('.pdf'):
                    pdf_files.append(os.path.join(folder, f))
    return pdf_files


def save_results_markdown(results: list, output_path: str):
    """Save results to markdown file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Paper Summaries\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total papers: {len(results)}\n\n")
        f.write("---\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"## {i}. {result['filename']}\n\n")
            if result['status'] == 'success':
                f.write(result['summary'])
            else:
                f.write(f"**Error:** {result.get('error', 'Unknown error')}")
            f.write("\n\n---\n\n")


def save_results_json(results: list, output_path: str):
    """Save results to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Batch process PDF papers using DeepSeek API with parallel workers"
    )
    parser.add_argument(
        "--input-dirs", nargs='+', required=True,
        help="One or more directories containing PDF files"
    )
    parser.add_argument(
        "--output-dir", default="./output",
        help="Directory to save results (default: ./output)"
    )
    parser.add_argument(
        "--workers", type=int, default=10,
        help="Number of parallel workers (default: 10)"
    )
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DEEPSEEK_API_KEY environment variable is not set.")
        print("Please set it with: export DEEPSEEK_API_KEY='your-api-key'")
        sys.exit(1)

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.deepseek.com"
    )

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    output_md = os.path.join(output_dir, "paper_summaries.md")
    output_json = os.path.join(output_dir, "paper_summaries.json")
    
    # Collect all PDFs
    pdf_files = collect_all_pdfs(args.input_dirs)
    print(f"Found {len(pdf_files)} PDF files")
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    # Process in parallel
    results = []
    max_workers = args.workers
    
    print(f"Processing with {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdf = {
            executor.submit(process_single_pdf, client, pdf): pdf
            for pdf in pdf_files
        }
        
        for i, future in enumerate(as_completed(future_to_pdf), 1):
            pdf_path = future_to_pdf[future]
            result = future.result()
            results.append(result)
            
            status = "✓" if result['status'] == 'success' else "✗"
            print(f"[{i}/{len(pdf_files)}] {status} {result['filename']}")
    
    # Sort by filename
    results.sort(key=lambda x: x['filename'])
    
    # Save results
    save_results_markdown(results, output_md)
    save_results_json(results, output_json)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\nDone! {success_count}/{len(results)} papers processed successfully")
    print(f"Results saved to:\n  - {output_md}\n  - {output_json}")


if __name__ == "__main__":
    main()

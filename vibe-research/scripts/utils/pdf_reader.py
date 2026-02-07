#!/usr/bin/env python3
"""
使用 DeepSeek API 批量阅读PDF论文并生成摘要
"""

import os
import sys
import argparse
import base64
import fitz  # PyMuPDF
from pathlib import Path
from openai import OpenAI
import json
from tqdm import tqdm
import time

# DeepSeek API 配置
BASE_URL = "https://api.deepseek.com"


def load_api_keys(api_keys_file: str = None) -> list:
    """加载 API keys from file or environment variable."""
    if api_keys_file and os.path.exists(api_keys_file):
        with open(api_keys_file, 'r') as f:
            keys = [line.strip() for line in f if line.strip()]
        return keys

    # Fall back to environment variable
    env_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if env_key:
        return [env_key]

    return []


def extract_text_from_pdf(pdf_path: str, max_pages: int = 20) -> str:
    """从PDF提取文本内容"""
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(min(len(doc), max_pages)):
            page = doc[page_num]
            text = page.get_text()
            text_parts.append(text)
        
        doc.close()
        full_text = "\n".join(text_parts)
        
        # 限制文本长度（DeepSeek token限制）
        if len(full_text) > 50000:
            full_text = full_text[:50000] + "\n...[内容已截断]"
        
        return full_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek 客户端"""
    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL
    )


def summarize_paper(client: OpenAI, paper_text: str, paper_name: str) -> dict:
    """使用 DeepSeek 分析论文并生成结构化摘要"""
    
    prompt = f"""请阅读以下学术论文内容，并提供结构化的分析摘要。

论文标题: {paper_name}

论文内容:
{paper_text}

请按以下格式输出分析结果（使用中文回答）：

## 1. 论文基本信息
- **标题**: 
- **发表会议/期刊**: 
- **研究领域**: 

## 2. 研究背景与动机
（简要描述研究背景和该工作要解决的问题）

## 3. 主要贡献
（列出论文的主要贡献点）

## 4. 方法概述
（描述论文提出的方法或框架）

## 5. 实验结果
（总结关键实验结果和性能表现）

## 6. 核心创新点
（提炼最重要的创新之处）

## 7. 局限性与未来工作
（如果论文中提到）

## 8. 一句话总结
（用一句话概括这篇论文的核心贡献）
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的学术论文阅读助手，擅长分析和总结科学论文。请用中文回答。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4096
        )
        
        summary = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        return {
            "success": True,
            "summary": summary,
            "usage": usage
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_all_pdfs(pdf_dirs: list) -> list:
    """获取所有PDF文件路径"""
    pdf_files = []
    for pdf_dir in pdf_dirs:
        if os.path.exists(pdf_dir):
            for f in os.listdir(pdf_dir):
                if f.endswith('.pdf'):
                    pdf_files.append(os.path.join(pdf_dir, f))
    return pdf_files


def test_single_pdf(api_keys: list, pdf_dirs: list, output_dir: str, pdf_path: str = None):
    """测试单个PDF的阅读效果"""
    
    client = create_client(api_keys[0])
    
    # 如果没有指定PDF，选择一个较小的PDF进行测试
    if pdf_path is None:
        all_pdfs = get_all_pdfs(pdf_dirs)
        # 选择一个文件大小适中的PDF
        for pdf in all_pdfs:
            size = os.path.getsize(pdf)
            if 500000 < size < 3000000:  # 500KB - 3MB
                pdf_path = pdf
                break
        if pdf_path is None and all_pdfs:
            pdf_path = all_pdfs[0]
    
    if pdf_path is None:
        print("No PDF files found!")
        return None
    
    print(f"测试PDF: {pdf_path}")
    print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
    
    # 提取文本
    print("\n提取PDF文本...")
    paper_text = extract_text_from_pdf(pdf_path)
    print(f"提取文本长度: {len(paper_text)} 字符")
    
    # 调用API
    print("\n调用 DeepSeek API 分析论文...")
    paper_name = os.path.basename(pdf_path).replace('.pdf', '')
    
    start_time = time.time()
    result = summarize_paper(client, paper_text, paper_name)
    elapsed_time = time.time() - start_time
    
    if result["success"]:
        print(f"\n✅ 分析成功! 用时: {elapsed_time:.2f}秒")
        print(f"Token使用: {result['usage']}")
        print("\n" + "="*80)
        print("论文摘要:")
        print("="*80)
        print(result["summary"])
        
        # 保存结果
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{paper_name}_summary.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {paper_name}\n\n")
            f.write(result["summary"])
        print(f"\n结果已保存到: {output_file}")
    else:
        print(f"\n❌ 分析失败: {result['error']}")
    
    return result


def batch_process_pdfs(api_keys: list, pdf_dirs: list, output_dir: str,
                       max_papers: int = None, skip_existing: bool = True):
    """批量处理所有PDF"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 轮换使用 API keys
    key_index = 0
    
    all_pdfs = get_all_pdfs(pdf_dirs)
    if max_papers:
        all_pdfs = all_pdfs[:max_papers]
    
    print(f"共找到 {len(all_pdfs)} 个PDF文件")
    
    success_count = 0
    fail_count = 0
    
    for pdf_path in tqdm(all_pdfs, desc="处理PDF"):
        paper_name = os.path.basename(pdf_path).replace('.pdf', '')
        output_file = os.path.join(output_dir, f"{paper_name}_summary.md")
        
        # 跳过已处理的
        if skip_existing and os.path.exists(output_file):
            continue
        
        # 提取文本
        paper_text = extract_text_from_pdf(pdf_path)
        if paper_text.startswith("Error"):
            fail_count += 1
            continue
        
        # 轮换API key
        client = create_client(api_keys[key_index])
        key_index = (key_index + 1) % len(api_keys)
        
        # 分析论文
        result = summarize_paper(client, paper_text, paper_name)
        
        if result["success"]:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {paper_name}\n\n")
                f.write(result["summary"])
            success_count += 1
        else:
            fail_count += 1
            print(f"\n失败: {paper_name} - {result.get('error', 'Unknown error')}")
        
        # 避免API限流
        time.sleep(1)
    
    print(f"\n处理完成! 成功: {success_count}, 失败: {fail_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 DeepSeek API 阅读PDF论文")
    parser.add_argument("--test", action="store_true", help="测试单个PDF")
    parser.add_argument("--pdf", type=str, help="指定要测试的PDF路径")
    parser.add_argument("--batch", action="store_true", help="批量处理所有PDF")
    parser.add_argument("--max", type=int, default=None, help="最多处理的论文数量")
    parser.add_argument(
        "--api-keys-file", type=str, default=None,
        help="Path to a file containing DeepSeek API keys (one per line). "
             "If not provided, uses DEEPSEEK_API_KEY environment variable."
    )
    parser.add_argument(
        "--pdf-dirs", nargs='+', required=True,
        help="One or more directories containing PDF files"
    )
    parser.add_argument(
        "--output-dir", default="./summaries",
        help="Directory to save summary results (default: ./summaries)"
    )
    
    args = parser.parse_args()

    # Load API keys
    api_keys = load_api_keys(args.api_keys_file)
    if not api_keys:
        print("Error: No API keys available.")
        print("Provide --api-keys-file or set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)
    
    if args.test or args.pdf:
        test_single_pdf(api_keys, args.pdf_dirs, args.output_dir, args.pdf)
    elif args.batch:
        batch_process_pdfs(api_keys, args.pdf_dirs, args.output_dir, max_papers=args.max)
    else:
        # 默认测试单个
        print("默认模式: 测试单个PDF")
        print("使用 --batch 进行批量处理")
        print("使用 --pdf <path> 指定PDF文件")
        print()
        test_single_pdf(api_keys, args.pdf_dirs, args.output_dir)

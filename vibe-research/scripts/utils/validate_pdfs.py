#!/usr/bin/env python
"""
Test script to validate if MuPDF can process each PDF in a given folder.
Also checks for meaningful content (intro, abstract, etc.) and computes statistics.
Outputs a file containing titles of PDFs that cannot be processed or have issues.
"""

import os
import re
import argparse
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
from collections import defaultdict


def get_paper_title_from_filename(filename: str) -> str:
    """Extract paper title from filename by removing .pdf extension."""
    return filename.replace('.pdf', '').replace('_', ' ')


def check_content_sections(text: str) -> dict:
    """
    Check if the text contains common paper sections.
    Returns a dict with section presence and other stats.
    """
    text_lower = text.lower()
    
    # Common section keywords to look for
    sections = {
        'abstract': bool(re.search(r'\babstract\b', text_lower)),
        'introduction': bool(re.search(r'\bintroduction\b', text_lower)),
        'methods': bool(re.search(r'\b(method|methodology|materials?\s+and\s+methods?)\b', text_lower)),
        'results': bool(re.search(r'\bresults?\b', text_lower)),
        'discussion': bool(re.search(r'\bdiscussion\b', text_lower)),
        'conclusion': bool(re.search(r'\bconclusion\b', text_lower)),
        'references': bool(re.search(r'\breferences?\b', text_lower)),
    }
    
    return sections


def test_mupdf_can_process(pdf_path: str) -> dict:
    """
    Test if MuPDF can process a PDF file and extract content statistics.
    
    Returns:
        dict with processing results and statistics
    """
    result = {
        'can_open': False,
        'page_count': 0,
        'total_chars': 0,
        'total_words': 0,
        'avg_chars_per_page': 0,
        'has_text': False,
        'sections': {},
        'error': '',
        'quality': 'unknown'
    }
    
    try:
        doc = fitz.open(pdf_path)
        result['can_open'] = True
        result['page_count'] = len(doc)
        
        if result['page_count'] == 0:
            result['error'] = "Document has 0 pages"
            doc.close()
            return result
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            full_text += page_text
        
        doc.close()
        
        # Calculate statistics
        result['total_chars'] = len(full_text)
        result['total_words'] = len(full_text.split())
        result['avg_chars_per_page'] = result['total_chars'] / result['page_count'] if result['page_count'] > 0 else 0
        result['has_text'] = result['total_chars'] > 100  # More than 100 chars means has text
        
        # Check for common sections
        result['sections'] = check_content_sections(full_text)
        
        # Determine quality
        sections_found = sum(result['sections'].values())
        if result['total_chars'] < 100:
            result['quality'] = 'empty_or_scanned'
        elif sections_found == 0:
            result['quality'] = 'no_sections_detected'
        elif sections_found < 3:
            result['quality'] = 'partial_structure'
        else:
            result['quality'] = 'good'
        
        return result
        
    except Exception as e:
        result['error'] = str(e)
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate if MuPDF can process each PDF in a directory"
    )
    parser.add_argument(
        "--input-dir", required=True,
        help="Directory containing PDF files to validate"
    )
    parser.add_argument(
        "--output", default="./mupdf_validation_report.txt",
        help="Output file path for the validation report (default: ./mupdf_validation_report.txt)"
    )
    args = parser.parse_args()

    downloads_dir = Path(args.input_dir)
    output_file = Path(args.output)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(downloads_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files to test")
    
    # Track results
    results = []
    quality_counts = defaultdict(int)
    section_counts = defaultdict(int)
    total_chars = 0
    total_words = 0
    total_pages = 0
    
    # Test each PDF
    for pdf_path in tqdm(pdf_files, desc="Analyzing PDFs with MuPDF"):
        result = test_mupdf_can_process(str(pdf_path))
        result['filename'] = pdf_path.name
        result['title'] = get_paper_title_from_filename(pdf_path.name)
        results.append(result)
        
        # Aggregate statistics
        quality_counts[result['quality']] += 1
        total_chars += result['total_chars']
        total_words += result['total_words']
        total_pages += result['page_count']
        
        for section, found in result['sections'].items():
            if found:
                section_counts[section] += 1
    
    # Categorize papers
    failed_papers = [r for r in results if r['error']]
    empty_papers = [r for r in results if r['quality'] == 'empty_or_scanned' and not r['error']]
    no_sections = [r for r in results if r['quality'] == 'no_sections_detected']
    partial_papers = [r for r in results if r['quality'] == 'partial_structure']
    good_papers = [r for r in results if r['quality'] == 'good']
    
    # Write detailed report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"MuPDF Comprehensive Validation Report\n")
        f.write(f"{'='*70}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall Statistics
        f.write(f"{'='*70}\n")
        f.write(f"OVERALL STATISTICS\n")
        f.write(f"{'='*70}\n")
        f.write(f"Total PDFs tested:        {len(pdf_files)}\n")
        f.write(f"Total pages:              {total_pages:,}\n")
        f.write(f"Total characters:         {total_chars:,}\n")
        f.write(f"Total words:              {total_words:,}\n")
        f.write(f"Avg chars per paper:      {total_chars // len(pdf_files) if pdf_files else 0:,}\n")
        f.write(f"Avg words per paper:      {total_words // len(pdf_files) if pdf_files else 0:,}\n")
        f.write(f"Avg pages per paper:      {total_pages / len(pdf_files) if pdf_files else 0:.1f}\n\n")
        
        # Quality Distribution
        f.write(f"{'='*70}\n")
        f.write(f"QUALITY DISTRIBUTION\n")
        f.write(f"{'='*70}\n")
        f.write(f"Good (complete):          {len(good_papers)} ({100*len(good_papers)/len(pdf_files):.1f}%)\n")
        f.write(f"Partial structure:        {len(partial_papers)} ({100*len(partial_papers)/len(pdf_files):.1f}%)\n")
        f.write(f"No sections detected:     {len(no_sections)} ({100*len(no_sections)/len(pdf_files):.1f}%)\n")
        f.write(f"Empty/Scanned:            {len(empty_papers)} ({100*len(empty_papers)/len(pdf_files):.1f}%)\n")
        f.write(f"Failed to process:        {len(failed_papers)} ({100*len(failed_papers)/len(pdf_files):.1f}%)\n\n")
        
        # Section Detection Stats
        f.write(f"{'='*70}\n")
        f.write(f"SECTION DETECTION STATISTICS\n")
        f.write(f"{'='*70}\n")
        for section in ['abstract', 'introduction', 'methods', 'results', 'discussion', 'conclusion', 'references']:
            count = section_counts[section]
            f.write(f"{section.capitalize():20s}: {count:4d} ({100*count/len(pdf_files):.1f}%)\n")
        f.write("\n")
        
        # Problem Papers Details
        if failed_papers:
            f.write(f"{'='*70}\n")
            f.write(f"FAILED TO PROCESS ({len(failed_papers)} papers)\n")
            f.write(f"{'='*70}\n")
            for i, paper in enumerate(failed_papers, 1):
                f.write(f"\n{i}. {paper['title']}\n")
                f.write(f"   Filename: {paper['filename']}\n")
                f.write(f"   Error: {paper['error']}\n")
            f.write("\n")
        
        if empty_papers:
            f.write(f"{'='*70}\n")
            f.write(f"EMPTY OR SCANNED (no extractable text) ({len(empty_papers)} papers)\n")
            f.write(f"{'='*70}\n")
            for i, paper in enumerate(empty_papers, 1):
                f.write(f"\n{i}. {paper['title']}\n")
                f.write(f"   Filename: {paper['filename']}\n")
                f.write(f"   Pages: {paper['page_count']}, Chars: {paper['total_chars']}\n")
            f.write("\n")
        
        if no_sections:
            f.write(f"{'='*70}\n")
            f.write(f"NO SECTIONS DETECTED ({len(no_sections)} papers)\n")
            f.write(f"{'='*70}\n")
            for i, paper in enumerate(no_sections, 1):
                f.write(f"\n{i}. {paper['title']}\n")
                f.write(f"   Filename: {paper['filename']}\n")
                f.write(f"   Pages: {paper['page_count']}, Chars: {paper['total_chars']:,}, Words: {paper['total_words']:,}\n")
            f.write("\n")
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Validation Complete!")
    print(f"{'='*70}")
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Total words: {total_words:,}")
    print(f"\nQuality Distribution:")
    print(f"  Good:              {len(good_papers)}")
    print(f"  Partial:           {len(partial_papers)}")
    print(f"  No sections:       {len(no_sections)}")
    print(f"  Empty/Scanned:     {len(empty_papers)}")
    print(f"  Failed:            {len(failed_papers)}")
    print(f"\nSection Detection:")
    for section in ['abstract', 'introduction', 'methods', 'conclusion', 'references']:
        print(f"  {section.capitalize():15s}: {section_counts[section]}")
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()

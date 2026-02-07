#!/usr/bin/env python3
"""Split paper_summaries.md by journal/conference."""

import os
import re
import shutil
import argparse
from collections import defaultdict

# Known journals/conferences (add more as needed)
KNOWN_JOURNALS = {
    "AAAI", "ACL", "ASCE", "Annual", "Arxiv", "Bioinformatics", "CVPR", 
    "EMNLP", "ICLR", "ICML", "IEEE", "IJCAI", "International", "NAACL", 
    "Nature", "Nature Biotechnology", "Nature Chem", "Nature Comm", 
    "Nature Comp. Sci", "Nature MI", "Nature Methods", "NeurIPS", 
    "Science", "TKDE", "KDD", "WWW", "SIGIR", "CIKM", "WSDM",
    "Cell", "PNAS", "Nucleic Acids Research", "BMC", "JACS", "ACS",
    "Chemical Science", "Briefings in Bioinformatics", "Journal"
}


def main():
    parser = argparse.ArgumentParser(
        description="Split paper_summaries.md by journal/conference"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to the input paper_summaries.md file"
    )
    parser.add_argument(
        "--output", default="./summary",
        help="Output directory for split files (default: ./summary)"
    )
    args = parser.parse_args()

    input_file = args.input
    output_dir = args.output

    # Clear output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by paper sections (## N. ...)
    pattern = r'^## \d+\. '
    sections = re.split(pattern, content, flags=re.MULTILINE)

    # First section is the header
    header = sections[0]

    # Group papers by journal
    papers_by_journal = defaultdict(list)

    for i, section in enumerate(sections[1:], 1):
        if not section.strip():
            continue
        # Extract journal name (before first -)
        first_line = section.split('\n')[0]
        if '-' in first_line:
            journal = first_line.split('-')[0].strip()
            # Check if it's a known journal
            if journal not in KNOWN_JOURNALS:
                journal = "unknown"
        else:
            journal = "unknown"
        
        papers_by_journal[journal].append((i, section))

    # Write each journal to a separate file
    for journal, papers in papers_by_journal.items():
        out_file = os.path.join(output_dir, f"{journal}_summary.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# {journal} Paper Summaries\n\n")
            f.write(f"Total papers: {len(papers)}\n\n---\n\n")
            for idx, (orig_num, section) in enumerate(papers, 1):
                f.write(f"## {idx}. {section}\n")
        print(f"Created: {out_file} ({len(papers)} papers)")

    print(f"\nTotal journals/conferences: {len(papers_by_journal)}")
    print(f"Total papers processed: {sum(len(p) for p in papers_by_journal.values())}")


if __name__ == "__main__":
    main()

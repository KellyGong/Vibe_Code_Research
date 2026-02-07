import os
import re
import json
import argparse


def get_all_md_files(root):
    md_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".md"):
                md_files.append(os.path.join(dirpath, f))
    return md_files

def extract_bibtex_keys(filepath):
    keys = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match BibTeXKey: <key>
            matches = re.findall(r'BibTeXKey:\s*(\S+)', content)
            keys.extend(matches)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return keys

def main():
    parser = argparse.ArgumentParser(
        description="Analyze paper coverage: compare papers referenced in mindmap "
                    "markdown files against available paper JSON files."
    )
    parser.add_argument(
        "--base-dir", required=True,
        help="Base directory containing 'by_subsubsection' and 'paper_json' subdirectories"
    )
    args = parser.parse_args()

    base_dir = args.base_dir
    mindmap_root = os.path.join(base_dir, "by_subsubsection")
    paper_json_dir = os.path.join(base_dir, "paper_json")

    md_files = get_all_md_files(mindmap_root)
    
    paper_counts = {}
    all_used_keys = set()
    
    for md_file in md_files:
        rel_path = os.path.relpath(md_file, mindmap_root)
        keys = extract_bibtex_keys(md_file)
        paper_counts[rel_path] = len(keys)
        all_used_keys.update(keys)
    
    # Sort mindmaps by name for better output
    sorted_mindmaps = sorted(paper_counts.items())
    
    print("Paper counts per mindmap:")
    for mindmap, count in sorted_mindmaps:
        print(f"- {mindmap}: {count} papers")
    
    # Get all json files
    json_files = [f for f in os.listdir(paper_json_dir) if f.endswith(".json")]
    all_json_keys = set([os.path.splitext(f)[0] for f in json_files])
    
    unused_keys = all_json_keys - all_used_keys
    
    print(f"\nTotal papers in paper_json: {len(all_json_keys)}")
    print(f"Total unique papers used in mindmaps: {len(all_used_keys)}")
    print(f"Number of papers in paper_json NOT used in mindmaps: {len(unused_keys)}")
    if unused_keys:
        print(f"Unused paper(s): {', '.join(sorted(unused_keys))}")

if __name__ == "__main__":
    main()

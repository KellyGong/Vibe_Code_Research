#!/usr/bin/env python3
"""Rename PDFs from title.pdf to Journal-title.pdf format."""

import os
import re
import argparse
import pandas as pd
from pathlib import Path

def normalize_title(title):
    """Normalize title for matching: remove special chars, lowercase."""
    if pd.isna(title):
        return ""
    # Replace special characters with underscore, similar to filename conversion
    normalized = re.sub(r'[^\w\s-]', '', str(title))
    normalized = re.sub(r'\s+', '_', normalized)
    return normalized.lower().strip('_')

def normalize_filename(filename):
    """Normalize filename for matching."""
    # Remove .pdf extension
    name = filename.replace('.pdf', '')
    return name.lower().replace('_', ' ').replace('-', ' ')

def get_journal_abbrev(journal):
    """Get abbreviated journal name."""
    if pd.isna(journal) or not journal:
        return "Unknown"
    
    journal = str(journal).strip()
    
    # Common mappings
    mappings = {
        'arxiv': 'Arxiv',
        'arxiv.org': 'Arxiv',
        'neurips': 'NeurIPS',
        'neural information processing systems': 'NeurIPS',
        'nips': 'NeurIPS',
        'aaai': 'AAAI',
        'acl': 'ACL',
        'emnlp': 'EMNLP',
        'naacl': 'NAACL',
        'icml': 'ICML',
        'iclr': 'ICLR',
        'cvpr': 'CVPR',
        'iccv': 'ICCV',
        'eccv': 'ECCV',
        'tkde': 'TKDE',
        'ieee transactions on knowledge and data engineering': 'TKDE',
        'nature': 'Nature',
        'nature machine intelligence': 'NatureMI',
        'nature communications': 'NatureComm',
        'nature methods': 'NatureMethods',
        'science': 'Science',
        'cell': 'Cell',
        'pnas': 'PNAS',
        'jacs': 'JACS',
        'journal of the american chemical society': 'JACS',
        'acs': 'ACS',
        'rsc': 'RSC',
        'chemical science': 'ChemSci',
        'journal of chemical information and modeling': 'JCIM',
        'journal of medicinal chemistry': 'JMedChem',
        'bioinformatics': 'Bioinformatics',
        'briefings in bioinformatics': 'BIB',
        'nucleic acids research': 'NAR',
        'plos': 'PLoS',
        'biorxiv': 'bioRxiv',
        'chemrxiv': 'ChemRxiv',
        'medrxiv': 'medRxiv',
        'ijcai': 'IJCAI',
        'kdd': 'KDD',
        'www': 'WWW',
        'wsdm': 'WSDM',
        'sigir': 'SIGIR',
        'cikm': 'CIKM',
    }
    
    journal_lower = journal.lower()
    
    # Check for exact or partial matches
    for key, abbrev in mappings.items():
        if key in journal_lower:
            return abbrev
    
    # If no mapping found, use first word or abbreviation
    # Handle cases like "NeurIPS 2024"
    parts = journal.split()
    if parts:
        first = parts[0]
        # If already looks like an abbreviation (mostly uppercase)
        if first.isupper() or (len(first) <= 6 and first[0].isupper()):
            return first
        return first.capitalize()
    
    return "Unknown"

def main():
    parser = argparse.ArgumentParser(
        description="Rename PDFs from title.pdf to Journal-title.pdf format"
    )
    parser.add_argument(
        "--input-dir", required=True,
        help="Directory containing PDF files to rename"
    )
    parser.add_argument(
        "--csv", required=True,
        help="Path to the CSV file with paper metadata (Title, venue/Journal columns)"
    )
    args = parser.parse_args()

    downloads_dir = Path(args.input_dir)
    csv_path = args.csv
    
    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} papers from CSV")
    
    # Create title -> journal mapping
    # Use both Journal and venue columns
    title_to_journal = {}
    for _, row in df.iterrows():
        title = row.get('Title', '')
        if pd.isna(title):
            continue
        
        # Prefer venue over Journal if available
        journal = row.get('venue', row.get('Journal', ''))
        if pd.isna(journal) or not journal:
            journal = row.get('Journal', 'Unknown')
        
        title_to_journal[str(title).strip()] = str(journal).strip() if not pd.isna(journal) else "Unknown"
    
    print(f"Created mapping for {len(title_to_journal)} unique titles")
    
    # Get all PDF files
    pdf_files = list(downloads_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    renamed_count = 0
    skipped_count = 0
    not_found_count = 0
    
    for pdf_path in pdf_files:
        filename = pdf_path.name
        title_from_file = pdf_path.stem  # filename without .pdf
        
        # Skip if already has journal prefix (contains '-' after first word that looks like venue)
        if '-' in title_from_file:
            first_part = title_from_file.split('-')[0]
            # Check if first part looks like a venue abbreviation
            if first_part in ['AAAI', 'NeurIPS', 'ACL', 'ICML', 'ICLR', 'CVPR', 'Arxiv', 'Nature', 'TKDE', 'EMNLP', 'NAACL', 'KDD', 'IJCAI']:
                print(f"Skipping (already has prefix): {filename}")
                skipped_count += 1
                continue
        
        # Try to find matching title in CSV
        matched_journal = None
        matched_title = None
        
        # Try exact match first
        title_normalized = title_from_file.replace('_', ' ')
        for csv_title, journal in title_to_journal.items():
            if csv_title == title_normalized:
                matched_journal = journal
                matched_title = csv_title
                break
        
        # If no exact match, try fuzzy matching
        if not matched_journal:
            title_lower = title_from_file.lower().replace('_', ' ').replace('-', ' ')
            for csv_title, journal in title_to_journal.items():
                csv_lower = csv_title.lower().replace(':', '').replace('-', ' ')
                # Check if titles are similar enough
                if title_lower.startswith(csv_lower[:50]) or csv_lower.startswith(title_lower[:50]):
                    matched_journal = journal
                    matched_title = csv_title
                    break
                # Also check if the main content matches
                if len(title_lower) > 20 and len(csv_lower) > 20:
                    if title_lower[:40] in csv_lower or csv_lower[:40] in title_lower:
                        matched_journal = journal
                        matched_title = csv_title
                        break
        
        if matched_journal:
            abbrev = get_journal_abbrev(matched_journal)
            # Create new filename
            new_filename = f"{abbrev}-{filename}"
            new_path = pdf_path.parent / new_filename
            
            # Check if new file already exists
            if new_path.exists():
                print(f"Skipping (target exists): {filename}")
                skipped_count += 1
                continue
            
            print(f"Renaming: {filename} -> {new_filename}")
            pdf_path.rename(new_path)
            renamed_count += 1
        else:
            print(f"No match found: {filename}")
            not_found_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Renamed: {renamed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Not found in CSV: {not_found_count}")

if __name__ == "__main__":
    main()

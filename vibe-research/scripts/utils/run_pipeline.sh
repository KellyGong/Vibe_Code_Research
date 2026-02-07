#!/bin/bash
# Complete pipeline: batch process -> filter -> merge mindmaps
# Usage: ./run_pipeline.sh [--workers N]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKERS=${1:-100}

echo "=========================================="
echo "Step 1: Batch process all PDFs"
echo "=========================================="
python "$SCRIPT_DIR/pdf_constructor.py" --batch --force --workers "$WORKERS"

echo ""
echo "=========================================="
echo "Step 2: Filter unrelated papers"
echo "=========================================="
python "$SCRIPT_DIR/pdf_constructor.py" --filter-unrelated --workers "$WORKERS"

echo ""
echo "=========================================="
echo "Step 3: Merge into mindmaps"
echo "=========================================="
python "$SCRIPT_DIR/pdf_constructor.py" --merge

echo ""
echo "=========================================="
echo "Done! Check output in ./mindmap_output/"
echo "=========================================="

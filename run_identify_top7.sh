#!/bin/bash
# Runner script for identifying top 7 meeting types from calendar data

cd "$(dirname "$0")"

echo "=================================================="
echo "Top 7 Meeting Type Identification"
echo "=================================================="
echo ""
echo "Using Ollama LLM (gpt-oss:20b) to classify meetings"
echo ""

# Run the identification script
python tools/identify_top7_meetings.py "$@"

echo ""
echo "=================================================="
echo "Complete!"
echo "=================================================="

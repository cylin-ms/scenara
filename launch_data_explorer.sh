#!/bin/bash
# Meeting PromptCoT Data Explorer Launcher
# Quick launcher for the native UX interface

set -e

echo "🚀 Launching Meeting PromptCoT Data Explorer..."
echo "=============================================="

# Check if data exists
if [[ -f "meeting_prep_real_data/mevals_training_data.jsonl" ]]; then
    echo "✅ Real meeting data found!"
    echo "📊 Data will be automatically loaded"
else
    echo "⚠️  No real meeting data found"
    echo "💡 Generate data first with:"
    echo "   python mevals_promptcot_bridge.py --mevals-data MEvals/data/meeting_prep.prompt.samples --output meeting_prep_real_data"
    echo ""
    echo "🔄 Continuing with empty interface..."
fi

echo ""
echo "🌐 Starting web interface..."
echo "📱 Interface will open in your browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "💡 Features available:"
echo "   📊 Data Overview & Quality Analysis"
echo "   📅 Meeting Type & Organizer Analysis" 
echo "   🎯 Detailed Metrics Visualization"
echo "   🔍 Individual Scenario Explorer"
echo "   💾 Data Export & Reporting"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="

# Launch Streamlit
STREAMLIT_EMAIL="" streamlit run meeting_data_explorer.py --server.headless true
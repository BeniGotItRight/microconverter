#!/usr/bin/env bash
# Convertex - Start the file converter app (macOS / Linux)
cd "$(dirname "$0")"
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || echo "python3")
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt
echo ""
echo "Starting Convertex..."
echo "  Local:   http://localhost:8501"
echo "  Network: http://$(hostname -I 2>/dev/null | awk '{print $1}'):8501"
echo ""
streamlit run app.py --server.headless=true --server.port=8501

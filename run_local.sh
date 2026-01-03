#!/bin/bash
# Start Streamlit app on local network
# This allows colleagues on the same network to access the app

echo "🚀 Starting Panel Schedule Extractor Web App..."
echo ""
echo "This will start the web server accessible on your local network."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install streamlit if not already installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing Streamlit (first time only)..."
    pip install streamlit==1.40.0
fi

# Get local IP address
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo ""
echo "🌐 Starting server..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ACCESS THE APP:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📍 On this computer:"
echo "     http://localhost:8501"
echo ""
echo "  📍 From other computers on your network:"
echo "     http://${LOCAL_IP}:8501"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Share the network URL with your colleagues!"
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit with network access
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true

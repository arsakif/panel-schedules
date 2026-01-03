#!/bin/bash
# Start Streamlit app with ngrok tunnel for internet access

echo "🚀 Starting Panel Schedule Extractor with ngrok..."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Kill any existing streamlit or ngrok processes
pkill -f streamlit 2>/dev/null
pkill -f ngrok 2>/dev/null
sleep 2

echo "📦 Starting Streamlit server..."
# Start Streamlit in the background
nohup streamlit run app.py --server.address=localhost --server.port=8501 --server.headless=true > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
echo "⏳ Waiting for Streamlit to start..."
sleep 5

# Check if Streamlit is running
if ! ps -p $STREAMLIT_PID > /dev/null; then
    echo "❌ Failed to start Streamlit. Check streamlit.log for errors."
    exit 1
fi

echo "✅ Streamlit started successfully"
echo ""

echo "🌐 Starting ngrok tunnel..."
# Start ngrok
ngrok http 8501 --log=stdout

# Cleanup on exit
trap "pkill -f streamlit; pkill -f ngrok" EXIT

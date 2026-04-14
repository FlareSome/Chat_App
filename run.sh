#!/bin/bash

# 1. Setup Virtual Environment
if [ ! -d ".venv" ]; then
    echo "Creating environment..."
    python3 -m venv .venv
fi

# 2. Activate and Install
source .venv/bin/activate
echo "Installing dependencies..."
pip install "python-socketio[client]" websocket-client --quiet

if [ ! -d "node_modules" ]; then
    npm install --quiet
fi

# 3. Server Cleanup
pkill -f "node server.js" 2>/dev/null

# 4. Start Server
node server.js > /dev/null 2>&1 &
SERVER_PID=$!
sleep 1

# 5. Launch UI
python3 client.py

# 6. Final Cleanup
kill $SERVER_PID
deactivate
#!/usr/bin/env bash
set -e

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

echo "==> Creating Python venv"
python3 -m venv .venv
source .venv/bin/activate

echo "==> Installing Python requirements"
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Reminder: Install OLA via your OS (e.g., 'sudo apt install ola') if you need real DMX output."
echo "    OLA web UI: http://localhost:9090   Start daemon: 'sudo systemctl start olad'"

# Start backend
echo "==> Starting backend (FastAPI @ :8000)"
uvicorn backend.dmx_server:app --host 0.0.0.0 --port 8000 &
BACK_PID=$!

# Simple static server for frontend (Python http.server)
echo "==> Starting static server for frontend @ :5500"
cd frontend
python3 -m http.server 5500 &
FRONT_PID=$!
cd ..

trap 'echo "Stopping..."; kill $BACK_PID $FRONT_PID 2>/dev/null || true; deactivate' INT TERM

echo "Frontend: http://127.0.0.1:5500"
echo "Backend : http://127.0.0.1:8000"
echo "Press Ctrl+C to stop."
wait

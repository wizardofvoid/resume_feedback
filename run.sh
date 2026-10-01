#!/usr/bin/env bash
# Start the FastAPI backend and Next.js frontend together on macOS or Linux.
#
# Usage: ./run.sh (run `chmod +x run.sh` once first)
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -d frontend/node_modules ]]; then
  echo "Frontend dependencies are missing. Run 'npm --prefix frontend install' first." >&2
  exit 1
fi

echo "Starting FastAPI backend on http://localhost:8000 ..."
python -m uvicorn backend.api:app --port 8000 &
BACKEND_PID=$!

# Ensure the backend is stopped when this script exits.
trap 'echo "Shutting down backend (PID $BACKEND_PID) ..."; kill "$BACKEND_PID" 2>/dev/null || true' EXIT

sleep 2
echo "Starting Glance on http://localhost:3000 ..."
npm --prefix frontend run dev

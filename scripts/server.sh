#!/usr/bin/env bash
# Simple server control script for the Hotel Management System
# Usage: ./scripts/server.sh start|stop|restart|status

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$ROOT_DIR/backend/.venv/bin/python"
APP_MODULE="backend.app"
LOG_FILE="$ROOT_DIR/server.log"
PID_FILE="$ROOT_DIR/server.pid"
PORT=${PORT:-5000}

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Server appears to be running (pid $(cat "$PID_FILE"))"
    return 0
  fi
  echo "Starting server with $VENV_PY -m $APP_MODULE on port $PORT"
  # start in background, redirect output
  nohup "$VENV_PY" -m "$APP_MODULE" &> "$LOG_FILE" &
  echo $! > "$PID_FILE"
  sleep 0.5
  echo "Started (pid $(cat "$PID_FILE")), logs -> $LOG_FILE"
}

stop() {
  if [ ! -f "$PID_FILE" ]; then
    echo "No pid file found, server not running?"
    return 0
  fi
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "Stopping server pid $PID"
    kill "$PID"
    sleep 0.5
    if kill -0 "$PID" 2>/dev/null; then
      echo "Server still running, sending SIGKILL"
      kill -9 "$PID" || true
    fi
  else
    echo "Process $PID not running"
  fi
  rm -f "$PID_FILE"
}

status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Running (pid $(cat "$PID_FILE"))"
    return 0
  fi
  echo "Not running"
  return 1
}

case "${1:-}" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop || true
    start
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 2
    ;;
esac

#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="logs/analysis-$(date '+%Y%m%d-%H%M%S').log"

mkdir -p logs

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== Flink Log Analysis === [$TIMESTAMP]"
echo ""

# Job Manager Errors
echo "=== Job Manager Errors ==="
if docker ps --format '{{.Names}}' | grep -q "flink-jobmanager"; then
  docker logs flink-jobmanager 2>&1 | grep -i error | tail -10
else
  echo "[WARN] flink-jobmanager container not found or not running"
fi
echo ""

# Task Manager Performance (dynamic discovery)
echo "=== Task Manager Performance ==="
TM_LIST=$(docker ps --format '{{.Names}}' | grep "flink-taskmanager" || true)

if [ -z "$TM_LIST" ]; then
  echo "[WARN] No task manager containers found"
else
  for tm in $TM_LIST; do
    echo "--- $tm ---"
    docker logs "$tm" 2>&1 | grep -iE "memory|cpu|performance" | tail -5
    echo ""
  done
fi

# Checkpoint & Failure Analysis (new)
echo "=== Checkpoint & Failure Analysis ==="
if docker ps --format '{{.Names}}' | grep -q "flink-jobmanager"; then
  docker logs flink-jobmanager 2>&1 | grep -iE "checkpoint|fail|exception" | tail -10
fi
echo ""

# Network Issues
echo "=== Network Issues ==="
if docker ps --format '{{.Names}}' | grep -q "flink-jobmanager"; then
  docker logs flink-jobmanager 2>&1 | grep -iE "connection|network|timeout" | tail -5
fi
echo ""

echo "=== Analysis Complete === Log saved to: $LOG_FILE"

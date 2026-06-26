#!/bin/bash

INTERVAL=${1:-5}
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/swarm-monitor-$(date +%F).log"

mkdir -p "$LOG_DIR"

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running."
    exit 1
fi

trap 'echo -e "\nMonitoring stopped."; exit 0' SIGINT

while true; do
    clear

    TIMESTAMP=$(date)

    {
        echo "====================================================="
        echo " Docker Swarm Status - $TIMESTAMP"
        echo "====================================================="
        echo
        echo "[Nodes]"
        docker node ls
        echo "====================================================="
        echo "[Services]"
        docker service ls
        echo
        echo "[Web Service Tasks]"
        docker service ps webapp-stack_web
        echo
    } | tee -a "$LOG_FILE"

    sleep "$INTERVAL"
done

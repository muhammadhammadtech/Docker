#!/bin/bash

# ==============================
# Docker Swarm Monitoring Script
# ==============================

set -e

LOG_FILE="monitor.log"

# Function: check docker availability
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "[ERROR] Docker is not installed."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo "[ERROR] Docker daemon is not running."
        exit 1
    fi
}

# Function: print section header
section() {
    echo "====================================="
    echo "$1"
    echo "====================================="
}

# Function: monitor swarm
monitor_once() {
    section "Docker Nodes"
    docker node ls

    section "Docker Services"
    docker service ls

    section "Docker Stacks"
    docker stack ls

    section "Resource Usage"
    docker stats --no-stream
}

# Function: log output
log_output() {
    echo "[INFO] Logging output to $LOG_FILE"
    monitor_once >> "$LOG_FILE"
}

# ==============================
# Main Execution
# ==============================

check_docker

if [ "$1" == "--watch" ]; then
    echo "[INFO] Running in watch mode (refresh every 5 seconds)..."
    while true; do
        clear
        monitor_once
        sleep 5
    done
elif [ "$1" == "--log" ]; then
    log_output
else
    monitor_once
fi

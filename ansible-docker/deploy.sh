#!/bin/bash

# Docker + Ansible Deployment Script

set -euo pipefail

ENVIRONMENT=${1:-development}
SERVICE=${2:-all}
MODE=${3:-deploy}

INVENTORY_FILE=${INVENTORY_FILE:-inventory.ini}
LOG_FILE="deployment-$(date +%F-%H%M%S).log"

START_TIME=$(date +%s)

log() {
    echo "[$(date '+%F %T')] $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {

    log "Checking prerequisites..."

    command -v ansible >/dev/null || { log "Ansible is not installed."; exit 1; }
    command -v docker >/dev/null || { log "Docker is not installed."; exit 1; }

    [ -f "$INVENTORY_FILE" ] || {
        log "Inventory file not found: $INVENTORY_FILE"
        exit 1
    }

    log "Prerequisites check passed."
}

run_playbook() {

    local playbook=$1

    ansible-playbook --syntax-check -i "$INVENTORY_FILE" "$playbook"

    if [ "$MODE" = "check" ]; then
        ansible-playbook --check -i "$INVENTORY_FILE" "$playbook" \
            -e "environment=$ENVIRONMENT"
    else
        ansible-playbook -i "$INVENTORY_FILE" "$playbook" \
            -e "environment=$ENVIRONMENT"
    fi
}

deploy_service() {

    case "$SERVICE" in
        nginx)
            log "Deploying Nginx..."
            run_playbook deploy-nginx.yml
            ;;
        wordpress)
            log "Deploying WordPress..."
            run_playbook deploy-wordpress.yml
            ;;
        all)
            log "Deploying all services..."
            SERVICE=nginx
            deploy_service
            SERVICE=wordpress
            deploy_service
            ;;
        *)
            log "Unknown service: $SERVICE"
            exit 1
            ;;
    esac
}

health_check() {

    FAILED=0

    log "Running health checks..."

    curl -fs http://localhost:8080 >/dev/null || FAILED=1
    curl -fs http://localhost:8081 >/dev/null || FAILED=1

    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

    if [ "$FAILED" -eq 1 ]; then
        log "Health checks failed."
        exit 1
    fi

    log "Health checks passed."
}

main() {

    log "Environment : $ENVIRONMENT"
    log "Service     : $SERVICE"
    log "Mode        : $MODE"

    check_prerequisites

    deploy_service

    sleep 10

    health_check

    END_TIME=$(date +%s)

    log "Deployment completed successfully."

    log "Duration: $((END_TIME-START_TIME)) seconds."
}

main

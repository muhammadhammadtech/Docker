#!/bin/bash

set -euo pipefail

ENVIRONMENT=${1:-blue}
ACTION=${2:-deploy}

MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_INTERVAL=${RETRY_INTERVAL:-2}

LOG_FILE="deployment-$(date +%F-%H%M%S).log"

log() {
    echo "[$(date '+%F %T')] $1" | tee -a "$LOG_FILE"
}

validate_environment() {

    case "$ENVIRONMENT" in
        blue|green) ;;
        *)
            log "Invalid environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
}

check_prerequisites() {

    command -v docker-compose >/dev/null || {
        log "docker-compose is not installed."
        exit 1
    }

    command -v curl >/dev/null || {
        log "curl is not installed."
        exit 1
    }
}

deploy_environment() {

    docker-compose -f docker-compose.$ENVIRONMENT.yml up -d --build

    PORT=3001
    [ "$ENVIRONMENT" = "green" ] && PORT=3002

    log "Waiting for $ENVIRONMENT environment to become healthy..."

    for ((i=1;i<=MAX_RETRIES;i++)); do

        if curl -fs http://localhost:$PORT/health >/dev/null; then
            log "$ENVIRONMENT deployment completed successfully."
            return
        fi

        log "Health check attempt $i/$MAX_RETRIES failed."

        sleep "$RETRY_INTERVAL"
    done

    log "Deployment failed. Health check timeout reached."
    exit 1
}

case "$ACTION" in

deploy)

    START=$(date +%s)

    check_prerequisites

    validate_environment

    log "Deploying $ENVIRONMENT environment..."

    deploy_environment

    END=$(date +%s)

    log "Deployment finished in $((END-START)) seconds."

    ;;

stop)

    log "Stopping $ENVIRONMENT environment..."

    docker-compose -f docker-compose.$ENVIRONMENT.yml down

    ;;

status)

    docker-compose -f docker-compose.$ENVIRONMENT.yml ps

    ;;

*)

    echo "Usage: $0 {blue|green} {deploy|stop|status}"

    exit 1

    ;;
esac

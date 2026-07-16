#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: ./deploy.sh <environment> <version>"
    exit 1
fi

ENVIRONMENT="$1"
VERSION="$2"

TFVARS_FILE="${ENVIRONMENT}.tfvars"
PLAN_FILE="tfplan-${ENVIRONMENT}-$(date +%Y%m%d%H%M%S)"
LOG_FILE="deploy-${ENVIRONMENT}-$(date +%F-%H%M%S).log"

log() {
    echo "[$(date '+%F %T')] $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {

    for cmd in terraform jq curl; do
        command -v "$cmd" >/dev/null || {
            log "$cmd is not installed."
            exit 1
        }
    done
}

START_TIME=$(date +%s)

check_prerequisites

[ -f "$TFVARS_FILE" ] || {
    log "$TFVARS_FILE not found."
    exit 1
}

log "Deploying environment: $ENVIRONMENT"
log "Application version: $VERSION"

if [ ! -d ".terraform" ]; then
    terraform init
fi

terraform fmt -check
terraform validate

if [ -f terraform.tfstate ]; then
    cp terraform.tfstate "terraform.tfstate.pre_${ENVIRONMENT}_deploy"
    log "Terraform state snapshot created."
fi

terraform plan \
    -var-file="$TFVARS_FILE" \
    -out="$PLAN_FILE"

terraform apply "$PLAN_FILE"

FAILED=0

log "Running health checks..."

PORTS=$(terraform output -json external_ports | jq -r '.[]')

for PORT in $PORTS
do
    STATUS=$(curl -s \
        -o /dev/null \
        -w "%{http_code}" \
        --max-time 5 \
        http://localhost:$PORT || echo "000")

    if [ "$STATUS" != "200" ]; then
        FAILED=1
        log "Health check failed on port $PORT (HTTP $STATUS)"
    else
        log "Healthy: http://localhost:$PORT"
    fi
done

if [ "$FAILED" -eq 1 ]; then
    log "Deployment failed."
    log "Rollback command:"
    log "bash rollback.sh $ENVIRONMENT"
    exit 1
fi

END_TIME=$(date +%s)

log "Deployment completed successfully."
log "Duration: $((END_TIME-START_TIME)) seconds."

#!/bin/bash

# Docker + Ansible Deployment Script
# Usage: ./deploy.sh [environment] [service]

set -e

ENVIRONMENT=${1:-development}
SERVICE=${2:-all}
INVENTORY_FILE="inventory.ini"

echo "=== Docker + Ansible Deployment Script ==="
echo "Environment: $ENVIRONMENT"
echo "Service: $SERVICE"
echo "=========================================="

check_prerequisites() {
    echo "Checking prerequisites..."

    if ! command -v ansible &> /dev/null; then
        echo "Error: Ansible is not installed"
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed"
        exit 1
    fi

    if [ ! -f "$INVENTORY_FILE" ]; then
        echo "Error: Inventory file not found: $INVENTORY_FILE"
        exit 1
    fi

    echo "Prerequisites check passed!"
}

deploy_service() {
    local service=$1
    local env=$2

    case $service in
        "nginx")
            echo "Deploying Nginx service..."
            ansible-playbook -i $INVENTORY_FILE deploy-nginx.yml -e "environment=$env"
            ;;
        "wordpress")
            echo "Deploying WordPress service..."
            ansible-playbook -i $INVENTORY_FILE deploy-wordpress.yml -e "environment=$env"
            ;;
        "all")
            echo "Deploying all services..."
            deploy_service "nginx" "$env"
            deploy_service "wordpress" "$env"
            ;;
        *)
            echo "Unknown service: $service"
            echo "Available services: nginx, wordpress, all"
            exit 1
            ;;
    esac
}

health_check() {
    echo "Running health checks..."

    if curl -f http://localhost:8080 > /dev/null 2>&1; then
        echo "Nginx service is healthy"
    else
        echo "Nginx service is not responding"
    fi

    if curl -f http://localhost:8081 > /dev/null 2>&1; then
        echo "WordPress service is healthy"
    else
        echo "WordPress service is not responding"
    fi

    echo "Running containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

main() {
    check_prerequisites
    deploy_service "$SERVICE" "$ENVIRONMENT"
    echo "Waiting for services to start..."
    sleep 10
    health_check
    echo "Deployment completed successfully!"
}

main

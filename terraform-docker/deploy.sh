#!/bin/bash
set -e

if [ "$#" -ne 2 ]; then
  echo "Usage: bash deploy.sh <environment> <version>"
  exit 1
fi

ENVIRONMENT=$1
VERSION=$2
TFVARS_FILE="${ENVIRONMENT}.tfvars"

if [ ! -f "$TFVARS_FILE" ]; then
  echo "ERROR: $TFVARS_FILE not found!"
  exit 1
fi

echo "===> Deploying to: $ENVIRONMENT (version: $VERSION)"

if [ ! -d ".terraform" ]; then
  echo "===> Running terraform init..."
  terraform init
fi

# Deploy se PEHLE current state ka snapshot lo
if [ -f "terraform.tfstate" ]; then
  cp terraform.tfstate "terraform.tfstate.pre_${ENVIRONMENT}_deploy"
  echo "===> State snapshot saved: terraform.tfstate.pre_${ENVIRONMENT}_deploy"
fi

echo "===> Running terraform plan..."
terraform plan -var-file="$TFVARS_FILE" -out=tfplan

echo "===> Running terraform apply..."
terraform apply tfplan

# Health checks
echo "===> Running health checks..."
PORTS=$(terraform output -json external_ports | jq -r '.[]')
FAILED=0

for PORT in $PORTS; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:${PORT}" || echo "000")
  if [ "$HTTP_CODE" = "200" ]; then
    echo "  ✓ http://localhost:${PORT} => HTTP $HTTP_CODE"
  else
    echo "  ✗ http://localhost:${PORT} => HTTP $HTTP_CODE (FAILED)"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo "ERROR: Health checks failed! Run: bash rollback.sh $ENVIRONMENT"
  exit 1
fi

echo "===> Deployment successful! All containers are healthy."

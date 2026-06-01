#!/bin/bash
set -e
ENVIRONMENT=${1:-""}
SNAPSHOT_FILE=""
if [ -n "$ENVIRONMENT" ] && [ -f "terraform.tfstate.pre_${ENVIRONMENT}_deploy" ]; then
  SNAPSHOT_FILE="terraform.tfstate.pre_${ENVIRONMENT}_deploy"
  echo "===> Using snapshot: $SNAPSHOT_FILE"
elif [ -f "terraform.tfstate.backup" ]; then
  SNAPSHOT_FILE="terraform.tfstate.backup"
  echo "===> Using default backup: $SNAPSHOT_FILE"
else
  echo "ERROR: No backup state found."
  exit 1
fi
echo "===> Force removing all current containers..."
docker ps -aq | xargs -r docker rm -f
echo "===> All containers removed."
cp "$SNAPSHOT_FILE" terraform.tfstate
echo "===> State restored."
echo "===> Clearing stale container references..."
terraform state list 2>/dev/null | grep "docker_container" | while read resource; do
  terraform state rm "$resource" 2>/dev/null || true
done
echo "===> Re-applying previous infrastructure..."
terraform apply -var-file="${ENVIRONMENT:-custom}.tfvars" -auto-approve
echo "===> Verifying rollback health..."
PORTS=$(terraform output -json external_ports 2>/dev/null | jq -r ".[]" || echo "")
if [ -z "$PORTS" ]; then echo "===> No containers."; exit 0; fi
ALL_OK=1
for PORT in $PORTS; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:${PORT}" || echo "000")
  if [ "$HTTP_CODE" = "200" ]; then
    echo "  OK http://localhost:${PORT} => HTTP $HTTP_CODE"
  else
    echo "  FAIL http://localhost:${PORT} => HTTP $HTTP_CODE"
    ALL_OK=0
  fi
done
if [ "$ALL_OK" -eq 1 ]; then
  echo "===> Rollback successful!"
else
  echo "WARNING: Some health checks failed."
fi

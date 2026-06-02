#!/bin/bash
set -e

NETWORK="ci-lab104-net"
CONTAINER="ci-webapp"
RESULTS_DIR="/tmp/ci-results"
RPS_THRESHOLD=40

mkdir -p "$RESULTS_DIR"

# Cleanup function - runs always (even on failure)
cleanup() {
  echo ""
  echo "--- Cleaning up ---"
  docker rm -f "$CONTAINER" 2>/dev/null || true
  docker network rm "$NETWORK" 2>/dev/null || true
  echo "Cleanup done."
}
trap cleanup EXIT

echo "=== CI Pipeline Start ==="

# Step 1: Build app image
echo "[1] Building Docker image..."
docker build -t ci-lab104-app ~/lab104/app/

# Step 2: Create network
echo "[2] Creating network..."
docker network create "$NETWORK"

# Step 3: Start app container
echo "[3] Starting app container..."
docker run -d \
  --name "$CONTAINER" \
  --network "$NETWORK" \
  ci-lab104-app

# Step 4: Health check retry loop
echo "[4] Waiting for app to be ready..."
RETRIES=10
until docker run --rm --network "$NETWORK" curlimages/curl:latest \
  curl -sf http://$CONTAINER:3000/ > /dev/null 2>&1; do
  RETRIES=$((RETRIES - 1))
  if [ "$RETRIES" -le 0 ]; then
    echo "ERROR: App did not become healthy in time."
    exit 1
  fi
  echo "  Waiting... ($RETRIES retries left)"
  sleep 2
done
echo "  App is healthy!"

# Step 5: Run Apache Bench
echo "[5] Running Apache Bench..."
docker run --rm \
  --network "$NETWORK" \
  lab104-ab \
  ab -n 500 -c 20 http://$CONTAINER:3000/ > "$RESULTS_DIR/ab.txt" 2>&1

# Step 6: Extract metrics
RPS=$(grep "Requests per second" "$RESULTS_DIR/ab.txt" | awk '{print $4}' | cut -d'.' -f1)
FAILED=$(grep "Failed requests" "$RESULTS_DIR/ab.txt" | awk '{print $3}')

echo ""
echo "=== CI Results ==="
echo "Requests per second : $RPS (threshold: $RPS_THRESHOLD)"
echo "Failed requests     : $FAILED (threshold: 0)"

# Step 7: Threshold check
PASS=true

if [ "$RPS" -lt "$RPS_THRESHOLD" ]; then
  echo "FAIL: RPS $RPS is below threshold $RPS_THRESHOLD"
  PASS=false
fi

if [ "$FAILED" -gt 0 ]; then
  echo "FAIL: $FAILED failed requests detected"
  PASS=false
fi

echo ""
if [ "$PASS" = true ]; then
  echo "✅ VERDICT: PASS"
  exit 0
else
  echo "❌ VERDICT: FAIL"
  exit 1
fi

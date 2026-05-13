#!/bin/bash

echo "=== Docker Content Trust Verification Demo ==="

echo "1. Checking trust info for alpine:latest:"
docker trust inspect --pretty alpine:latest 2>/dev/null || echo "No trust data available"

echo ""
echo "2. Pull with trust DISABLED:"
export DOCKER_CONTENT_TRUST=0
if docker pull alpine:3.14 >/dev/null 2>&1; then
    echo "Pull succeeded (no verification)"
else
    echo "Pull failed"
fi

echo ""
echo "3. Pull with trust ENABLED:"
export DOCKER_CONTENT_TRUST=1
if docker pull alpine:3.14 >/dev/null 2>&1; then
    echo "Pull succeeded (verified)"
else
    echo "Pull failed (verification enforced)"
fi

echo ""
echo "=== Demo Complete ==="

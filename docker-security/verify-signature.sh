#!/bin/bash

echo "=== Docker Content Trust Verification Demo ==="

echo "1. Checking trust info for alpine:latest:"
docker trust inspect --pretty alpine:latest 2>/dev/null || echo "No trust data available"

echo ""
echo "2. Pull with trust DISABLED:"
export DOCKER_CONTENT_TRUST=0
docker pull alpine:3.14 >/dev/null 2>&1 && echo "Pull succeeded (no verification)" || echo "Pull failed"

echo ""
echo "3. Pull with trust ENABLED:"
export DOCKER_CONTENT_TRUST=1
docker pull alpine:3.14 >/dev/null 2>&1 && echo "Pull succeeded (trust verified)" || echo "Pull failed — no trust data"

echo ""
echo "Trust enforcement active: unsigned images will be rejected."

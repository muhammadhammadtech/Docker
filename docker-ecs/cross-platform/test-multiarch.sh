#!/bin/bash

DOCKER_USERNAME="hammad2005"
IMAGE_NAME="${DOCKER_USERNAME}/cross-platform-demo:latest"

echo "AMD64:"
docker run --rm --platform linux/amd64 ${IMAGE_NAME} node -e "console.log(process.arch)"

echo "ARM64:"
docker run --rm --platform linux/arm64 ${IMAGE_NAME} node -e "console.log(process.arch)"

#!/bin/bash
# =============================================================================
# monitor-scaling.sh — Kubernetes Autoscaling Monitor
# Usage: ./monitor-scaling.sh [-n <namespace>] [-i <interval_seconds>]
# =============================================================================

set -euo pipefail

# ---------- defaults ----------
NAMESPACE="default"
INTERVAL=10

# ---------- argument parsing ----------
while getopts "n:i:h" opt; do
  case $opt in
    n) NAMESPACE="$OPTARG" ;;
    i) INTERVAL="$OPTARG" ;;
    h)
      echo "Usage: $0 [-n namespace] [-i interval_seconds]"
      echo "  -n  Kubernetes namespace to monitor (default: default)"
      echo "  -i  Refresh interval in seconds    (default: 10)"
      exit 0
      ;;
    *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
  esac
done

# ---------- color helpers ----------
BOLD='\033[1m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RESET='\033[0m'

header() { echo -e "${CYAN}${BOLD}--- $1 ---${RESET}"; }

# ---------- graceful exit ----------
trap 'echo -e "\n${YELLOW}Monitor stopped at $(date). Namespace: ${NAMESPACE}${RESET}"; exit 0' INT TERM

# ---------- main loop ----------
echo -e "${BOLD}=== Kubernetes Autoscaling Monitor ===${RESET}"
echo -e "Namespace: ${NAMESPACE} | Interval: ${INTERVAL}s | Press Ctrl+C to stop\n"

while true; do
  clear
  echo -e "${BOLD}=== Time: $(date) | Namespace: ${NAMESPACE} ===${RESET}"
  echo

  header "HPA Status"
  kubectl get hpa web-app-hpa -n "$NAMESPACE" 2>&1 || echo "  HPA not found in namespace '${NAMESPACE}'"
  echo

  header "Deployment Rollout"
  kubectl get deployment web-app -n "$NAMESPACE" 2>&1 || echo "  Deployment not found"
  echo

  header "Pod Count & Placement"
  kubectl get pods -l app=web-app -n "$NAMESPACE" -o wide 2>&1 || echo "  No pods found"
  echo

  header "Pod Resource Usage"
  TOP_OUT=$(kubectl top pods -l app=web-app -n "$NAMESPACE" 2>&1) \
    && echo "$TOP_OUT" \
    || echo "  Metrics unavailable — is metrics-server running? ($TOP_OUT)"
  echo

  header "Node Resource Usage"
  kubectl top nodes 2>&1 || echo "  Node metrics unavailable"
  echo

  sleep "$INTERVAL"
done

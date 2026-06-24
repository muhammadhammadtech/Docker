#!/bin/bash

REPORT_DIR="/tmp/docker-security-reports"
REPO_DIR="$HOME/Docker/docker-bench/docker-bench-security"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$REPORT_DIR"

if [ ! -d "$REPO_DIR" ]; then
    echo "Error: Docker Bench Security directory not found."
    exit 1
fi

echo "Running Docker security audit..."

cd "$REPO_DIR" || exit 1

if ! sudo ./docker-bench-security.sh > "$REPORT_DIR/audit_$DATE.txt" 2>&1; then
    echo "Error: Audit execution failed."
    exit 1
fi

FAILS=$(grep -c "FAIL" "$REPORT_DIR/audit_$DATE.txt")
WARNS=$(grep -c "WARN" "$REPORT_DIR/audit_$DATE.txt")
PASSES=$(grep -c "PASS" "$REPORT_DIR/audit_$DATE.txt")

echo "Audit Complete - $DATE"
echo "Report saved: $REPORT_DIR/audit_$DATE.txt"
echo "  Passed:   $PASSES"
echo "  Failed:   $FAILS"
echo "  Warnings: $WARNS"

if [ "$FAILS" -gt 10 ]; then
    echo "ALERT: High number of failures detected!"
    grep "FAIL" "$REPORT_DIR/audit_$DATE.txt" | head -5
fi

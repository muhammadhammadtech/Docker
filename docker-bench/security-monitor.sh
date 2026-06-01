#!/bin/bash

REPORT_DIR="/tmp/docker-security-reports"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $REPORT_DIR

echo "Running Docker security audit..."
cd ~/docker-security/docker-bench-security
sudo ./docker-bench-security.sh > $REPORT_DIR/audit_$DATE.txt 2>&1

FAILS=$(grep -c "FAIL" $REPORT_DIR/audit_$DATE.txt)
WARNS=$(grep -c "WARN" $REPORT_DIR/audit_$DATE.txt)
PASSES=$(grep -c "PASS" $REPORT_DIR/audit_$DATE.txt)

echo "Audit Complete - $DATE"
echo "Report saved: $REPORT_DIR/audit_$DATE.txt"
echo "  Passed:   $PASSES"
echo "  Failed:   $FAILS"
echo "  Warnings: $WARNS"

if [ "$FAILS" -gt 10 ]; then
    echo "ALERT: High number of failures detected!"
    grep "FAIL" $REPORT_DIR/audit_$DATE.txt | head -5
fi

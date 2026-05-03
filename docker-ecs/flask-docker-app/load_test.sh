#!/bin/bash
for i in {1..10}; do
  curl -s http://localhost > /dev/null
  echo "Request $i sent"
done

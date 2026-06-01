#!/bin/bash
if ! pgrep nginx > /dev/null; then
    echo "Nginx not running"
    exit 1
fi
if ! curl -f -s http://localhost/ > /dev/null; then
    echo "Web page not accessible"
    exit 1
fi
echo "Health check passed"
exit 0

#!/bin/bash
while true; do
    clear
    echo "=== Docker Swarm Status — $(date) ==="
    echo ""
    echo "--- Nodes ---"
    sudo docker node ls
    echo ""
    echo "--- Services ---"
    sudo docker service ls
    echo ""
    echo "--- Tasks (webapp) ---"
    sudo docker service ps webapp-stack_web
    sleep 5
done

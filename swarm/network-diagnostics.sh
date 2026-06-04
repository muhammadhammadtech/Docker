#!/bin/bash
set -euo pipefail   # ← fail fast on errors / unset vars

# Dependency check
if ! command -v jq &>/dev/null; then
  echo "Error: 'jq' is required but not installed." >&2
  exit 1
fi

inspect_network() {
  local net="$1"
  if docker network inspect "$net" &>/dev/null; then
    docker network inspect "$net" --format '{{json .}}' | jq '{
      Name: .Name, Driver: .Driver, Scope: .Scope,
      Subnet: .IPAM.Config[0].Subnet,
      Gateway: .IPAM.Config[0].Gateway
    }'
  else
    echo "  Network '$net' not found." >&2
  fi
}

echo "=== Docker Swarm Network Diagnostics ==="

echo "1. Swarm Status:"
docker info | grep -A 5 "Swarm:"

echo -e "\n2. Network List:"
docker network ls

echo -e "\n3. Service Status:"
docker service ls

echo -e "\n4. Webapp Network Details:"
inspect_network "webapp-network"

echo -e "\n5. Backend Network Details:"
inspect_network "backend-network"

echo -e "\n6. Service VIP Info:"
while IFS= read -r service; do                           # ← quoted, safe loop
  echo "Service: $service"
  docker service inspect "$service" \
    --format '{{range .Endpoint.VirtualIPs}}  Network: {{.NetworkID}} | IP: {{.Addr}}{{"\n"}}{{end}}'
done < <(docker service ls --format '{{.Name}}')

echo -e "\n7. Node Status:"
docker node ls

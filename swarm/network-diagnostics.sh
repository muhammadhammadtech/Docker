#!/bin/bash

echo "=== Docker Swarm Network Diagnostics ==="

echo "1. Swarm Status:"
docker info | grep -A 5 "Swarm:"

echo ""
echo "2. Network List:"
docker network ls

echo ""
echo "3. Service Status:"
docker service ls

echo ""
echo "4. Webapp Network Details:"
docker network inspect webapp-network --format '{{json .}}' | jq '{
  Name: .Name,
  Driver: .Driver,
  Scope: .Scope,
  Subnet: .IPAM.Config[0].Subnet,
  Gateway: .IPAM.Config[0].Gateway
}'

echo ""
echo "5. Backend Network Details:"
docker network inspect backend-network --format '{{json .}}' | jq '{
  Name: .Name,
  Driver: .Driver,
  Scope: .Scope,
  Subnet: .IPAM.Config[0].Subnet,
  Gateway: .IPAM.Config[0].Gateway
}'

echo ""
echo "6. Service VIP Info:"
for service in $(docker service ls --format '{{.Name}}'); do
    echo "Service: $service"
    docker service inspect $service --format '{{range .Endpoint.VirtualIPs}}  Network: {{.NetworkID}} | IP: {{.Addr}}{{"\n"}}{{end}}'
done

echo ""
echo "7. Node Status:"
docker node ls

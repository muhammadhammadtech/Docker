output "container_names" {
  description = "List of all container names"
  value       = [for c in docker_container.nginx : c.name]
}

output "external_ports" {
  description = "List of all external ports"
  value       = [for c in docker_container.nginx : c.ports[0].external]
}

output "access_urls" {
  description = "HTTP access URLs for all containers"
  value       = [for c in docker_container.nginx : "http://localhost:${c.ports[0].external}"]
}

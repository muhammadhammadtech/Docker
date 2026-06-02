terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = true
}

resource "docker_container" "nginx" {
  count = var.container_count
  name  = "${var.name_prefix}-${count.index}"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = var.base_external_port + count.index
  }

  env = [
    "ENVIRONMENT=${var.environment_label}"
  ]
}

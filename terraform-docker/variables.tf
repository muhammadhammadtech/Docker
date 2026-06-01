variable "container_count" {
  description = "Number of nginx containers to create"
  type        = number
  default     = 2
}

variable "name_prefix" {
  description = "Prefix for container names"
  type        = string
  default     = "nginx-lab"
}

variable "base_external_port" {
  description = "Starting external port number"
  type        = number
  default     = 8080
}

variable "environment_label" {
  description = "Environment name (staging/production)"
  type        = string
  default     = "dev"
}

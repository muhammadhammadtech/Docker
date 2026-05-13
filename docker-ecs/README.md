# Docker & Kubernetes Labs Portfolio

This repository contains my hands-on Docker and Kubernetes lab work, demonstrating practical containerization, orchestration, and microservices concepts.  
It serves as a portfolio for containerized application deployment, monitoring, and automation.

## 🎯 Purpose of This Repository

- Learn and practice containerization with Docker  
- Explore multi-container apps using Docker Compose  
- Implement Kubernetes deployments and services  
- Understand health checks, restart policies, and monitoring  
- Build microservices and secure containerized applications  
- Apply ML models within Docker containers  

This repository is continuously updated with new labs and projects.

## 🧪 Lab Environment

- **Container Engine:** Docker installed on Al Nafi lab cloud machines  
- **Orchestration:** Kubernetes (minikube / provided lab cluster)  
- **Languages:** Python, Node.js  
- **Focus:** Real-world scenarios, microservices, secure deployments

## 📂 Repository Structure

Each folder represents a lab or project:

- `aks-demo-app` – Demo app deployed on AKS with Kubernetes manifests  
- `docker-compose-lab` – Multi-service apps with Docker Compose (Python, Redis, Nginx)  
- `docker-healthcheck-lab` – Health checks, restart policies, and monitoring scripts  
- `flask-docker-app` – Flask web app containerization with Docker & Nginx  
- `k8s-lab` – Kubernetes pods, deployments, and services  
- `microservices-lab` – Multi-service architecture with Docker & Nginx load balancing  
- `ml-docker` – Machine learning model containerization  
- `ml-docker-lab` – Dockerized ML API with model management and database integration  
- `sample-app` – CI/CD demo with Docker, Jenkins, and SonarQube  
- `secure-app` – Secure Docker deployments with read-only containers and best practices  
- `webapp-k8s` – Flask web application deployed on Kubernetes  

Each directory contains Dockerfiles, configuration files, manifests, and scripts for practical execution.

## 🚀 Topics Covered

- Docker basics and advanced features  
- Docker Compose for multi-container apps  
- Health checks and restart policies  
- Kubernetes basics: Pods, Deployments, Services  
- Microservices architecture  
- Flask and Node.js containerization  
- ML model deployment in containers  
- Secure Docker deployments and best practices  
- CI/CD pipelines with Docker  

## ▶️ How to Use

Clone the repository:

```bash
git clone https://github.com/<your-username>/Docker.git
cd Docker
```
Run Docker or Compose apps:

```bash
# Build and run a single container
docker build -t <image_name> <folder>
docker run -d -p <host_port>:<container_port> <image_name>

# Run Docker Compose apps
docker-compose -f docker-compose.yml up -d
```
Kubernetes manifests can be applied with:
```bash
kubectl apply -f <manifest.yaml>
```

## 🔄 Continuous Updates

This repository is actively maintained.
New labs, microservices setups, ML integration, and secure containerization examples will be added regularly.

## 📘 Notes

- Labs are run on **Al Nafi cloud machines**, not local system
- Safe environment for experimentation and learning

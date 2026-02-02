# DEVOPS.md

## Project Overview

This repository contains a simple full‑stack application built as part of a DevOps assessment.

* **Backend:** Django REST API
* **Frontend:** React (Vite)
* **Containerization:** Docker (multi‑stage builds, non‑root containers)
* **CI/CD:** GitHub Actions
* **Registry:** Docker Hub
* **Deployment:** Local machine using a self‑hosted GitHub Actions runner

---

## 1. Setup Guide

### 1.1 Prerequisites

Make sure the following tools are installed on your system:

* Git
* Docker & Docker Compose
* Node.js (v18+)
* Python (v3.10+)
* GitHub account
* Docker Hub account

---

## 1.2 Running the Project Locally (Without CI/CD)

This is useful for development and debugging.

### Step 1: Clone the repository

```bash
git clone https://github.com/<your-username>/devops-assessment.git
cd devops-assessment
```

### Step 2: Build and run using Docker Compose

From the project root:

```bash
docker compose up --build
```

### Step 3: Access the application

* Backend API: [http://localhost:8000/api/hello/](http://localhost:8000/api/hello/)
* Frontend UI: [http://localhost:3000](http://localhost:3000)

Stop containers:

```bash
docker compose down
```

---

## 1.3 CI/CD Pipeline (Docker Image Build)

A GitHub Actions workflow is configured to automatically build and push Docker images to Docker Hub whenever code is pushed to the `main` branch.

### What the pipeline does

* Builds backend Docker image
* Builds frontend Docker image
* Pushes both images to Docker Hub

### Docker Images

* Backend: `sagargoswami27/devops-backend:latest`
* Frontend: `sagargoswami27/devops-frontend:latest`

Docker Hub authentication is handled securely using GitHub Secrets and Docker Hub access tokens.

---

## 1.4 Deployment on Local Machine (Self‑Hosted Runner)

Since no cloud provider is used, deployment is done on the local machine using a **self‑hosted GitHub Actions runner**.

### Step 1: Install GitHub Actions Runner

```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf actions-runner.tar.gz
```

### Step 2: Configure the runner

Go to:

```
Repository → Settings → Actions → Runners → New self-hosted runner
```

Copy the provided configuration command and run it:

```bash
./config.sh --url https://github.com/<your-username>/devops-assessment --token <TOKEN>
```

### Step 3: Start the runner

```bash
./run.sh
```

The runner will now listen for deployment jobs.

---

## 1.5 Automated Local Deployment

A separate GitHub Actions workflow (`deploy-local.yml`) is used for deployment.

### Deployment flow

1. Code is pushed to `main`
2. GitHub triggers the deployment workflow
3. Job is picked up by the self‑hosted runner
4. Latest Docker images are pulled from Docker Hub
5. Containers are started using Docker Compose

### Access after deployment

* Backend: [http://localhost:8000/api/hello/](http://localhost:8000/api/hello/)
* Frontend: [http://localhost:3000](http://localhost:3000)

---

## 2. Troubleshooting Log

### Issue: Docker Pull Failed on Self‑Hosted Runner

**Error Message:**

```
error getting credentials - fork/exec docker-credential-desktop.exe: exec format error
```

### Root Cause

The self‑hosted runner was running on Linux (WSL), but Docker was trying to use the Windows credential helper (`docker-credential-desktop.exe`). This happened because Docker Desktop credentials were automatically copied into the Linux Docker configuration.

Linux cannot execute Windows `.exe` binaries, which caused Docker authentication to fail during image pulls.

### Resolution

1. Removed the Windows credential helper configuration:

```bash
rm ~/.docker/config.json
```

2. Logged in to Docker Hub directly from Linux using an access token:

```bash
docker login
```

3. Verified image pull manually:

```bash
docker pull sagargoswami27/devops-backend:latest
docker pull sagargoswami27/devops-frontend:latest
```

4. Restarted the GitHub Actions runner

After this fix, the deployment workflow run successfully and containers started without issues.

---

## Phase 3: Infrastructure as Code (Bonus / Plus Point)

I have created this DEVOPS.md file to clearly explain my own approach and the work completed during this assignment.

For Phase 3, the task was to deploy the application to a cloud provider using Terraform and provision infrastructure such as a Virtual Machine along with security rules. I understand that this can be implemented on any major cloud platform such as AWS (EC2), Azure (Virtual Machine), or Google Cloud (Compute Engine) using Terraform.

However, I did not implement this phase practically because I currently do not have access to any free-tier cloud account. Without a free-tier or sponsored account, provisioning real cloud infrastructure would incur costs, so I intentionally avoided deploying to the cloud.

### Proposed Terraform Setup

The Terraform configuration would provision:

* A Virtual Machine (EC2 / Azure VM / GCE)
* Docker and Docker Compose installed via user-data / startup script
* Firewall / Security Group with restricted access

### Security Configuration

The VM firewall would allow **only the required ports**:

* **22** – SSH (restricted to developer IP)
* **80** – HTTP
* **443** – HTTPS

All other inbound traffic would be denied by default, following the principle of least privilege.

### Example (AWS – Conceptual Terraform Snippet)

```hcl
resource "aws_security_group" "devops_sg" {
  name = "devops-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP/32"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

# Local / Main Development Machine Setup

![DevMachine-Setup](./images/pt-k8s-local-dev-machine-setup.png)

This document outlines the required prerequisites for setting up your local development environment. These steps are designed for Linux distributions and Windows Subsystem for Linux (WSL).

## System Requirements

- A virtual machine running a Linux distribution (Ubuntu Server is recommended). There are many guides on the interenet to achieve this.

## Required Tools

These are required on your **local dev machine** - not the Virtual Machine you have set up.

### Kubernetes CLI (kubectl)

kubectl is the command-line tool for interacting with Kubernetes clusters.

[Installation Documentation](https://kubernetes.io/docs/tasks/tools/)

### Helm

Helm is the package manager for Kubernetes that helps deploy and manage applications.

[Installation Documentation](https://helm.sh/docs/intro/install/)

### Git

Git is required for version control and downloading the project repository.

#### Git Installation

1. **Update package index**:
   ```bash
   sudo apt-get update
   ```

2. **Install Git**:
   ```bash
   sudo apt-get install -y git
   ```

3. **Verify installation**:
   ```bash
   git --version
   ```

4. **Configure Git** (optional but recommended):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

5. **Clone the project repository**:
   ```bash
   git clone git@github.com:Lom209/pt-k8s.git ~/
   cd ~/pt-k8s
   ```

   Note: To use SSH for cloning, ensure you have set up SSH keys with your GitHub account. If you haven't, you can follow [GitHub's guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to create and add SSH keys.

   Alternatively, you can use HTTPS to clone:
   ```bash
   git clone https://github.com/Lom209/pt-k8s.git ~/
   cd ~/pt-k8s
   ```

### K9s

K9s is a terminal-based UI to interact with your Kubernetes clusters. It makes it easier to navigate, observe and manage your applications.

#### K9s Installation

1. **Download the latest release**:
   ```bash
   curl -sS https://webinstall.dev/k9s | bash
   ```

   Alternatively, you can use Homebrew if installed:
   ```bash
   brew install k9s
   ```

2. **Verify installation**:
   ```bash
   k9s version
   ```

### Docker

Docker is a platform for developing, shipping, and running containerised applications.

[Docker Overview](https://docs.docker.com/get-started/docker-overview/)

#### Docker Installation for Linux/WSL2

1. **Update package index**:
   ```bash
   sudo apt-get update
   ```

2. **Install dependencies**:
   ```bash
   sudo apt-get install -y ca-certificates curl gnupg
   ```

3. **Add Docker's official GPG key**:
   ```bash
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   ```

4. **Configure Docker repository**:
   ```bash
   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Install Docker Engine**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

6. **Verify installation**:
   ```bash
   sudo docker --version
   ```

### Python

Python is required for various scripts and automation tasks in this project.

#### Python Installation

1. **Update package index**:
   ```bash
   sudo apt-get update
   ```

2. **Install Python and pip**:
   ```bash
   sudo apt-get install -y python3 python3-pip
   ```

3. **Verify installation**:
   ```bash
   python3 --version
   pip3 --version
   ```


After installing all prerequisites, you can proceed with the cluster setup as outlined in the other documentation files:
[Setting Up Kubernetes on your Virtual Machine](./kubernetes-cluster-vm-setup.md)
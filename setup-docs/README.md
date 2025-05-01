# PT-K8S: Setup and Deployment Guide

![Setup](./images/pt-k8s-setup-guide.png)

This document provides detailed instructions for setting up and deploying the PT-K8S platform.

**NOTE: This guide will detail how to set up a dev environment - the cluster will be hosted on a VMWare VM locally on my dev machine (which is running WSL2 in Windows).
Other implementations (Cloud / Dedicated Server / Local Cluster Hosting / Powershell) may vary.

## Hardware Requirements

### Local Development Machine

Your local development machine is where you'll control the Kubernetes cluster and develop/interact with the penetration testing environment:

- **Operating System**: Linux or Windows with WSL2
- **CPU**: 4+ cores recommended (for running Docker and development tools)
- **RAM**: 8GB+ recommended
- **Storage**: 20GB+ available space for tools and project files
- **Network**: Stable internet connection

### Kubernetes VM Requirements

For the virtual machine that will host your Kubernetes cluster:

- **Operating System**: Linux distribution (Ubuntu Server recommended)
- **CPU**: 2+ CPU cores
- **RAM**: 4GB+ RAM
- **Storage**: 50GB+ storage
- **Virtualisation**: Running in VMware, VirtualBox, or Proxmox

### Production Environment (Optional)

For production deployments, consider these specifications:

- **CPU**: 8+ CPU cores
- **RAM**: 16GB+ RAM
- **Storage**: 100GB+ SSD storage
- **Network**: Proper network isolation
- **Deployment**: Dedicated server or VM

It is strongly recommended to run the cluster initialisation scripts from a dedicated virtual machine or server rather than directly on your workstation. This ensures proper isolation of the Kubernetes environment and prevents potential conflicts with existing services.

## Local / Main Development Machine Setup

Please refer to the [Local Dev Machine Setup](./local-dev-machine-setup.md) documentation for details on setting up your development environment.

## Setting Up Kubernetes on your Virtual Machine

Please refer to the [Setting Up Kubernetes on your Virtual Machine](./kubernetes-cluster-vm-setup.md) documentation for initialisation and local access to your cluster.



# PT-K8s: Kubernetes-Based Penetration Testing Platform

![PT-K8s Platform](./setup-docs/images/pt-k8s-overview.png)

A comprehensive platform for deploying and managing penetration testing environments in Kubernetes, featuring a containerised Kali Linux environment & monitoring stack.

## Table of Contents
- [Usage Screenshots](#usage-screenshots)
- [Setup Guide](#setup-guide)
- [Project Overview](#project-overview)
- [Cluster Components](#cluster-components)
  - [pt-main](#pt-main)
  - [Monitoring Stack](#monitoring-stack)
- [Network Architecture](#network-architecture)
- [Repository Structure](#repository-structure)
- [Use Cases](#use-cases)

## Usage Screenshots

[To see screenshots of tool / cluster usage for a better understanding of cluster management click here](./setup-docs/screenshots-of-usage.md)


## Setup Guide

For detailed setup and deployment instructions, please refer to the [Setup Guide](./setup-docs/README.md).

## Project Overview

PT-K8s provides a complete solution for running penetration testing workloads in Kubernetes environments. 
The project includes:

- **pt-main**: A containerised Kali Linux environment with pre-configured security tools
- **Monitoring stack**: Prometheus, Grafana, Loki, and Promtail for comprehensive monitoring and log aggregation
- **Kubernetes configurations & deployment scripts**: Application / Infrastructure management (from deploy -> maintenance) 
- **KSAK (Kubernetes Swiss Army Knife)**: A CLI tool for managing Kubernetes resources and interacting with pods

This platform enables security professionals to:
- Deploy isolated, scalable, containerised penetration testing environments with minimal intervention.
- Connect securely to target networks via VPN
- Extensive resource (applications, services, networking) management with ease due to nature of Kubernetes
- Pentest against targets from any host OS
- Monitor resource usage and collect logs from penetration testing activities (including predefined dashboards for k8s metrics)

## Cluster Components

### pt-main

A containerised penetration testing environment based on Kali Linux with:
- Pre-installed security tools (nmap, metasploit, etc.)
- VPN connectivity for secure penetration testing
- SOCKS proxy functionality (uses include ability to port forward local browser traffic via the cluster w/Burp Suite - passing through the VPN connected pt-main pod)
- SSH access for remote management 

[More details in the pt-main README](./pt-main/README.md)

### Monitoring Stack

A comprehensive monitoring solution for the platform:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboarding with pre-configured PT-K8s dashboards
- **Loki**: Log aggregation system designed for Kubernetes
- **Promtail**: Log collection agent to ship logs to Loki

[More details in the Monitoring README](./k8s/monitoring/README.md)

## Network Architecture

For simplicity - only the pt-main pod is displayed within the K3s cluster.

```
┌─────────────────────────────────────────────────────────────┐
│                  Local Development Machine                  |
|                                                             |
│        ┌───────────────────────┐   ┌───────────────┐        │
│        │ kubectl / k9s / ksak  │   │  Helm / Bash  │        │
│        └───────────────────────┘   └───────────────┘        │
│                    |                       |                │
│                    │                       │                │
└────────────────────┼───────────────────────┼────────────────┘
                     │                       │
         management  │                       │  deployment
                     │                       │ 
                     └───────────────────────┘
                                 │
                                 │ .kubeconfig provides local dev -> cluster access
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Ubuntu Server VM                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                        K3s Cluster                         │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │                     pt-main Pod                      │  │  │
│  │  │                                                      │  │  │
│  │  │   ┌────────────────┐      ┌───────────────────────┐  │  │  │
│  │  │   │ Kali Container │      │   Tools & Utilities   │  │  │  │
│  │  │   └────────────────┘      └───────────────────────┘  │  │  │
│  │  │                                                      │  │  │
│  │  │   ┌────────────────┐      ┌───────────────────────┐  │  │  │
│  │  │   │  SOCKS Proxy   │◄────►│     VPN Connection    │  │  │  │
│  │  │   └────────────────┘      └───────────────────────┘  │  │  │
│  │  │           │                           │              │  │  │
│  │  └───────────┼───────────────────────────┼──────────────┘  │  │
│  │              │                           │                 │  │
│  └──────────────┼───────────────────────────┼─────────────────┘  │
│                 │                           │                    │
│                 ▼                           ▼                    │
│        ┌─────────────────┐       ┌─────────────────────┐         │
│        │ Local Services  │       │  Target Networks    │         │ 
│        │ (Port Forward)  │       │  (HackTheBox, etc.) │         │
│        └─────────────────┘       └─────────────────────┘         │
|                                                                  |
└──────────────────────────────────────────────────────────────────┘
```

## Repository Structure

```
pt-k8s/
├── k8s/                           # Kubernetes configuration files
│   ├── k3s.kubeconfig              # k3s cluster configuration
│   ├── monitoring/                 # Monitoring stack resources
│   │   ├── README.md                  # Monitoring documentation
│   │   ├── helm/                      # Helm chart for monitoring
│   │   │   ├── Chart.lock                 # Helm dependencies lock file
│   │   │   ├── Chart.yaml                 # Helm chart metadata
│   │   │   ├── values.yaml                # Configurable values for monitoring
│   │   │   ├── charts/                    # Packaged dependency charts
│   │   │   │   ├── kube-prometheus-stack-49.1.0.tgz  # Prometheus & Grafana
│   │   │   │   ├── loki-5.8.0.tgz                    # Log aggregation
│   │   │   │   └── promtail-6.15.0.tgz               # Log collection agent
│   │   │   └── templates/                 # Helm templates
│   │   └── scripts/                   # Deployment scripts
│   │       └── deploy-monitoring.sh       # Script to deploy monitoring stack
│   └── pt-main/                    # pt-main Kubernetes resources
│       ├── helm/                       # Helm chart for pt-main
│       │   ├── Chart.yaml                  # Helm chart metadata
│       │   ├── values.yaml                 # Configurable values for deployment
│       │   └── templates/                  # Helm templates
│       │       ├── deployment.yaml             # Deployment template
│       │       └── service.yaml                # Service template
│       └── scripts/                    # Deployment scripts
│           └── deploy-pt-main.sh           # Script to deploy pt-main with Helm
├── ksak/                          # Kubernetes Swiss Army Knife tool
│   ├── k3s.kubeconfig              # Configuration for KSAK
│   ├── ksak.py                     # Main KSAK application
│   ├── README.md                   # KSAK documentation
│   └── functions/                  # KSAK modules
│       ├── file_retriever.py           # Pod file system navigation
│       ├── port_forward.py             # Service port forwarding
├── pt-main/                       # Containerised penetration testing environment
│   ├── README.md                   # pt-main documentation
│   ├── docker/                     # Docker configuration
│   │   └── Dockerfile                   # Kali Linux container definition
│   ├── scripts/                    # Utility scripts
│   │   ├── proxy-startup.sh            # SOCKS proxy configuration
│   │   └── pt-commands.py              # Penetration testing command helper
│   └── vpn/                        # VPN configurations
│       └── htb.ovpn                    # HackTheBox VPN configuration
├── setup-docs/                    # Setup documentation
│   ├── README.md                   # Main setup guide
│   ├── local-dev-machine-setup.md  # Local machine setup instructions
│   ├── kubernetes-cluster-vm-setup.md  # VM and K8s setup instructions
│   └── images/                     # Documentation images
│       ├── pt-k8s-kubernetes-vm-setup.png
│       ├── pt-k8s-local-dev-machine-setup.png
│       ├── pt-k8s-overview.png
│       ├── pt-k8s-pt-main.png
│       └── pt-k8s-setup-guide.png
└── transfers/                     # Directory for file transfers from pods
```
## Use Cases

- **Security Assessments**: Deploy isolated environments for security testing
- **Training and Education**: Provide secure, isolated penetration testing labs
- **Red Team Operations**: Manage penetration testing infrastructure
- **Home Lab**: Deployable & customisable monitoring Home Lab
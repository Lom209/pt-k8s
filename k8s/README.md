# PT-K8s: Kubernetes Resources and Deployments

![Kubernetes Resources](../setup-docs/images/pt-k8s-overview.png)

This directory contains all Kubernetes deployment resources, configurations, and helper scripts for the PT-K8s platform.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Components](#components)
  - [pt-main](#pt-main)
  - [Monitoring Stack](#monitoring-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)

## Overview

The `k8s` directory houses all Kubernetes-related resources needed to deploy and manage the PT-K8s platform components. This includes Helm charts, configuration files, deployment scripts, and monitoring resources. These resources are designed to be deployed on a K3s cluster running on a virtual machine.

## Directory Structure

```
k8s/
├── k3s.kubeconfig           # K3s cluster configuration file
├── monitoring/              # Monitoring stack resources
│   ├── README.md            # Monitoring documentation
│   ├── dashboards/          # Grafana dashboard configurations
│   │   └── pt-main-dashboard.json  # Main PT-K8s dashboard
│   ├── helm/                # Helm chart for the monitoring stack
│   │   ├── Chart.lock       # Helm dependencies lock file
│   │   ├── Chart.yaml       # Helm chart metadata
│   │   ├── values.yaml      # Configurable values for monitoring
│   │   ├── charts/          # Packaged dependency charts
│   │   │   ├── kube-prometheus-stack-49.1.0.tgz  # Prometheus & Grafana
│   │   │   ├── loki-5.8.0.tgz                    # Log aggregation
│   │   │   └── promtail-6.15.0.tgz               # Log collection agent
│   │   └── templates/       # Helm templates
│   └── scripts/             # Deployment scripts
│       └── deploy-monitoring.sh  # Script to deploy monitoring stack
└── pt-main/                 # pt-main Kubernetes resources
    ├── helm/                # Helm chart for pt-main
    │   ├── Chart.yaml       # Helm chart metadata
    │   ├── values.yaml      # Configurable values for deployment
    │   └── templates/       # Helm templates
    │       ├── deployment.yaml  # Deployment template
    │       └── service.yaml     # Service template
    └── scripts/             # Deployment scripts
        └── deploy-pt-main.sh    # Script to deploy pt-main
```

## Components

### pt-main

The pt-main component is the core penetration testing pod based on Kali Linux. It provides:

- Containerised Kali Linux with pre-installed security tools
- VPN connectivity for secure target engagement
- SOCKS proxy functionality for web traffic routing
- SSH access for remote management

For more details, see the [pt-main documentation](../pt-main/README.md).

## Deployment Steps

Refer to [pt-main deployment steps](../setup-docs/pt-main-deployment.md).

### Monitoring Stack

The monitoring stack provides comprehensive observability for the PT-K8s platform through:

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualisation and dashboards
- **Loki**: Log aggregation
- **Promtail**: Log collection agent

Custom dashboards for PT-K8s are available in the `monitoring/dashboards/` directory.

For more details, see the [monitoring stack documentation](../k8s/monitoring/README.md).

## Deployment Steps

Refer to [Monitoring stack deployment](../setup-docs/monitoring-stack-deployment.md).
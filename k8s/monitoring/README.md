# PT-K8s Monitoring Stack

![Monitoring-Stack](../../setup-docs/images/pt-k8s-monitoring-stack.png)

This directory contains the Helm chart and deployment scripts for the PT-K8s monitoring stack, which provides comprehensive observability for your Kubernetes-based penetration testing platform.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Components](#components)
  - [Prometheus](#prometheus)
  - [Grafana](#grafana)
  - [Loki](#loki)
  - [Promtail](#promtail)
- [Deployment](#deployment)

## Overview

The monitoring stack provides comprehensive monitoring, metrics collection, and log aggregation for the PT-K8s platform. It helps track resource usage, performance metrics, and logs from your penetration testing environments, enabling better operational visibility and troubleshooting capabilities.

## Directory Structure

```
monitoring/
├── README.md                 # This file
├── dashboards/              # Grafana dashboard configurations
│   └── pt-main-dashboard.json  # Main PT-K8s dashboard
├── helm/                    # Helm chart for the monitoring stack
│   ├── Chart.lock           # Helm dependencies lock file
│   ├── Chart.yaml           # Helm chart metadata
│   ├── values.yaml          # Configurable values for monitoring
│   ├── charts/              # Packaged dependency charts
│   │   ├── kube-prometheus-stack-49.1.0.tgz  # Prometheus & Grafana
│   │   ├── loki-5.8.0.tgz                    # Log aggregation
│   │   └── promtail-6.15.0.tgz               # Log collection agent
│   └── templates/           # Helm templates
└── scripts/                 # Deployment scripts
    ├── deploy-monitoring.sh      # Script to deploy monitoring stack
    └── monitoring-stack-deployment.md  # Detailed deployment guide
```

## Components

### Prometheus
- **Purpose**: Time-series metrics collection and alerting
- **Deployment**: Deployed as part of the kube-prometheus-stack Helm chart
- **Features**:
  - Metrics collection from Kubernetes components and applications
  - Alerting rules and notification capabilities
  - Long-term metrics storage with configurable retention (currently 10 days)
  - Resource limits configured for compatibility with smaller clusters

### Grafana
- **Purpose**: Metrics visualization and dashboarding
- **Deployment**: Deployed as part of the kube-prometheus-stack Helm chart
- **Features**:
  - Pre-configured PT-K8s dashboard for monitoring the pt-main pods
  - Memory and CPU usage metrics for penetration testing activities
  - Persistent storage for dashboards and settings (10Gi)
  - Default login: username `admin`, password `ptk8sadmin`

### Loki
- **Purpose**: Log aggregation system optimized for Kubernetes
- **Deployment**: Deployed via the Loki Helm chart
- **Features**:
  - Centralized log collection and querying
  - Configured for single-node deployments with anti-affinity rules disabled
  - Integration with Grafana for unified monitoring experience
  - Persistent storage for log data (10Gi)

### Promtail
- **Purpose**: Log collection agent
- **Deployment**: Deployed via the Promtail Helm chart
- **Features**:
  - Collects and forwards logs from all pods to Loki
  - Runs as a DaemonSet to ensure logs are collected from all nodes
  - Automatic relabeling and structuring of log data

## Deployment Steps

Refer to [Monitoring Stack Deployment Steps](../../setup-docs/monitoring-stack-deployment.md).
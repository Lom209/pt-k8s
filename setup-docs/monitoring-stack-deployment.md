# PT-K8s Monitoring Stack Deployment

![Monitoring-Stack](./images/pt-k8s-monitoring-stack.png)

This document contains the steps to deploy the PT-K8s monitoring stack in your Kubernetes cluster.
For more information on the Monitoring Stack see monitoring-stack-deployment.md

## Prerequisites

Before deploying the monitoring stack, ensure you have the following requirements:

- A running Kubernetes cluster
- `kubectl` configured to access your cluster
- `helm` installed on your local machine
- The kubeconfig file at the expected location (`k8s/k3s.kubeconfig`)

## Configuration

Deployment of the monitoring stack is managed through Helm charts, which define the Kubernetes resources needed. The deployment can be customized through the `k8s/monitoring/helm/values.yaml` file.

Key configuration options include:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `grafana.adminPassword` | Admin password for Grafana | `ptk8sadmin` |
| `prometheus.retention` | Data retention period | `10d` |
| `loki.persistence.size` | Storage size for Loki | `10Gi` |
| `grafana.persistence.size` | Storage size for Grafana | `10Gi` |

## Deployment Steps

1. **Execute deploy-monitoring.sh**

   To deploy the monitoring stack, run the deployment script from the project root directory:

   ```bash
   ./k8s/monitoring/scripts/deploy-monitoring.sh
   ```

   **What the script does:**
   - Checks for required tools (kubectl, helm)
   - Adds necessary Helm repositories if they don't exist
   - Builds Helm dependencies
   - Creates a monitoring namespace if it doesn't exist
   - Installs or upgrades the Helm release
   - Waits for all monitoring pods to become ready
   - Displays deployment information including pod status, service details, and access methods

2. **Verify Deployment**

   After deployment, you can verify the status with:

   ```bash
   kubectl get pods -n monitoring
   kubectl get svc -n monitoring
   helm status pt-monitoring -n monitoring
   ```

## Accessing the Monitoring Stack

You can access the monitoring components using port-forwarding:

### Grafana
```bash
kubectl port-forward svc/pt-loki-grafana 3000:80 -n monitoring --address 0.0.0.0
```
- **URL**: http://localhost:3000
- **Default Credentials**: admin / ptk8sadmin

### Prometheus
```bash
kubectl port-forward svc/pt-kube-prometheus-stack-prometheus 9090:9090 -n monitoring --address 0.0.0.0
```
- **URL**: http://localhost:9090

### Loki (for debugging)
```bash
kubectl port-forward svc/pt-loki 3100:3100 -n monitoring --address 0.0.0.0
```
- **URL**: http://localhost:3100

## Dashboard Overview

The default PT-K8s dashboard provides the following metrics and visualizations:

- **PT-Main Memory Usage**: Real-time and historical memory consumption by pt-main pods
- **PT-Main CPU Usage**: CPU utilisation metrics for penetration testing activities
- **PT-Main Network Traffic**: Bandwidth utilization by pt-main pods
- **PT-Main Pod Status**: Current running status of all pt-main pods
- **PT-Main Disk Usage**: Storage usage metrics for pt-main pods
- **PT-Main Process Count**: Number of running processes in pt-main containers
- **PT-Main Logs**: Consolidated logs from all pt-main pods
- **PT-Main VPN/SSH/Proxy Logs**: Filtered logs related to connectivity services

## Next Steps

After successfully deploying the Monitoring stack, proceed to the how to manage the cluster once deployed steps:
[How to manage Cluster post deployment](./how-to-manage-cluster-once-deployed.md)
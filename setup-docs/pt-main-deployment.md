# PT-K8s: PT-MAIN Deployment

![PT-Main-Deploy](./images/pt-k8s-deploy-guide.png)

This document contains the steps to take to deploy a pt-main instance into your Kubernetes cluster.

## Prerequisites

Before deploying PT-MAIN, ensure you have the following requirements:

- A running Kubernetes cluster
- `kubectl` configured to access your cluster
- `helm` installed on your local machine
- `docker` installed for building the container image
- The kubeconfig file at the expected location (`k8s/k3s.kubeconfig`)

## Configuration

Deployment of pt-main is managed through Helm charts, which define the Kubernetes resources needed (deployments, services, etc.). 
The deployment can be customised through the `k8s/pt-main/helm/values.yaml` directory.

The values you need to change prior to deployment are:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `image.repository` | Docker repository for the PT-MAIN image | `lomeow/pt-main` |
| `image.tag` | Image tag for the PT-MAIN container | `latest` |


## Deployment Steps

## Execute deploy-pt-main.sh

   To deploy PT-MAIN, run the deployment script from the project root directory:

   ```bash
   ./k8s/pt-main/scripts/deploy-pt-main.sh -u <username> [IMAGE_TAG]
   ```

   **Command Arguments:**
   - `-u, --username <USERNAME>`: **(Required)** Specify the username for the container
     - Must contain only letters, numbers, and underscores
   - `IMAGE_TAG` (optional): Specify a custom image tag in the format `repository:tag` 
     - Example: `lomeow/pt-main:v1.2.3`
     - If not provided, the default `lomeow/pt-main:latest` will be used

   **Example:**
   ```bash
   ~/pt-k8s/k8s/pt-main/scripts/deploy-pt-main.sh -u hacker lomeow/pt-main:v1.2.3
   ```

   **What the script does:**
   - Checks for required tools (docker, kubectl, helm)
   - Verifies if the specified Docker image exists locally
     - If the image doesn't exist, it will build it with the specified username
     - If the image exists, it will ask if you want to rebuild it with the specified username
   - Deploys or upgrades the Helm chart with the specified image
   - Waits for the pod to become ready
   - Displays deployment information including pod status, service details, and Helm release status

   You can view usage information with:
   ```bash
   ~/pt-k8s/k8s/pt-main/scripts/deploy-pt-main.sh --help
   ```

2. **Verify Deployment**

   After deployment, you can verify the status with:

   ```bash
   kubectl get pods -l app=pt-main
   kubectl get svc pt-main-service
   helm status pt-main
   ```

## Accessing PT-MAIN

You can access PT-MAIN using the exposed NodePorts:

- SSH: `ssh -p 30022 <username>@<node-ip>`
- SOCKS Proxy: Configure your application to use `<node-ip>:31080` as a SOCKS proxy

Alternatively, you can use port-forwarding for easier access:

```bash
kubectl port-forward svc/pt-main-service 1080:1080 --address 0.0.0.0
kubectl port-forward svc/pt-main-service 2222:22 --address 0.0.0.0
```

## Security Considerations

PT-MAIN runs with elevated privileges and capabilities:
- NET_ADMIN, NET_RAW, and SYS_ADMIN capabilities
- Privileged container mode

This is necessary for VPN connectivity and network tools but should be considered when deploying in shared environments.

## Data Persistence

By default, PT-MAIN mounts a host directory (`/tmp/pt-main-data`) to the container path (`/home/main/data`). Ensure this directory exists on your Kubernetes nodes and has appropriate permissions.

## Next Steps

After successfully deploying pt-main, proceed to the deployment of the monitoring stack as detailed here:
[Monitoring Stack Overview](../k8s/monitoring/README.md)
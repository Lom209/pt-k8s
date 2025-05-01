# Managing Your Kubernetes Cluster

![Cluster-Management](./images/pt-k8s-overview.png)

This document provides guidance on managing your Kubernetes cluster after it has been successfully deployed. It covers common kubectl commands and includes a detailed guide to using k9s, a powerful terminal-based UI for Kubernetes.

## Usage Screenshots

[To see screenshots of tool / cluster usage for a better understanding of cluster management click here](./screenshots-of-usage.md)

## Prerequisites

- A running Kubernetes cluster (k3s)
- kubectl installed on your local machine
- k9s installed on your local machine
- Access to the kubeconfig file

## Key Management Features with k9s

k9s (https://k9scli.io/) is a terminal-based UI that dramatically simplifies Kubernetes cluster management.

### 1. Pod Management

k9s makes it easy to manage pods with these powerful features:

- **Real-time Pod Monitoring**: View all pods across namespaces with real-time status updates
- **One-Key Pod Deletion**: Press `Ctrl+d` to instantly delete pods that need to be restarted
- **Watch Self-Healing in Action**: Delete a pod and watch in real-time as Kubernetes recreates it
- **Container Shell Access**: Press `s` to instantly get a shell inside any container
- **Log Streaming**: Press `l` to view live-streaming logs from any pod
- **Multiple Container Support**: Easily switch between containers in multi-container pods

```bash
# Start k9s and immediately view pods
k9s --command pods
```

### 2. Resource Management Across Namespaces

k9s provides powerful namespace navigation and cross-namespace visibility:

- **Quick Namespace Switching**: Use numeric keys (0-9) to switch between namespaces
- **View All Namespaces**: Press `0` to view resources across all namespaces
- **Namespace Filtering**: Type `:namespace <name>` to filter to a specific namespace
- **Custom Resource Views**: Create custom resource views filtered by namespace

```bash
# Start k9s in a specific namespace
k9s --namespace monitoring
```

### 3. Complete Cluster Visibility

Gain instant visibility into all aspects of your cluster:

- **Resource Navigation**: Easily navigate between different resource types
- **Real-time Updates**: All views update in real-time showing current cluster state
- **Resource Usage Metrics**: View CPU and memory usage across pods and nodes
- **Event Monitoring**: View cluster events to diagnose issues quickly
- **Logs Aggregation**: View logs across multiple pods simultaneously

```bash
# View all available resources in your cluster
# In k9s: press ':' then type 'alias' and press Enter
```

### 4. Interactive Debugging Tools

Debug issues directly from the k9s interface:

- **Describe Resources**: Press `d` to view detailed descriptions of any resource
- **YAML Editing**: Press `e` to edit resources directly in your terminal
- **Port Forwarding**: Press `Shift+f` to set up port forwarding to any pod or service
- **Container Exec**: Press `s` to execute commands in containers
- **Resource Scaling**: Scale deployments up or down directly from the interface

```bash
# Find pods in a CrashLoopBackOff state
# In k9s: press '/' then type 'status:CrashLoop' and press Enter
```

### k9s Keyboard Shortcuts Reference

| Action                      | Shortcut      | Description                              |
|----------------------------|---------------|------------------------------------------|
| Open command mode          | `:`           | Enter commands like `:pod`, `:deploy`    |
| Go back/Cancel             | `Esc`         | Return to previous view or cancel action |
| View all resources         | `Ctrl+a`      | Show all available resource types        |
| Switch namespace (by index)| `0-9`         | Quickly switch between namespaces        |
| Filter resources           | `/`           | Filter resources in current view         |
| View resource logs         | `l`           | View logs for selected pod               |
| Shell into container       | `s`           | Open shell in selected container         |
| Describe resource          | `d`           | Show detailed description of resource    |
| Delete resource            | `Ctrl+d`      | Delete the selected resource             |
| Edit resource              | `e`           | Edit the selected resource               |
| Port forward               | `Shift+f`     | Set up port forwarding                   |
| View YAML                  | `y`           | View resource YAML                        |
| Help menu                  | `?`           | Open the help menu                        |
| Kill/delete pod            | `Ctrl+k`      | Kill the selected pod                     |
| Restart pod                | `r`           | Restart the selected pod                  |
| Toggle wide view           | `w`           | Toggle wide view with additional details  |
| Copy resource name         | `c`           | Copy resource name to clipboard           |

## Common k9s Use Cases

### 1. Troubleshooting a Failing Pod

```
1. Start k9s
2. Type `:pods` (or just press Enter as pods is the default view)
3. Use `/` to filter for the failing pod name or status
4. Select the pod and press `l` to view logs
5. Press `d` to describe the pod and check events
6. If needed, press `s` to shell into the container to debug
7. If you need to restart, press `Ctrl+d` to delete the pod and let it recreate
```

### 2. Monitoring Deployment Updates

```
1. Start k9s
2. Type `:deploy` to view deployments
3. Find your deployment being updated
4. Press `d` to describe and view update status
5. Press `l` to watch logs during the update
6. Press `0` to view resources across all namespaces and watch new pods come up
```

### 3. Debugging Service Connectivity Issues

```
1. Start k9s
2. Type `:svc` to view services
3. Select the service having issues
4. Press `d` to describe and check endpoints
5. Type `:endpoints` to check endpoint details
6. Type `:pods` and filter for the service's selector labels to check backing pods
7. Use `Shift+f` to set up port-forwarding and test directly
```

## Using kubectl to Manage Your Cluster

kubectl is the command-line tool for interacting with Kubernetes clusters. Below are common commands that you'll use for cluster management.

### Essential kubectl Commands

#### Cluster Information

```bash
# Check cluster info
kubectl cluster-info

# View nodes in the cluster
kubectl get nodes

# Get detailed information about a specific node
kubectl describe node <node-name>

# Check cluster status
kubectl get componentstatuses
```

#### Working with Namespaces

```bash
# List all namespaces
kubectl get namespaces

# Create a namespace
kubectl create namespace <namespace-name>

# Set the default namespace for kubectl commands
kubectl config set-context --current --namespace=<namespace-name>

# View resources in a specific namespace
kubectl get <resource-type> -n <namespace-name>
```

#### Pod Management

```bash
# List all pods
kubectl get pods --all-namespaces

# List pods in a specific namespace
kubectl get pods -n <namespace-name>

# Get detailed information about a specific pod
kubectl describe pod <pod-name> -n <namespace-name>

# View pod logs
kubectl logs <pod-name> -n <namespace-name>

# View logs for a specific container in a multi-container pod
kubectl logs <pod-name> -c <container-name> -n <namespace-name>

# Execute a command in a pod
kubectl exec -it <pod-name> -n <namespace-name> -- <command>

# Delete a pod
kubectl delete pod <pod-name> -n <namespace-name>
```

#### Deployment Management

```bash
# List all deployments
kubectl get deployments --all-namespaces

# Get details about a specific deployment
kubectl describe deployment <deployment-name> -n <namespace-name>

# Scale a deployment
kubectl scale deployment <deployment-name> --replicas=<number> -n <namespace-name>

# Update a deployment image
kubectl set image deployment/<deployment-name> <container-name>=<new-image> -n <namespace-name>

# Rollout status of a deployment
kubectl rollout status deployment/<deployment-name> -n <namespace-name>

# Rollback a deployment
kubectl rollout undo deployment/<deployment-name> -n <namespace-name>
```


#### Port Forwarding

```bash
# Forward a local port to a port on a pod
kubectl port-forward <pod-name> <local-port>:<pod-port> -n <namespace-name>

# Forward a local port to a service
kubectl port-forward svc/<service-name> <local-port>:<service-port> -n <namespace-name>
```

#### ConfigMaps and Secrets

```bash
# List configmaps
kubectl get configmaps -n <namespace-name>

# Create a configmap from a file
kubectl create configmap <configmap-name> --from-file=<path-to-file> -n <namespace-name>

# List secrets
kubectl get secrets -n <namespace-name>

# Create a secret
kubectl create secret generic <secret-name> --from-literal=<key>=<value> -n <namespace-name>
```

#### Resource Monitoring

```bash
# Show resource usage for nodes
kubectl top nodes

# Show resource usage for pods
kubectl top pods --all-namespaces

# Show resource usage for pods in a specific namespace
kubectl top pods -n <namespace-name>
```
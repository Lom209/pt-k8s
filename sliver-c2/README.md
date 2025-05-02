# PT-K8s: Sliver C2 Integration with PT-Main

![PT-K8s Integration](../setup-docs/images/pt-k8s-overview.png)

This document explains how to integrate the Sliver Command & Control (C2) server with the PT-Main pod, allowing you to control your Sliver C2 server directly from within your penetration testing environment.

## Overview

The Sliver C2 integration enables a streamlined workflow for penetration testers by:

- Allowing direct control of the Sliver C2 server from within the PT-Main pod
- Enabling secure communication between the PT-Main pod and the Sliver C2 server
- Simplifying management of implants and C2 infrastructure during engagements

## Prerequisites

- A running Kubernetes cluster with the PT-K8s platform deployed
- Both PT-Main and Sliver-C2 pods deployed and running
- kubectl access to the cluster

## Integration Steps

### 1. Deploy both the PT-Main and Sliver C2 pods

If you haven't already done so, deploy both components using their respective deployment scripts:

```bash
# Deploy PT-Main (replace 'your_username' with your preferred username)
./k8s/pt-main/scripts/deploy-pt-main.sh -u your_username

# Deploy Sliver C2
./k8s/sliver-c2/scripts/deploy-sliver-c2.sh
```

### 2. Install the Sliver client in PT-Main

Once both pods are running, you need to install the Sliver client in the PT-Main pod:

```bash
# Get the name of your PT-Main pod
kubectl get pods -l app=pt-main

# Install the Sliver client in the PT-Main pod
kubectl exec -it $(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- bash -c 'curl -sSL https://sliver.sh/install | bash'
```

### 3. Generate a client configuration on the Sliver server and transfer it to PT-Main

This creates secure MTLS authentication credentials for PT-Main to connect to the Sliver server:

```bash
# Get the Sliver C2 pod name and service IP
SLIVER_POD_NAME=$(kubectl get pods -l app=sliver-c2 -o jsonpath='{.items[0].metadata.name}')
SLIVER_SERVICE_IP=$(kubectl get svc sliver-c2 -o jsonpath='{.spec.clusterIP}')

# Create a new operator configuration
kubectl exec -it $SLIVER_POD_NAME -- sliver-server operator --name pt-main-operator --lhost $SLIVER_SERVICE_IP

# Copy the configuration from the Sliver server to your local machine
kubectl cp $SLIVER_POD_NAME:/root/.sliver/pt-main-operator.cfg ./pt-main-operator.cfg

# Copy the configuration from your local machine to the PT-Main pod
PT_MAIN_POD=$(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}')
PT_MAIN_USER=$(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].env[?(@.name=="USERNAME")].value}')
kubectl cp ./pt-main-operator.cfg $PT_MAIN_POD:/home/$PT_MAIN_USER/pt-main-operator.cfg
```

### 4. Connect from PT-Main to Sliver C2

Access the PT-Main pod and connect to the Sliver C2 server:

```bash
# Access the PT-Main pod
kubectl exec -it $(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- bash

# Inside the PT-Main pod, you can use the convenience script:
sliver-connect

# Or directly start the Sliver client:
sliver --config pt-main-operator.cfg
```

## Using the Sliver C2 Server

Once connected to the Sliver C2 server from PT-Main, you can use the following basic commands:

- `help` - Show available commands
- `sessions` - List active sessions (live connections from implants)
- `beacons` - List active beacons (intermittently connecting implants)
- `implants` - List available implants
- `generate` - Generate new implants for various platforms
- `use <session>` - Interact with a session
- `jobs` - List and manage jobs running on the server

## Generating Implants for Target Systems

To generate an implant for a target system:

```bash
# Inside the Sliver client on PT-Main
generate --os windows --arch amd64 --format exe --save /home/username/implants/

# Or for a more covert implant as shellcode:
generate --os linux --arch amd64 --format shellcode --save /home/username/implants/
```

## Security Considerations

- The Sliver C2 operator configuration file contains sensitive credentials - protect it appropriately
- Sliver C2 communications are encrypted, but ensure your Kubernetes network policies are appropriately configured
- Consider using namespaces and network policies to further isolate the C2 infrastructure

## Troubleshooting

If you encounter issues connecting to the Sliver C2 server:

1. Verify both pods are running:
   ```bash
   kubectl get pods -l app=pt-main
   kubectl get pods -l app=sliver-c2
   ```

2. Check network connectivity:
   ```bash
   # From PT-Main to Sliver C2
   kubectl exec -it $(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- curl -v <sliver-service-ip>:80
   ```

3. Verify the Sliver client is installed correctly:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- which sliver
   ```

4. Check the operator config file exists and has correct permissions:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- ls -la ~/pt-main-operator.cfg
   ```
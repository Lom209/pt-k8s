# Setting Up Kubernetes on your Virtual Machine

![Kubernetes-Setup](./images/pt-k8s-kubernetes-vm-setup.png)

This document outlines the steps required to set up a Kubernetes cluster on your virtual machine. Follow these instructions sequentially to ensure proper configuration.

## Prerequisites

- A virtual machine with a Linux distribution installed
- Administrative (sudo) privileges on the target machine
- Basic familiarity with command-line operations

## K3s Cluster Setup

K3s is a lightweight Kubernetes distribution designed for resource-constrained environments. Follow these steps to initialise a K3s cluster:

## Commands to be ran on Virtual Machine where K3s cluster will be hosted

### 1. Retrieve the VM's IP Address and make a note of it

This commands will display the IP address of your server. Look for the `inet` entry under the relevant network interface (e.g., `eth0` or `enp0s3`).
Take note of the IP address (it will be in the format like `192.168.x.x` or `10.x.x.x`).

```bash
ip addr show
```

### 2. SSH onto your Virtual Machine from your local IDE / Terminal
```bash
ssh USERNAME@IPADDRESS
```

### 3. Update apt & upgrade packages

```bash
sudo apt update && sudo apt upgrade
```

### 4. Create the Initialisation Script

Execute the following command to create the `k3s-init.sh` initialisation script:

```bash
cat << 'EOF' > k3s-init.sh
#!/bin/bash

# Path to kube directory for a user-accessible copy of the kubeconfig
# K3s will still create its main config at /etc/rancher/k3s/k3s.yaml
KUBE_DIR="$HOME/.kube/config"
KUBE_CONFIG="$KUBE_DIR/k3s.kubeconfig"
mkdir -p "$KUBE_DIR"

# Configuration
K3S_VERSION="v1.27.1+k3s1" # Specify the version of k3s to install
INSTALL_K3S_EXEC="--write-kubeconfig-mode 644 --write-kubeconfig=$KUBE_CONFIG"

# Update and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl

# Install k3s
# This will create the primary kubeconfig at /etc/rancher/k3s/k3s.yaml
# and also write a copy to the location specified by --write-kubeconfig
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=$K3S_VERSION sh -s - $INSTALL_K3S_EXEC

# Verify installation
k3s --version
sudo kubectl get nodes -o wide
sudo kubectl get pods -A

# Note: K3s writes its kubeconfig to two locations:
# 1. Default location: /etc/rancher/k3s/k3s.yaml (requires sudo to access)
# 2. Custom location: $KUBE_CONFIG (user-accessible as specified above)
EOF
```

### 5. Execute the Initialisation Script

Make the script executable and run it:

```bash
chmod +x k3s-init.sh && ./k3s-init.sh
```
You should see something like this:

```bash
lom@pt-control:~$ sudo kubectl get nodes -o wide
NAME         STATUS   ROLES                  AGE   VERSION        INTERNAL-IP       EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
pt-control   Ready    control-plane,master   40s   v1.27.1+k3s1   xxx.xxx.xxx.xxx   <none>        Ubuntu 24.04.2 LTS   6.8.0-58-generic   containerd://1.6.19-k3s1
lom@pt-control:~$ sudo kubectl get pods -A
NAMESPACE     NAME                                     READY   STATUS              RESTARTS     AGE
kube-system   coredns-77ccd57875-ps7dv                 1/1     Running             0            34s
kube-system   local-path-provisioner-957fdf8bc-shxx6   1/1     Running             0            34s
kube-system   helm-install-traefik-9qm67               1/1     Running             1 (5s ago)   35s
kube-system   traefik-84745cf649-47lsh                 0/1     ContainerCreating   0            2s
kube-system   metrics-server-54dc485875-2td69          1/1     Running             0            34s
kube-system   svclb-traefik-cb0c7afe-clxn8             0/2     ContainerCreating   0            2s
kube-system   helm-install-traefik-crd-ttv7k           0/1     Completed           0            35s
```

## Commands to be ran on Local Development Machine / Workstation

### 1. Retrieve the Kubeconfig File from your Local Development Machine

Now that your K3s cluster is running, you'll need to copy the kubeconfig file to your local development machine. 
From your local development machine, **replacing the values** - run:

```bash
# Replace VM_USER with your VM username and VM_IP with the VM's IP address from step 4
# Replace the path to which you want to save your .kubeconfig
scp VM_USER@VM_IP:~/.kube/config/k3s.kubeconfig ~/pt-k8s/k8s/k3s.kubeconfig && \
cp ~/pt-k8s/k8s/k3s.kubeconfig ~/pt-k8s/ksak/k3s.kubeconfig
```

### 2. Update the Kubeconfig with the VM's IP Address

The .kubeconfig file might contain `localhost` or `127.0.0.1` as the server address, which won't work from your local dev machine. 
Open the retrieved kubeconfig file on your local dev / main machine and update the server URL
**replace the xx.xx.xx.xx with the IP you retrieved earlier**:

`server: https://localhost:6443` -> `server: https://xx.xx.xx.xx:6443`

### 3. Verify Connection from Local Machine

Test that you can connect to your K3s cluster from your local development machine:

```bash
export KUBECONFIG=~/pt-k8s/k8s/k3s.kubeconfig
kubectl get nodes
```

If successful, you'll see the list of nodes in your K3s cluster like so:
```bash
me0w@DESKTOP-5JKN8MB:~/dev/pt-k8s/k8s$ kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
pt-control   Ready    control-plane,master   24m   v1.27.1+k3s1
```

## Next Steps

After successfully setting up your K3s cluster and configuring local access, proceed to the deployment of pt-main as detailed here:
[pt-main Overview](../pt-main/README.md)


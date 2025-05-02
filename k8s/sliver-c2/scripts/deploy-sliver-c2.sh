#!/bin/bash

# Sliver C2 Server Deployment Script with Docker Hub Repository
# This script builds, pushes to Docker Hub, and deploys the Sliver C2 server

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
HELM_DIR="$(dirname "$SCRIPT_DIR")/helm"
DOCKER_DIR="$REPO_ROOT/sliver-c2/docker"

# Display script header
echo "==================================================================="
echo "           Sliver C2 Server Build and Deploy Script                "
echo "==================================================================="

# Check for required tools
for cmd in docker kubectl helm; do
  if ! command -v $cmd &> /dev/null; then
    echo "Error: $cmd is required but not installed."
    exit 1
  fi
done

# Build Docker image
echo "[+] Building sliver C2 Docker image..."
docker build -t lomeow/sliver-c2:latest $DOCKER_DIR

# Push to Docker Hub (you should be logged in with docker login)
echo "[+] Pushing image to Docker Hub as lomeow/sliver-c2:latest..."
docker push lomeow/sliver-c2:latest

# Update the values.yaml file to use your Docker Hub repo
echo "[+] Updating Helm values to use Docker Hub image..."
sed -i 's#repository: .*#repository: lomeow/sliver-c2#' $HELM_DIR/values.yaml

# Deploy with Helm
echo "[+] Deploying sliver C2 server with Helm..."
helm upgrade --install sliver-c2 $HELM_DIR

echo "[+] Deployment complete! sliver C2 server should be available soon."
echo "[+] To check the status, run: kubectl get pods -l app=sliver-c2"
echo "[+] To access logs, run: kubectl logs -l app=sliver-c2"

# Get the cluster IP for internal access from pt-main
SLIVER_SERVICE_IP=$(kubectl get svc sliver-c2 -o jsonpath='{.spec.clusterIP}')
SLIVER_POD_NAME=$(kubectl get pods -l app=sliver-c2 -o jsonpath='{.items[0].metadata.name}')

# Provide information for connecting from pt-main
echo ""
echo "==================================================================="
echo "            PT-MAIN Integration Information                        "
echo "==================================================================="
echo "[+] To access the Sliver C2 server from pt-main:"
echo "    - Sliver C2 Service ClusterIP: $SLIVER_SERVICE_IP"
echo ""
echo "[+] From pt-main pod, you can connect to Sliver using:"
echo "    - MTLS: $SLIVER_SERVICE_IP:31337"
echo "    - HTTP: http://$SLIVER_SERVICE_IP:80"
echo "    - HTTPS: https://$SLIVER_SERVICE_IP:443"
echo ""
echo "[+] To install the Sliver client in pt-main, run:"
echo "    kubectl exec -it \$(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}') -- bash -c 'curl -sSL https://sliver.sh/install | bash'"
echo ""
echo "[+] To generate a client config and copy it into pt-main:"
echo "    kubectl exec -it $SLIVER_POD_NAME -- sliver-server operator --name pt-main-operator --lhost $SLIVER_SERVICE_IP"
echo "    kubectl cp $SLIVER_POD_NAME:/root/.sliver/pt-main-operator.cfg ./pt-main-operator.cfg"
echo "    kubectl cp ./pt-main-operator.cfg \$(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].metadata.name}'):/home/\$(kubectl get pod -l app=pt-main -o jsonpath='{.items[0].env[?(@.name==\"USERNAME\")].value}')/pt-main-operator.cfg"
echo ""
echo "[+] Then from inside the pt-main pod, start the Sliver client with:"
echo "    sliver --config pt-main-operator.cfg"
echo "==================================================================="

# Show available endpoints
echo "[+] Once running, sliver C2 should be available externally at:"
echo "    - HTTP: http://<server-IP>:30080"
echo "    - HTTPS: https://<server-IP>:30443"
echo "    - MTLS: <server-IP>:31337"
echo "    - DNS: <server-IP>:30053 (UDP)"
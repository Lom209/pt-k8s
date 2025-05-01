#!/bin/bash

# deploy-monitoring.sh
# Script to deploy the monitoring stack (Prometheus, Grafana, Loki) using Helm

# Path to project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HELM_CHART_DIR="${PROJECT_ROOT}/helm"
KUBE_CONFIG="${PROJECT_ROOT}/../../k8s/k3s.kubeconfig"

# Set default Kubernetes context
if [ -f "$KUBE_CONFIG" ]; then
  export KUBECONFIG="$KUBE_CONFIG"
  echo "Using kubeconfig: $KUBE_CONFIG"
else
  echo "Warning: Default kubeconfig not found at $KUBE_CONFIG"
  echo "Using current kubeconfig: $KUBECONFIG"
fi

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required tools
check_requirements() {
  echo -e "${BLUE}Checking for required tools...${NC}"
  
  local missing_tools=()
  
  if ! command_exists kubectl; then
    missing_tools+=("kubectl")
  fi
  
  if ! command_exists helm; then
    missing_tools+=("helm")
  fi
  
  if [ ${#missing_tools[@]} -ne 0 ]; then
    echo -e "${RED}Error: The following required tools are missing:${NC}"
    for tool in "${missing_tools[@]}"; do
      echo "  - $tool"
    done
    echo -e "${YELLOW}Please install the missing tools and try again.${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}All required tools are installed.${NC}"
}

# Build Helm dependencies
build_helm_dependencies() {
  echo -e "\n${BLUE}Building Helm dependencies...${NC}"
  
  # Navigate to the Helm chart directory
  if [ ! -d "$HELM_CHART_DIR" ]; then
    echo -e "${RED}Error: Helm chart directory not found at $HELM_CHART_DIR${NC}"
    exit 1
  fi
  
  echo -e "${YELLOW}Running helm dependency build...${NC}"
  if helm dependency build "$HELM_CHART_DIR"; then
    echo -e "${GREEN}Helm dependencies built successfully.${NC}"
  else
    echo -e "${RED}Error: Failed to build Helm dependencies.${NC}"
    echo -e "${YELLOW}Checking if dependencies can be updated...${NC}"
    # Try to update dependencies if the build fails
    if helm dependency update "$HELM_CHART_DIR"; then
      echo -e "${GREEN}Helm dependencies updated successfully.${NC}"
    else
      echo -e "${RED}Error: Failed to update Helm dependencies.${NC}"
      exit 1
    fi
  fi
}

# Add Helm repositories if they don't exist
add_helm_repos() {
  echo -e "\n${BLUE}Adding required Helm repositories...${NC}"
  
  # Add Prometheus community repo
  if ! helm repo list | grep -q "prometheus-community"; then
    echo -e "${YELLOW}Adding prometheus-community repository...${NC}"
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  else
    echo -e "${GREEN}prometheus-community repository already exists.${NC}"
  fi
  
  # Add Grafana repo
  if ! helm repo list | grep -q "grafana"; then
    echo -e "${YELLOW}Adding grafana repository...${NC}"
    helm repo add grafana https://grafana.github.io/helm-charts
  else
    echo -e "${GREEN}grafana repository already exists.${NC}"
  fi
  
  # Update repositories
  echo -e "${YELLOW}Updating Helm repositories...${NC}"
  helm repo update
}

# Function to deploy using Helm
deploy_with_helm() {
  echo -e "\n${BLUE}Deploying monitoring stack with Helm...${NC}"
  
  # Check if Helm chart directory exists
  if [ ! -d "$HELM_CHART_DIR" ]; then
    echo -e "${RED}Error: Helm chart directory not found at $HELM_CHART_DIR${NC}"
    exit 1
  fi
  
  # Check if kubectl and helm are configured correctly
  if ! kubectl get nodes >/dev/null 2>&1; then
    echo -e "${RED}Error: kubectl is not configured correctly or cannot connect to the cluster.${NC}"
    echo -e "${YELLOW}Make sure your Kubernetes cluster is running and kubectl is properly configured.${NC}"
    exit 1
  fi
  
  # Create monitoring namespace if it doesn't exist
  if ! kubectl get namespace monitoring >/dev/null 2>&1; then
    echo -e "${YELLOW}Creating monitoring namespace...${NC}"
    kubectl create namespace monitoring
    if [ $? -ne 0 ]; then
      echo -e "${RED}Error: Failed to create monitoring namespace.${NC}"
      exit 1
    fi
  else
    echo -e "${GREEN}Monitoring namespace already exists.${NC}"
  fi
  
  # Check if release exists
  if helm list -n monitoring | grep -q "pt-monitoring"; then
    echo -e "${YELLOW}Upgrading existing Helm release...${NC}"
    if helm upgrade pt-monitoring "$HELM_CHART_DIR" -n monitoring; then
      echo -e "${GREEN}Helm upgrade completed successfully.${NC}"
    else
      echo -e "${RED}Error: Failed to upgrade Helm release.${NC}"
      exit 1
    fi
  else
    echo -e "${YELLOW}Installing new Helm release...${NC}"
    if helm install pt-monitoring "$HELM_CHART_DIR" -n monitoring; then
      echo -e "${GREEN}Helm installation completed successfully.${NC}"
    else
      echo -e "${RED}Error: Failed to install Helm release.${NC}"
      exit 1
    fi
  fi
}

# Function to wait for pods to be ready
wait_for_pods_ready() {
  echo -e "\n${BLUE}Waiting for monitoring pods to be ready...${NC}"
  
  local timeout=600  # 10 minutes timeout
  local interval=10  # check every 10 seconds
  local elapsed=0
  
  while [ $elapsed -lt $timeout ]; do
    local grafana_ready=$(kubectl get pods -n monitoring -l "app.kubernetes.io/name=grafana" -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' | grep -c "True")
    local prometheus_ready=$(kubectl get pods -n monitoring -l "app=prometheus" -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' | grep -c "True")
    local loki_ready=$(kubectl get pods -n monitoring -l "app=loki" -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' | grep -c "True")
    
    if [[ $grafana_ready -gt 0 && $prometheus_ready -gt 0 && $loki_ready -gt 0 ]]; then
      echo -e "${GREEN}All monitoring pods are ready!${NC}"
      return 0
    fi
    
    echo -e "${YELLOW}Waiting for pods to be ready... ($elapsed seconds elapsed)${NC}"
    sleep $interval
    elapsed=$((elapsed + interval))
  done
  
  echo -e "${RED}Timeout waiting for pods to be ready.${NC}"
  return 1
}

# Function to display deployment information
display_deployment_info() {
  echo -e "\n${BLUE}Monitoring Stack Deployment Information:${NC}"
  
  # Get pod info
  echo -e "\n${YELLOW}Pod information:${NC}"
  kubectl get pods -n monitoring
  
  # Get service info
  echo -e "\n${YELLOW}Service information:${NC}"
  kubectl get svc -n monitoring
  
  # Display helm status
  echo -e "\n${YELLOW}Helm release status:${NC}"
  helm status pt-monitoring -n monitoring
  
  # Get Grafana service info
  local grafana_svc=$(kubectl get svc -n monitoring -l "app.kubernetes.io/name=grafana" -o name | head -n 1)
  if [ -n "$grafana_svc" ]; then
    local grafana_svc_name=${grafana_svc#service/}
    echo -e "\n${YELLOW}Access Grafana dashboard:${NC}"
    echo -e "kubectl port-forward -n monitoring svc/$grafana_svc_name 3000:80 --address 0.0.0.0"
    echo -e "Then open http://localhost:3000 in your browser"
    echo -e "Default credentials: admin / ptk8sadmin"
  fi
  
  # Get Prometheus service info
  local prometheus_svc=$(kubectl get svc -n monitoring -l "app=prometheus" -o name | head -n 1)
  if [ -n "$prometheus_svc" ]; then
    local prometheus_svc_name=${prometheus_svc#service/}
    echo -e "\n${YELLOW}Access Prometheus UI:${NC}"
    echo -e "kubectl port-forward -n monitoring svc/$prometheus_svc_name 9090:9090 --address 0.0.0.0"
    echo -e "Then open http://localhost:9090 in your browser"
  fi
}

# Main function
main() {
  echo -e "${BOLD}${GREEN}=== PT-K8s Monitoring Stack Deployment ===${NC}"
  echo -e "This script will deploy Prometheus, Grafana, and Loki monitoring stack using Helm."
  
  # Check for required tools
  check_requirements
  
  # Add Helm repositories
  add_helm_repos
  
  # Build Helm dependencies
  build_helm_dependencies
  
  # Deploy with Helm
  deploy_with_helm
  
  # Wait for pods to be ready
  wait_for_pods_ready
  
  # Display deployment information
  display_deployment_info
  
  echo -e "\n${GREEN}PT-K8s Monitoring Stack deployment completed successfully!${NC}"
}

# Run the main function
main
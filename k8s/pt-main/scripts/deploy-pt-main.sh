#!/bin/bash

# deploy-pt-main.sh
# Script to deploy the pt-main penetration testing environment using Helm

# Default image to use if not specified
DEFAULT_IMAGE="lomeow/pt-main:latest"
DEFAULT_USERNAME="lom"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -u|--username)
      USERNAME="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS] [IMAGE_TAG]"
      echo "Options:"
      echo "  -u, --username USERNAME   Specify the username for the container (required)"
      echo "  -h, --help                Show this help message"
      echo ""
      echo "Example: $0 -u hacker lomeow/pt-main:v1.2.3"
      echo "If IMAGE_TAG is not provided, default \"$DEFAULT_IMAGE\" will be used."
      exit 0
      ;;
    *)
      IMAGE_TAG="$1"
      shift
      ;;
  esac
done

# Check if username is provided
if [ -z "$USERNAME" ]; then
  echo -e "${RED}Error: Username is required. Use -u or --username to specify.${NC}"
  echo "Example: $0 -u hacker [IMAGE_TAG]"
  exit 1
fi

# Validate username (alphanumeric and underscores only)
if ! [[ $USERNAME =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo -e "${RED}Error: Username must contain only letters, numbers, and underscores.${NC}"
  exit 1
fi

# Set image tag if not provided
if [ -z "$IMAGE_TAG" ]; then
  echo "No image tag provided. Using default: $DEFAULT_IMAGE"
  IMAGE_TAG="$DEFAULT_IMAGE"
fi

# Path to project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_DIR="${PROJECT_ROOT}/../../pt-main/docker"
HELM_CHART_DIR="${PROJECT_ROOT}/helm"
KUBE_CONFIG="${PROJECT_ROOT}/../k8s/k3s.kubeconfig"

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
  
  if ! command_exists docker; then
    missing_tools+=("docker")
  fi
  
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

# Function to build the Docker image
build_docker_image() {
  echo -e "\n${BLUE}Building Docker image...${NC}"
  
  # Check if Dockerfile exists
  if [ ! -f "${DOCKER_DIR}/Dockerfile" ]; then
    echo -e "${RED}Error: Dockerfile not found at ${DOCKER_DIR}/Dockerfile${NC}"
    exit 1
  fi
  
  # Navigate to the pt-main directory (parent of docker dir)
  cd "${DOCKER_DIR}/.." || { echo -e "${RED}Error: Could not navigate to ${DOCKER_DIR}/..${NC}"; exit 1; }
  
  # Build the Docker image with username argument
  echo -e "${YELLOW}Building image ${IMAGE_TAG} with username: ${USERNAME}...${NC}"
  if docker build --build-arg USERNAME="${USERNAME}" -t "$IMAGE_TAG" -f docker/Dockerfile .; then
    echo -e "${GREEN}Docker image built successfully with username: ${USERNAME}.${NC}"
  else
    echo -e "${RED}Error: Failed to build Docker image.${NC}"
    exit 1
  fi
}

# Function to check if image is available in local Docker registry
check_image_exists() {
  if docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
    return 0  # Image exists
  else
    return 1  # Image does not exist
  fi
}

# Function to deploy using Helm
deploy_with_helm() {
  echo -e "\n${BLUE}Deploying with Helm...${NC}"
  
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
  
  # Check if release exists
  if helm list | grep -q "pt-main"; then
    echo -e "${YELLOW}Upgrading existing Helm release...${NC}"
    if helm upgrade pt-main "$HELM_CHART_DIR" --set image.repository="$(echo $IMAGE_TAG | cut -d':' -f1)" --set image.tag="$(echo $IMAGE_TAG | cut -d':' -f2)"; then
      echo -e "${GREEN}Helm upgrade completed successfully.${NC}"
    else
      echo -e "${RED}Error: Failed to upgrade Helm release.${NC}"
      exit 1
    fi
  else
    echo -e "${YELLOW}Installing new Helm release...${NC}"
    if helm install pt-main "$HELM_CHART_DIR" --set image.repository="$(echo $IMAGE_TAG | cut -d':' -f1)" --set image.tag="$(echo $IMAGE_TAG | cut -d':' -f2)"; then
      echo -e "${GREEN}Helm installation completed successfully.${NC}"
    else
      echo -e "${RED}Error: Failed to install Helm release.${NC}"
      exit 1
    fi
  fi
}

# Function to wait for pod to be ready
wait_for_pod_ready() {
  echo -e "\n${BLUE}Waiting for pt-main pod to be ready...${NC}"
  
  local timeout=300  # 5 minutes timeout
  local interval=5   # check every 5 seconds
  local elapsed=0
  
  while [ $elapsed -lt $timeout ]; do
    if kubectl get pods -l app=pt-main -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' | grep -q "True"; then
      echo -e "${GREEN}Pod is ready!${NC}"
      return 0
    fi
    
    echo -e "${YELLOW}Waiting for pod to be ready... ($elapsed seconds elapsed)${NC}"
    sleep $interval
    elapsed=$((elapsed + interval))
  done
  
  echo -e "${RED}Timeout waiting for pod to be ready.${NC}"
  return 1
}

# Function to display pod and service information
display_deployment_info() {
  echo -e "\n${BLUE}Deployment Information:${NC}"
  
  # Get pod info
  echo -e "\n${YELLOW}Pod information:${NC}"
  kubectl get pods -l app=pt-main -o wide
  
  # Get service info
  echo -e "\n${YELLOW}Service information:${NC}"
  kubectl get svc pt-main-service
  
  # Display helm status
  echo -e "\n${YELLOW}Helm release status:${NC}"
  helm status pt-main
  
  # Display the deployed image
  echo -e "\n${YELLOW}Deployed image:${NC}"
  echo -e "$IMAGE_TAG"
  
  # Also display the username that was used
  echo -e "\n${YELLOW}Container username:${NC}"
  echo -e "$USERNAME"
  
  # Display port-forward commands
  echo -e "\n${YELLOW}Port-forwarding for easier access:${NC}"
  echo -e "kubectl port-forward svc/pt-main-service 1080:1080 --address 0.0.0.0"
  echo -e "kubectl port-forward svc/pt-main-service 2222:22 --address 0.0.0.0"
}

# Main function
main() {
  echo -e "${BOLD}${GREEN}=== PT-main Helm Deployment ===${NC}"
  echo -e "This script will deploy the pt-main penetration testing environment using Helm."
  echo -e "Using image: ${IMAGE_TAG}"
  echo -e "Using username: ${USERNAME}"
  
  # Check for required tools
  check_requirements
  
  # Check if Docker image exists, build if it doesn't
  if check_image_exists; then
    echo -e "${GREEN}Docker image ${IMAGE_TAG} already exists.${NC}"
    echo -e "${YELLOW}Do you want to rebuild the Docker image with username '${USERNAME}'? (y/n)${NC}"
    read -r rebuild_image
    
    if [[ $rebuild_image == "y" || $rebuild_image == "Y" ]]; then
      build_docker_image
    fi
  else
    build_docker_image
  fi
  
  # Deploy with Helm
  deploy_with_helm
  
  # Wait for pod to be ready
  wait_for_pod_ready
  
  # Display deployment information
  display_deployment_info
  
  echo -e "\n${GREEN}PT-main deployment with Helm completed successfully!${NC}"
}

# Run the main function
main

"""
File retrieval functionality for ksak.
"""

from kubernetes import client, config
import subprocess
import os
import json

def get_all_pods():
    """Get a list of all pods in the cluster."""
    try:
        # Get the script directory to find the kubeconfig file
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        kubeconfig_path = os.path.join(script_dir, 'k3s.kubeconfig')
        
        # Load Kubernetes configuration from explicit file path
        if os.path.isfile(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            # Fall back to default loading method
            config.load_kube_config()

        # Get the pods
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces()
        
        # Create a list of pod names with namespaces
        pod_list = []
        for pod in pods.items:
            pod_list.append(f"{pod.metadata.namespace}/{pod.metadata.name}")
        
        return pod_list
    except Exception as e:
        print(f"Error listing pods: {e}")
        return []

def get_pod_containers(pod_with_namespace):
    """Get a list of containers in a pod."""
    try:
        # Get the script directory to find the kubeconfig file
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        kubeconfig_path = os.path.join(script_dir, 'k3s.kubeconfig')
        
        # Load Kubernetes configuration from explicit file path
        if os.path.isfile(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            # Fall back to default loading method
            config.load_kube_config()

        # Parse the namespace and pod name
        namespace, pod_name = pod_with_namespace.split('/')
        
        # Get the pod details
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(pod_name, namespace)
        
        # Get container names
        container_list = []
        for container in pod.spec.containers:
            container_list.append(container.name)
        
        return container_list
    except Exception as e:
        print(f"Error listing containers: {e}")
        return []

def list_pod_files(pod_with_namespace, container_name, path='/'):
    """List files in a directory on a pod."""
    try:
        # Parse the namespace and pod name
        namespace, pod_name = pod_with_namespace.split('/')
        
        # Run ls command on the pod
        command = [
            "kubectl", "exec", "-n", namespace, pod_name, "-c", container_name, 
            "--", "ls", "-la", path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error listing files: {result.stderr}")
            return []
        
        # Parse the output and extract file names
        files = []
        for line in result.stdout.splitlines()[1:]:  # Skip the first line (total)
            parts = line.split()
            if len(parts) >= 9:
                file_name = ' '.join(parts[8:])
                is_dir = parts[0].startswith('d')
                files.append({"name": file_name, "is_dir": is_dir})
        
        return files
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def suggest_save_path(file_name):
    """Suggest a save path for a file."""
    # Current directory as default
    base_dir = os.getcwd()
    return os.path.join(base_dir, file_name)

def retrieve_file(pod_with_namespace, container_name, file_path, save_path):
    """Retrieve a file from a Kubernetes pod."""
    try:
        # Get the script directory to find the kubeconfig file
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        kubeconfig_path = os.path.join(script_dir, 'k3s.kubeconfig')
        
        # Load Kubernetes configuration from explicit file path
        if os.path.isfile(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            # Fall back to default loading method
            config.load_kube_config()

        # Parse the namespace and pod name
        namespace, pod_name = pod_with_namespace.split('/')

        # Run the kubectl cp command
        command = [
            "kubectl", "cp", 
            f"{namespace}/{pod_name}:{file_path}", 
            save_path, 
            "-c", container_name
        ]
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error copying file: {result.stderr}")
            return False
        
        return True

    except Exception as e:
        print(f"Error during file retrieval: {e}")
        return False
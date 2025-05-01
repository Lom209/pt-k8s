"""
Port-forwarding functionality for ksak.
"""

from kubernetes import client, config
import subprocess
import os

def get_all_services():
    """Get a list of all services in the cluster."""
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

        # Get the services
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces()
        
        # Create a list of service names with namespaces
        service_list = []
        for svc in services.items:
            service_list.append(f"{svc.metadata.namespace}/{svc.metadata.name}")
        
        return service_list
    except Exception as e:
        print(f"Error listing services: {e}")
        return []

def get_service_ports(service_with_namespace):
    """Get the ports exposed by a service."""
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

        # Parse the namespace and service name
        namespace, service_name = service_with_namespace.split('/')
        
        # Get the service details
        v1 = client.CoreV1Api()
        service = v1.read_namespaced_service(service_name, namespace)
        
        # Get port information
        port_list = []
        for port in service.spec.ports:
            port_info = {
                "port": port.port,
                "target_port": port.target_port,
                "name": port.name if hasattr(port, "name") else None,
                "protocol": port.protocol if hasattr(port, "protocol") else "TCP"
            }
            port_list.append(port_info)
        
        return port_list
    except Exception as e:
        print(f"Error getting service ports: {e}")
        return []

def suggest_local_ports(remote_ports):
    """Suggest available local ports to use."""
    # Simply use the same port numbers for now, but could be made smarter
    return [p["port"] for p in remote_ports]

def port_forward(service_with_namespace, local_port, remote_port):
    """Port-forward a Kubernetes service."""
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

        # Parse the namespace and service name
        namespace, service_name = service_with_namespace.split('/')

        # Run the port-forward command
        command = [
            "kubectl", "port-forward", 
            f"svc/{service_name}", 
            f"{local_port}:{remote_port}", 
            "-n", namespace
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command)

    except Exception as e:
        print(f"Error during port-forwarding: {e}")
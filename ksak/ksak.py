#!/usr/bin/env python3
"""
Kubernetes Swiss Army Knife (ksak)
A one-stop shop for Kubernetes cluster management.
"""

import sys
import os
from simple_term_menu import TerminalMenu
from kubernetes import client, config
from functions.port_forward import port_forward, get_all_services, get_service_ports
from functions.file_retriever import (
    retrieve_file, get_all_pods, get_pod_containers, list_pod_files, suggest_save_path
)



def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_numeric_input(prompt, min_value=None, max_value=None):
    """Get numeric input with validation."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def list_services_menu():
    """Display list services menu."""
    clear_screen()
    print("\nListing services...\n")
    
    services = get_all_services()
    if not services:
        print("No services found or error occurred while listing services.")
    else:
        print("Available services:")
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
    
    input("\nPress Enter to continue...")


def port_forward_menu():
    """Display port-forward menu and handle input with interactive selection."""
    clear_screen()
    print("\nPort-Forward Service\n")
    
    # Step 1: Get list of services and select one
    services = get_all_services()
    if not services:
        print("No services found or error occurred while listing services.")
        input("\nPress Enter to continue...")
        return
    
    # Display services for selection
    print("Select a service to port-forward:")
    terminal_menu = TerminalMenu(services, title="Available Services:")
    service_index = terminal_menu.show()
    
    if service_index is None:
        print("Operation cancelled.")
        input("\nPress Enter to continue...")
        return
    
    selected_service = services[service_index]
    
    # Step 2: Get available ports for the selected service
    remote_ports = get_service_ports(selected_service)
    if not remote_ports:
        print(f"No ports found for service {selected_service} or error occurred.")
        input("\nPress Enter to continue...")
        return
    
    # Display port options
    port_options = []
    for port_info in remote_ports:
        port_name = f"{port_info['port']}"
        if port_info['name']:
            port_name += f" ({port_info['name']})"
        port_name += f" → {port_info['target_port']} {port_info['protocol']}"
        port_options.append(port_name)
    
    print("Select a port to forward:")
    terminal_menu = TerminalMenu(port_options, title=f"Ports on {selected_service}:")
    port_index = terminal_menu.show()
    
    if port_index is None:
        print("Operation cancelled.")
        input("\nPress Enter to continue...")
        return
    
    selected_remote_port = remote_ports[port_index]['port']
    
    # Step 3: Get suggested local ports (default is same as remote port)
    suggested_port = selected_remote_port
    
    print(f"\nEnter local port [default: {suggested_port}]: ")
    local_port_input = input()
    if not local_port_input:
        local_port = suggested_port
    else:
        try:
            local_port = int(local_port_input)
            if local_port < 1 or local_port > 65535:
                print("Port must be between 1 and 65535. Using default port.")
                local_port = suggested_port
        except ValueError:
            print("Invalid port number. Using default port.")
            local_port = suggested_port
    
    # Step 4: Start port-forwarding
    clear_screen()
    print(f"\nPort-forwarding service {selected_service}")
    print(f"Remote port {selected_remote_port} → Local port {local_port}")
    print("Press Ctrl+C to stop port-forwarding\n")
    
    try:
        port_forward(selected_service, local_port, selected_remote_port)
    except KeyboardInterrupt:
        print("\nPort-forwarding cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPress Enter to continue...")


def retrieve_file_menu():
    """Display retrieve file menu and handle input with interactive selection."""
    clear_screen()
    print("\nRetrieve File from Pod\n")
    
    # Step 1: Select a pod from the list
    pods = get_all_pods()
    if not pods:
        print("No pods found or error occurred while listing pods.")
        input("\nPress Enter to continue...")
        return
    
    print("Select a pod:")
    terminal_menu = TerminalMenu(pods, title="Available Pods:")
    pod_index = terminal_menu.show()
    
    if pod_index is None:
        print("Operation cancelled.")
        input("\nPress Enter to continue...")
        return
    
    selected_pod = pods[pod_index]
    
    # Step 2: Select a container from the pod
    containers = get_pod_containers(selected_pod)
    if not containers:
        print(f"No containers found in pod {selected_pod} or error occurred.")
        input("\nPress Enter to continue...")
        return
    
    if len(containers) == 1:
        # If there's only one container, select it automatically
        selected_container = containers[0]
        print(f"Using the only container: {selected_container}")
    else:
        print("Select a container:")
        terminal_menu = TerminalMenu(containers, title=f"Containers in {selected_pod}:")
        container_index = terminal_menu.show()
        
        if container_index is None:
            print("Operation cancelled.")
            input("\nPress Enter to continue...")
            return
        
        selected_container = containers[container_index]
    
    # Step 3: Navigate file system and select a file
    current_path = "/"
    while True:
        clear_screen()
        print(f"\nNavigating: {selected_pod}, Container: {selected_container}")
        print(f"Current path: {current_path}")
        
        files = list_pod_files(selected_pod, selected_container, current_path)
        if not files:
            print("No files found or error listing files.")
            input("\nPress Enter to continue...")
            # Go back to parent directory if possible
            if current_path != "/":
                current_path = os.path.dirname(current_path)
                if current_path == "":
                    current_path = "/"
                continue
            else:
                return
        
        # Prepare display items for menu
        menu_items = []
        is_dir_list = []
        
        # Add parent directory option if not at root
        if current_path != "/":
            menu_items.append(".. (Parent Directory)")
            is_dir_list.append(True)
        
        # Add files and directories
        for file_info in files:
            display_name = file_info["name"]
            if file_info["is_dir"]:
                display_name += "/"
            menu_items.append(display_name)
            is_dir_list.append(file_info["is_dir"])
        
        # Add option to select current file
        menu_items.append("[ SELECT CURRENT PATH ]")
        is_dir_list.append(False)
        
        print("Select a file or directory:")
        terminal_menu = TerminalMenu(menu_items, title=f"Files in {current_path}:")
        file_index = terminal_menu.show()
        
        if file_index is None:
            print("Operation cancelled.")
            input("\nPress Enter to continue...")
            return
        
        # Handle parent directory
        if current_path != "/" and file_index == 0:
            current_path = os.path.dirname(current_path)
            if current_path == "":
                current_path = "/"
            continue
        
        # Adjust index to account for parent directory option
        if current_path != "/":
            adjusted_index = file_index - 1
        else:
            adjusted_index = file_index
        
        # Handle selection of current path
        if file_index == len(menu_items) - 1:
            selected_file_path = current_path
            break
        
        # Handle navigation or file selection
        if adjusted_index < len(files):
            selected_name = files[adjusted_index]["name"]
            is_dir = files[adjusted_index]["is_dir"]
            
            if is_dir:
                # Navigate to directory
                if current_path.endswith("/"):
                    current_path = current_path + selected_name
                else:
                    current_path = current_path + "/" + selected_name
            else:
                # Select file
                if current_path.endswith("/"):
                    selected_file_path = current_path + selected_name
                else:
                    selected_file_path = current_path + "/" + selected_name
                break
    
    # Step 4: Get save path (with a default suggestion)
    base_name = os.path.basename(selected_file_path)
    suggested_path = suggest_save_path(base_name)
    
    print(f"\nEnter local save path [default: {suggested_path}]: ")
    save_path = input()
    if not save_path:
        save_path = suggested_path
    
    # Step 5: Retrieve the file
    clear_screen()
    print(f"\nRetrieving {selected_file_path} from pod {selected_pod}, container {selected_container}...")
    
    try:
        success = retrieve_file(selected_pod, selected_container, selected_file_path, save_path)
        if success:
            print(f"\nFile saved to {save_path}")
        else:
            print("\nFile retrieval failed.")
    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPress Enter to continue...")


def main():
    """Main function to display the terminal UI and handle user interaction."""
    # Load Kubernetes configuration
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        kubeconfig_path = os.path.join(script_dir, 'k3s.kubeconfig')
        
        # Check if the kubeconfig file exists
        if os.path.isfile(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
            print(f"Using kubeconfig: {kubeconfig_path}")
        else:
            # Fall back to default loading method
            config.load_kube_config()
            print("Using default kubeconfig")
    except Exception as e:
        print(f"Error loading kubeconfig: {e}")
        sys.exit(1)
    
    while True:
        clear_screen()
        print("\nKubernetes Swiss Army Knife (ksak)")
        print("=================================\n")
        
        options = ["List Services", "Port-Forward Service", "Retrieve File from Pod", "Exit"]
        terminal_menu = TerminalMenu(options, title="Select an option:")
        menu_index = terminal_menu.show()
        
        if menu_index == 0:
            list_services_menu()
        elif menu_index == 1:
            port_forward_menu()
        elif menu_index == 2:
            retrieve_file_menu()
        elif menu_index == 3 or menu_index is None:
            clear_screen()
            print("Exiting KSAK. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nOperation cancelled by user. Exiting...")
        sys.exit(0)
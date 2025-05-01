# pt-main: Containerised Penetration Testing Environment

![Setup](../setup-docs/images/pt-k8s-pt-main.png)

A Kubernetes-deployed penetration testing environment based on Kali Linux with pre-configured tools, VPN connectivity, and SOCKS proxy capabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Components](#components)
  - [Docker Container](#docker-container)
- [Deployment](#deployment-steps)
- [Usage](#using-the-vpn-connection)
  - [Proxy Setup](#proxy-setup)
  - [Using the VPN Connection](#using-the-vpn-connection)
  - [Using the Penetration Testing Commands Tool](#using-the-penetration-testing-commands-tool)

## Project Overview

pt-main is a containerized penetration testing platform that:

- Runs a fully-featured Kali Linux environment in a container
- Supports VPN connectivity for secure penetration testing
- Provides SOCKS proxy functionality for routing traffic
- Deploys easily to Kubernetes environments (k3s, minikube)
- Includes a wide range of pre-installed penetration testing tools

## Directory Structure

```
pt-main/
├── docker/
│   └── Dockerfile                # Container definition with Kali Linux and security tools
├── scripts/
│   ├── proxy-startup.sh          # Script to initialize the SSH and SOCKS proxy
│   └── pt-commands.py            # Penetration testing command reference tool
└── vpn/
    └── htb.ovpn                  # OpenVPN configuration file (e.g., for HackTheBox)
```

## Components

### Docker Container

The Docker container is based on Kali Linux with numerous security tools pre-installed:

- Network tools: nmap, netcat, curl, wget
- Web application testing: dirb, sqlmap, gobuster
- Password cracking: hydra, john, hashcat
- Rust-based tools: rustscan, feroxbuster
- Metasploit framework
- And many more

The container also sets up:
- A non-root user (`main`) with sudo privileges
- SSH server for remote access and SOCKS proxy functionality
- TUN device for VPN connectivity

## Deployment Steps

Refer to [pt-main deployment steps](../setup-docs/pt-main-deployment.md).

## Usage

### Proxy Setup

The `proxy-startup.sh` script:
- Configures SSH server for internal SOCKS proxy functionality
- Sets up SSH keys for password-less local authentication
- Creates a SOCKS proxy on port 1080 for routing traffic
- Maintains the container in a running state

### Using the VPN Connection

To connect to a VPN (e.g., HackTheBox):

```bash
sudo -b openvpn --config /home/main/vpn/htb.ovpn
```

### Using the Penetration Testing Commands Tool

The `pt-commands.py` script provides a comprehensive reference of penetration testing commands categorized by:

- Reconnaissance
- Scanning
- Authentication Testing
- Injection Testing
- File Upload Testing
- API Testing
- CSRF Testing
- Privilege Escalation
- Tools & Frameworks

The script offers:
- Interactive menu for browsing commands
- Command customization with target host substitution
- Copy-to-clipboard functionality
- Command-line options for non-interactive usage


```bash
python3 /home/main/scripts/pt-commands.py --host target.example.com
```
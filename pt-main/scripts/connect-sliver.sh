#!/bin/bash
# Script to connect to Sliver C2 server from pt-main

# Check if Sliver client is installed
if ! command -v sliver &> /dev/null; then
    echo "[!] Sliver client not found. Installing..."
    curl -sSL https://sliver.sh/install | bash
    if [ $? -ne 0 ]; then
        echo "[!] Failed to install Sliver client"
        exit 1
    fi
fi

# Check if config file exists
CONFIG_FILE="$HOME/pt-main-operator.cfg"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[!] Configuration file not found at $CONFIG_FILE"
    echo "[!] You need to set up the operator config file first"
    echo "[!] See the integration guide for instructions"
    exit 1
fi

# Connect to Sliver C2 server
echo "[+] Connecting to Sliver C2 server..."
sliver --config "$CONFIG_FILE"
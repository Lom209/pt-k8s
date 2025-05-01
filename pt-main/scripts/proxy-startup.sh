#!/bin/bash

# Check if SSH server is already running
if pgrep sshd > /dev/null; then
  echo "SSH server is already running, no need to start it again"
else
  # Start SSH server with more verbose output
  echo "Starting SSH server..."
  sudo /usr/sbin/sshd
  echo "SSH server started"
fi

# Wait a moment for SSH to fully initialize
echo "Waiting for SSH service to initialize..."
sleep 2

# Generate SSH key for local authentication without password
echo "Setting up SSH key for local authentication..."
mkdir -p ~/.ssh
if [ ! -f ~/.ssh/id_rsa ]; then
  ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
else
  echo "SSH keys already exist, skipping generation"
fi

# Start the SOCKS proxy with verbose logging
echo "Starting SOCKS proxy on port 1080..."
ssh -v -N -D 0.0.0.0:1080 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null localhost > /tmp/ssh_proxy.log 2>&1 &
PROXY_PID=$!
echo "SOCKS proxy started with PID: $PROXY_PID"

# Verify the proxy is listening 
sleep 2
echo "Checking if proxy is listening on port 1080..."
if command -v ss > /dev/null; then
  ss -tulpn | grep 1080 || echo "Warning: Could not find service listening on port 1080"
elif command -v netstat > /dev/null; then
  netstat -tulpn | grep 1080 || echo "Warning: Could not find service listening on port 1080"
else
  # Alternative check if ss and netstat are not available
  if ps -p $PROXY_PID > /dev/null; then
    echo "Proxy process is running with PID: $PROXY_PID"
  else
    echo "Warning: Proxy process with PID $PROXY_PID is not running"
  fi
fi

echo "SSH server and SOCKS proxy setup completed!"
echo "You can check proxy logs with: cat /tmp/ssh_proxy.log"

# Keep container running
tail -f /dev/null
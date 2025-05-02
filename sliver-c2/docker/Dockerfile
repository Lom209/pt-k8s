FROM debian:bullseye-slim

# Install necessary tools and dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    wget \
    curl \
    nmap \
    iputils-ping \
    netcat-openbsd \
    vim \
    dnsutils \
    openssh-client \
    unzip \
    libncurses5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/sliver

# Download pre-built Sliver release (latest version)
RUN SLIVER_VERSION=$(curl -s https://api.github.com/repos/BishopFox/sliver/releases/latest | grep "tag_name" | cut -d '"' -f 4) && \
    SLIVER_URL="https://github.com/BishopFox/sliver/releases/download/${SLIVER_VERSION}/sliver-server_linux" && \
    curl -L -o sliver-server $SLIVER_URL && \
    chmod +x sliver-server && \
    SLIVER_CLIENT_URL="https://github.com/BishopFox/sliver/releases/download/${SLIVER_VERSION}/sliver-client_linux" && \
    curl -L -o sliver-client $SLIVER_CLIENT_URL && \
    chmod +x sliver-client

# Add to PATH
ENV PATH="/opt/sliver:${PATH}"

# Create a data directory for persistence
RUN mkdir -p /data
VOLUME ["/data"]

# Create directories for configuration
RUN mkdir -p /root/.sliver-client/configs /root/.sliver

# Expose ports
# Default HTTP/S C2 listener ports
EXPOSE 80
EXPOSE 443
# Default for Mtls listeners
EXPOSE 31337
# Default for DNS listener
EXPOSE 53/udp
# SSH server (for operator connection)
EXPOSE 22

# Set entrypoint
ENTRYPOINT ["/opt/sliver/sliver-server"]
CMD ["daemon"]
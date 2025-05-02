FROM kalilinux/kali-rolling

# Set default username as a build argument
ARG USERNAME=lom

# Update and install common tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    vim \
    openvpn \
    curl \
    wget \
    git \
    gnupg \
    software-properties-common \
    sudo \
    openssh-server \
    nmap \
    netcat-traditional \
    python3 \
    python3-pip \
    metasploit-framework \
    dirb \
    sqlmap \
    hydra \
    john \
    hashcat \
    gobuster \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the TUN device directory
RUN mkdir -p /dev/net && \
    mknod /dev/net/tun c 10 200 && \
    chmod 600 /dev/net/tun

# Install Rust and common Rust-based tools
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Rust pentesting tools
RUN cargo install rustscan feroxbuster

# Create non-root user based on build argument
RUN useradd -m -s /bin/bash ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}

# Set up SSH server for proxy capability
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "${USERNAME}:${USERNAME}" | chpasswd

# Create directory for VPN files and scripts
RUN mkdir -p /home/${USERNAME}/vpn /home/${USERNAME}/scripts

# Create bash aliases for user
RUN echo '\n\
# Pentesting aliases\n\
alias home="cd /home/'${USERNAME}'"\n\
alias ll="ls -lah"\n\
alias scripts="cd /home/'${USERNAME}'/scripts"\n\
alias ptcmd="python3 /home/'${USERNAME}'/scripts/pt-commands.py"\n\
alias start-proxy="sudo /home/'${USERNAME}'/scripts/proxy-startup.sh"\n\
alias start-vpn="sudo -b openvpn --config /home/'${USERNAME}'/vpn/htb.ovpn"\n\
alias sliver-connect="/home/'${USERNAME}'/scripts/connect-sliver.sh"\n\
' >> /home/${USERNAME}/.bashrc && \
    chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc

# Copy files from the host into the container
COPY vpn/* /home/${USERNAME}/vpn/
COPY scripts/* /home/${USERNAME}/scripts/
RUN chmod +x /home/${USERNAME}/scripts/*.sh && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# Switch to non-root user
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Expose SSH port for proxy
EXPOSE 22 1080

# Keep the container running
CMD ["sudo", "/usr/sbin/sshd", "-D"]
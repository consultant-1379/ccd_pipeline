FROM ubuntu:20.04

LABEL maintainer="Adam Gajak <zadagaj>"

# Install tzdata package non-interactively for Ubuntu
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get install tzdata -qy && \
    ln -fs /usr/share/zoneinfo/Europe/Dublin /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    echo "Europe/Dublin" > /etc/timezone && \
# Make sure the package repository is up to date
    apt-get -qy full-upgrade && \
    apt-get install -qy git && \
# Install a basic SSH server for Jenkins docker plugin
    apt-get install -qy openssh-server && \
    sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd && \
# Install JDK 8 for Jenkins docker plugin
    apt-get install -qy openjdk-11-jdk && \
# Install other tools
    apt-get install -qy python3-pip wget curl unzip tar gzip sshpass vim rsync jq

# Download kubectl and its checksum
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

# Verify the checksum
RUN echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl kubectl.sha256 

# Download and install the latest Helm 2
RUN curl -fsSL -o get_helm2.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get && \
    chmod +x get_helm2.sh && \
    ./get_helm2.sh && \
    rm get_helm2.sh

# Download and install the latest Helm 3
RUN curl -fsSL -o get_helm3.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod +x get_helm3.sh && \
    ./get_helm3.sh && \
    rm get_helm3.sh

# Install YQ package
RUN    curl -O -L https://github.com/mikefarah/yq/releases/download/3.3.0/yq_linux_amd64 && \
    chmod +x yq_linux_amd64 && \
    cp yq_linux_amd64 /usr/local/bin/yq && \
    rm yq_linux_amd64 && \
# Cleanup old packages
    apt-get -qy autoremove && \
# Add user jenkins to the image
    adduser --quiet lciadm100 && \
# Set password for the jenkins user
    echo "lciadm100:ericsson123" | chpasswd

COPY python3_modules.txt /root/python3_modules.txt

RUN /usr/bin/pip3 install -r /root/python3_modules.txt

RUN apt-get install -qy lftp

# Copy files to set up ssh for gerrit
RUN mkdir /home/lciadm100/.ssh
COPY config /home/lciadm100/.ssh/config
COPY id_rsa /home/lciadm100/.ssh/id_rsa
COPY id_rsa.pub /home/lciadm100/.ssh/id_rsa.pub

RUN chown lciadm100:lciadm100 /home/lciadm100/.ssh/id_rsa.pub /home/lciadm100/.ssh/id_rsa /home/lciadm100/.ssh/config /home/lciadm100/.ssh && \
    chmod 644 /home/lciadm100/.ssh/id_rsa.pub && \
    chmod 600 /home/lciadm100/.ssh/id_rsa && \
    chmod 700 /home/lciadm100/.ssh

USER lciadm100

# Install ansible community kubernetes module
RUN ansible-galaxy collection install community.kubernetes

# Install ansible community openstack cloud module
RUN ansible-galaxy collection install openstack.cloud

USER root

# Standard SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]


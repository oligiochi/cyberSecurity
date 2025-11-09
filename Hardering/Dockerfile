FROM debian:13.1-slim

RUN apt-get update && apt-get install -y openssh-server
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo 'root:root' | chpasswd

RUN mkdir -p /etc/ssh/sshd_config.d
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config.d/PermitRootLogin-custom.conf

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
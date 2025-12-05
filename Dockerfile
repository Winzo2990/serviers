FROM debian:12

# Install dependencies
RUN apt-get update && apt-get install -y curl wget tar openssl unzip

# Install PufferPanel
RUN wget https://github.com/PufferPanel/PufferPanel/releases/download/v2.7.5/pufferpanel-2.7.5-linux-amd64.tar.gz \
    && tar -xzf pufferpanel-2.6.0-linux-amd64.tar.gz \
    && mv pufferpanel /usr/local/bin/pufferpanel

# Create required folders
RUN mkdir -p /etc/pufferpanel /var/lib/pufferpanel

# Copy default config
RUN pufferpanel --config /etc/pufferpanel/config.json

# Expose port
EXPOSE 8080

# Run panel
CMD ["pufferpanel", "--config", "/etc/pufferpanel/config.json"]

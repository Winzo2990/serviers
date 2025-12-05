FROM debian:12

# Install dependencies
RUN apt-get update && apt-get install -y curl bash

# Download SSHX binary
RUN curl -sSf https://sshx.io/get | sh

# Railway will assign a port using $PORT
ENV PORT=8080
EXPOSE 8080

# Run sshx on Railway port
CMD ["/bin/bash", "-c", "sshx --port $PORT"]

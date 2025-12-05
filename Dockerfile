FROM debian:12

# Install dependencies
RUN apt-get update && apt-get install -y curl bash

# Download sshx
RUN curl -sSf https://sshx.io/get | sh

# Expose port for Railway
ENV PORT=8080
EXPOSE 8080

# Start sshx server on Railway assigned PORT
CMD ["/bin/bash", "-c", "sshx-server --port $PORT"]

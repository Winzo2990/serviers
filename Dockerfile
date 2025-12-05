FROM debian:12

# Install dependencies
RUN apt-get update && apt-get install -y curl bash

# Download and run sshx
RUN curl -sSf https://sshx.io/get | sh -s install

# Railway port
ENV PORT=8080
EXPOSE 8080

# Start sshx in RUN mode on port $PORT
CMD ["/bin/bash", "-c", "sshx run --port $PORT"]

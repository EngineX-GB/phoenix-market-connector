# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system packages
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip git nano curl unzip python-is-python3

# Install Python packages
RUN pip install beautifulsoup4==4.12.3 \
                requests==2.31.0 \
                cloudscraper==1.2.71 \
                pyinstaller

# Create the /apps directory
RUN mkdir /apps

# Set working directory
WORKDIR /apps

# Default command
CMD ["/bin/bash"]

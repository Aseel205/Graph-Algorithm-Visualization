# Use an official Ubuntu image as the base
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install essential tools, including python3-venv
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    python3-venv \
    git && \
    apt-get clean

# Install Google Test (gmock) and related libraries
RUN apt-get update && \
    apt-get install -y \
    libgtest-dev && \
    apt-get clean

# Install Meson build system in a virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install meson pytest coverage

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy your project files into the container
COPY . .

# Specify the default command to run in the container (bash shell)
CMD ["/bin/bash"]


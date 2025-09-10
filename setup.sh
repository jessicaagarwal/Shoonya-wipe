#!/bin/bash

# SafeErasePro Development Environment Setup Script
# This script automates the Docker setup process

set -e  # Exit on any error

echo "🚀 SafeErasePro Development Environment Setup"
echo "=============================================="

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

echo "🖥️  Detected OS: $OS"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    if [[ "$OS" == "Linux" ]]; then
        echo "   Run: sudo apt-get update && sudo apt-get install docker.io"
        echo "   Then: sudo systemctl start docker && sudo systemctl enable docker"
        echo "   And: sudo usermod -aG docker $USER"
        echo "   Then log out and back in, and run this script again."
    elif [[ "$OS" == "Mac" ]]; then
        echo "   Download Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    elif [[ "$OS" == "Windows" ]]; then
        echo "   Download Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    else
        echo "   Please install Docker for your operating system."
    fi
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is installed and running"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t saferase-pro .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test the setup
echo "🧪 Testing the setup..."
docker run --rm -v /dev:/dev:ro -v /proc:/proc:ro -v /sys:/sys:ro saferase-pro

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Use 'docker-compose up' to start the development environment"
    echo "2. Use 'docker-compose exec saferase-dev python test_device_scan.py' to run tests"
    echo "3. Start developing your SafeErasePro features!"
else
    echo "❌ Test failed. Please check the error messages above."
    exit 1
fi

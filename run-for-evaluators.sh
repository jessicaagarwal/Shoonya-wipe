#!/bin/bash

echo "========================================"
echo "Shoonya Wipe - National Submission"
echo "NIST SP 800-88r2 Compliant E-Waste Solution"
echo "========================================"
echo

echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not running"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

echo "Docker is installed and running"
echo

echo "Pulling Shoonya Wipe image..."
docker pull jessicaagarwal/shoonya-wipe:latest

echo
echo "Starting Shoonya Wipe application..."
docker run -d -p 5000:5000 --name shoonya-wipe jessicaagarwal/shoonya-wipe:latest

echo
echo "========================================"
echo "Application is starting..."
echo
echo "Once started, open your browser to:"
echo "http://localhost:5000"
echo
echo "Features to test:"
echo "1. Device Scanning"
echo "2. NIST Compliance Form"
echo "3. Wipe Simulation"
echo "4. Certificate Generation"
echo "5. Digital Signature Verification"
echo "========================================"
echo

echo "Waiting for application to start..."
sleep 10

echo
echo "Opening browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
elif command -v open &> /dev/null; then
    open http://localhost:5000
else
    echo "Please open http://localhost:5000 in your browser"
fi

echo
echo "To stop the application, run:"
echo "docker stop shoonya-wipe"
echo "docker rm shoonya-wipe"
echo

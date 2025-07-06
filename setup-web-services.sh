#!/bin/bash

# RedTeamCUA Web Services Setup Script
# This script sets up all required web services for RedTeamCUA

echo "🚀 Starting RedTeamCUA Web Services Setup..."

# Create downloads directory
mkdir -p downloads
cd downloads

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "📥 Downloading Reddit Forum image..."
# Download Reddit Forum image
if [ ! -f "postmill-populated-exposed-withimg.tar" ]; then
    echo "Downloading Reddit Forum Docker image..."
    curl -L -o postmill-populated-exposed-withimg.tar "http://metis.lti.cs.cmu.edu/webarena-images/postmill-populated-exposed-withimg.tar"
    echo "✅ Reddit Forum image downloaded"
else
    echo "✅ Reddit Forum image already exists"
fi

# Load Reddit image
echo "📦 Loading Reddit Forum Docker image..."
docker load --input postmill-populated-exposed-withimg.tar

# Go back to main directory
cd ..

echo "🐳 Starting all web services..."
# Start all services using Docker Compose
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Wait for RocketChat to be ready
echo "🚀 Waiting for RocketChat to initialize..."
until curl -f http://localhost:3000 >/dev/null 2>&1; do
    echo "Waiting for RocketChat..."
    sleep 5
done

# Wait for OwnCloud to be ready
echo "☁️ Waiting for OwnCloud to initialize..."
until curl -f http://localhost:8092 >/dev/null 2>&1; do
    echo "Waiting for OwnCloud..."
    sleep 5
done

# Wait for Reddit Forum to be ready
echo "💬 Waiting for Reddit Forum to initialize..."
until curl -f http://localhost:9999 >/dev/null 2>&1; do
    echo "Waiting for Reddit Forum..."
    sleep 5
done

echo "🎉 All services are now running!"
echo ""
echo "📋 Service URLs:"
echo "   🔹 Reddit Forum: http://localhost:9999"
echo "   🔹 OwnCloud: http://localhost:8092"
echo "   🔹 RocketChat: http://localhost:3000"
echo ""
echo "🔑 Default credentials:"
echo "   🔹 OwnCloud: theagentcompany / theagentcompany"
echo "   🔹 RocketChat: theagentcompany / theagentcompany"
echo ""
echo "✅ Web services setup completed!"

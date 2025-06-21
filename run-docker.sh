#!/bin/bash

# Script to run the Task Manager app in Docker

echo "🚀 Starting Desktop Task Manager in Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Allow X11 connections from Docker containers
echo "🔧 Setting up X11 permissions..."
xhost +local:docker

# Create data directory if it doesn't exist
mkdir -p ./data

# Build and run the container
echo "📦 Building and running Task Manager container..."
docker-compose up --build

# Clean up X11 permissions when done
echo "🧹 Cleaning up X11 permissions..."
xhost -local:docker

echo "✅ Task Manager container stopped." 
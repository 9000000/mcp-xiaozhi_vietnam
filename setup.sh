#!/bin/bash

# Setup script for MCP Xiaozhi Vietnam
# This script helps you configure and run the Docker containers

set -e

echo "🚀 MCP Xiaozhi Vietnam - Setup Script"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Ask for MCP token
echo "📝 Configuration"
echo "----------------"
read -p "Enter your MCP token (or press Enter to edit docker-compose.yml manually): " TOKEN

if [ -n "$TOKEN" ]; then
    # Update docker-compose.yml with the token
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|YOUR_TOKEN_HERE|$TOKEN|g" docker-compose.yml
    else
        # Linux
        sed -i "s|YOUR_TOKEN_HERE|$TOKEN|g" docker-compose.yml
    fi
    echo "✓ Token configured in docker-compose.yml"
else
    echo "⚠️  Please edit docker-compose.yml manually and replace YOUR_TOKEN_HERE with your actual token"
    echo ""
    read -p "Press Enter to continue after editing docker-compose.yml..."
fi

echo ""
echo "🔨 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting containers..."
docker-compose up -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Useful commands:"
echo "  - View logs:        docker-compose logs -f"
echo "  - Stop containers:  docker-compose down"
echo "  - Restart:          docker-compose restart"
echo "  - View status:      docker-compose ps"
echo ""
echo "📖 For more information, see DOCKER.md"

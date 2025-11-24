#!/bin/bash

# Script to compare Docker image sizes

echo "🔍 Comparing Docker Image Sizes"
echo "================================"
echo ""

# Build slim version
echo "📦 Building Slim version (Debian-based)..."
docker-compose build --quiet
SLIM_SIZE=$(docker images mcp-xiaozhi-vietnam --format "{{.Size}}" | head -1)

# Build alpine version
echo "📦 Building Alpine version..."
docker-compose -f docker-compose.alpine.yml build --quiet
ALPINE_SIZE=$(docker images mcp-xiaozhi-vietnam:alpine --format "{{.Size}}" | head -1)

# Display results
echo ""
echo "📊 Results:"
echo "----------"
echo "Slim (Debian):  $SLIM_SIZE"
echo "Alpine (Linux): $ALPINE_SIZE"
echo ""

# Show detailed info
echo "📋 Detailed Information:"
echo "------------------------"
docker images | grep -E "REPOSITORY|mcp-xiaozhi-vietnam"

echo ""
echo "💡 Recommendations:"
echo "-------------------"
echo "- Use Alpine for production (smallest size)"
echo "- Use Slim for development (better compatibility)"
echo ""
echo "To use Alpine version:"
echo "  docker-compose -f docker-compose.alpine.yml up -d"

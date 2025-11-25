#!/bin/bash
# Check Docker build context size

echo "🔍 Checking Docker Build Context"
echo "================================="
echo ""

# Create temporary build context
echo "Creating build context..."
docker build --no-cache -t test-context -f - . <<EOF
FROM alpine
WORKDIR /context
COPY . .
RUN du -sh /context && \
    find /context -type f | wc -l && \
    ls -lah /context
EOF

echo ""
echo "✅ Check complete"

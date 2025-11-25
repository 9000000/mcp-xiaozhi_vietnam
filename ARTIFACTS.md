# Using GitHub Actions Artifacts

Hướng dẫn download và sử dụng Docker images từ GitHub Actions artifacts.

## 📦 Tổng quan

GitHub Actions tự động build Docker images cho mỗi commit và release. Images được lưu dưới dạng artifacts và có thể download để sử dụng.

## 🎯 Lợi ích

- ✅ Không cần build locally
- ✅ Pre-built cho nhiều platforms (amd64, arm64)
- ✅ Tested và verified
- ✅ Consistent builds
- ✅ Tiết kiệm thời gian

## 📥 Download Artifacts

### Cách 1: Via GitHub Web UI

1. Vào repository trên GitHub
2. Click tab **Actions**
3. Chọn workflow run (ví dụ: "Docker Build")
4. Scroll xuống phần **Artifacts**
5. Click để download artifact mong muốn

### Cách 2: Via GitHub CLI

```bash
# Cài đặt GitHub CLI (nếu chưa có)
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
# See: https://github.com/cli/cli#installation

# Login
gh auth login

# List recent workflow runs
gh run list --workflow=docker-build.yml --limit 5

# Download artifacts từ run cụ thể
gh run download <RUN_ID>

# Download artifact cụ thể
gh run download <RUN_ID> -n docker-image-slim-0

# Download latest successful run
gh run download $(gh run list --workflow=docker-build.yml --status=success --limit=1 --json databaseId --jq '.[0].databaseId')
```

### Cách 3: Via API

```bash
# Get latest workflow run
RUN_ID=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/workflows/docker-build.yml/runs?status=success&per_page=1" \
  | jq -r '.workflow_runs[0].id')

# List artifacts
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/$RUN_ID/artifacts"

# Download artifact
curl -L -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/artifacts/ARTIFACT_ID/zip" \
  -o artifact.zip
```

## 📂 Artifact Structure

### Build Artifacts (Retention: 1 day)

```
docker-image-slim-0/
  └── image-slim-linux/amd64.tar

docker-image-slim-1/
  └── image-slim-linux/arm64.tar

docker-image-alpine-0/
  └── image-alpine-linux/amd64.tar

docker-image-alpine-1/
  └── image-alpine-linux/arm64.tar
```

### Release Artifacts (Retention: 30 days)

```
docker-image-slim-v1.0.0.tar    # Multi-arch OCI archive
docker-image-alpine-v1.0.0.tar  # Multi-arch OCI archive
```

## 🔧 Load và Sử dụng

### 1. Extract artifact

```bash
# Unzip downloaded artifact
unzip docker-image-slim-0.zip

# Hoặc nếu download từ release
# File đã là .tar, không cần unzip
```

### 2. Load image vào Docker

```bash
# Load Slim image (amd64)
docker load < image-slim-linux/amd64.tar

# Load Alpine image (amd64)
docker load < image-alpine-linux/amd64.tar

# Load từ release artifact
docker load < docker-image-slim-v1.0.0.tar
```

### 3. Verify image

```bash
# List images
docker images mcp-xiaozhi-vietnam

# Check image details
docker inspect mcp-xiaozhi-vietnam:slim-latest

# Test run
docker run --rm mcp-xiaozhi-vietnam:slim-latest python --version
```

### 4. Tag và sử dụng

```bash
# Tag với tên ngắn hơn
docker tag mcp-xiaozhi-vietnam:slim-latest mcp:latest

# Run với environment variables
docker run --rm \
  -e MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN" \
  mcp:latest
```

## 🏗️ Platform-specific Usage

### AMD64 (x86_64)

```bash
# Download và load amd64 image
gh run download <RUN_ID> -n docker-image-slim-0
docker load < image-slim-linux/amd64.tar

# Run
docker run --rm --platform linux/amd64 mcp-xiaozhi-vietnam:slim-latest
```

### ARM64 (Apple Silicon, ARM servers)

```bash
# Download và load arm64 image
gh run download <RUN_ID> -n docker-image-slim-1
docker load < image-slim-linux/arm64.tar

# Run
docker run --rm --platform linux/arm64 mcp-xiaozhi-vietnam:slim-latest
```

## 📊 Choosing the Right Artifact

### Development

```bash
# Download latest build artifact
gh run download --name docker-image-slim-0

# Load và test
docker load < image-slim-linux/amd64.tar
docker run --rm mcp-xiaozhi-vietnam:slim-latest python -c "import fastmcp"
```

### Production

```bash
# Download release artifact (stable)
gh release download v1.0.0 --pattern "docker-image-alpine-*.tar"

# Load
docker load < docker-image-alpine-v1.0.0.tar

# Deploy
docker run -d \
  --name mcp-prod \
  --restart unless-stopped \
  -e MCP_ENDPOINT="$MCP_ENDPOINT" \
  mcp-xiaozhi-vietnam:alpine-latest
```

## 🔄 Automation Scripts

### Download Latest Build

```bash
#!/bin/bash
# download-latest.sh

REPO="OWNER/REPO"
WORKFLOW="docker-build.yml"

# Get latest successful run
RUN_ID=$(gh run list \
  --repo "$REPO" \
  --workflow "$WORKFLOW" \
  --status success \
  --limit 1 \
  --json databaseId \
  --jq '.[0].databaseId')

echo "Downloading from run: $RUN_ID"

# Download all artifacts
gh run download "$RUN_ID" --repo "$REPO"

echo "Download complete!"
```

### Load All Images

```bash
#!/bin/bash
# load-images.sh

# Load Slim images
if [ -f "docker-image-slim-0/image-slim-linux/amd64.tar" ]; then
  echo "Loading Slim amd64..."
  docker load < docker-image-slim-0/image-slim-linux/amd64.tar
fi

if [ -f "docker-image-slim-1/image-slim-linux/arm64.tar" ]; then
  echo "Loading Slim arm64..."
  docker load < docker-image-slim-1/image-slim-linux/arm64.tar
fi

# Load Alpine images
if [ -f "docker-image-alpine-0/image-alpine-linux/amd64.tar" ]; then
  echo "Loading Alpine amd64..."
  docker load < docker-image-alpine-0/image-alpine-linux/amd64.tar
fi

if [ -f "docker-image-alpine-1/image-alpine-linux/arm64.tar" ]; then
  echo "Loading Alpine arm64..."
  docker load < docker-image-alpine-1/image-alpine-linux/arm64.tar
fi

echo "All images loaded!"
docker images mcp-xiaozhi-vietnam
```

## 🐛 Troubleshooting

### Artifact not found

**Vấn đề:** Artifact đã expired (retention period)

**Giải pháp:**
- Build artifacts: 1 day retention
- Release artifacts: 30 days retention
- Trigger new build hoặc download từ release

### Wrong platform

**Vấn đề:** Image không chạy được trên platform hiện tại

**Giải pháp:**
```bash
# Check platform
uname -m
# x86_64 = amd64
# aarch64 = arm64

# Download đúng artifact
# artifact-0 = amd64
# artifact-1 = arm64
```

### Image too large

**Vấn đề:** Download chậm, artifact quá lớn

**Giải pháp:**
- Dùng Alpine variant (nhỏ hơn 60-70%)
- Download chỉ platform cần thiết
- Sử dụng compression

### Permission denied

**Vấn đề:** Không thể download private repository artifacts

**Giải pháp:**
```bash
# Login với GitHub CLI
gh auth login

# Hoặc set token
export GITHUB_TOKEN="your_token_here"
```

## 📈 Best Practices

### 1. Version pinning

```bash
# Download specific version
gh release download v1.0.0

# Tag locally
docker tag mcp-xiaozhi-vietnam:slim-v1.0.0 mcp:v1.0.0
```

### 2. Verify checksums

```bash
# Generate checksum
sha256sum docker-image-slim-v1.0.0.tar > checksums.txt

# Verify
sha256sum -c checksums.txt
```

### 3. Clean up old images

```bash
# Remove old images
docker images mcp-xiaozhi-vietnam --format "{{.ID}} {{.CreatedAt}}" | \
  awk '$2 < "2024-01-01" {print $1}' | \
  xargs docker rmi
```

### 4. Use specific tags

```bash
# Avoid :latest in production
docker run mcp-xiaozhi-vietnam:slim-v1.0.0

# Not recommended
docker run mcp-xiaozhi-vietnam:latest
```

## 🔗 Related Documentation

- [GitHub Actions Workflows](.github/workflows/README.md)
- [Docker Guide](DOCKER.md)
- [Optimization Guide](OPTIMIZATION.md)

## 💡 Tips

1. **Use GitHub CLI** - Fastest và easiest way
2. **Download release artifacts** - More stable, longer retention
3. **Verify images** - Always test before production
4. **Clean up** - Remove old artifacts locally
5. **Automate** - Use scripts for repetitive tasks

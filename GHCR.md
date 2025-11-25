# Using GitHub Container Registry (GHCR)

Hướng dẫn sử dụng Docker images từ GitHub Container Registry.

## 📦 Tổng quan

Docker images được tự động build và push lên GitHub Container Registry (ghcr.io) thông qua GitHub Actions.

## 🎯 Lợi ích

- ✅ Tự động build và deploy
- ✅ Multi-architecture support (amd64, arm64)
- ✅ Public access (không cần authentication để pull)
- ✅ Versioning với Git tags
- ✅ Tích hợp với GitHub
- ✅ Unlimited bandwidth và storage cho public repos

## 🔗 Registry URL

```
ghcr.io/OWNER/REPO
```

Thay `OWNER/REPO` bằng GitHub username và repository name của bạn.

## 📥 Pull Images

### Public Images (Không cần login)

```bash
# Pull latest Slim version
docker pull ghcr.io/OWNER/REPO:latest-slim

# Pull latest Alpine version (recommended for production)
docker pull ghcr.io/OWNER/REPO:latest-alpine

# Pull specific version
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine

# Pull from specific branch
docker pull ghcr.io/OWNER/REPO:main-slim
docker pull ghcr.io/OWNER/REPO:develop-alpine
```

### Private Images (Cần authentication)

```bash
# Tạo Personal Access Token (PAT) với quyền read:packages
# https://github.com/settings/tokens

# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/OWNER/REPO:latest-alpine
```

## 🏷️ Image Tags

### Branch-based Tags

| Branch | Slim Tag | Alpine Tag |
|--------|----------|------------|
| main | `main-slim` | `main-alpine` |
| develop | `develop-slim` | `develop-alpine` |

### Version Tags

| Version | Slim Tags | Alpine Tags |
|---------|-----------|-------------|
| v1.2.3 | `v1.2.3-slim`, `v1.2-slim`, `v1-slim` | `v1.2.3-alpine`, `v1.2-alpine`, `v1-alpine` |
| latest | `latest-slim` | `latest-alpine` |

### Commit-based Tags

```bash
# Pull by commit SHA
docker pull ghcr.io/OWNER/REPO:main-abc1234-slim
```

## 🚀 Usage Examples

### Quick Start

```bash
# Pull Alpine version (smallest)
docker pull ghcr.io/OWNER/REPO:latest-alpine

# Run with environment variable
docker run --rm \
  -e MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN" \
  ghcr.io/OWNER/REPO:latest-alpine
```

### Docker Compose

```yaml
version: '3.8'

services:
  mcp-servers:
    image: ghcr.io/OWNER/REPO:latest-alpine
    container_name: mcp-xiaozhi-vietnam
    restart: unless-stopped
    environment:
      - MCP_ENDPOINT=${MCP_ENDPOINT}
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Production Deployment

```bash
# Pull specific version
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine

# Run with restart policy
docker run -d \
  --name mcp-prod \
  --restart unless-stopped \
  -e MCP_ENDPOINT="$MCP_ENDPOINT" \
  ghcr.io/OWNER/REPO:v1.0.0-alpine

# Check logs
docker logs -f mcp-prod
```

### Multi-platform

```bash
# Pull for specific platform
docker pull --platform linux/amd64 ghcr.io/OWNER/REPO:latest-alpine
docker pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest-alpine

# Docker automatically selects correct platform
docker pull ghcr.io/OWNER/REPO:latest-alpine
```

## 🔐 Authentication

### For Pulling Private Images

```bash
# Method 1: Using Personal Access Token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Method 2: Using GitHub CLI
gh auth token | docker login ghcr.io -u USERNAME --password-stdin

# Method 3: Interactive login
docker login ghcr.io
# Username: your-github-username
# Password: your-personal-access-token
```

### For CI/CD

```yaml
# GitHub Actions
- name: Log in to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

## 📊 Image Information

### View Available Tags

```bash
# Using GitHub CLI
gh api /users/OWNER/packages/container/REPO/versions

# Using Docker
docker search ghcr.io/OWNER/REPO
```

### Inspect Image

```bash
# Pull and inspect
docker pull ghcr.io/OWNER/REPO:latest-alpine
docker inspect ghcr.io/OWNER/REPO:latest-alpine

# View layers
docker history ghcr.io/OWNER/REPO:latest-alpine

# Check size
docker images ghcr.io/OWNER/REPO
```

## 🔄 Update Images

### Pull Latest

```bash
# Pull latest version
docker pull ghcr.io/OWNER/REPO:latest-alpine

# Restart container with new image
docker stop mcp-prod
docker rm mcp-prod
docker run -d --name mcp-prod ghcr.io/OWNER/REPO:latest-alpine
```

### Auto-update with Watchtower

```yaml
version: '3.8'

services:
  mcp-servers:
    image: ghcr.io/OWNER/REPO:latest-alpine
    container_name: mcp-prod
    
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 3600 mcp-prod
```

## 🏗️ Platform Support

| Platform | Architecture | Support |
|----------|-------------|---------|
| linux/amd64 | x86_64 | ✅ Full |
| linux/arm64 | ARM64/aarch64 | ✅ Full |

### Platform-specific Pull

```bash
# AMD64 (Intel/AMD)
docker pull --platform linux/amd64 ghcr.io/OWNER/REPO:latest-alpine

# ARM64 (Apple Silicon, ARM servers)
docker pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest-alpine
```

## 📈 Best Practices

### 1. Use Specific Versions in Production

```bash
# ✅ Good - Pinned version
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine

# ❌ Bad - Latest tag (unpredictable)
docker pull ghcr.io/OWNER/REPO:latest-alpine
```

### 2. Use Alpine for Production

```bash
# Alpine is 60-70% smaller
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine  # ~50-80MB
# vs
docker pull ghcr.io/OWNER/REPO:v1.0.0-slim    # ~150-200MB
```

### 3. Verify Image Signatures

```bash
# Check image digest
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine
docker inspect --format='{{.RepoDigests}}' ghcr.io/OWNER/REPO:v1.0.0-alpine
```

### 4. Clean Up Old Images

```bash
# Remove old images
docker images ghcr.io/OWNER/REPO --format "{{.ID}} {{.Tag}}" | \
  grep -v latest | \
  awk '{print $1}' | \
  xargs docker rmi

# Or use prune
docker image prune -a
```

## 🐛 Troubleshooting

### Image Not Found

**Problem:** `Error response from daemon: manifest unknown`

**Solutions:**
1. Check repository name: `ghcr.io/OWNER/REPO`
2. Verify tag exists
3. Check if image is public or needs authentication
4. Wait for GitHub Actions to complete build

### Authentication Failed

**Problem:** `unauthorized: authentication required`

**Solutions:**
```bash
# Verify token has read:packages scope
# Create new token: https://github.com/settings/tokens

# Login again
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Wrong Platform

**Problem:** `exec format error`

**Solutions:**
```bash
# Check your platform
uname -m
# x86_64 = amd64
# aarch64 = arm64

# Pull correct platform
docker pull --platform linux/amd64 ghcr.io/OWNER/REPO:latest-alpine
```

### Rate Limiting

**Problem:** Too many requests

**Solutions:**
- GHCR has generous rate limits for authenticated users
- Login to increase limits
- Use caching in CI/CD

## 🔗 Useful Links

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Package Settings](https://github.com/OWNER/REPO/pkgs/container/REPO)
- [GitHub Actions Workflows](.github/workflows/README.md)

## 💡 Tips

1. **Always use specific versions** in production
2. **Use Alpine variant** for smaller size
3. **Enable auto-updates** with Watchtower for development
4. **Pin versions** in docker-compose.yml for production
5. **Check Security tab** for vulnerability reports
6. **Use multi-stage builds** when customizing images

## 📝 Examples

### Development

```bash
# Pull latest for development
docker pull ghcr.io/OWNER/REPO:develop-alpine

# Run with volume mount
docker run --rm -it \
  -v $(pwd):/app \
  -e MCP_ENDPOINT="$MCP_ENDPOINT" \
  ghcr.io/OWNER/REPO:develop-alpine
```

### Production

```bash
# Pull stable version
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine

# Run as daemon
docker run -d \
  --name mcp-prod \
  --restart unless-stopped \
  --memory="256m" \
  --cpus="0.5" \
  -e MCP_ENDPOINT="$MCP_ENDPOINT" \
  ghcr.io/OWNER/REPO:v1.0.0-alpine
```

### CI/CD

```yaml
# .gitlab-ci.yml example
deploy:
  image: docker:latest
  script:
    - echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin
    - docker pull ghcr.io/OWNER/REPO:latest-alpine
    - docker run -d ghcr.io/OWNER/REPO:latest-alpine
```

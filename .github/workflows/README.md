# GitHub Actions Workflows

Tài liệu về GitHub Actions workflow trong dự án.

## 📋 Workflow

### Docker Build and Push (`docker-release.yml`)

**Trigger:**
- Push to `main` or `develop` branches
- Push tags `v*.*.*` (semantic versioning)
- Pull requests to `main`
- Manual dispatch

**Chức năng:**
- Build Docker images cho cả Slim và Alpine variants
- Build cho 2 platforms: `linux/amd64` và `linux/arm64`
- Push images lên GitHub Container Registry (ghcr.io)
- Test images sau khi push
- Tạo GitHub Release (khi push tag)
- Generate build summary

**Registry:**
- Images được push lên: `ghcr.io/OWNER/REPO`
- Public access (có thể pull mà không cần authentication)

**Tags:**
- Branch builds: `main-slim`, `main-alpine`, `develop-slim`, `develop-alpine`
- Version builds: `v1.0.0-slim`, `v1.0.0-alpine`, `v1.0-slim`, `v1-slim`
- Latest: `latest-slim`, `latest-alpine` (từ main branch)

## 🚀 Cách sử dụng

### Build thủ công

Trigger manual build:

```bash
# Via GitHub UI
Actions → Build and Push Docker Images → Run workflow

# Via GitHub CLI
gh workflow run docker-release.yml
```

### Tạo Release

**Push tag để trigger release:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

Workflow sẽ tự động:
1. Build multi-arch images
2. Push lên GHCR với version tags
3. Tạo GitHub Release với release notes

### Pull Images từ GHCR

```bash
# Pull latest Slim version
docker pull ghcr.io/OWNER/REPO:latest-slim

# Pull latest Alpine version (recommended)
docker pull ghcr.io/OWNER/REPO:latest-alpine

# Pull specific version
docker pull ghcr.io/OWNER/REPO:v1.0.0-alpine

# Pull from specific branch
docker pull ghcr.io/OWNER/REPO:main-alpine
docker pull ghcr.io/OWNER/REPO:develop-alpine
```

Xem thêm chi tiết tại [GHCR.md](../../GHCR.md)

## 🏗️ Build Matrix

### Platforms

| Platform | Architecture | Support |
|----------|-------------|---------|
| linux/amd64 | x86_64 | ✅ Full |
| linux/arm64 | ARM64/aarch64 | ✅ Full |

### Variants

| Variant | Dockerfile | Base Image | Size |
|---------|-----------|------------|------|
| Slim | Dockerfile | python:3.12-slim | ~150-200MB |
| Alpine | Dockerfile.alpine | python:3.12-alpine | ~50-80MB |

## 📊 Workflow Status Badge

Add to README.md:

```markdown
![Docker Build](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-release.yml/badge.svg)
```

## 🔧 Configuration

### Secrets Required

- `GITHUB_TOKEN`: Tự động có sẵn, dùng để push lên GHCR
- Không cần thêm secrets khác

### Environment Variables

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}  # Tự động: owner/repo
```

### Cache

Workflows sử dụng GitHub Actions cache:
- Type: `gha` (GitHub Actions cache)
- Mode: `max` (cache all layers)
- Automatic cleanup sau 7 ngày

## 🐛 Troubleshooting

### Build fails on arm64

**Vấn đề:** QEMU emulation chậm hoặc timeout

**Giải pháp:**
```yaml
# Tăng timeout
timeout-minutes: 60

# Hoặc build riêng
strategy:
  matrix:
    platform: [linux/amd64, linux/arm64]
```

### Out of disk space

**Vấn đề:** GitHub runner hết disk space

**Giải pháp:**
```yaml
- name: Free disk space
  run: |
    docker system prune -af
    df -h
```

### Cache not working

**Vấn đề:** Build không sử dụng cache

**Giải pháp:**
```yaml
cache-from: type=gha,scope=${{ github.ref_name }}
cache-to: type=gha,mode=max,scope=${{ github.ref_name }}
```



## 📈 Performance Tips

### 1. Parallel builds

Workflows đã được cấu hình để build parallel:
- Slim và Alpine build đồng thời
- amd64 và arm64 build đồng thời

### 2. Cache optimization

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

### 3. Conditional runs

```yaml
on:
  push:
    paths:
      - 'Dockerfile*'
      - '*.py'
```

## 🔒 Security

### Update dependencies

```bash
# Update Python packages
pip list --outdated
pip install --upgrade package_name

# Update base image
# Edit Dockerfile: FROM python:3.12-slim
```

### Pin versions

```dockerfile
# Good - pinned version
FROM python:3.12.1-slim

# Better - with digest
FROM python:3.12.1-slim@sha256:abc123...
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Multi-platform builds](https://docs.docker.com/build/building/multi-platform/)
- [GHCR Guide](../../GHCR.md)

## 🤝 Contributing

Khi thêm workflow mới:

1. Test locally với [act](https://github.com/nektos/act)
2. Add documentation vào file này
3. Add status badge vào README.md
4. Test trên branch trước khi merge

## 📝 Changelog

### v1.0.0
- Initial workflows
- Multi-arch build support
- Security scanning
- Release automation

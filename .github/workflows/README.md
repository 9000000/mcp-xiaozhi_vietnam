# GitHub Actions Workflows

Tài liệu về các GitHub Actions workflows trong dự án.

## 📋 Danh sách Workflows

### 1. Docker Build (`docker-build.yml`)

**Trigger:**
- Push to `main` or `develop` branches
- Push tags `v*`
- Pull requests to `main`
- Manual dispatch

**Chức năng:**
- Build Docker images cho cả Slim và Alpine variants
- Build cho 2 platforms: `linux/amd64` và `linux/arm64`
- Test images sau khi build
- Upload artifacts
- Generate build summary

**Artifacts:**
- `docker-image-slim-*`: Slim variant images
- `docker-image-alpine-*`: Alpine variant images
- Retention: 1 day

### 2. Docker Test (`docker-test.yml`)

**Trigger:**
- Pull requests thay đổi:
  - Dockerfile*
  - docker-compose*.yml
  - requirements.txt
  - *.py files
  - workflow files

**Chức năng:**
- Quick build test chỉ cho amd64
- Test import các modules chính
- So sánh kích thước images
- Nhanh hơn full build

### 3. Docker Release (`docker-release.yml`)

**Trigger:**
- Push tags `v*.*.*` (semantic versioning)
- Manual dispatch với version input

**Chức năng:**
- Build multi-arch images cho release
- Tạo GitHub Release với artifacts
- Upload OCI image archives
- Generate release notes
- Retention: 30 days

**Release Artifacts:**
- `docker-image-slim-v*.tar`: Slim variant OCI archive
- `docker-image-alpine-v*.tar`: Alpine variant OCI archive

### 4. Docker Security (`docker-security.yml`)

**Trigger:**
- Push to `main` (Dockerfile hoặc requirements.txt thay đổi)
- Pull requests
- Weekly schedule (Monday 00:00 UTC)
- Manual dispatch

**Chức năng:**
- Scan vulnerabilities với Trivy
- Upload results to GitHub Security tab
- Check CRITICAL và HIGH severity issues
- Generate security summary

## 🚀 Cách sử dụng

### Build thủ công

Trigger manual build:

```bash
# Via GitHub UI
Actions → Docker Build → Run workflow

# Via GitHub CLI
gh workflow run docker-build.yml
```

### Tạo Release

1. **Tự động** - Push tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **Thủ công** - Via GitHub UI:
```
Actions → Build Release Images → Run workflow
Input version: v1.0.0
```

### Download Artifacts

**Via GitHub UI:**
1. Go to Actions tab
2. Click on workflow run
3. Scroll to Artifacts section
4. Download desired artifact

**Via GitHub CLI:**
```bash
# List artifacts
gh run list --workflow=docker-build.yml

# Download artifact
gh run download <run-id>
```

### Load Downloaded Images

```bash
# Extract artifact
unzip docker-image-slim-*.zip

# Load image
docker load < docker-image-slim-*.tar

# Verify
docker images mcp-xiaozhi-vietnam
```

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

## 📊 Workflow Status Badges

Add to README.md:

```markdown
![Docker Build](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-build.yml/badge.svg)
![Docker Security](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-security.yml/badge.svg)
```

## 🔧 Configuration

### Secrets Required

Không cần secrets cho build cơ bản. Chỉ cần `GITHUB_TOKEN` (tự động có).

### Environment Variables

```yaml
env:
  IMAGE_NAME: mcp-xiaozhi-vietnam
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

### Security scan fails

**Vấn đề:** Trivy scan timeout hoặc fail

**Giải pháp:**
```yaml
- name: Run Trivy
  uses: aquasecurity/trivy-action@master
  with:
    timeout: 10m
    ignore-unfixed: true
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

## 🔒 Security Best Practices

### 1. Scan regularly

Security workflow chạy weekly để phát hiện vulnerabilities mới.

### 2. Review scan results

Check Security tab thường xuyên:
```
Repository → Security → Code scanning alerts
```

### 3. Update dependencies

```bash
# Update Python packages
pip list --outdated
pip install --upgrade package_name

# Update base image
# Edit Dockerfile: FROM python:3.12-slim
```

### 4. Pin versions

```dockerfile
# Good - pinned version
FROM python:3.12.1-slim

# Better - with digest
FROM python:3.12.1-slim@sha256:abc123...
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
- [Multi-platform builds](https://docs.docker.com/build/building/multi-platform/)

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

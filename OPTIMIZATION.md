# Docker Image Optimization Guide

Hướng dẫn tối ưu hóa Docker image để đạt kích thước nhỏ nhất.

## Tổng quan

Dự án cung cấp 2 phiên bản Dockerfile:

1. **Dockerfile** (Debian Slim) - ~150-200MB
   - Tương thích tốt hơn
   - Dễ debug
   - Khuyến nghị cho development

2. **Dockerfile.alpine** (Alpine Linux) - ~50-80MB
   - Kích thước nhỏ nhất
   - Tối ưu cho production
   - Tiết kiệm băng thông và storage

## So sánh kích thước

### Chạy script so sánh

**Linux/macOS:**
```bash
chmod +x compare-images.sh
./compare-images.sh
```

**Windows PowerShell:**
```powershell
.\compare-images.ps1
```

### Kết quả dự kiến

| Version | Base Image | Size | Use Case |
|---------|-----------|------|----------|
| Slim | python:3.12-slim | ~150-200MB | Development, Debugging |
| Alpine | python:3.12-alpine | ~50-80MB | Production, Minimal footprint |

## Kỹ thuật tối ưu hóa đã áp dụng

### 1. Multi-stage Build

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
# Install build tools and dependencies

# Stage 2: Runtime
FROM python:3.12-slim
# Copy only necessary files from builder
```

**Lợi ích:**
- Loại bỏ build tools khỏi image cuối
- Giảm 30-50% kích thước
- Tăng bảo mật (ít tools hơn)

### 2. .dockerignore (Đã tối ưu)

Loại bỏ các file không cần thiết:
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.venv/`)
- IDE configs (`.vscode/`, `.idea/`)
- Git files (`.git/`, `.github/`)
- Documentation (`*.md`, `docs/`)
- Docker files (`Dockerfile*`, `docker-compose*.yml`)
- Scripts (`setup.sh`, `*.ps1`)
- Tests (`test_*.py`, `.pytest_cache/`)
- Environment files (`.env`)
- Temporary files (`*.tmp`, `*.bak`)

**Lợi ích:**
- Build context nhỏ hơn (~90% reduction)
- Build nhanh hơn (ít files để copy)
- Image sạch hơn (chỉ có code cần thiết)

**Kiểm tra:**
```bash
# Linux/macOS
./check-build-context.sh

# Windows
.\check-build-context.ps1
```

### 3. Layer Caching

```dockerfile
# Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code later
COPY . .
```

**Lợi ích:**
- Rebuild nhanh hơn khi chỉ thay đổi code
- Tận dụng Docker layer cache

### 4. Minimal Base Image

- Sử dụng `python:3.12-slim` thay vì `python:3.12`
- Hoặc `python:3.12-alpine` cho kích thước tối thiểu

**So sánh:**
- `python:3.12`: ~1GB
- `python:3.12-slim`: ~150MB
- `python:3.12-alpine`: ~50MB

### 5. Cleanup trong cùng layer

```dockerfile
RUN apt-get update && apt-get install -y gcc \
    && pip install -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
```

**Lợi ích:**
- Không tạo intermediate layers
- Giảm kích thước image

### 6. Copy chỉ file cần thiết

```dockerfile
# Thay vì COPY . .
COPY mcp_pipe.py .
COPY mcp_config.json .
COPY *.py ./
```

**Lợi ích:**
- Loại bỏ file không cần thiết
- Image nhỏ hơn

### 7. No Cache cho pip

```dockerfile
ENV PIP_NO_CACHE_DIR=1
RUN pip install --no-cache-dir -r requirements.txt
```

**Lợi ích:**
- Không lưu pip cache
- Giảm 10-20MB

### 8. User dependencies location

```dockerfile
RUN pip install --user --no-warn-script-location -r requirements.txt
COPY --from=builder /root/.local /home/appuser/.local
```

**Lợi ích:**
- Dễ copy giữa stages
- Tách biệt dependencies

## Sử dụng

### Development (Slim)

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Size check
docker images mcp-xiaozhi-vietnam
```

### Production (Alpine)

```bash
# Build
docker-compose -f docker-compose.alpine.yml build

# Run
docker-compose -f docker-compose.alpine.yml up -d

# Size check
docker images mcp-xiaozhi-vietnam:alpine
```

## Best Practices

### 1. Chọn base image phù hợp

```dockerfile
# Development
FROM python:3.12-slim

# Production
FROM python:3.12-alpine
```

### 2. Combine RUN commands

```dockerfile
# ❌ Bad - Creates multiple layers
RUN apt-get update
RUN apt-get install -y gcc
RUN pip install -r requirements.txt

# ✅ Good - Single layer
RUN apt-get update && \
    apt-get install -y gcc && \
    pip install -r requirements.txt && \
    apt-get purge -y gcc && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Order matters

```dockerfile
# ✅ Good - Stable layers first
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ Bad - Invalidates cache often
COPY . .
RUN pip install -r requirements.txt
```

### 4. Use .dockerignore

```
# Always ignore
.git/
__pycache__/
*.pyc
*.md
tests/
```

### 5. Minimize layers

```dockerfile
# ❌ Bad - Many layers
RUN pip install package1
RUN pip install package2
RUN pip install package3

# ✅ Good - One layer
RUN pip install package1 package2 package3
```

## Advanced Optimization

### 1. Distroless Images

Cho security tối đa:

```dockerfile
FROM gcr.io/distroless/python3-debian12
COPY --from=builder /app /app
```

**Lợi ích:**
- Không có shell, package manager
- Bảo mật cao nhất
- Kích thước nhỏ

**Nhược điểm:**
- Khó debug
- Không có shell access

### 2. Scratch Images

Cho kích thước tối thiểu (chỉ với compiled binaries):

```dockerfile
FROM scratch
COPY --from=builder /app/binary /
```

### 3. Compress layers

```bash
# Squash all layers into one
docker build --squash -t mcp-xiaozhi-vietnam:squashed .
```

**Lưu ý:** Mất layer caching benefits

## Monitoring Image Size

### Check image size

```bash
docker images mcp-xiaozhi-vietnam --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Analyze layers

```bash
docker history mcp-xiaozhi-vietnam:latest
```

### Use dive tool

```bash
# Install dive
brew install dive  # macOS
# or download from https://github.com/wagoodman/dive

# Analyze image
dive mcp-xiaozhi-vietnam:latest
```

## Troubleshooting

### Alpine compatibility issues

Một số Python packages cần build tools:

```dockerfile
# Add build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev
```

### Missing libraries

```dockerfile
# Add runtime libraries
RUN apk add --no-cache \
    libffi \
    openssl
```

### Slow builds

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build .

# Or enable globally
export DOCKER_BUILDKIT=1
```

## Benchmarks

### Build time

| Version | First Build | Rebuild (code change) |
|---------|-------------|----------------------|
| Slim | ~2-3 min | ~10-20 sec |
| Alpine | ~3-4 min | ~10-20 sec |

### Runtime performance

Cả hai versions có performance tương đương cho Python applications.

### Memory usage

| Version | Idle | Under load |
|---------|------|------------|
| Slim | ~50MB | ~100-150MB |
| Alpine | ~40MB | ~80-120MB |

## Recommendations

### Development
- ✅ Use `Dockerfile` (Slim)
- ✅ Mount volumes for hot reload
- ✅ Keep debug tools

### Staging
- ✅ Use `Dockerfile` (Slim)
- ✅ Test compatibility
- ✅ Profile performance

### Production
- ✅ Use `Dockerfile.alpine`
- ✅ Set resource limits
- ✅ Enable health checks
- ✅ Use image scanning

## Security Considerations

### 1. Non-root user

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 2. Read-only filesystem

```yaml
# docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
```

### 3. Scan images

```bash
# Using Trivy
trivy image mcp-xiaozhi-vietnam:latest

# Using Docker Scout
docker scout cves mcp-xiaozhi-vietnam:latest
```

## Further Reading

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Alpine Linux](https://alpinelinux.org/)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

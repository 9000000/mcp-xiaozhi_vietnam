# Multi-Stage Build Explained

Giải thích chi tiết về kỹ thuật Multi-Stage Build trong Docker.

## 🎯 Multi-Stage Build là gì?

**Multi-stage build** là kỹ thuật chia quá trình build Docker image thành nhiều giai đoạn (stages), mỗi stage có một mục đích riêng.

## 📊 So sánh

### ❌ Single-Stage Build (Cũ)

```dockerfile
FROM python:3.12-alpine

# Install build tools
RUN apk add gcc musl-dev libffi-dev openssl-dev

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

CMD ["python", "app.py"]
```

**Vấn đề:**
- Image chứa cả build tools (gcc, musl-dev, etc.)
- Kích thước: ~150-200MB
- Không cần thiết cho runtime

### ✅ Multi-Stage Build (Mới)

```dockerfile
# Stage 1: Builder
FROM python:3.12-alpine AS builder
RUN apk add gcc musl-dev libffi-dev openssl-dev
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-alpine
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
CMD ["python", "app.py"]
```

**Lợi ích:**
- Image chỉ chứa runtime dependencies
- Kích thước: ~50-80MB (giảm 60-70%)
- Sạch hơn, an toàn hơn

## 🔍 Phân tích Dockerfile của bạn

### Stage 1: Builder (Build Environment)

```dockerfile
# Stage 1: Builder
FROM python:3.12-alpine AS builder
#                           ^^^^^^^^
#                           Đặt tên cho stage này

WORKDIR /app

# Install BUILD dependencies
RUN apk add --no-cache \
    gcc \           # C compiler
    musl-dev \      # C library
    libffi-dev \    # Foreign Function Interface
    openssl-dev     # SSL/TLS library

# Install Python packages
COPY requirements.txt .
RUN pip install --user -r requirements.txt
#               ^^^^^^
#               Install vào /root/.local
```

**Mục đích:**
- Cài đặt build tools (gcc, musl-dev, etc.)
- Compile Python packages
- Tạo dependencies

**Kết quả:**
- `/root/.local/` chứa tất cả Python packages đã compiled

### Stage 2: Runtime (Production Environment)

```dockerfile
# Stage 2: Runtime
FROM python:3.12-alpine
#    ^^^^^^^^^^^^^^^^^^
#    Bắt đầu từ image sạch mới

WORKDIR /app

# Install RUNTIME dependencies only
RUN apk add --no-cache \
    libffi \        # Runtime library (không cần -dev)
    openssl         # Runtime library (không cần -dev)

# Copy Python packages từ builder
COPY --from=builder /root/.local /home/appuser/.local
#    ^^^^^^^^^^^^^^
#    Copy từ stage "builder"

# Copy application code
COPY mcp_pipe.py .
COPY mcp_config.json .
COPY *.py ./

CMD ["python", "mcp_pipe.py"]
```

**Mục đích:**
- Chỉ giữ runtime dependencies
- Copy compiled packages từ builder
- Không có build tools

**Kết quả:**
- Image nhỏ gọn, chỉ có những gì cần để chạy

## 📈 Lợi ích

### 1. Kích thước nhỏ hơn

| Component | Single-Stage | Multi-Stage |
|-----------|--------------|-------------|
| Base image | 50MB | 50MB |
| Build tools | 100MB | ❌ 0MB |
| Dependencies | 50MB | 50MB |
| **Total** | **200MB** | **100MB** |

### 2. Bảo mật tốt hơn

```
Single-Stage:
✅ Python runtime
✅ Your code
❌ gcc (có thể compile malicious code)
❌ Build tools (attack surface lớn)

Multi-Stage:
✅ Python runtime
✅ Your code
✅ Không có build tools
✅ Attack surface nhỏ
```

### 3. Build nhanh hơn (với cache)

```bash
# Lần 1: Build đầy đủ
Stage 1: 2 phút
Stage 2: 30 giây
Total: 2.5 phút

# Lần 2: Chỉ thay đổi code
Stage 1: Cached! (0 giây)
Stage 2: 30 giây
Total: 30 giây
```

## 🎨 Ví dụ thực tế

### Ví dụ 1: Python với C extensions

```dockerfile
# Stage 1: Build
FROM python:3.12-alpine AS builder
RUN apk add gcc musl-dev
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-alpine
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
CMD ["python", "app.py"]
```

**Giảm:** 200MB → 80MB

### Ví dụ 2: Node.js

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Giảm:** 500MB → 150MB

### Ví dụ 3: Go (Extreme)

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o app

# Stage 2: Runtime
FROM scratch
COPY --from=builder /app/app /app
CMD ["/app"]
```

**Giảm:** 300MB → 10MB!

## 🔧 Kỹ thuật nâng cao

### 1. Multiple stages

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
COPY package*.json .
RUN npm ci

# Stage 2: Build
FROM node:18-alpine AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:18-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

### 2. Conditional stages

```dockerfile
# Development stage
FROM python:3.12-alpine AS development
RUN apk add gcc musl-dev
COPY requirements.txt requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
CMD ["python", "app.py"]

# Production stage
FROM python:3.12-alpine AS production
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
CMD ["python", "app.py"]
```

Build specific stage:
```bash
# Development
docker build --target development -t app:dev .

# Production
docker build --target production -t app:prod .
```

### 3. Shared base

```dockerfile
# Base stage
FROM python:3.12-alpine AS base
RUN apk add --no-cache libffi openssl

# Builder stage
FROM base AS builder
RUN apk add --no-cache gcc musl-dev
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM base
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
CMD ["python", "app.py"]
```

## 💡 Best Practices

### 1. Đặt tên stages rõ ràng

```dockerfile
# ✅ Good
FROM python:3.12-alpine AS builder
FROM python:3.12-alpine AS runtime

# ❌ Bad
FROM python:3.12-alpine AS stage1
FROM python:3.12-alpine AS stage2
```

### 2. Copy chỉ những gì cần

```dockerfile
# ✅ Good
COPY --from=builder /root/.local /home/appuser/.local

# ❌ Bad
COPY --from=builder / /
```

### 3. Sử dụng .dockerignore

```
# Tránh copy vào builder stage
.git/
tests/
*.md
```

### 4. Order matters

```dockerfile
# ✅ Good - Dependencies trước, code sau
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ Bad - Code trước, dependencies sau
COPY . .
RUN pip install -r requirements.txt
```

## 🎯 Khi nào dùng Multi-Stage?

### ✅ Nên dùng khi:
- Cần compile code (C, C++, Go, Rust)
- Cần build tools (npm, webpack, gcc)
- Muốn image nhỏ nhất
- Production deployment

### ❌ Không cần khi:
- Pure Python (không có C extensions)
- Development environment
- Image đã đủ nhỏ

## 📊 Kết quả trong project này

```
Before Multi-Stage:
- Base: python:3.12-alpine (50MB)
- Build tools: gcc, musl-dev, etc. (100MB)
- Dependencies: fastmcp, websockets (50MB)
- Code: 1MB
Total: ~200MB

After Multi-Stage:
- Base: python:3.12-alpine (50MB)
- Runtime libs: libffi, openssl (5MB)
- Dependencies: fastmcp, websockets (25MB)
- Code: 1MB
Total: ~80MB

Savings: 60% smaller! 🎉
```

## 🔗 Xem thêm

- [Dockerfile](Dockerfile) - Implementation thực tế
- [OPTIMIZATION.md](OPTIMIZATION.md) - Các kỹ thuật tối ưu khác
- [Docker Multi-Stage Docs](https://docs.docker.com/build/building/multi-stage/)

## 💬 Tóm tắt

**Multi-stage build = Tách build và runtime**

1. **Stage 1 (Builder):** Compile, build, install
2. **Stage 2 (Runtime):** Chỉ copy kết quả, không có tools
3. **Kết quả:** Image nhỏ hơn, sạch hơn, an toàn hơn

Đơn giản nhưng cực kỳ hiệu quả! 🚀

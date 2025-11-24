# Docker Deployment Guide

Hướng dẫn triển khai MCP Xiaozhi Vietnam bằng Docker.

## Yêu cầu

- Docker Engine 20.10+
- Docker Compose 2.0+

## Cài đặt Docker

### Windows
1. Tải và cài đặt [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Khởi động Docker Desktop
3. Kiểm tra: `docker --version` và `docker-compose --version`

### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Cài Docker Compose
sudo apt-get install docker-compose-plugin
```

### macOS
1. Tải và cài đặt [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Khởi động Docker Desktop

## Cấu hình

### Cách 1: Chỉnh sửa trực tiếp trong docker-compose.yml (Đơn giản)

Mở file `docker-compose.yml` và thay `YOUR_TOKEN_HERE` bằng token thực tế:

```yaml
environment:
  - MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_ACTUAL_TOKEN_HERE
```

### Cách 2: Sử dụng biến môi trường hệ thống

Set biến môi trường trước khi chạy:

```bash
# Linux/macOS
export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=YOUR_ACTUAL_TOKEN_HERE"

# Windows PowerShell
$env:MCP_ENDPOINT = "wss://api.xiaozhi.me/mcp/?token=YOUR_ACTUAL_TOKEN_HERE"

# Sau đó chạy
docker-compose up -d
```

### Cách 3: Sử dụng file .env (Tùy chọn)

Nếu muốn dùng file .env, tạo file `.env` trong thư mục gốc:

```bash
# Tạo file .env
echo 'MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_ACTUAL_TOKEN_HERE' > .env
```

Docker Compose sẽ tự động load biến từ file `.env`.

### Kiểm tra cấu hình

Đảm bảo file `mcp_config.json` đã được cấu hình đúng với các server bạn muốn chạy.

## Sử dụng

### Quick Start với Setup Script

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows PowerShell:**
```powershell
.\setup.ps1
```

Setup script sẽ tự động:
1. Kiểm tra Docker và Docker Compose
2. Hỏi token và cấu hình vào docker-compose.yml
3. Build Docker image
4. Khởi động containers

### Build và chạy thủ công

```bash
# Build image
docker-compose build

# Chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f

# Xem logs của một service cụ thể
docker-compose logs -f mcp-servers
```

### Dừng và xóa

```bash
# Dừng containers
docker-compose stop

# Dừng và xóa containers
docker-compose down

# Xóa cả volumes (cẩn thận!)
docker-compose down -v
```

### Khởi động lại

```bash
# Khởi động lại tất cả services
docker-compose restart

# Khởi động lại một service cụ thể
docker-compose restart mcp-servers
```

## Development Mode

Để phát triển với hot-reload, file source code đã được mount vào container:

```yaml
volumes:
  - ./:/app
```

Mỗi khi bạn thay đổi code, chỉ cần restart container:

```bash
docker-compose restart mcp-servers
```

## Production Mode

Để chạy production, comment dòng volume trong `docker-compose.yml`:

```yaml
# volumes:
#   - ./:/app
```

Sau đó rebuild:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### 1. Container không khởi động

```bash
# Xem logs chi tiết
docker-compose logs mcp-servers

# Kiểm tra trạng thái
docker-compose ps
```

### 2. Lỗi kết nối WebSocket

- Kiểm tra biến `MCP_ENDPOINT` trong `docker-compose.yml` hoặc biến môi trường
- Đảm bảo token còn hạn
- Kiểm tra kết nối internet

```bash
# Kiểm tra biến môi trường trong container
docker-compose exec mcp-servers env | grep MCP_ENDPOINT

# Test kết nối từ trong container
docker-compose exec mcp-servers ping -c 3 api.xiaozhi.me
```

### 3. Module không tìm thấy

```bash
# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### 4. Xem logs real-time

```bash
# Tất cả services
docker-compose logs -f

# Chỉ 100 dòng cuối
docker-compose logs --tail=100 -f mcp-servers
```

### 5. Vào trong container để debug

```bash
docker-compose exec mcp-servers bash

# Hoặc nếu bash không có
docker-compose exec mcp-servers sh
```

## Multi-Service Setup

Nếu bạn cần chạy thêm các service phụ trợ (mp3-proxy, invidious-proxy), uncomment các service trong `docker-compose.yml`:

```yaml
services:
  mcp-servers:
    # ... existing config ...
    depends_on:
      - mp3-proxy
      - invidious-proxy

  mp3-proxy:
    image: your-mp3-proxy-image
    # ... config ...

  invidious-proxy:
    image: your-invidious-proxy-image
    # ... config ...
```

## Resource Limits

Để giới hạn tài nguyên, thêm vào service trong `docker-compose.yml`:

```yaml
services:
  mcp-servers:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Health Checks

Thêm health check vào service:

```yaml
services:
  mcp-servers:
    # ... existing config ...
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Backup và Restore

### Backup logs

```bash
docker-compose logs > backup-logs-$(date +%Y%m%d).txt
```

### Export container

```bash
docker export mcp-xiaozhi-vietnam > mcp-backup.tar
```

## Security Best Practices

1. **Không commit file .env** vào Git
2. **Sử dụng secrets** cho production:
   ```yaml
   services:
     mcp-servers:
       secrets:
         - mcp_token
   secrets:
     mcp_token:
       file: ./secrets/mcp_token.txt
   ```
3. **Chạy với non-root user** (đã được cấu hình trong Dockerfile)
4. **Cập nhật base image thường xuyên**

## Performance Tuning

### Giảm kích thước image

```dockerfile
# Sử dụng multi-stage build
FROM python:3.12-slim as builder
# ... build dependencies ...

FROM python:3.12-slim
COPY --from=builder /app /app
```

### Tối ưu layer caching

Dockerfile đã được tối ưu với việc copy `requirements.txt` trước để tận dụng Docker layer caching.

## Monitoring

### Xem resource usage

```bash
# CPU, Memory usage
docker stats mcp-xiaozhi-vietnam

# Disk usage
docker system df
```

### Log rotation

Đã được cấu hình trong `docker-compose.yml`:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## CI/CD Integration

### GitHub Actions example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run mcp-servers python -m pytest
```

## Useful Commands

```bash
# Xem tất cả containers
docker ps -a

# Xem images
docker images

# Dọn dẹp unused resources
docker system prune -a

# Xem network
docker network ls

# Inspect container
docker inspect mcp-xiaozhi-vietnam

# Copy file từ container
docker cp mcp-xiaozhi-vietnam:/app/logs ./local-logs
```

## Support

Nếu gặp vấn đề, hãy:
1. Kiểm tra logs: `docker-compose logs -f`
2. Kiểm tra file `.env`
3. Đảm bảo Docker daemon đang chạy
4. Kiểm tra port conflicts
5. Xem issues trên GitHub repository

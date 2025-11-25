# Troubleshooting Guide

## 🔴 Lỗi WebSocket 4004 Internal Server Error

### Triệu chứng
```
ERROR - [server] received 4004 (private use) Internal server error
WARNING - [server] Connection closed (attempt X)
```

### ⚠️ Quan trọng
**Đây là lỗi từ server WebSocket, KHÔNG phải lỗi code!**

### Nguyên nhân
1. Token hết hạn hoặc không hợp lệ
2. Quá nhiều servers (server giới hạn connections)
3. Rate limiting
4. Server đang bảo trì

### Giải pháp

#### 1. Lấy token mới
- Truy cập https://xiaozhi.me
- Lấy token mới
- Cập nhật file `.env` hoặc `docker-compose.yml`

#### 2. Giảm số servers
Chỉnh `mcp_config.json`:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator.py"],
      "type": "stdio"
    }
  }
}
```

Hoặc dùng config tối thiểu:
```bash
# Copy minimal config
cp mcp_config.minimal.json mcp_config.json

# Restart
docker-compose restart
```

#### 3. Đợi và thử lại
```bash
# Stop
docker-compose down

# Đợi 5-10 phút

# Start lại
docker-compose up -d
```

#### 4. Test với 1 server
```bash
# Local
python mcp_pipe.py calculator.py

# Docker
docker-compose down
# Edit mcp_config.json (chỉ 1 server)
docker-compose up -d
```

## 🔴 Lỗi: Module not found

### Giải pháp
```bash
pip install -r requirements.txt
```

## 🔴 Lỗi: MCP_ENDPOINT not set

### Giải pháp

**Local:**
```bash
# Tạo .env
echo "MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN" > .env
```

**Docker:**
Cập nhật `docker-compose.yml`:
```yaml
environment:
  - MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN
```

## 💡 Best Practices

1. **Chỉ chạy servers cần thiết**
   - Disable servers không dùng
   - Tránh chạy quá nhiều servers cùng lúc

2. **Monitor logs**
   ```bash
   # Local
   python mcp_pipe.py 2>&1 | tee mcp.log
   
   # Docker
   docker-compose logs -f
   ```

3. **Token management**
   - Lưu token an toàn
   - Lấy token mới khi cần
   - Không commit token vào Git

4. **Gradual scaling**
   - Bắt đầu với 1 server
   - Thêm dần nếu cần
   - Monitor errors

## 🔗 Xem thêm

- [README.md](README.md) - Hướng dẫn chính
- [DOCKER.md](DOCKER.md) - Docker guide
- [mcp_config.minimal.json](mcp_config.minimal.json) - Config tối thiểu

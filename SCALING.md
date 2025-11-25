# Scaling MCP Servers

Hướng dẫn chạy nhiều MCP servers khi gặp giới hạn connections.

## 🔍 Vấn đề

Server WebSocket (api.xiaozhi.me) giới hạn số connections đồng thời từ một token:
- Thường: 1-2 connections/token
- Khi vượt quá: Error 4004 "Internal server error"

**Đây KHÔNG phải lỗi của Docker hay code!**

## 💡 Giải pháp

### Cách 1: Sử dụng nhiều tokens (Khuyến nghị)

Tạo nhiều tokens từ xiaozhi.me và phân bổ cho mỗi server.

**Config:** `mcp_config.multi-token.json`

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator.py"],
      "type": "stdio",
      "env": {
        "MCP_ENDPOINT": "wss://api.xiaozhi.me/mcp/?token=TOKEN_1"
      }
    },
    "VnExpress": {
      "command": "python",
      "args": ["VnExpress.py"],
      "type": "stdio",
      "env": {
        "MCP_ENDPOINT": "wss://api.xiaozhi.me/mcp/?token=TOKEN_2"
      }
    }
  }
}
```

**Sử dụng:**
```bash
# Copy config
cp mcp_config.multi-token.json mcp_config.json

# Update tokens
# Edit mcp_config.json và thay TOKEN_1, TOKEN_2, etc.

# Run
python mcp_pipe.py
```

**Docker:**
```yaml
# docker-compose.yml
services:
  mcp-servers:
    image: ghcr.io/OWNER/REPO:latest-alpine
    environment:
      # Default token (fallback)
      - MCP_ENDPOINT=${MCP_ENDPOINT}
    volumes:
      - ./mcp_config.json:/app/mcp_config.json
```

### Cách 2: Connection Multiplexing (Experimental)

Chia sẻ 1 connection cho nhiều servers.

**File:** `mcp_multiplexer.py`

```bash
# Run multiplexer
python mcp_multiplexer.py
```

**Ưu điểm:**
- Chỉ cần 1 token
- Tất cả servers chạy đồng thời

**Nhược điểm:**
- Phức tạp hơn
- Cần test kỹ
- Có thể có latency

### Cách 3: Sequential Execution

Chạy servers lần lượt, mỗi server 5 phút.

**File:** `mcp_sequential.py`

```bash
# Run sequential
python mcp_sequential.py
```

**Ưu điểm:**
- Đơn giản
- Chỉ cần 1 token
- Không bị giới hạn connections

**Nhược điểm:**
- Không có tất cả servers cùng lúc
- Phải đợi rotation

### Cách 4: Giảm số servers (Đơn giản nhất)

Chỉ chạy servers thực sự cần thiết.

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

## 📊 So sánh

| Cách | Tokens | Complexity | Đồng thời | Khuyến nghị |
|------|--------|------------|-----------|-------------|
| Multi-token | Nhiều | Thấp | ✅ | ⭐⭐⭐⭐⭐ |
| Multiplexing | 1 | Cao | ✅ | ⭐⭐⭐ |
| Sequential | 1 | Thấp | ❌ | ⭐⭐ |
| Giảm servers | 1 | Rất thấp | ✅ | ⭐⭐⭐⭐ |

## 🎯 Khuyến nghị

### Cho Development:
```bash
# Chỉ chạy 1-2 servers
cp mcp_config.minimal.json mcp_config.json
python mcp_pipe.py
```

### Cho Production:
```bash
# Sử dụng nhiều tokens
# 1. Tạo tokens từ xiaozhi.me
# 2. Cập nhật mcp_config.multi-token.json
# 3. Deploy

cp mcp_config.multi-token.json mcp_config.json
docker-compose up -d
```

## 🔧 Testing

### Test với 1 server:
```bash
python mcp_pipe.py calculator.py
```

### Test với nhiều tokens:
```bash
# Set tokens
export TOKEN_1="wss://..."
export TOKEN_2="wss://..."

# Update config
# Edit mcp_config.multi-token.json

# Run
python mcp_pipe.py
```

### Test multiplexer:
```bash
python mcp_multiplexer.py
```

### Test sequential:
```bash
python mcp_sequential.py
```

## ❓ FAQ

### Q: Tại sao không thể chạy nhiều servers?
**A:** Server WebSocket giới hạn connections/token. Đây là giới hạn từ backend, không phải Docker hay code.

### Q: Docker có vấn đề gì không?
**A:** Không! Docker hoàn toàn bình thường. Vấn đề là từ server WebSocket.

### Q: Tại sao Windows chạy được mà Docker không?
**A:** Có thể do:
1. **Token khác nhau** - Windows dùng token từ .env, Docker dùng placeholder
2. **Config khác nhau** - Số servers khác nhau
3. **Timing** - Windows chạy trước, Docker chạy sau (rate limit)

Chạy `.\verify-docker-config.ps1` để kiểm tra!

### Q: Làm sao biết giới hạn là bao nhiêu?
**A:** Thử nghiệm. Thường là 1-2 connections/token.

### Q: Có cách nào bypass không?
**A:** Không nên bypass. Hãy:
1. Sử dụng nhiều tokens (hợp pháp)
2. Giảm số servers
3. Liên hệ xiaozhi.me để tăng quota

### Q: Multiplexer có ổn định không?
**A:** Experimental. Cần test kỹ trước khi dùng production.

### Q: Nên dùng cách nào?
**A:** 
- **Best:** Multi-token (nếu có nhiều tokens)
- **Good:** Giảm servers (nếu không cần nhiều)
- **OK:** Sequential (nếu chấp nhận không đồng thời)
- **Experimental:** Multiplexing

## 🔗 Xem thêm

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Xử lý lỗi
- [DOCKER.md](DOCKER.md) - Docker guide
- [README.md](README.md) - Main documentation

# VnExpress Tool - Công cụ Tin tức MCP

[![Docker Build](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-release.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-release.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Công cụ MCP để lấy tin tức mới nhất từ VnExpress.net và các chức năng tìm kiếm tin tức.

## Tổng quan

MCP (Model Context Protocol) là một giao thức cho phép máy chủ cung cấp các công cụ có thể được gọi bởi các mô hình ngôn ngữ. Các công cụ cho phép mô hình tương tác với các hệ thống bên ngoài, chẳng hạn như truy vấn cơ sở dữ liệu, gọi API hoặc thực hiện các phép tính. Mỗi công cụ được xác định duy nhất bởi một tên và bao gồm siêu dữ liệu mô tả lược đồ của nó.
- 🔌 Giao tiếp hai chiều giữa AI và các công cụ bên ngoài
- 🔄 Tự động kết nối lại với thời gian chờ tăng dần
- 📊 Truyền dữ liệu thời gian thực
- 🛠️ Giao diện tạo công cụ dễ sử dụng
- 🔒 Giao tiếp WebSocket an toàn
- ⚙️ Hỗ trợ nhiều loại truyền tải (stdio/sse/http)

## Tính năng

- 📰 **Tin tức mới nhất**: Lấy tin nổi bật từ trang chủ VnExpress
- 🏷️ **Phân loại tin tức**: Hỗ trợ nhiều chuyên mục
- 🔍 **Tìm kiếm**: Tìm kiếm tin tức theo từ khóa
- 📖 **Nội dung chi tiết**: Lấy toàn bộ nội dung bài viết
- ⚡ **Real-time**: Cập nhật tin tức theo thời gian thực

## Yêu cầu cài đặt

### Cách 1: Sử dụng Docker (Khuyến nghị)

- Docker Engine 20.10+
- Docker Compose 2.0+

### Cách 2: Cài đặt trực tiếp

- [Python 3.12+](https://www.python.org/downloads/)

## Cài đặt và Chạy

### 🐳 Sử dụng Docker (Khuyến nghị)

#### Cách 1: Sử dụng Setup Script (Dễ nhất)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows PowerShell:**
```powershell
.\setup.ps1
```

Script sẽ tự động:
- Kiểm tra Docker
- Hỏi token và cấu hình
- Build image
- Khởi động containers

#### Cách 2: Cấu hình thủ công

**Bước 1: Cấu hình token**

**Option A: Chỉnh sửa docker-compose.yml (Đơn giản nhất)**

Mở `docker-compose.yml` và thay `YOUR_TOKEN_HERE`:
```yaml
environment:
  - MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_ACTUAL_TOKEN_HERE
```

**Option B: Dùng biến môi trường**
```bash
# Linux/macOS
export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN_HERE"

# Windows PowerShell
$env:MCP_ENDPOINT = "wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN_HERE"
```

**Bước 2: Build và chạy**

```bash
# Sử dụng Docker Compose
docker-compose up -d

# Hoặc sử dụng Makefile (nếu có make)
make build
make up

# Xem logs
docker-compose logs -f
# hoặc
make logs
```

#### 3. Quản lý containers

```bash
# Dừng
docker-compose down

# Khởi động lại
docker-compose restart

# Xem trạng thái
docker-compose ps

# Hoặc dùng Makefile
make down
make restart
make ps
```

#### 4. Tối ưu kích thước (Alpine version)

Để có image nhỏ nhất (~50-80MB thay vì ~150-200MB):

```bash
# Build Alpine version
docker-compose -f docker-compose.alpine.yml build

# Run
docker-compose -f docker-compose.alpine.yml up -d

# Hoặc dùng Makefile
make build-alpine
make up-alpine

# So sánh kích thước
make compare
```

📖 **Xem thêm**: [OPTIMIZATION.md](OPTIMIZATION.md) để biết chi tiết về tối ưu hóa

📖 **Xem thêm**: 
- [GHCR.md](GHCR.md) - Sử dụng images từ GitHub Container Registry
- [DOCKER.md](DOCKER.md) - Chi tiết về Docker deployment
- [OPTIMIZATION.md](OPTIMIZATION.md) - Tối ưu hóa Docker image
- [.github/workflows/README.md](.github/workflows/README.md) - CI/CD workflows

## ⚠️ Lưu ý quan trọng

### Lỗi WebSocket 4004

Nếu gặp lỗi `4004 Internal server error`:

1. **Token hết hạn** - Lấy token mới từ https://xiaozhi.me
2. **Quá nhiều servers** - Chỉ chạy 1-2 servers trong `mcp_config.json`
3. **Rate limiting** - Đợi 5-10 phút rồi thử lại

Xem chi tiết: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🔄 CI/CD

Dự án sử dụng GitHub Actions để tự động build và push Docker images lên GitHub Container Registry (GHCR):

- **Multi-arch builds**: Tự động build cho amd64 và arm64
- **GitHub Container Registry**: Images được push lên ghcr.io
- **Auto-deploy**: Tự động push khi commit vào main/develop
- **Release automation**: Tự động tạo release và push images khi push tag

### 📦 Pull Images từ GHCR

```bash
# Latest version (Alpine Linux)
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO:latest

# Specific version
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO:v1.0.0
```

Xem chi tiết tại [Workflows Documentation](.github/workflows/README.md)

### 💻 Cài đặt trực tiếp

#### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

#### 2. Thiết lập biến môi trường

```bash
# Linux/macOS
export MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN_HERE

# Windows PowerShell
$env:MCP_ENDPOINT = "wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN_HERE"
```

#### 3. Chạy

##### Chạy riêng lẻ
```bash
python mcp_pipe.py VnExpress.py
```

##### Chạy tất cả servers
```bash
python mcp_pipe.py
```

Cấu hình trong `mcp_config.json`:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator.py"],
      "type": "stdio"
    },
    "VnExpress": {
      "command": "python",
      "args": ["VnExpress.py"],
      "type": "stdio"
    },
    "dantri_news": {
      "command": "python",
      "args": ["dantri_news.py"],
      "type": "stdio"
    },
    "radio": {
      "command": "python",
      "args": ["radio.py"],
      "type": "stdio"
    }
  }
}
```

*Hỗ trợ các loại truyền tải: stdio/sse/http*

## Cấu trúc dự án

- `mcp_pipe.py`: Ống giao tiếp chính xử lý các kết nối WebSocket và quản lý quy trình
- `VnExpress.py`: Triển khai Công cụ MCP để lấy tin tức mới nhất từ VnExpress.net và các chức năng tìm kiếm tin tức
- `requirements.txt`: Các phụ thuộc của dự án

## Máy chủ điều khiển bằng cấu hình

Chỉnh sửa tệp `mcp_config.json` để cấu hình danh sách máy chủ (cũng có thể đặt biến môi trường `MCP_CONFIG` trỏ đến tệp cấu hình khác).

Hướng dẫn cấu hình:

- Không có tham số sẽ khởi động tất cả các máy chủ đã cấu hình (tự động bỏ qua các mục `disabled: true`)
- Có tham số sẽ chạy một tệp kịch bản cục bộ duy nhất
- `type=stdio` khởi động trực tiếp; `type=sse/http` thông qua proxy `python -m mcp_proxy`

## Các công cụ có sẵn

### 1. `get_vnexpress_news` - Lấy tin tức theo chuyên mục

**Cú pháp:**
```python
get_vnexpress_news(category: str = "home", limit: int = 10)
```

**Chuyên mục hỗ trợ:**
- `home`: Trang chủ (tin nổi bật)
- `thoi-su`: Thời sự
- `goc-nhin`: Góc nhìn
- `the-gioi`: Thế giới
- `kinh-doanh`: Kinh doanh
- `bat-dong-san`: Bất động sản
- `khoa-hoc`: Khoa học
- `giai-tri`: Giải trí
- `the-thao`: Thể thao
- `phap-luat`: Pháp luật
- `giao-duc`: Giáo dục
- `suc-khoe`: Sức khỏe
- `doi-song`: Đời sống
- `du-lich`: Du lịch
- `so-hoa`: Số hóa
- `xe`: Xe

**Ví dụ sử dụng:**
```python
get_vnexpress_news("home", 5)          # 5 tin nổi bật
get_vnexpress_news("thoi-su", 10)      # 10 tin thời sự
get_vnexpress_news("the-thao", 8)      # 8 tin thể thao
```

### 2. `get_article_content` - Lấy nội dung chi tiết bài viết

**Cú pháp:**
```python
get_article_content(url: str)
```

**Ví dụ:**
```python
get_article_content("https://vnexpress.net/title-123456.html")
```

### 3. `search_vnexpress_news` - Tìm kiếm tin tức

**Cú pháp:**
```python
search_vnexpress_news(keyword: str, limit: int = 5)
```

**Ví dụ:**
```python
search_vnexpress_news("covid", 10)
search_vnexpress_news("bóng đá", 5)
search_vnexpress_news("kinh tế", 8)
```

## Ví dụ kết quả

### Tin tức mới nhất
```json
{
  "success": true,
  "category": "thoi-su",
  "total_articles": 10,
  "articles": [
    {
      "title": "Thủ tướng: 'Chính phủ quyết tâm thực hiện mục tiêu tăng trưởng 6,5-7%'",
      "url": "https://vnexpress.net/thu-tuong-chinh-phu-quyet-tam-thuc-hien-muc-tieu-tang-truong-6-5-7-4567890.html",
      "description": "Thủ tướng Phạm Minh Chính cho biết Chính phủ sẽ tập trung nguồn lực...",
      "time": "2 giờ trước",
      "category": "thoi-su"
    }
  ],
  "timestamp": "2024-11-03 15:30:00",
  "source": "VnExpress.net"
}
```

### Nội dung bài viết
```json
{
  "success": true,
  "title": "Tiêu đề bài viết",
  "description": "Mô tả ngắn gọn...",
  "content": "Nội dung đầy đủ của bài viết...",
  "author": "Tên tác giả",
  "publish_time": "Thứ 7, 3/11/2024, 15:30",
  "url": "https://vnexpress.net/...",
  "timestamp": "2024-11-03 15:30:00"
}
```

## Ví dụ tích hợp với AI

```
AI: "Tin tức mới nhất hôm nay?"
→ get_vnexpress_news("home", 5)

AI: "Có tin gì về bóng đá không?"
→ search_vnexpress_news("bóng đá", 5)

AI: "Tin tức kinh tế mới nhất?"
→ get_vnexpress_news("kinh-doanh", 8)

AI: "Đọc chi tiết bài này giúp tôi: [URL]"
→ get_article_content(url)
```

## Xử lý lỗi

### Lỗi kết nối
```json
{
  "success": false,
  "error": "Network error: Connection timeout"
}
```

### Lỗi parsing
```json
{
  "success": false, 
  "error": "Unexpected error: No articles found"
}
```

## Lưu ý quan trọng

### 1. **Tuân thủ robots.txt**
Tool được thiết kế để lấy thông tin công khai và không vi phạm robots.txt của VnExpress.

### 2. **Rate Limiting**
Tránh gọi quá nhiều request trong thời gian ngắn để không bị chặn IP.

### 3. **Cấu trúc website có thể thay đổi**
VnExpress có thể thay đổi cấu trúc HTML, tool sẽ cần cập nhật selector tương ứng.

### 4. **Mã hóa UTF-8**
Tool đã xử lý encoding UTF-8 cho tiếng Việt trên Windows.

## Troubleshooting

### 1. Module không tìm thấy
```bash
pip install beautifulsoup4 lxml requests
```

### 2. Không tìm thấy bài viết
- Kiểm tra kết nối internet
- VnExpress có thể đã thay đổi cấu trúc
- Thử chuyên mục khác

### 3. Encoding lỗi
Code đã xử lý UTF-8 tự động.

### 4. Blocked IP
Nếu bị chặn, đợi một thời gian hoặc thay đổi User-Agent.

## Phát triển thêm

Có thể mở rộng:
- Hỗ trợ nhiều trang tin tức khác
- Lưu cache tin tức
- Phân tích sentiment
- Tóm tắt tin tức tự động
- Export PDF/Word

## Khuyến nghị sử dụng

1. **Sử dụng có trách nhiệm**: Không spam request
2. **Tôn trọng bản quyền**: Chỉ lấy thông tin cần thiết
3. **Cập nhật thường xuyên**: Check code khi website thay đổi
4. **Backup data**: Lưu tin tức quan trọng

## License

MIT License - Sử dụng cho mục đích học tập và nghiên cứu.
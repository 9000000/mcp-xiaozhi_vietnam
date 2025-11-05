# News Tool - Công cụ Tin tức MCP

Công cụ MCP để lấy tin tức mới nhất từ VnExpress.net và các chức năng tìm kiếm tin tức.

## Tính năng

- 📰 **Tin tức mới nhất**: Lấy tin nổi bật từ trang chủ VnExpress
- 🏷️ **Phân loại tin tức**: Hỗ trợ nhiều chuyên mục
- 🔍 **Tìm kiếm**: Tìm kiếm tin tức theo từ khóa
- 📖 **Nội dung chi tiết**: Lấy toàn bộ nội dung bài viết
- ⚡ **Real-time**: Cập nhật tin tức theo thời gian thực

## Yêu cầu cài đặt

```bash
pip install requests beautifulsoup4 lxml
```

## Cách chạy

### Chạy riêng lẻ
```bash
python mcp_pipe.py news.py
```

### Chạy cùng các tool khác
Cập nhật file `mcp_config.json`:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator.py"],
      "type": "stdio"
    },
    "weather": {
      "command": "python",
      "args": ["weather.py"],
      "type": "stdio"
    },
    "news": {
      "command": "python",
      "args": ["news.py"],
      "type": "stdio"
    }
  }
}
```

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
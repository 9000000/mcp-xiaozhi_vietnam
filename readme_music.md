# Music Tool - Công cụ Âm nhạc MCP

Công cụ MCP để tìm kiếm thông tin bài hát, playlist từ ZingMP3 và hướng dẫn nghe nhạc hợp pháp.

## ⚠️ Lưu ý quan trọng về Bản quyền

- **KHÔNG download** hay cung cấp link tải nhạc trái phép
- **CHỈ** lấy thông tin metadata (tên bài, ca sĩ, album)  
- **Hướng dẫn** mở website chính thức để nghe nhạc hợp pháp
- **Tuân thủ** luật bản quyền âm nhạc

## Tính năng

- 🔍 **Tìm kiếm bài hát**: Lấy thông tin metadata từ ZingMP3
- 📋 **Playlist**: Tìm kiếm các playlist theo chủ đề
- 🏆 **BXH**: Lấy top bài hát trending
- 🌐 **Mở trình duyệt**: Hướng dẫn nghe nhạc hợp pháp
- ℹ️ **Thông tin only**: Không cung cấp link download

## Yêu cầu cài đặt

```bash
pip install requests beautifulsoup4 lxml
```

## Cách chạy

### Chạy riêng lẻ
```bash
python mcp_pipe.py music.py
```

### Chạy cùng các tool khác
Cập nhật `mcp_config.json`:
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
    },
    "music": {
      "command": "python",
      "args": ["music.py"],
      "type": "stdio"
    }
  }
}
```

## Các công cụ có sẵn

### 1. `search_zingmp3_songs` - Tìm kiếm bài hát

**Cú pháp:**
```python
search_zingmp3_songs(keyword: str, limit: int = 10)
```

**Ví dụ:**
```python
search_zingmp3_songs("Nơi này có anh", 5)
search_zingmp3_songs("Sơn Tùng MTP", 10)  
search_zingmp3_songs("Em của ngày hôm qua", 3)
```

**Kết quả:**
```json
{
  "success": true,
  "keyword": "Nơi này có anh",
  "total_songs": 5,
  "songs": [
    {
      "title": "Nơi Này Có Anh", 
      "artist": "Sơn Tùng M-TP",
      "duration": "04:10",
      "page_url": "https://zingmp3.vn/bai-hat/...",
      "thumbnail": "https://...",
      "keyword": "Nơi này có anh"
    }
  ],
  "note": "Chỉ hiển thị thông tin metadata, không cung cấp link download"
}
```

### 2. `get_zingmp3_playlists` - Tìm playlist

**Cú pháp:**
```python
get_zingmp3_playlists(keyword: str, limit: int = 5)
```

**Ví dụ:**
```python
get_zingmp3_playlists("nhạc trẻ", 5)
get_zingmp3_playlists("K-Pop", 3)
get_zingmp3_playlists("ballad", 10)
```

### 3. `get_zingmp3_top_songs` - Top bài hát

**Cú pháp:**
```python
get_zingmp3_top_songs(category: str = "vn", limit: int = 20)
```

**Categories:**
- `vn`: Việt Nam
- `usuk`: Âu Mỹ
- `kpop`: K-Pop  
- `others`: Khác

**Ví dụ:**
```python
get_zingmp3_top_songs("vn", 10)      # Top 10 V-Pop
get_zingmp3_top_songs("kpop", 15)    # Top 15 K-Pop
get_zingmp3_top_songs("usuk", 20)    # Top 20 US-UK
```

### 4. `open_zingmp3_in_browser` - Mở trình duyệt

**Cú pháp:**
```python
open_zingmp3_in_browser(song_title: str, artist: str = "")
```

**Ví dụ:**
```python
open_zingmp3_in_browser("Nơi này có anh", "Sơn Tùng MTP")
open_zingmp3_in_browser("See Tình")
```

**Kết quả:**
```json
{
  "success": true,
  "song": "Nơi này có anh",
  "artist": "Sơn Tùng MTP", 
  "search_url": "https://zingmp3.vn/tim-kiem/bai-hat?q=...",
  "browser_commands": {
    "windows": "start \"\" \"https://...\"",
    "macos": "open \"https://...\"", 
    "linux": "xdg-open \"https://...\""
  },
  "message": "Sử dụng lệnh trên để mở ZingMP3 trong trình duyệt"
}
```

## Cách sử dụng với AI

```
AI: "Tìm bài hát của Sơn Tùng MTP"
→ search_zingmp3_songs("Sơn Tùng MTP", 10)

AI: "Top 10 bài hát Việt Nam hiện tại?"
→ get_zingmp3_top_songs("vn", 10)

AI: "Tìm playlist nhạc trẻ"  
→ get_zingmp3_playlists("nhạc trẻ", 5)

AI: "Mở bài 'Nơi này có anh' để nghe"
→ open_zingmp3_in_browser("Nơi này có anh", "Sơn Tùng MTP")
```

## Lưu ý Pháp lý

### ✅ Được phép:
- Tìm kiếm thông tin bài hát (metadata)
- Lấy danh sách playlist công khai
- Hướng dẫn truy cập website chính thức
- Hiển thị BXH âm nhạc

### ❌ KHÔNG được phép:
- Download/stream nhạc trái phép
- Cung cấp link tải trực tiếp
- Bypass bản quyền
- Sao chép nội dung âm thanh

## Hướng dẫn Nghe nhạc Hợp pháp

### 1. **Qua Website chính thức**
```bash
# Windows
start "" "https://zingmp3.vn/tim-kiem/bai-hat?q=ten-bai-hat"

# macOS  
open "https://zingmp3.vn/tim-kiem/bai-hat?q=ten-bai-hat"

# Linux
xdg-open "https://zingmp3.vn/tim-kiem/bai-hat?q=ten-bai-hat"
```

### 2. **Các nền tảng khác**
- Spotify
- Apple Music  
- YouTube Music
- JOOX
- NCT

## Troubleshooting

### 1. Không tìm thấy bài hát
- Kiểm tra chính tả từ khóa
- Thử tìm theo tên ca sĩ
- ZingMP3 có thể đã thay đổi cấu trúc

### 2. Lỗi kết nối
```bash
pip install --upgrade requests beautifulsoup4
```

### 3. Encoding issues
Code đã xử lý UTF-8 cho tiếng Việt.

### 4. Bị chặn IP
- Đợi một lúc rồi thử lại
- Đổi User-Agent string
- Sử dụng VPN nếu cần

## Phát triển thêm

### Có thể mở rộng:
- ✅ Hỗ trợ NCT, Spotify API
- ✅ Lưu danh sách yêu thích  
- ✅ Phân tích xu hướng âm nhạc
- ✅ Recommendation engine
- ❌ Stream/Download (vi phạm bản quyền)

### Tích hợp API hợp pháp:
```python
# Spotify Web API (cần đăng ký)
# YouTube Music API  
# Apple Music API
# Last.fm API
```

## Khuyến nghị

1. **Tôn trọng bản quyền**: Chỉ nghe nhạc từ nguồn hợp pháp
2. **Hỗ trợ nghệ sĩ**: Mua/stream từ nền tảng chính thức
3. **Sử dụng có trách nhiệm**: Không spam request
4. **Cập nhật thường xuyên**: Website có thể thay đổi cấu trúc

## License & Disclaimer

- **MIT License** cho code
- **Chỉ dùng cho mục đích học tập/nghiên cứu**
- **Không chịu trách nhiệm** về việc vi phạm bản quyền
- **Người dùng tự chịu trách nhiệm** tuân thủ pháp luật
# Weather Tool - Công cụ Thời tiết MCP

Công cụ MCP để lấy thông tin thời tiết hiện tại và dự báo thời tiết cho các thành phố trên thế giới.

## Tính năng

- 🌤️ **Thời tiết hiện tại**: Lấy thông tin thời tiết real-time
- 📅 **Dự báo thời tiết**: Dự báo 1-5 ngày tới (mỗi 3 giờ)
- 🌍 **Hỗ trợ toàn cầu**: Thành phố bất kỳ trên thế giới
- 🇻🇳 **Tiếng Việt**: Mô tả thời tiết bằng tiếng Việt
- 📊 **Thông tin chi tiết**: Nhiệt độ, độ ẩm, áp suất, gió, tầm nhìn

## Yêu cầu cài đặt

### 1. Cài đặt dependencies
```bash
pip install requests mcp
```

### 2. Đăng ký API Key miễn phí
1. Truy cập: https://openweathermap.org/api
2. Tạo tài khoản miễn phí
3. Lấy API key từ dashboard
4. Thay thế `YOUR_API_KEY_HERE` trong file `weather.py`

```python
api_key = "your_actual_api_key_here"
```

## Cách chạy

### Chạy riêng lẻ
```bash
python mcp_pipe.py weather.py
```

### Chạy cùng các tool khác
Tạo/chỉnh sửa file `mcp_config.json`:
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
    }
  }
}
```

Chạy tất cả:
```bash
python mcp_pipe.py
```

## Các công cụ có sẵn

### 1. `get_weather` - Thời tiết hiện tại

**Cú pháp:**
```python
get_weather(city: str, country_code: str = "VN")
```

**Tham số:**
- `city`: Tên thành phố (bắt buộc)
- `country_code`: Mã quốc gia ISO 3166 (tùy chọn, mặc định "VN")

**Ví dụ sử dụng:**
```python
get_weather("Ho Chi Minh City", "VN")
get_weather("Hanoi", "VN") 
get_weather("Tokyo", "JP")
get_weather("New York", "US")
get_weather("London", "GB")
```

**Kết quả trả về:**
```json
{
  "success": true,
  "data": {
    "city": "Ho Chi Minh City",
    "country": "VN",
    "temperature": 28.5,
    "feels_like": 32.1,
    "humidity": 78,
    "pressure": 1013,
    "weather": "mây rải rác",
    "wind_speed": 3.2,
    "visibility": 10000,
    "timestamp": "2024-11-03 14:30:15"
  },
  "message": "Weather in Ho Chi Minh City: 28.5°C, mây rải rác"
}
```

### 2. `get_weather_forecast` - Dự báo thời tiết

**Cú pháp:**
```python
get_weather_forecast(city: str, country_code: str = "VN", days: int = 3)
```

**Tham số:**
- `city`: Tên thành phố (bắt buộc)
- `country_code`: Mã quốc gia (tùy chọn, mặc định "VN")
- `days`: Số ngày dự báo 1-5 (tùy chọn, mặc định 3)

**Ví dụ sử dụng:**
```python
get_weather_forecast("Hanoi", "VN", 2)
get_weather_forecast("Da Nang", "VN", 5)
get_weather_forecast("Bangkok", "TH", 1)
```

**Kết quả trả về:**
```json
{
  "success": true,
  "city": "Hanoi",
  "country": "VN",
  "forecasts": [
    {
      "datetime": "2024-11-03 15:00:00",
      "temperature": 25.2,
      "weather": "trời quang",
      "humidity": 65,
      "wind_speed": 2.1
    },
    {
      "datetime": "2024-11-03 18:00:00", 
      "temperature": 23.8,
      "weather": "mây ít",
      "humidity": 72,
      "wind_speed": 1.8
    }
  ],
  "message": "3-day forecast for Hanoi"
}
```

## Mã quốc gia phổ biến

| Quốc gia | Mã | Ví dụ thành phố |
|----------|----|-----------------| 
| Việt Nam | VN | Ho Chi Minh City, Hanoi, Da Nang |
| Mỹ | US | New York, Los Angeles, Chicago |
| Nhật Bản | JP | Tokyo, Osaka, Kyoto |
| Anh | GB | London, Manchester, Birmingham |
| Pháp | FR | Paris, Lyon, Marseille |
| Đức | DE | Berlin, Hamburg, Munich |
| Thái Lan | TH | Bangkok, Chiang Mai, Phuket |
| Singapore | SG | Singapore |
| Malaysia | MY | Kuala Lumpur, Johor Bahru |
| Indonesia | ID | Jakarta, Surabaya, Medan |

## Xử lý lỗi

Tool sẽ trả về `success: false` kèm thông báo lỗi trong các trường hợp:

### Lỗi API Key
```json
{
  "success": false,
  "error": "Network error: 401 Client Error: Unauthorized"
}
```
**Giải pháp:** Kiểm tra API key có đúng không

### Lỗi tên thành phố
```json
{
  "success": false, 
  "error": "Network error: 404 Client Error: Not Found"
}
```
**Giải pháp:** Kiểm tra tên thành phố và mã quốc gia

### Lỗi kết nối mạng
```json
{
  "success": false,
  "error": "Network error: HTTPSConnectionPool timeout"
}
```
**Giải pháp:** Kiểm tra kết nối internet

## Thông tin API

- **Nhà cung cấp**: OpenWeatherMap
- **Giới hạn miễn phí**: 1,000 calls/ngày
- **Tần suất cập nhật**: 10 phút
- **Độ chính xác**: Dự báo 5 ngày, mỗi 3 giờ

## Ví dụ tích hợp với AI

Khi AI muốn biết thời tiết, nó có thể gọi:

```
AI: "Thời tiết Hà Nội hôm nay như thế nào?"
→ get_weather("Hanoi", "VN")
→ Trả về: "Hà Nội hiện tại 25°C, trời quang, độ ẩm 60%..."

AI: "Dự báo thời tiết TP.HCM 3 ngày tới?"  
→ get_weather_forecast("Ho Chi Minh City", "VN", 3)
→ Trả về dự báo chi tiết 3 ngày
```

## Logging

Tool ghi log các hoạt động:
- Yêu cầu thời tiết
- Kết quả trả về
- Lỗi xảy ra

Xem log trong console khi chạy tool.

## Troubleshooting

### 1. Module 'requests' not found
```bash
pip install requests
```

### 2. API key không hoạt động
- Đảm bảo đã active API key (có thể mất vài phút)
- Kiểm tra subscription plan
- Xem usage trong dashboard

### 3. Encoding lỗi trên Windows
Code đã xử lý UTF-8 tự động cho Windows console.

### 4. Timeout error
Tăng timeout trong code nếu mạng chậm:
```python
response = requests.get(url, params=params, timeout=30)
```

## Phát triển thêm

Có thể mở rộng thêm các tính năng:
- Air quality index
- UV index  
- Weather alerts
- Historical weather data
- Weather maps

## License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.
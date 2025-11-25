from mcp.server.fastmcp import FastMCP
import sys
import logging
import requests
import json
import os
from datetime import datetime

logger = logging.getLogger('Weather')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city: str, country_code: str = "VN") -> dict:
    """Get current weather information for a specific city. Use country_code like 'VN', 'US', 'JP', etc."""
    try:
        # Sử dụng OpenWeatherMap API (miễn phí)
        # Bạn cần đăng ký tại: https://openweathermap.org/api
        api_key = os.getenv("OPENWEATHER_API_KEY")
        
        # API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country_code}",
            "appid": api_key,
            "units": "metric",  # Celsius
            "lang": "vi"  # Tiếng Việt
        }
        
        logger.info(f"Getting weather for: {city}, {country_code}")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Trích xuất thông tin quan trọng
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", "N/A"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"Weather data retrieved for {city}: {weather_info['temperature']}°C, {weather_info['weather']}")
        
        return {
            "success": True,
            "data": weather_info,
            "message": f"Weather in {weather_info['city']}: {weather_info['temperature']}°C, {weather_info['weather']}"
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {e}")
        return {"success": False, "error": f"Network error: {str(e)}"}
    except KeyError as e:
        logger.error(f"Data parsing error: {e}")
        return {"success": False, "error": f"Invalid response format: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

@mcp.tool()
def get_weather_forecast(city: str, country_code: str = "VN", days: int = 3) -> dict:
    """Get weather forecast for multiple days (1-5 days)."""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
        
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": f"{city},{country_code}",
            "appid": api_key,
            "units": "metric",
            "lang": "vi",
            "cnt": min(days * 8, 40)  # 8 forecasts per day (every 3 hours), max 40
        }
        
        logger.info(f"Getting {days}-day forecast for: {city}, {country_code}")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        forecasts = []
        for item in data["list"]:
            forecast = {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"]
            }
            forecasts.append(forecast)
        
        return {
            "success": True,
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": forecasts,
            "message": f"{days}-day forecast for {data['city']['name']}"
        }
        
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")

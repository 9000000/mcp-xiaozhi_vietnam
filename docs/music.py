from mcp.server.fastmcp import FastMCP
import sys
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import urllib.parse

logger = logging.getLogger('Music')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("Music")

@mcp.tool()
def search_zingmp3_songs(keyword: str, limit: int = 10) -> dict:
    """
    Tìm kiếm bài hát trên ZingMP3 theo từ khóa.
    Trả về thông tin metadata (tên bài, ca sĩ, album) chứ KHÔNG phải link download.
    """
    try:
        # URL tìm kiếm ZingMP3
        search_query = urllib.parse.quote(keyword)
        search_url = f"https://zingmp3.vn/tim-kiem/bai-hat?q={search_query}"
        
        logger.info(f"Searching ZingMP3 for: {keyword}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Referer': 'https://zingmp3.vn/',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        songs = []
        
        # Tìm các selector có thể cho bài hát
        selectors = [
            '.list-item .item-song',
            '.zm-card-song',
            '.media-item',
            '.list .media',
            '[data-type="song"]'
        ]
        
        found_songs = []
        for selector in selectors:
            found_songs = soup.select(selector)
            if found_songs:
                logger.info(f"Found {len(found_songs)} songs with selector: {selector}")
                break
        
        if not found_songs:
            # Fallback: tìm theo pattern khác
            found_songs = soup.find_all(['div', 'li'], class_=re.compile(r'(song|track|item)'))
            logger.info(f"Fallback: Found {len(found_songs)} potential song items")
        
        count = 0
        for item in found_songs:
            if count >= limit:
                break
                
            try:
                # Tìm tên bài hát
                title_elem = item.find(['h3', '.title', '.song-title', '.media-title'])
                if not title_elem:
                    title_elem = item.find('a', title=True)
                
                title = title_elem.get_text(strip=True) if title_elem else ""
                if not title and title_elem:
                    title = title_elem.get('title', '')
                
                if not title or len(title) < 2:
                    continue
                
                # Tìm ca sĩ
                artist_elem = item.find(['.artist', '.singer', '.subtitle', '.media-subtitle'])
                artist = artist_elem.get_text(strip=True) if artist_elem else "Không rõ ca sĩ"
                
                # Tìm thời lượng
                duration_elem = item.find(['.duration', '.time'])
                duration = duration_elem.get_text(strip=True) if duration_elem else ""
                
                # Tìm link trang chi tiết (KHÔNG phải link download)
                link_elem = item.find('a')
                page_url = ""
                if link_elem:
                    href = link_elem.get('href', '')
                    if href.startswith('/'):
                        page_url = f"https://zingmp3.vn{href}"
                    elif href.startswith('http'):
                        page_url = href
                
                # Tìm hình ảnh thumbnail
                img_elem = item.find(['img', '.thumb'])
                thumbnail = ""
                if img_elem:
                    thumbnail = img_elem.get('src') or img_elem.get('data-src', '')
                
                song_info = {
                    "title": title,
                    "artist": artist,
                    "duration": duration,
                    "page_url": page_url,  # Link đến trang chi tiết, không phải download
                    "thumbnail": thumbnail,
                    "keyword": keyword
                }
                
                songs.append(song_info)
                count += 1
                
            except Exception as e:
                logger.warning(f"Error processing song item: {e}")
                continue
        
        logger.info(f"Successfully found {len(songs)} songs for '{keyword}'")
        
        return {
            "success": True,
            "keyword": keyword,
            "total_songs": len(songs),
            "songs": songs,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "ZingMP3.vn",
            "note": "Chỉ hiển thị thông tin metadata, không cung cấp link download"
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {e}")
        return {"success": False, "error": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

@mcp.tool()
def get_zingmp3_playlists(keyword: str, limit: int = 5) -> dict:
    """Tìm kiếm playlist trên ZingMP3"""
    try:
        search_query = urllib.parse.quote(keyword)
        search_url = f"https://zingmp3.vn/tim-kiem/playlist?q={search_query}"
        
        logger.info(f"Searching ZingMP3 playlists for: {keyword}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://zingmp3.vn/',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        playlists = []
        
        # Tìm playlist items
        selectors = [
            '.zm-card-playlist',
            '.playlist-item',
            '.media-playlist',
            '[data-type="playlist"]'
        ]
        
        found_playlists = []
        for selector in selectors:
            found_playlists = soup.select(selector)
            if found_playlists:
                break
        
        count = 0
        for item in found_playlists:
            if count >= limit:
                break
                
            try:
                # Tên playlist
                title_elem = item.find(['h3', '.title', '.playlist-title'])
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                if not title:
                    continue
                
                # Mô tả
                desc_elem = item.find(['.description', '.subtitle'])
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Link
                link_elem = item.find('a')
                page_url = ""
                if link_elem:
                    href = link_elem.get('href', '')
                    if href.startswith('/'):
                        page_url = f"https://zingmp3.vn{href}"
                
                # Số bài hát
                count_elem = item.find(['.count', '.song-count'])
                song_count = count_elem.get_text(strip=True) if count_elem else ""
                
                playlist_info = {
                    "title": title,
                    "description": description,
                    "song_count": song_count,
                    "page_url": page_url,
                    "keyword": keyword
                }
                
                playlists.append(playlist_info)
                count += 1
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "keyword": keyword,
            "total_playlists": len(playlists),
            "playlists": playlists,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "ZingMP3.vn"
        }
        
    except Exception as e:
        logger.error(f"Playlist search error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_zingmp3_top_songs(category: str = "vn", limit: int = 20) -> dict:
    """
    Lấy danh sách bài hát hot/trending trên ZingMP3
    
    Categories:
    - vn: Việt Nam
    - usuk: Âu Mỹ  
    - kpop: K-Pop
    - others: Khác
    """
    try:
        # Map category to ZingMP3 URLs
        category_urls = {
            "vn": "https://zingmp3.vn/zing-chart/bai-hat.html",
            "usuk": "https://zingmp3.vn/zing-chart-tuan/bai-hat/IWZ9Z08I.html", 
            "kpop": "https://zingmp3.vn/zing-chart-tuan/bai-hat/IWZ9Z08O.html",
            "others": "https://zingmp3.vn/zing-chart-tuan/bai-hat/IWZ9Z08W.html"
        }
        
        url = category_urls.get(category, category_urls["vn"])
        
        logger.info(f"Fetching top songs from: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://zingmp3.vn/',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        top_songs = []
        
        # Tìm chart items
        chart_items = soup.select('.zm-card-song, .list-item .item-song, [data-type="song"]')
        
        count = 0
        rank = 1
        for item in chart_items:
            if count >= limit:
                break
                
            try:
                # Title
                title_elem = item.find(['h3', '.title', '.song-title'])
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                if not title:
                    continue
                
                # Artist
                artist_elem = item.find(['.artist', '.singer', '.subtitle'])
                artist = artist_elem.get_text(strip=True) if artist_elem else ""
                
                # Duration
                duration_elem = item.find(['.duration', '.time'])
                duration = duration_elem.get_text(strip=True) if duration_elem else ""
                
                song_info = {
                    "rank": rank,
                    "title": title,
                    "artist": artist,
                    "duration": duration,
                    "category": category
                }
                
                top_songs.append(song_info)
                count += 1
                rank += 1
                
            except Exception as e:
                continue
        
        return {
            "success": True,
            "category": category,
            "total_songs": len(top_songs),
            "songs": top_songs,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "ZingMP3 Chart"
        }
        
    except Exception as e:
        logger.error(f"Top songs error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def open_zingmp3_in_browser(song_title: str, artist: str = "") -> dict:
    """
    Tạo lệnh mở ZingMP3 trong browser để nghe nhạc hợp pháp.
    Không download, chỉ hướng dẫn mở trình duyệt.
    """
    try:
        # Tạo từ khóa tìm kiếm
        if artist:
            search_keyword = f"{song_title} {artist}"
        else:
            search_keyword = song_title
        
        encoded_keyword = urllib.parse.quote(search_keyword)
        search_url = f"https://zingmp3.vn/tim-kiem/bai-hat?q={encoded_keyword}"
        
        # Tạo lệnh mở browser cho các OS khác nhau
        commands = {
            "windows": f'start "" "{search_url}"',
            "macos": f'open "{search_url}"',
            "linux": f'xdg-open "{search_url}"'
        }
        
        return {
            "success": True,
            "song": song_title,
            "artist": artist,
            "search_url": search_url,
            "browser_commands": commands,
            "message": "Sử dụng một trong các lệnh trên để mở ZingMP3 trong trình duyệt và nghe nhạc hợp pháp.",
            "note": "Tool này không download nhạc, chỉ hướng dẫn truy cập website chính thức."
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
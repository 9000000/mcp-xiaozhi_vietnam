from fastmcp import FastMCP
import sys
import logging
import urllib.request
import xml.etree.ElementTree as ET
import re

logger = logging.getLogger('VnExpress')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("VnExpress")

# RSS Feeds theo chủ đề
RSS_FEEDS = {
    "tin-moi": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "home": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "thoi-su": "https://vnexpress.net/rss/thoi-su.rss",
    "the-gioi": "https://vnexpress.net/rss/the-gioi.rss",
    "kinh-doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "startup": "https://vnexpress.net/rss/startup.rss",
    "bat-dong-san": "https://vnexpress.net/rss/bat-dong-san.rss",
    "giai-tri": "https://vnexpress.net/rss/giai-tri.rss",
    "the-thao": "https://vnexpress.net/rss/the-thao.rss",
    "phap-luat": "https://vnexpress.net/rss/phap-luat.rss",
    "giao-duc": "https://vnexpress.net/rss/giao-duc.rss",
    "suc-khoe": "https://vnexpress.net/rss/suc-khoe.rss",
    "doi-song": "https://vnexpress.net/rss/doi-song.rss",
    "du-lich": "https://vnexpress.net/rss/du-lich.rss",
    "khoa-hoc": "https://vnexpress.net/rss/khoa-hoc.rss",
    "so-hoa": "https://vnexpress.net/rss/so-hoa.rss",
    "oto-xe-may": "https://vnexpress.net/rss/oto-xe-may.rss",
    "xe": "https://vnexpress.net/rss/oto-xe-may.rss",
}

_TAG_RE = re.compile(r"<[^>]+>")

def strip_html(text):
    """Loại bỏ HTML tags và hình ảnh từ text"""
    if not text:
        return ""
    no_tags = _TAG_RE.sub("", text)
    no_images = re.sub(r"https?://\S+\.(?:png|jpg|jpeg|gif|svg)\S*", "", no_tags, flags=re.IGNORECASE)
    no_images = re.sub(r"data:image/[^;\s]+;base64,[A-Za-z0-9+/=]+", "", no_images, flags=re.IGNORECASE)
    return " ".join(no_images.split())

def parse_xml_to_dict(xml_text):
    """Parse XML thành dictionary"""
    root = ET.fromstring(xml_text)

    def elem_to_dict(elem):
        children = list(elem)
        if not children:
            text = elem.text.strip() if elem.text and elem.text.strip() else ""
            if elem.attrib:
                data = {"_text": text} if text else {}
                data.update({f"@{k}": v for k, v in elem.attrib.items()})
                return data
            return text

        result = {}
        for k, v in elem.attrib.items():
            result[f"@{k}"] = v
        for child in children:
            child_val = elem_to_dict(child)
            tag = child.tag
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_val)
            else:
                result[tag] = child_val
        return result

    return {root.tag: elem_to_dict(root)}

def extract_rss_items(parsed):
    """Trích xuất items từ RSS feed"""
    items = []
    if "rss" in parsed:
        channel = parsed["rss"].get("channel", {})
        raw_items = channel.get("item", [])
    elif "feed" in parsed:
        raw_items = parsed["feed"].get("entry", [])
    else:
        raw_items = parsed.get("item", [])
    
    if isinstance(raw_items, dict):
        raw_items = [raw_items]
    
    for it in raw_items:
        simple = {}
        if isinstance(it, dict):
            for k, v in it.items():
                val = v["_text"] if isinstance(v, dict) and "_text" in v and len(v) == 1 else v
                if isinstance(val, str):
                    simple[k] = strip_html(val)
                else:
                    simple[k] = val
        else:
            simple["content"] = strip_html(str(it))
        items.append(simple)
    return items

@mcp.tool()
def get_vnexpress_news(category: str = "home", limit: int = 10) -> dict:
    """
    Lấy tin tức mới nhất từ VnExpress qua RSS feed.
    
    Categories:
    - home/tin-moi: Tin mới nhất
    - thoi-su: Thời sự
    - the-gioi: Thế giới
    - kinh-doanh: Kinh doanh
    - startup: Startup
    - bat-dong-san: Bất động sản
    - khoa-hoc: Khoa học
    - giai-tri: Giải trí
    - the-thao: Thể thao
    - phap-luat: Pháp luật
    - giao-duc: Giáo dục
    - suc-khoe: Sức khỏe
    - doi-song: Đời sống
    - du-lich: Du lịch
    - so-hoa: Số hóa
    - xe/oto-xe-may: Xe
    """
    url = RSS_FEEDS.get(category, RSS_FEEDS["home"])
    
    try:
        logger.info(f"Fetching RSS from: {url}")
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_content = response.read().decode('utf-8')
        
        parsed = parse_xml_to_dict(xml_content)
        items = extract_rss_items(parsed)
        
        articles = []
        for item in items[:limit]:
            article = {
                "title": item.get("title", "Không có tiêu đề"),
                "url": item.get("link", ""),
                "description": item.get("description", "")[:300] + "..." if len(item.get("description", "")) > 300 else item.get("description", ""),
                "pubDate": item.get("pubDate", ""),
                "category": category
            }
            articles.append(article)
        
        logger.info(f"Successfully fetched {len(articles)} articles from {category}")
        
        return {
            "success": True,
            "category": category,
            "total_articles": len(articles),
            "articles": articles,
            "source": "VnExpress.net"
        }
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_article_content(url: str) -> dict:
    """Lấy nội dung chi tiết của một bài báo từ URL VnExpress"""
    try:
        logger.info(f"Fetching article content from: {url}")
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # Tìm tiêu đề
        title_match = re.search(r'<h1[^>]*class="[^"]*title-detail[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = strip_html(title_match.group(1)) if title_match else "Không tìm thấy tiêu đề"
        
        # Tìm mô tả/lead
        desc_match = re.search(r'<p[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
        description = strip_html(desc_match.group(1)) if desc_match else ""
        
        # Tìm nội dung chính - lấy tất cả paragraphs trong article body
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        clean_paras = [strip_html(p) for p in paragraphs if strip_html(p) and len(strip_html(p)) > 20]
        content = "\n\n".join(clean_paras[:20])
        
        # Tìm thời gian
        time_match = re.search(r'<span[^>]*class="[^"]*date[^"]*"[^>]*>(.*?)</span>', html, re.DOTALL)
        publish_time = strip_html(time_match.group(1)) if time_match else ""
        
        return {
            "success": True,
            "title": title,
            "description": description,
            "content": content[:2000] + "..." if len(content) > 2000 else content,
            "publish_time": publish_time,
            "url": url
        }
        
    except Exception as e:
        logger.error(f"Error fetching article content: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool() 
def search_vnexpress_news(keyword: str, limit: int = 5) -> dict:
    """Tìm kiếm tin tức trên VnExpress theo từ khóa"""
    try:
        import urllib.parse
        encoded_keyword = urllib.parse.quote_plus(keyword)
        search_url = f"https://timkiem.vnexpress.net/?q={encoded_keyword}"
        
        logger.info(f"Searching VnExpress for: {keyword}")
        
        req = urllib.request.Request(search_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # Tìm các tiêu đề bài viết trong kết quả tìm kiếm
        title_matches = re.findall(r'<h3[^>]*class="[^"]*title-news[^"]*"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
        
        articles = []
        for href, title_html in title_matches[:limit]:
            title = strip_html(title_html)
            
            # Tạo URL đầy đủ
            if href.startswith('/'):
                full_url = f"https://vnexpress.net{href}"
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = f"https://vnexpress.net/{href}"
            
            # Tìm description gần với link này
            desc_pattern = rf'{re.escape(href)}.*?<p[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</p>'
            desc_match = re.search(desc_pattern, html, re.DOTALL)
            description = strip_html(desc_match.group(1)) if desc_match else ""
            
            articles.append({
                "title": title,
                "url": full_url,
                "description": description[:200] + "..." if len(description) > 200 else description,
                "keyword": keyword
            })
        
        return {
            "success": True,
            "keyword": keyword,
            "total_results": len(articles),
            "articles": articles
        }
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")

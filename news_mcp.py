# news.py
from mcp.server.fastmcp import FastMCP
import requests
import xml.etree.ElementTree as ET
import re

mcp = FastMCP("NewsFetcher")

# === Nguồn RSS theo chủ đề ===
RSS_FEEDS = {
    "tin-moi": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "thoi-su": "https://vnexpress.net/rss/thoi-su.rss",
    "the-gioi": "https://vnexpress.net/rss/the-gioi.rss",
    "kinh-doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "startup": "https://vnexpress.net/rss/startup.rss",
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
}

_TAG_RE = re.compile(r"<[^>]+>")

def strip_html(text):
    if not text:
        return ""
    no_tags = _TAG_RE.sub("", text)
    no_images = re.sub(r"https?://\S+\.(?:png|jpg|jpeg|gif|svg)\S*", "", no_tags, flags=re.IGNORECASE)
    no_images = re.sub(r"data:image/[^;\s]+;base64,[A-Za-z0-9+/=]+", "", no_images, flags=re.IGNORECASE)
    return " ".join(no_images.split())

def parse_xml_to_dict(xml_text):
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
def get_latest_news(topic: str = "tin-moi", limit: int = 5) -> dict:
    """
    Lấy tin tức mới nhất từ VNExpress theo chủ đề.
    Chủ đề hỗ trợ: tin-moi, the-gioi, thoi-su, the-thao, cong-nghe (so-hoa), giai-tri, kinh-doanh, suc-khoe, du-lich, ...
    """
    url = RSS_FEEDS.get(topic, RSS_FEEDS["tin-moi"])
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        return {"success": False, "message": f"Không thể tải RSS: {e}"}

    try:
        parsed = parse_xml_to_dict(res.text)
        items = extract_rss_items(parsed)
        results = [
            {
                "title": i.get("title", "Không có tiêu đề"),
                "link": i.get("link", ""),
                "description": i.get("description", "")[:200] + "..."
            }
            for i in items[:limit]
        ]
        return {"success": True, "topic": topic, "items": results}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    # Test trước khi đưa vào mcp
    #print(get_latest_news("cong-nghe"))
    mcp.run(transport="stdio")

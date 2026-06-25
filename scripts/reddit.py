import requests
import xml.etree.ElementTree as ET

def get_reddit_post():
    url = "https://www.reddit.com/r/AITAH/.rss"
    headers = {"User-Agent": "ssuljari-ai"}

    res = requests.get(url, headers=headers)
    root = ET.fromstring(res.text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    for e in entries:
        title = e.find("atom:title", ns)
        content = e.find("atom:content", ns)

        if not title or not content:
            continue

        t = title.text.lower()

        if "rule" in t or "karma" in t:
            continue

        return {
            "title": title.text,
            "content": (content.text or "")[:1000]
        }

    return None

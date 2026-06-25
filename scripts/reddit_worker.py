import requests
import xml.etree.ElementTree as ET

def fetch_reddit_posts(limit=5):
    url = "https://www.reddit.com/r/AITAH/.rss"

    headers = {
        "User-Agent": "ssuljari-ai"
    }

    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    posts = []

    for entry in entries:
        title = entry.find("atom:title", ns)
        content = entry.find("atom:content", ns)

        if title is None or content is None:
            continue

        t = title.text.lower()

        if "rule" in t or "karma" in t:
            continue

        posts.append({
            "title": title.text,
            "content": content.text[:1500]
        })

        if len(posts) >= limit:
            break

    return posts

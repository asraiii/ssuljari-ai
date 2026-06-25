import requests
import xml.etree.ElementTree as ET
import re

def get_reddit_post():
    url = "https://www.reddit.com/r/AITAH/.rss"
    headers = {"User-Agent": "ssuljari-ai"}

    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    banned = ["wedding","marriage","bride","groom","guest","rsvp","ceremony"]

    for entry in entries:
        title = entry.find("atom:title", ns)
        content = entry.find("atom:content", ns)

        if not title or not content:
            continue

        title_text = title.text or ""
        content_text = content.text or ""

        if any(x in title_text.lower() for x in banned):
            continue

        content_text = re.sub(r"<.*?>", "", content_text)

        return {
            "title": title_text,
            "content": content_text[:2000]
        }

    return None

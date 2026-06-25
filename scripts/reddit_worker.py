import requests
import xml.etree.ElementTree as ET

def get_best_reddit_post():

    url = "https://www.reddit.com/r/AITAH/.rss"

    headers = {"User-Agent": "ssuljari-ai"}

    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    entries = root.findall("atom:entry", ns)

    for entry in entries:

        title = entry.find("atom:title", ns)
        content = entry.find("atom:content", ns)

        if title is None or content is None:
            continue

        if "rule" in title.text.lower():
            continue

        if "karma" in title.text.lower():
            continue

        return {
            "title": title.text,
            "content": content.text[:2000]
        }

    return None

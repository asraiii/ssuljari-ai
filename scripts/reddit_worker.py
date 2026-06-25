import requests
import xml.etree.ElementTree as ET

url = "https://www.reddit.com/r/AITAH/.rss"

headers = {
    "User-Agent": "ssuljari-ai"
}

response = requests.get(url, headers=headers)

root = ET.fromstring(response.text)

ns = {
    "atom": "http://www.w3.org/2005/Atom"
}

entries = root.findall("atom:entry", ns)

print("===== Reddit 썰 =====")

for entry in entries:

    title = entry.find("atom:title", ns)

    content = entry.find("atom:content", ns)

    if title is None:
        continue

    if "rule" in title.text.lower():
        continue

    if "karma" in title.text.lower():
        continue

    print()
    print("제목:")
    print(title.text)

    print()
    print("본문:")
    print(content.text[:500])

    break

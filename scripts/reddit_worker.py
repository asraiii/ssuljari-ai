import requests
import xml.etree.ElementTree as ET

url = "https://www.reddit.com/r/AITAH/.rss"

headers = {
    "User-Agent": "ssuljari-ai"
}

response = requests.get(url, headers=headers)

root = ET.fromstring(response.text)

print("=== 오늘의 AITAH 썰 ===")

for item in root.findall("{http://www.w3.org/2005/Atom}entry")[:5]:
    title = item.find("{http://www.w3.org/2005/Atom}title")

    if title is not None:
        print(title.text)

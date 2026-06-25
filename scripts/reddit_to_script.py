import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai

# Gemini 설정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# Reddit RSS
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

title_text = ""
content_text = ""

for entry in entries:

    title = entry.find("atom:title", ns)
    content = entry.find("atom:content", ns)

    if title is None:
        continue

    if "rule" in title.text.lower():
        continue

    if "karma" in title.text.lower():
        continue

    title_text = title.text
    content_text = content.text[:3000]

    break

prompt = f"""
너는 한국 유튜브 쇼츠 연애썰 전문 작가다.

다음 Reddit 실화를

한국 정서에 맞게 변환해라.

규칙

- 반드시 1인칭
- 45~60초 분량
- 짧은 문장
- 한 줄 한 문장
- 첫 줄은 강한 훅
- 현실성 우선
- 억지 반전 금지
- 쇼츠 스타일
- 연애썰 느낌

Reddit 제목

{title_text}

Reddit 본문

{content_text}
"""

response = model.generate_content(prompt)

print("===== 썰자리 대본 =====")
print(response.text)

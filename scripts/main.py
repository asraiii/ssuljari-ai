import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import re
import os

# ======================
# Gemini 설정
# ======================
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ======================
# Reddit 가져오기
# ======================
url = "https://www.reddit.com/r/AITAH/.rss"
headers = {"User-Agent": "ssuljari-ai"}

res = requests.get(url, headers=headers)
root = ET.fromstring(res.text)

ns = {"atom": "http://www.w3.org/2005/Atom"}
entries = root.findall("atom:entry", ns)

title = ""
content = ""

for e in entries:
    t = e.find("atom:title", ns)
    c = e.find("atom:content", ns)

    if not t or not c:
        continue

    title = t.text or ""
    content = re.sub(r"<.*?>", "", c.text or "")[:2000]
    break

# ======================
# 프롬프트
# ======================
prompt = f"""
너는 한국 유튜브 쇼츠 작가다.

조건:
- 1인칭
- 짧은 문장
- 현실적인 썰
- 45~60초

출력:

===== 제목 =====
===== 대본 =====

Reddit 제목:
{title}

Reddit 내용:
{content}
"""

# ======================
# 실행
# ======================
print("Reddit 가져오는 중...")

response = model.generate_content(prompt)

print("\n===== 결과 =====\n")
print(response.text)

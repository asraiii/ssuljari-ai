import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import re

# =========================
# Gemini 설정
# =========================
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# Reddit RSS
# =========================
url = "https://www.reddit.com/r/AITAH/.rss"
headers = {"User-Agent": "ssuljari-ai"}

response = requests.get(url, headers=headers)
root = ET.fromstring(response.text)

ns = {"atom": "http://www.w3.org/2005/Atom"}
entries = root.findall("atom:entry", ns)

# =========================
# 금지 키워드
# =========================
banned_keywords = [
    "rule", "karma",
    "wedding", "marriage", "bride", "groom",
    "guest", "rsvp", "ceremony"
]

# =========================
# 1. 후보 5개 수집
# =========================
candidates = []

for entry in entries:
    title = entry.find("atom:title", ns)
    content = entry.find("atom:content", ns)

    if title is None or content is None:
        continue

    title_text = title.text
    content_text = content.text or ""

    title_lower = title_text.lower()

    if any(w in title_lower for w in banned_keywords):
        continue

    content_text = re.sub(r"<.*?>", "", content_text)

    candidates.append({
        "title": title_text,
        "content": content_text[:2000]
    })

    if len(candidates) >= 5:
        break

# =========================
# 2. Gemini로 점수 매기기
# =========================
score_prompt = f"""
너는 유튜브 쇼츠 기획자다.

아래 5개 Reddit 글을 보고
조회수 가장 잘 나올 것 1개를 골라라.

조건:
- 갈등 강한 것
- 감정 강한 것
- 직장/연애/인간관계
- 쇼츠에 적합한 것

출력:
번호 하나만 (1~5)

---

"""

for i, c in enumerate(candidates, 1):
    score_prompt += f"""
[{i}]
제목: {c['title']}
내용: {c['content'][:200]}
"""

score_result = model.generate_content(score_prompt).text.strip()

try:
    best_index = int(re.findall(r"\d", score_result)[0]) - 1
except:
    best_index = 0

best = candidates[best_index]

# =========================
# 3. 썰 생성 + 제목 최적화
# =========================
script_prompt = f"""
너는 유튜브 쇼츠 "썰자리" 작가다.

아래 Reddit 글을 한국식 썰로 바꿔라.

규칙:
- 1인칭
- 짧은 문장
- 45~60초
- 감정 중심
- 현실적
- 과장 금지

반드시 출력:

===== 제목 =====
25자 이내 클릭형 제목

===== 대본 =====
쇼츠 대본

---

제목:
{best['title']}

내용:
{best['content']}
"""

response = model.generate_content(script_prompt)

# =========================
# 4. 출력
# =========================
print("\n===== STEP1 BEST SCORE RESULT =====")
print(score_result)

print("\n===== FINAL SCRIPT =====")
print(response.text)

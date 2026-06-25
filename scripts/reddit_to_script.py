import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import re

# =========================
# GEMINI SETUP
# =========================
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# REDDIT FETCH
# =========================
url = "https://www.reddit.com/r/AITAH/.rss"
headers = {"User-Agent": "ssuljari-ai"}

response = requests.get(url, headers=headers)
root = ET.fromstring(response.text)

ns = {"atom": "http://www.w3.org/2005/Atom"}
entries = root.findall("atom:entry", ns)

# =========================
# 후보 수집 (5개)
# =========================
candidates = []

for entry in entries:
    title = entry.find("atom:title", ns)
    content = entry.find("atom:content", ns)

    if title is None or content is None:
        continue

    title_text = title.text or ""
    content_text = content.text or ""

    # HTML 제거
    content_text = re.sub(r"<.*?>", "", content_text)

    # 너무 짧은 글 제외
    if len(content_text) < 200:
        continue

    candidates.append({
        "title": title_text,
        "content": content_text[:2000]
    })

    if len(candidates) >= 5:
        break

# =========================
# 후보 부족 방지
# =========================
if len(candidates) == 0:
    print("No Reddit posts found")
    exit()

# =========================
# 🔥 1. 조회수 점수 시스템
# =========================
score_prompt = """
너는 유튜브 쇼츠 데이터 분석가다.

아래 Reddit 글 중
조회수 가장 잘 나올 순서를 골라라.

기준:
- 감정 강도 (중요)
- 갈등 구조
- 배신 / 연애 / 직장 / 인간관계
- 한방 반전 가능성
- 쇼츠 몰입도

출력:
1~5 순위만 숫자로 나열

예:
3 1 5 2 4
"""

for i, c in enumerate(candidates, 1):
    score_prompt += f"""

[{i}]
제목: {c['title']}
내용: {c['content'][:200]}
"""

score_result = model.generate_content(score_prompt).text.strip()

print("\n===== SCORE RESULT =====")
print(score_result)

# =========================
# 점수 해석 (1등 뽑기)
# =========================
numbers = re.findall(r"\d", score_result)

if numbers:
    best_index = int(numbers[0]) - 1
else:
    best_index = 0

best = candidates[best_index]

# =========================
# 🔥 2. 썰 생성 + 제목 최적화
# =========================
script_prompt = f"""
너는 한국 유튜브 쇼츠 "썰자리" 작가다.

목표:
조회수 터지는 리얼 썰 제작

규칙:
- 1인칭
- 짧은 문장
- 감정 중심
- 설명 금지
- 현실 기반
- 과장 금지
- 쇼츠 리듬

구조:
1. 강한 훅
2. 사건 발생
3. 갈등
4. 감정 폭발
5. 짧은 결말

반드시 출력:

===== 제목 =====
25자 이내 클릭형 제목

===== 대본 =====
쇼츠용 대본

---

Reddit 제목:
{best['title']}

Reddit 내용:
{best['content']}
"""

response = model.generate_content(script_prompt)

# =========================
# OUTPUT
# =========================
print("\n===== BEST PICK =====")
print(best["title"])

print("\n===== FINAL RESULT =====")
print(response.text)

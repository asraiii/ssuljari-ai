import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import re
import random

# =========================
# Gemini 설정
# =========================
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# Reddit RSS
# =========================
url = "https://www.reddit.com/r/AITAH/.rss"

headers = {
    "User-Agent": "ssuljari-ai"
}

response = requests.get(url, headers=headers)
root = ET.fromstring(response.text)

ns = {"atom": "http://www.w3.org/2005/Atom"}

entries = root.findall("atom:entry", ns)

# =========================
# 금지 키워드
# =========================
banned_keywords = [
    "wedding", "marriage", "bride", "groom",
    "guest", "rsvp", "ceremony",
    "religion", "church", "priest"
]

# =========================
# 점수 함수
# =========================
def score_post(title):
    score = 0
    title_lower = title.lower()

    # 클릭 유도 키워드
    hooks = [
        "aitah", "cheated", "caught", "secret",
        "hidden", "lied", "revenge", "divorce",
        "ex", "boss", "job", "salary", "pay"
    ]

    for h in hooks:
        if h in title_lower:
            score += 2

    # 길이 적당하면 추가 점수
    if 30 < len(title) < 120:
        score += 1

    # 물음형이면 추가
    if "?" in title:
        score += 1

    return score

# =========================
# 후보 글 수집
# =========================
candidates = []

for entry in entries:
    title = entry.find("atom:title", ns)
    content = entry.find("atom:content", ns)

    if title is None or content is None:
        continue

    title_text = title.text or ""
    content_text = content.text or ""

    title_lower = title_text.lower()

    # 필터
    if any(word in title_lower for word in banned_keywords):
        continue
    if "rule" in title_lower or "karma" in title_lower:
        continue

    score = score_post(title_text)

    candidates.append({
        "title": title_text,
        "content": content_text[:3000],
        "score": score
    })

# =========================
# 상위 5개 중 랜덤 선택
# =========================
candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:5]

if not candidates:
    print("No valid posts found")
    exit()

picked = random.choice(candidates)

title_text = picked["title"]
content_text = picked["content"]

# =========================
# HTML 제거
# =========================
content_text = re.sub(r"<.*?>", "", content_text)

# =========================
# GEMINI PROMPT
# =========================
prompt = f"""
너는 유튜브 쇼츠 "썰자리" 시나리오 작가다.

목표
- Reddit 글을 한국식 현실 썰로 변환
- 조회수 잘 나오는 쇼츠 대본

규칙
- 1인칭
- 등장인물 3명 이하
- 한 줄 = 한 문장
- 45~60초 분량
- 짧고 빠른 전개
- 괄호/대사/설명 금지

구성
- 첫 줄: 강한 훅
- 초반 3줄 안에 사건 시작
- 중간: 이상한 상황
- 마지막: 짧은 결말

스타일
- 현실적인 직장/연애/일상
- 과장 금지
- 드라마 같은 설정 금지
- 억지 반전 금지

금지
- 교훈, 질문, 감성설명
- "여러분이라면?"
- 회사기밀/해킹/비현실 설정

출력 형식

===== 제목 =====
(25자 이내)

===== 대본 =====

Reddit 제목:
{title_text}

Reddit 본문:
{content_text}
"""

# =========================
# 실행
# =========================
print("STEP1 Reddit 분석")

response = model.generate_content(prompt)

print("\n===== 결과 =====")
print(response.text)

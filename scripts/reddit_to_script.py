import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import re

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

# Reddit 글 하나 가져오기
for entry in entries:

    title = entry.find("atom:title", ns)
    content = entry.find("atom:content", ns)

    if title is None or content is None:
        continue

    if "rule" in title.text.lower():
        continue

    if "karma" in title.text.lower():
        continue

    title_text = title.text
    content_text = content.text[:3000]

    break

# HTML 제거 (중요)
content_text = re.sub(r"<.*?>", "", content_text)

# =========================
# GEMINI PROMPT
# =========================
prompt = f"""
너는 유튜브 쇼츠 "썰자리" 전용 시나리오 작가다.

너의 목표는 "조회수가 터지는 쇼츠 대본"이다.

=====================
🔥 핵심 규칙 (매우 중요)
=====================

- 반드시 1인칭
- 실제 사람이 말하는 느낌
- 짧은 문장 (한 줄 = 한 문장)
- 45~60초 분량
- 과장 금지 (현실적 썰)
- 설명하지 말고 "상황을 보여줘"
- 감정이 반드시 들어가야 함
- 너무 정리된 글 금지

=====================
🔥 구조 (고정)
=====================

1. 첫 문장 = 충격 훅 (무조건 중요)
2. 바로 사건 시작 (설명 금지)
3. 이상한 느낌 발생
4. 감정 폭발
5. 짧은 결말 또는 찝찝한 마무리

=====================
🔥 훅 예시 스타일
=====================

- "결혼식 앞두고 친구랑 손절할 뻔했습니다"
- "소개팅에서 제 연봉이 들통났습니다"
- "회사에서 이상한 메일을 받았습니다"
- "친구한테 배신당한 날이었습니다"

=====================
🔥 금지
=====================

- 교훈 말하기 금지
- 설명형 문장 금지
- 뉴스 기사처럼 쓰기 금지
- 모든 걸 친절하게 설명하지 말 것
- 드라마 같은 과한 설정 금지

=====================
🔥 입력 데이터
=====================

Reddit 제목:
{title_text}

Reddit 본문:
{content_text}

=====================
🔥 출력 형식 (반드시 지켜라)
=====================

===== 제목 =====
(25자 이내 클릭형 제목)

===== 대본 =====
(쇼츠용 대본)
"""

# =========================
# GEMINI 실행 (이게 핵심!)
# =========================
print("STEP1: Reddit 가져오는 중")
print("title:", title_text)
print("content:", content_text[:200])

response = model.generate_content(prompt)

# =========================
# 결과 출력
# =========================
print("\n==== GEMINI RAW RESPONSE ====")
print(response.text)
print("=============================")

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
너는 한국 유튜브 쇼츠 채널 '썰자리'의 전문 작가다.

목표
- Reddit 실화를 한국 정서에 맞게 재구성
- 실제 사람이 겪은 경험처럼 작성
- 조회수가 잘 나오는 쇼츠 스타일로 작성

규칙

- 1인칭 유지
- 한 줄 한 문장
- 짧고 구어체 느낌
- 실제 사람이 말하는 느낌
- 너무 정리된 글 금지
- 일부 디테일은 흐리게 표현
- 감정이 드러나야 함

중요

- 첫 문장은 무조건 충격적이어야 함
- 예: "결혼식 앞두고 친구랑 손절할 뻔했습니다"
- 또는 "소개팅에서 이상한 일을 겪었습니다"
- 설명형 시작 금지

금지

- 너무 완벽한 사건 구조 금지
- 뉴스 기사처럼 쓰지 말 것
- 교과서식 전개 금지
- 모든 정보를 명확하게 설명하지 말 것

스타일

- 실제 사람의 하소연 느낌
- 중간중간 감정 섞기
- 약간 애매하게 끝내기

제목 규칙
- 25자 이내 클릭 유도형

출력 형식

===== 제목 =====
제목

===== 대본 =====
대본

Reddit 제목:
{title_text}

Reddit 본문:
{content_text}
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

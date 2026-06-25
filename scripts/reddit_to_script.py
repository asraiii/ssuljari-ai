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
너는 한국 유튜브 쇼츠 채널 '썰자리'의 전문 작가다.

목표

- Reddit 실화를 한국 정서에 맞게 재구성
- 실제 사람이 겪은 경험처럼 작성
- 조회수가 잘 나오는 쇼츠 스타일로 작성

규칙

- 반드시 1인칭 시점
- 한 줄당 한 문장
- 짧고 읽기 쉽게 작성
- 45~60초 분량
- 자막용 문장만 작성
- 괄호 사용 금지
- 나레이션 표시 금지
- 대사 표시 금지

중요

- 첫 문장은 반드시 강한 훅
- 첫 3줄 안에 사건 시작
- 배경 설명 최소화
- 사건 전개 중심
- 현실성 최우선
- 억지 반전 금지
- 실제 커뮤니티 썰처럼 작성

금지

- 여러분이라면?
- 제가 잘못한 걸까요?
- 어떻게 생각하시나요?
- 교훈
- 억지 감동
- 억지 사이다

절대 금지

- 회사 기밀 유출
- 인사팀이 연봉 공개
- 개인정보 무단 조회
- 해킹
- 우연히 모든 것을 알게 되는 설정
- 드라마 같은 설정
- 영화 같은 반전

제목 규칙

- 제목은 반드시 생성
- 25자 이내
- 클릭하고 싶게 작성
- 과장 금지
- 실제 경험담처럼 작성

출력 형식

===== 제목 =====
제목

===== 대본 =====
대본

Reddit 제목

{title_text}

Reddit 본문

{content_text}
"""

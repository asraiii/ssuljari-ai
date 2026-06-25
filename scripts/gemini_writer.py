import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ssul(title, content):

    prompt = f"""
너는 한국 유튜브 쇼츠 썰 채널 "썰자리"의 전문 작가다.

너의 임무는 아래 Reddit 글을 기반으로
"한국에서 실제 있었던 것처럼 보이는 쇼츠 썰"을 만드는 것이다.

━━━━━━━━━━━━━━
[입력 Reddit 글]
제목: {title}
내용: {content}
━━━━━━━━━━━━━━

🔥 반드시 해야 할 것:

1. 완전히 한국화
- 미국 문화/법/회사 제거
- 한국 직장 / 연애 / 가족 구조로 변환
- 블라인드 / 네이트판 스타일

2. 쇼츠 최적화
- 45~60초 길이
- 한 줄 = 한 문장
- 짧고 강한 문장

3. 구조 (무조건 지켜라)
- 훅 (첫 문장 충격)
- 상황 설명
- 이상한 느낌 / 갈등
- 반전
- 결말

4. 스타일
- 1인칭
- 감정 중심
- 눈치 / 갈등 / 분위기 중심
- 현실적으로 있을 법한 이야기
- 등장인물 최대 3명
- 쇼츠 중독성 스타일로 작성

5. 금지
- 영상 설명 금지
- 나레이션 금지
- 괄호 금지
- 번역 느낌 금지

━━━━━━━━━━━━━━
🔥 추가 출력 (중요)

마지막에 반드시 아래도 생성:

[제목]
- 클릭 유도형 한국식 제목 3개

[핵심 한줄]
- 영상 썸네일용 한 줄 요약
━━━━━━━━━━━━━━

출력은 반드시 한국 쇼츠 스크립트 형태로 작성해라.
"""

    response = model.generate_content(prompt)
    return response.text

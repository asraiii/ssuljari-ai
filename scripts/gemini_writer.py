import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_content_pack(title, content):

    prompt = f"""
너는 유튜브 쇼츠 콘텐츠 제작 AI다.

아래 Reddit 글을 기반으로 "한국 유튜브 쇼츠 완성 패키지"를 만들어라.

━━━━━━━━━━━━━━
[Reddit 제목]
{title}

[Reddit 내용]
{content}
━━━━━━━━━━━━━━

🔥 반드시 생성할 것:

1. 한국식 썰 (45~60초)
- 완전히 한국화
- 블라인드 / 네이트판 스타일
- 1인칭
- 한 줄 = 한 문장

2. CTR 제목 5개
- 클릭 유도 강하게
- "충격", "실화", "왜" 포함

3. 썸네일 문장 3개
- 3~6단어
- 감정 폭발

4. 첫 1줄 훅 3개
- 1초 안에 끌리는 문장

조건
a. 완전히 한국화
- 미국 문화/법/회사 제거
- 한국 직장 / 연애 / 가족 구조로 변환
- 블라인드 / 네이트판 스타일

b. 쇼츠 최적화
- 45~60초 길이
- 한 줄 = 한 문장
- 짧고 강한 문장

c. 구조 (무조건 지켜라)
- 훅 (첫 문장 충격)
- 상황 설명
- 이상한 느낌 / 갈등
- 반전
- 결말

d. 스타일
- 1인칭
- 감정 중심
- 눈치 / 갈등 / 분위기 중심
- 현실적으로 있을 법한 이야기
- 등장인물 최대 3명
- 쇼츠 중독성 스타일로 작성

e. 금지
- 영상 설명 금지
- 나레이션 금지
- 괄호 금지
- 번역 느낌 금지


━━━━━━━━━━━━━━
출력 형식:

[STORY]
...

[TITLES]
1.
2.
3.
4.
5.

[THUMBNAIL]
1.
2.
3.

[HOOK]
1.
2.
3.

출력은 반드시 위 형식을 정확히 지켜라.
다른 설명은 절대 하지 마라.
"""

    response = model.generate_content(prompt)
    return response.text

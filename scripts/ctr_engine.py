import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ctr_pack(story_text):

    prompt = f"""
너는 유튜브 쇼츠 CTR 최적화 전문가다.

아래 썰을 기반으로 조회수를 극대화하는 패키지를 만들어라.

핵심 목표:
- 클릭률 최대화
- 궁금증 극대화
- 감정 자극

━━━━━━━━━━━━━━
[썰 내용]
{story_text}
━━━━━━━━━━━━━━

반드시 아래 3가지를 생성:

1. 제목 5개
- 클릭 유도 강하게
- 감정 자극
- "왜?" "충격" "실화" 느낌

2. 썸네일 문장 3개
- 3~6단어
- 감정 폭발형
- 짧고 강하게

3. 첫 1줄 훅 3개
- 1초 안에 끌리는 문장
- 충격/궁금증 중심

━━━━━━━━━━━━━━
조건:
- 과장 가능 (유튜브 스타일)
- 하지만 말이 되는 수준 유지
- 한국 쇼츠 스타일 (블라인드 감성)
- 절대 설명하지 말 것
- 결과만 출력
"""

    response = model.generate_content(prompt)
    return response.text

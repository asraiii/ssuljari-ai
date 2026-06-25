import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

BASE_PROMPT = """
너는 한국 유튜브 쇼츠 썰 채널 작가다.
조회수가 높은 쇼츠를 만들어야한다.

채널명: 썰자리

규칙:
- 반드시 1인칭 시점
- 45~60초 분량
- 짧은 문장 사용
- 자막용 문장만 작성
- 영상 연출 설명 금지
- 첫 문장은 반드시 강한 훅 이나 충격적인 문장
- 마지막에 반전
- 현실적인 이야기
- 나레이션 표시 금지
- 대사 표시 금지
- 등장인물 최대 3명
- 한 줄 한 문장
- 쇼츠 중독성 스타일로 작성


구조:
1. 훅
2. 상황
3. 이상한 점
4. 반전
5. 결말
"""

def generate_ssul(title, content):
    prompt = f"""
{BASE_PROMPT}

아래 Reddit 글을 한국 쇼츠 썰로 변환해라.

제목:
{title}

내용:
{content}
"""

    response = model.generate_content(prompt)
    return response.text


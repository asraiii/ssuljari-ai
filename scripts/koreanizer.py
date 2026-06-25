import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def koreanize_story(title, content):

    prompt = f"""
너는 Reddit 글을 한국 직장/연애 커뮤니티 썰처럼 재구성하는 AI다.

아래 글을 "완전히 한국식 사건"으로 바꿔라.

규칙:
- 미국 문화 제거
- 한국 직장/연애 상황으로 변경
- 등장인물 한국화
- 사건 구조만 유지
- 번역 느낌 금지
- 블라인드/네이트판 썰처럼 자연스럽게

제목:
{title}

내용:
{content}

출력:
한국에서 실제 있었던 썰처럼 재구성된 사건만 작성
"""

    response = model.generate_content(prompt)
    return response.text

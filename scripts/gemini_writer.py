import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def make_script(title, content):

    prompt = f"""
너는 한국 유튜브 쇼츠 썰자리 작가다.

규칙:
- 1인칭
- 짧은 문장
- 45~60초
- 현실적인 썰
- 과장 금지

출력:
===== 제목 =====
(25자 이내)

===== 대본 =====

Reddit 제목:
{title}

Reddit 본문:
{content}
"""

    response = model.generate_content(prompt)
    return response.text

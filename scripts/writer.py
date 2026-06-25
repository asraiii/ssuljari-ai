import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def make_script(title, content):

    prompt = f"""
너는 한국 쇼츠 썰 작가다.

규칙:
- 1인칭
- 짧은 문장
- 45~60초
- 설명 금지
- 현실 썰 느낌

출력:

===== 제목 =====
===== 대본 =====

제목: {title}
본문: {content}
"""

    res = model.generate_content(prompt)
    return res.text

import os
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
다음 제목을 기반으로

1. 한국 정서로 변환
2. 1인칭 시점
3. 45~60초 쇼츠 분량
4. 훅 포함
5. 반전 포함

제목:

소개팅녀가 제 연봉을 알고 있었습니다.
"""

response = model.generate_content(prompt)

print(response.text)

import os
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
너는 한국 유튜브 쇼츠 썰 채널 작가다.

채널명: 썰자리

규칙:

- 반드시 1인칭 시점
- 45~60초 분량
- 짧은 문장 사용
- 자막용 문장만 작성
- 영상 연출 설명 금지
- 괄호 사용 금지
- 나레이션 표시 금지
- 대사 표시 금지
- 첫 문장은 강한 훅
- 마지막에 반전 또는 결말
- 한국 20~30대 정서에 맞게 변환

구조:

1. 훅
2. 상황 설명
3. 이상한 점 발견
4. 반전
5. 결말

제목:

소개팅녀가 제 연봉을 알고 있었습니다.
"""

response = model.generate_content(prompt)

print("===== 썰자리 대본 =====")
print(response.text)

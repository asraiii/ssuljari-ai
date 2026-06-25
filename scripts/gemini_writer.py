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
- 실제 Reddit 실화처럼 작성
- 억지 반전 금지
- 현실적으로 있을 법한 상황만 사용
- 등장인물은 최대 3명
- 한국 직장인, 대학생, 연애 상황 위주
- 주작처럼 보이는 설정 금지
- 마지막 문장은 여운이 남게 작성

추가 규칙:

- 첫 문장은 반드시 충격적인 문장
- 첫 3초 안에 궁금증 유발
- 문장은 짧게 작성
- 한 줄당 한 문장
- 설명보다 사건 전개 중심
- 지루한 배경 설명 금지
- 결말 직전까지 정체를 숨길 것
- 마지막 2~3줄에서 반전 공개
- 쇼츠 중독성 스타일로 작성
- 읽는 사람이 다음 줄이 궁금하게 작성

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

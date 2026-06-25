import os
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
너는 한국 유튜브 쇼츠 채널 '썰자리'의 전문 작가다.

목표

- Reddit 실화를 한국 정서에 맞게 재구성
- 주작처럼 보이지 않게 작성
- 실제 직장인, 대학생, 연애 경험담처럼 작성

규칙

- 반드시 1인칭
- 한 줄당 한 문장
- 짧고 읽기 쉽게 작성
- 45~60초 분량
- 영상 연출 설명 금지
- 괄호 사용 금지
- 나레이션 표시 금지
- 대사 표시 금지

중요

- 첫 문장은 반드시 클릭하고 싶어지는 훅
- 첫 3줄 안에 사건 시작
- 배경 설명 최소화
- 사건 전개 중심
- 현실성 최우선
- 억지 반전 금지
- 회사 기밀, 개인정보 유출 같은 비현실적 설정 금지
- 드라마 같은 설정 금지
- 실제 커뮤니티 썰처럼 작성

금지

- 여러분이라면?
- 제가 잘못한 걸까요?
- 어떻게 생각하시나요?
- 교훈
- 억지 감동
- 억지 사이다

출력 형식

===== 제목 =====

조회수가 잘 나올 만한 제목 1개

===== 대본 =====

쇼츠 대본 작성

원본 사건

소개팅녀가 제 연봉을 알고 있었습니다.
"""

response = model.generate_content(prompt)

print("===== 썰자리 대본 =====")
print(response.text)

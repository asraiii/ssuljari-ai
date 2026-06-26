import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_content_pack(title, content):

    prompt = f"""
너는 한국 유튜브 쇼츠 채널 '썰자리'의 콘텐츠 제작 AI다.

아래 Reddit 글을 기반으로 조회수가 잘 나올 한국 쇼츠 콘텐츠 패키지를 만들어라.

━━━━━━━━━━━━━━
[Reddit 제목]
{title}

[Reddit 내용]
{content}
━━━━━━━━━━━━━━

목표
- 미국 글을 한국인이 실제 겪은 일처럼 완전히 재구성한다.
- 번역처럼 보이면 실패다.
- 블라인드, 네이트판, 에브리타임에 올라올 것 같은 현실적인 썰을 만든다.

반드시 생성할 것

1. 한국식 쇼츠 썰
- 45~60초 분량
- 완전히 한국화
- 1인칭
- 한 줄 = 한 문장
- 첫 문장은 반드시 강한 훅
- 마지막은 여운 또는 반전
- 등장인물 최대 3명

2. 조회수용 제목 5개
- 클릭하고 싶게 작성
- 한국 쇼츠 스타일
- 짧고 강하게

3. 가장 좋은 썸네일 문구 1개
- 3~6단어
- 가장 클릭률이 높을 문구

4. 가장 좋은 첫 문장 훅 1개
- 영상 시작 1초 안에 시청자를 붙잡을 문장

추가 규칙

- 미국 문화 제거
- 미국 회사 제거
- 미국 학교 제거
- 미국 법률 제거
- 미국 지명 제거

- 한국 직장
- 한국 대학
- 한국 연애
- 한국 결혼
- 한국 가족 문화로 변경

- 설명 금지
- 영상 연출 금지
- 괄호 금지
- 번역체 금지

━━━━━━━━━━━━━━

반드시 JSON 하나만 출력한다.

설명 금지
마크다운 금지
```json 금지
JSON 외의 문자 출력 금지

출력 형식은 반드시 아래와 같다.

{{
  "story": "쇼츠 대본",

  "titles": [
    "제목1",
    "제목2",
    "제목3",
    "제목4",
    "제목5"
  ],

  "thumbnail": "썸네일 문구",

  "hook": "첫 문장",

  "hashtags": [
    "#썰",
    "#연애",
    "#실화",
    "#쇼츠",
    "#썰자리"
  ]
}}

규칙

story는 문자열 하나이다.

titles는 반드시 5개의 문자열 배열이다.

thumbnail은 문자열 하나이다.

hook은 문자열 하나이다.

hashtags는 문자열 배열이다.

JSON 형식이 아니면 실패다.

출력은 반드시 위 JSON만 출력한다.

다른 문장은 절대 출력하지 마라.
"""

    response = model.generate_content(prompt)
    return response.text

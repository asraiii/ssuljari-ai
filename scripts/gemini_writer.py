import os
import json
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_json(text):
    text = text.replace("```json", "").replace("```", "")
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:
        return json.loads(text[start:end+1])
    except:
        return None


def generate_content_pack(title, content):

    prompt = f"""
너는 한국 쇼츠 채널'썰자리'의 콘텐츠 바이럴 전문가다.
조회수가 가장 잘 나올 한국 쇼츠 콘텐츠를 만든다.

목표:
- CTR 최대화
- 시청 유지시간 최대화

입력:
제목: {title}
내용: {content}

규칙:
- 미국 → 한국으로 100% 로컬라이징
- 설명 금지
- 배경 설명 금지
- 감정 설명 금지
- 무조건 사건 중심
- 첫 줄 Hook = 무조건 사건 폭발
- 25자 이하 짧은 문장
- 줄바꿈은 \\n 문자열만 사용

스토리 구조:
1줄: 사건 발생
2줄: 이유 궁금증
3줄: 갈등 폭발
중반: 악화
후반: 반전/폭로/결단/후회

출력 JSON (무조건 이것만):

{{
  "story":"첫줄\\n둘째줄\\n셋째줄",
  "title":"...",
  "thumbnail":"...",
  "hook":"...",
  "bg_video":"cafe",
  "bgm":"tense",
  "emotion":"shock",
  "hashtags":["#썰","#연애","#실화","#쇼츠","#썰자리"]
}}

절대 규칙:
- JSON 외 출력 금지
- 코드블록 금지
- 설명 금지
"""

    for i in range(3):
        try:
            res = model.generate_content(prompt)
            text = res.text.strip()

            data = extract_json(text)

            if not data:
                time.sleep(2)
                continue

            required = [
                "story",
                "title",
                "thumbnail",
                "hook",
                "bg_video",
                "bgm",
                "emotion",
                "hashtags"
            ]

            if not all(k in data for k in required):
                time.sleep(2)
                continue

            data["bg_video"] = data["bg_video"].strip().lower()
            data["bgm"] = data["bgm"].strip().lower()
            data["emotion"] = data["emotion"].strip().lower()

            return data

        except Exception as e:
            print(f"Gemini error: {e}")
            time.sleep(2)

    return None

import os
import json
import re
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_json(text):
    """🔥 JSON만 안전하게 추출 (안정 버전)"""

    # 1. 코드블록 제거
    text = text.replace("```json", "").replace("```", "")

    # 2. JSON 시작/끝 위치 직접 찾기
    start = text.find("{")
    end = text.rfind("}")

    # JSON이 아예 없으면 실패
    if start == -1 or end == -1:
        return None

    json_str = text[start:end+1]

    try:
        return json.loads(json_str)
    except:
        return None

def generate_content_pack(title, content):

    prompt = f"""
너는 대한민국 최고의 쇼츠 스토리 작가다.

입력으로 제공되는 것은 뉴스 기사 또는 실제 사건이다.

너의 역할은

기사를 요약하는 것이 아니다.

기사를

실제 사람이 네이트판, 블라인드, 에브리타임, 디시인사이드에 올린 사연처럼

완전히 재구성하는 것이다.

====================

입력

제목

{title}

내용

{content}

====================

목표

조회수가 가장 잘 나오는

한국 쇼츠 사연 제작

====================

절대 규칙

기사체 금지

기자 말투 금지

설명체 금지

뉴스 요약 금지

사람이 직접 겪은 일처럼 작성

반드시 1인칭

====================

작성 방식

예시

"회사에서 이런 일이 있었습니다."

"친구랑 술 먹다가..."

"결혼 준비 중이었는데..."

"남친이 갑자기..."

처럼 시작한다.

====================

쇼츠 구조

1

첫 문장은

사건부터 시작

설명 금지

20자 이내

2

갈등 확대

3

긴장감 상승

4

반전

5

결말

====================

대본 규칙

45~60초

350~500자

한 줄 = 한 문장

한 문장 최대 25자

줄바꿈은 반드시 \\n

====================

제목

조회수가 가장 잘 나올 제목

12~20자

====================

썸네일

3~8글자

====================

Hook

story 첫 줄과 동일

====================

배경 선택

bg_video

subway
minecraft
rain
cafe
night
office
park

bgm

sad
tense
happy
calm

emotion

sad
shock
anger
happy
regret
revenge

====================

반드시 아래 JSON만 출력

{
"story":"",
"title":"",
"thumbnail":"",
"hook":"",
"bg_video":"",
"bgm":"",
"emotion":"",
"hashtags":[
"#썰",
"#실화",
"#사연",
"#쇼츠",
"#썰자리"
]
}

JSON 외 출력 금지

"""

    # ==========================
    # Gemini Retry
    # ==========================

    for attempt in range(3):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            data = extract_json(text)

            if not data:
                print(f"❌ JSON 파싱 실패 ({attempt+1}/3)")
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
                print(f"❌ 키 부족 ({attempt+1}/3)")
                time.sleep(2)
                continue

            data["bg_video"] = data["bg_video"].strip().lower()
            data["bgm"] = data["bgm"].strip().lower()
            data["emotion"] = data["emotion"].strip().lower()

            valid_bg = [
                "subway",
                "minecraft",
                "rain",
                "cafe",
                "night",
                "office",
                "park"
            ]

            valid_bgm = [
                "sad",
                "tense",
                "happy",
                "calm"
            ]

            valid_emotion = [
                "sad",
                "shock",
                "anger",
                "happy",
                "regret",
                "revenge"
            ]

            if data["bg_video"] not in valid_bg:
                data["bg_video"] = "subway"

            if data["bgm"] not in valid_bgm:
                data["bgm"] = "calm"

            if data["emotion"] not in valid_emotion:
                data["emotion"] = "sad"

            return data

        except Exception as e:

            print(f"Gemini 오류 ({attempt+1}/3) : {e}")
            time.sleep(2)

    print("❌ Gemini 최종 실패")

    return None

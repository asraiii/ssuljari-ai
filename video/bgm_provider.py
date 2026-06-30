import os
import requests
import random

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

BGM_KEYWORDS = {
    "sad": "sad piano",
    "tense": "cinematic tension",
    "happy": "happy upbeat",
    "calm": "ambient background",
    "shock": "dramatic cinematic",
    "anger": "dark tension",
    "regret": "emotional piano",
    "revenge": "intense cinematic",
    "default": "cinematic background"
}


def get_bgm_url(emotion: str):

    emotion = (emotion or "default").lower()

    query = BGM_KEYWORDS.get(
        emotion,
        BGM_KEYWORDS["default"]
    )

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 10
    }

    try:

        response = requests.get(
            PEXELS_VIDEO_URL,
            headers=headers,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        videos = data.get("videos", [])

        if not videos:
            print("❌ Pexels 결과 없음")
            return None

        candidates = []

        for video in videos:

            for file in video.get("video_files", []):

                link = file.get("link", "")

                if ".mp4" in link:
                    candidates.append(file)

        if not candidates:
            print("❌ mp4 없음")
            return None

        candidates.sort(
            key=lambda x: x.get("width", 99999)
        )

        return random.choice(
            candidates[:3]
        )["link"]

    except Exception as e:

        print("❌ Pexels BGM ERROR")
        print(e)

        return None

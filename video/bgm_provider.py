import requests
import random
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


BGM_KEYWORDS = {
    "sad": "sad piano music",
    "angry": "intense cinematic music",
    "suspense": "dark thriller music",
    "happy": "happy upbeat music",
    "shock": "cinematic hit sound",
    "default": "cinematic background music"
}


def get_bgm_url(emotion: str):

    query = BGM_KEYWORDS.get(emotion, BGM_KEYWORDS["default"])

    # ==========================
    # 1. PEXELS FIRST (우선)
    # ==========================
    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"

        headers = {
            "Authorization": PEXELS_API_KEY
        }

        res = requests.get(url, headers=headers).json()

        video_files = res["videos"][0]["video_files"]

        # 가장 작은 mp4 선택
        return random.choice(video_files)["link"]

    except Exception as e:
        print("⚠️ Pexels 실패 → fallback:", e)

    # ==========================
    # 2. FALLBACK (Pixabay)
    # ==========================
    try:
        url = f"https://pixabay.com/api/videos/?key=YOUR_KEY&q={query}"

        res = requests.get(url).json()

        hits = res["hits"]

        return hits[0]["videos"]["small"]["url"]

    except Exception as e:
        print("⚠️ Pixabay 실패 → 최종 fallback:", e)

    # ==========================
    # 3. LAST RESORT (safe silent)
    # ==========================
    return None

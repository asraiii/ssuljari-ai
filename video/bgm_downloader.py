import os
import requests

PIXABAY_KEY = os.getenv("PIXABAY_API_KEY")

def download_bgm(query):
    print("\n==============================")
    print(" BGM DOWNLOAD (API MODE) ")
    print("==============================")

    os.makedirs("output", exist_ok=True)

    # -------------------------
    # 1. Pixabay API 시도
    # -------------------------
    try:
        url = f"https://pixabay.com/api/music/?key={PIXABAY_KEY}&q={query}&per_page=3"

        res = requests.get(url, timeout=10)
        data = res.json()

        if "hits" in data and len(data["hits"]) > 0:
            audio_url = data["hits"][0]["audio"]

            r = requests.get(audio_url, timeout=10)

            path = "output/bgm.mp3"
            with open(path, "wb") as f:
                f.write(r.content)

            print("✅ Pixabay BGM 다운로드 성공")
            return path

    except Exception as e:
        print("❌ Pixabay 실패:", e)

    # -------------------------
    # 2. Pexels fallback
    # -------------------------
    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"

        headers = {
            "Authorization": os.getenv("PEXELS_API_KEY")
        }

        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        video_url = data["videos"][0]["video_files"][0]["link"]

        r = requests.get(video_url, timeout=10)

        path = "output/bgm.mp3"
        with open(path, "wb") as f:
            f.write(r.content)

        print("✅ Pexels fallback 성공")
        return path

    except Exception as e:
        print("❌ Pexels 실패:", e)

    # -------------------------
    # 3. 최종 fallback (무음)
    # -------------------------
    print("❌ 모든 BGM 실패 → 무음 생성")

    path = "output/bgm.mp3"
    os.system(f"ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t 1 {path}")

    return path

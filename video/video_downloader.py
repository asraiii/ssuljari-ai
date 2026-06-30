import os
import requests

PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"


def download_video(query, output_path="output/bg.mp4"):

    api_key = os.getenv("PEXELS_API_KEY")

    if not api_key:
        raise Exception("PEXELS_API_KEY가 없습니다.")

    headers = {
        "Authorization": api_key
    }

    params = {
        "query": query,
        "per_page": 10,
        "orientation": "portrait"
    }

    print("\n==============================")
    print(" VIDEO DOWNLOAD ")
    print("==============================")

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
            print("❌ 검색 결과 없음")
            return None

        video_files = videos[0].get("video_files", [])

        # mp4만 선택
        mp4_files = [
            v for v in video_files
            if ".mp4" in v.get("link", "")
        ]

        if not mp4_files:
            print("❌ mp4 없음")
            return None

        # 가장 작은 mp4 선택
        mp4_files = sorted(
            mp4_files,
            key=lambda x: x.get("width", 99999)
        )

        video_url = mp4_files[0]["link"]

        print("다운로드:", video_url)

        video = requests.get(video_url, timeout=60)

        video.raise_for_status()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(video.content)

        if not os.path.exists(output_path):
            print("❌ 저장 실패")
            return None

        if os.path.getsize(output_path) < 10000:
            print("❌ 영상이 너무 작음")
            return None

        print("✅ 영상 저장 완료")
        print(output_path)

        return output_path

    except Exception as e:

        print("❌ VIDEO DOWNLOAD ERROR")
        print(e)

        return None

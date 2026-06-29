import os
import requests

PEXELS_API_KEY = os.environ["PEXELS_API_KEY"]

PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"


def download_video(query, output_path="output/bg.mp4"):

    print("\n==============================")
    print(" PEXELS VIDEO DOWNLOAD ")
    print("==============================")

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 10,
        "orientation": "portrait"  # 쇼츠용 세로영상
    }

    try:
        response = requests.get(
            PEXELS_VIDEO_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        data = response.json()

        if "videos" not in data or len(data["videos"]) == 0:
            print("❌ 영상 없음")
            return None

        # 가장 첫번째 영상 선택
        video_files = data["videos"][0]["video_files"]

        # 해상도 적당한 것 선택
        video_url = None

        for v in video_files:
            if v.get("quality") == "sd":
                video_url = v["link"]
                break

        if not video_url:
            video_url = video_files[0]["link"]

        print("영상 URL:", video_url)

        video_data = requests.get(video_url, timeout=20)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(video_data.content)

        print(f"✅ 저장 완료: {output_path}")

        return output_path

    except Exception as e:
        print("❌ 다운로드 실패:", e)
        return None

import os
import requests

PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"


def download_video(query, output_path="output/bg.mp4"):

    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

    if not PEXELS_API_KEY:
        raise Exception("PEXELS_API_KEY가 설정되지 않았습니다")

    print("\n==============================")
    print(" PEXELS VIDEO DOWNLOAD ")
    print("==============================")

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 10,
        "orientation": "portrait"
    }

    try:
        response = requests.get(
            PEXELS_VIDEO_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "videos" not in data or len(data["videos"]) == 0:
            print("❌ 영상 없음")
            return None

        video_files = data["videos"][0]["video_files"]

        # --------------------------
        # mp4만 선택
        # --------------------------
        mp4_files = [
            v for v in video_files
            if ".mp4" in v.get("link", "")
        ]

        if not mp4_files:
            print("❌ mp4 파일 없음")
            return None

        # --------------------------
        # 가장 작은 mp4 선택
        # --------------------------
        mp4_files = sorted(
            mp4_files,
            key=lambda x: x.get("width", 99999)
        )

        video_url = mp4_files[0]["link"]

        print("선택된 영상:")
        print(video_url)

        video_data = requests.get(
            video_url,
            timeout=30
        )

        video_data.raise_for_status()

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(output_path, "wb") as f:
            f.write(video_data.content)

        # --------------------------
        # 다운로드 검증
        # --------------------------
        if (
            not os.path.exists(output_path)
            or os.path.getsize(output_path) < 100000
        ):
            print("❌ 다운로드 실패 (파일 손상)")
            return None

        print(f"✅ 저장 완료 : {output_path}")

        return output_path

    except Exception as e:
        print("❌ VIDEO DOWNLOAD ERROR")
        print(e)
        return None

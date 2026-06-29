import os
from video.video_downloader import download_video


def build_video(data):

    print("\n==============================")
    print(" VIDEO BUILDER ")
    print("==============================")

    print(f"제목 : {data['title']}")
    print(f"썸네일 : {data['thumbnail']}")

    print(f"배경영상 : {data['bg_video']}")
    print(f"BGM : {data['bgm']}")
    print(f"감정 : {data['emotion']}")

    print("\n===== STORY =====")

    lines = data["story"].split("\\n")

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    # ==========================
    # ⭐ 여기 핵심 추가 부분
    # ==========================

    print("\n==============================")
    print(" 영상 다운로드 시작 ")
    print("==============================")

    video_path = download_video(data["bg_video"])

    if video_path:
        print(f"\n✅ 영상 다운로드 완료: {video_path}")
    else:
        print("\n❌ 영상 다운로드 실패")

    print("\n영상 제작 준비 완료.")

import os


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

    print("\n영상 제작 준비 완료.")

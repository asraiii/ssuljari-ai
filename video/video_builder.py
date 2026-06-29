import json


def build_video(data):

    print("\n===== VIDEO BUILDER =====")

    print("제목 :", data["title"])
    print("배경 :", data["bg_video"])
    print("BGM :", data["bgm"])
    print("감정 :", data["emotion"])

    print("\n스토리")

    for line in data["story"].split("\\n"):
        print("-", line)

    print("\n영상 제작 시작...")

from scripts.telegram_sender import send_video

from scripts.gemini_writer import (
    generate_content_pack
)

# 🔥 변경됨
from video.video_builder import build_video


def run():

    print("\n[1] TEST MODE (Reddit skip)")

    # ==========================
    # 테스트 데이터
    # ==========================
    post = {
        "title": "남친이 내 통장을 몰래 봤다",
        "content": "I found out my boyfriend secretly checked my bank account and lied about it."
    }

    print("\n[2] Gemini 생성")

    data = generate_content_pack(
        post["title"],
        post["content"]
    )

    if not isinstance(data, dict):
        print("❌ Gemini 실패")
        return None

    required_keys = [
        "story",
        "title",
        "thumbnail",
        "hook",
        "bg_video",
        "bgm",
        "emotion",
        "hashtags"
    ]

    if not all(k in data for k in required_keys):
        print("❌ JSON 구조 실패")
        return None

    print("\n[3] VIDEO BUILDER 실행")

    video_path = build_video(data)

    print("\n[4] Telegram 전송")

    send_video(video_path)

    print("\n🎉 TEST COMPLETE")

    return video_path


if __name__ == "__main__":
    run()

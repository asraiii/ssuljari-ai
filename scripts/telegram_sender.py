import os
import requests


BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_video(video_path):

    if not BOT_TOKEN or not CHAT_ID:
        print("⚠ Telegram 설정 없음")
        return

    if not os.path.exists(video_path):
        print("⚠ 영상 없음")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    with open(video_path, "rb") as video:

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": "🎬 AI 쇼츠 생성 완료"
            },
            files={
                "video": video
            }
        )

    print("✅ Telegram 전송 완료")

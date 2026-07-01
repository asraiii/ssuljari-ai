import os
import requests


def send_video(video_path: str):

    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("❌ Telegram env missing")
        return False

    if not os.path.exists(video_path):
        print("❌ video file not found:", video_path)
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"

    try:
        with open(video_path, "rb") as video:

            files = {
                "video": video
            }

            data = {
                "chat_id": CHAT_ID,
                "supports_streaming": True,
                "caption": "🔥 자동 생성 쇼츠"
            }

            res = requests.post(url, files=files, data=data, timeout=60)

        if res.status_code == 200:
            print("✅ Telegram 전송 성공")
            return True
        else:
            print("❌ Telegram 실패:", res.text)
            return False

    except Exception as e:
        print("❌ Telegram error:", e)
        return False

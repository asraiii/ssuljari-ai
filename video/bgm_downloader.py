import subprocess
import os
from video.bgm_provider import get_bgm_url

OUTPUT = "output/bgm.mp3"


def download_bgm(emotion: str):

    url = get_bgm_url(emotion)

    # ==========================
    # 1. URL 없는 경우
    # ==========================
    if not url:
        print("❌ BGM 없음 → 무음 생성")
        open(OUTPUT, "wb").write(b"")
        return OUTPUT

    # ==========================
    # 2. 다운로드
    # ==========================
    try:
        subprocess.run([
            "curl",
            "-L",
            url,
            "-o",
            OUTPUT
        ], check=True)

    except Exception as e:
        print("❌ 다운로드 실패 → 무음:", e)
        open(OUTPUT, "wb").write(b"")

    # ==========================
    # 3. 안전 보장
    # ==========================
    if not os.path.exists(OUTPUT) or os.path.getsize(OUTPUT) < 1000:
        print("❌ BGM 깨짐 → 무음 fallback")
        open(OUTPUT, "wb").write(b"")

    return OUTPUT

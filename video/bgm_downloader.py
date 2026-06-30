import os
import subprocess

from video.bgm_provider import get_bgm_url

OUTPUT = "output/bgm.mp3"


def download_bgm(emotion: str):

    print("\n==============================")
    print(" BGM DOWNLOAD ")
    print("==============================")

    url = get_bgm_url(emotion)

    if not url:
        print("❌ BGM URL 없음")

        open(OUTPUT, "wb").write(b"")

        return OUTPUT

    try:

        # 다운로드
        subprocess.run([
            "curl",
            "-L",
            url,
            "-o",
            OUTPUT
        ], check=True)

        # 영상이면 오디오 추출
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", OUTPUT,
            "-vn",
            "-acodec", "mp3",
            "output/bgm_fixed.mp3"
        ], check=True)

        os.replace(
            "output/bgm_fixed.mp3",
            OUTPUT
        )

        print("✅ BGM 다운로드 완료")

    except Exception as e:

        print("❌ BGM 다운로드 실패")
        print(e)

        open(OUTPUT, "wb").write(b"")

    if not os.path.exists(OUTPUT):
        open(OUTPUT, "wb").write(b"")

    if os.path.getsize(OUTPUT) < 1000:
        print("❌ BGM 손상 → 무음")
        open(OUTPUT, "wb").write(b"")

    return OUTPUT

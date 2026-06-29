import subprocess
from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm


def build_final_video(data):

    print("\n==============================")
    print(" FINAL VIDEO BUILDER ")
    print("==============================")

    bg = "output/bg.mp4"
    voice = "output/voice.mp3"
    bgm = "output/bgm.mp3"
    output = "output/final.mp4"
    subtitle = "output/subtitle.srt"

    # ==========================
    # 1. 음성 생성
    # ==========================
    create_voice(data["story"])

    # ==========================
    # 2. BGM 다운로드
    # ==========================
    download_bgm(data["bgm"])

    # ==========================
    # 3. 자막 생성
    # ==========================
    lines = data["story"].split("\\n")

    with open(subtitle, "w", encoding="utf-8") as f:

        for i, line in enumerate(lines, start=1):

            start = i * 3
            end = start + 3

            f.write(f"{i}\n")
            f.write(f"00:00:{start:02},000 --> 00:00:{end:02},000\n")
            f.write(line + "\n\n")

    print("✅ 자막 생성 완료")

    # ==========================
    # 4. FFmpeg 합성 (핵심)
    # ==========================

    cmd = [
        "ffmpeg",
        "-y",

        "-i", bg,
        "-i", voice,
        "-i", bgm,

        "-vf", f"subtitles={subtitle}",

        "-filter_complex",
        "[1:a]volume=1.5[a1];[2:a]volume=0.3[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]",

        "-map", "0:v",
        "-map", "[aout]",

        "-c:v", "libx264",
        "-c:a", "aac",

        output
    ]

    subprocess.run(cmd, check=True)

    print("\n🎉 FINAL VIDEO 생성 완료!")
    print("👉", output)

    return output

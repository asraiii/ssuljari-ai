import subprocess
import json
import os

from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm
from video.emotion_timeline import build_emotion_timeline
from video.bgm_selector import select_bgm
from video.subtitle_style_engine import get_subtitle_style


# ==========================
# SAFE UTIL
# ==========================
def safe_file(path):
    return os.path.exists(path) and os.path.getsize(path) > 1000


def get_audio_duration(path):

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    data = json.loads(result.stdout)

    return float(data["format"]["duration"])


# ==========================
# MAIN PIPELINE
# ==========================
def build_final_video(data):

    print("\n==============================")
    print(" FINAL VIDEO BUILDER ")
    print("==============================")

    # ==========================
    # 🔥 절대경로 고정 (핵심)
    # ==========================
    BASE_DIR = os.getcwd()

    bg = os.path.join(BASE_DIR, "output/bg.mp4")
    voice = os.path.join(BASE_DIR, "output/voice.mp3")
    bgm = os.path.join(BASE_DIR, "output/bgm.mp3")
    output = os.path.join(BASE_DIR, "output/final.mp4")
    subtitle = os.path.join(BASE_DIR, "output/subtitle.srt")

    # ==========================
    # 1. TTS 생성
    # ==========================
    print("\n==============================")
    print(" TTS GENERATION ")
    print("==============================")

    create_voice(data["story"])
    print("✅ 음성 생성 완료: output/voice.mp3")

    # ==========================
    # 2. BGM 다운로드
    # ==========================
    print("\n==============================")
    print(" BGM DOWNLOAD ")
    print("==============================")

    download_bgm(data["bgm"])

    # 🔥 BGM fallback 처리
    if not safe_file(bgm):
        print("⚠️ BGM 없음 → 무음 생성")
        open(bgm, "wb").write(b"")

    print("✅ BGM 다운로드 완료: output/bgm.mp3")

    # ==========================
    # 3. 감정 타임라인
    # ==========================
    timeline = build_emotion_timeline(
        data["story"],
        data.get("emotion", "sad")
    )

    # ==========================
    # 4. BGM 선택
    # ==========================
    bgm_tracks = []

    for t in timeline:
        bgm_tracks.append(select_bgm(t["emotion"]))

    # ==========================
    # 5. 자막 생성
    # ==========================
    voice_duration = get_audio_duration(voice)

    lines = data["story"].split("\n")

    if len(lines) == 0:
        lines = [data["story"]]

    time_per_line = voice_duration / len(lines)

    style = get_subtitle_style(data.get("emotion", "default"))

    with open(subtitle, "w", encoding="utf-8") as f:

        current_time = 0

        for i, line in enumerate(lines, start=1):

            start = current_time
            end = current_time + time_per_line

            f.write(f"{i}\n")
            f.write(f"00:00:{int(start):02},000 --> 00:00:{int(end):02},000\n")

            styled_line = line

            if style.get("bold"):
                styled_line = f"**{line}**"

            f.write(styled_line + "\n\n")

            current_time = end

    print("✅ 자막 생성 완료")

    # ==========================
    # 6. bg 영상 체크 + fallback
    # ==========================
    if not safe_file(bg):
        print("❌ bg.mp4 없음 → fallback 생성")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=240x426:d=2",
            bg
        ], check=True)

    # ==========================
    # 7. FINAL CHECK
    # ==========================
    print("\n📦 FINAL CHECK")
    print("bg:", safe_file(bg))
    print("voice:", safe_file(voice))
    print("bgm:", safe_file(bgm))

    # ==========================
    # 8. FFmpeg 합성
    # ==========================
    print("\n==============================")
    print(" FFmpeg START ")
    print("==============================")

    final_filter = "[1:a]volume=1.0[a1];[2:a]volume=0.0[a2];[a1][a2]amix=inputs=2[aout]"

    cmd = [
        "ffmpeg",
        "-y",

        "-i", bg,
        "-i", voice,
        "-i", bgm,

        "-vf", f"subtitles={subtitle}:force_style='Fontsize={style.get('font_size', 24)},PrimaryColour=&HFFFFFF&'",

        "-filter_complex", final_filter,

        "-map", "0:v",
        "-map", "[aout]",

        "-t", str(voice_duration),

        "-c:v", "libx264",
        "-c:a", "aac",

        output
    ]

    subprocess.run(cmd, check=True)

    print("\n🎉 FINAL VIDEO 생성 완료!")
    print("👉", output)

    return output

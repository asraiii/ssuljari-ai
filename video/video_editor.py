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


def ensure_audio_only(path):
    """BGM이 영상이면 오디오로 변환"""
    if not os.path.exists(path):
        return

    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if "video" in result.stdout:
        print("⚠️ BGM이 영상 → 오디오 추출 변환")

        fixed = path.replace(".mp3", "_fixed.mp3")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", path,
            "-vn",
            "-acodec", "mp3",
            fixed
        ], check=True)

        os.replace(fixed, path)


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
# MAIN BUILDER
# ==========================
def build_final_video(data):

    print("\n==============================")
    print(" FINAL VIDEO BUILDER ")
    print("==============================")

    BASE_DIR = os.getcwd()

    bg = os.path.join(BASE_DIR, "output/bg.mp4")
    voice = os.path.join(BASE_DIR, "output/voice.mp3")
    bgm = os.path.join(BASE_DIR, "output/bgm.mp3")
    output = os.path.join(BASE_DIR, "output/final.mp4")
    subtitle = os.path.join(BASE_DIR, "output/subtitle.srt")

    # ==========================
    # TTS
    # ==========================
    print("\n==============================")
    print(" TTS GENERATION ")
    print("==============================")

    create_voice(data["story"])
    print("✅ 음성 생성 완료")

    # ==========================
    # BGM DOWNLOAD
    # ==========================
    print("\n==============================")
    print(" BGM DOWNLOAD ")
    print("==============================")

    download_bgm(data["bgm"])

    if not safe_file(bgm):
        print("❌ BGM 없음 → 무음 생성")
        open(bgm, "wb").write(b"")

    # 🔥 핵심 추가
    ensure_audio_only(bgm)

    print("✅ BGM 준비 완료")

    # ==========================
    # EMOTION TIMELINE
    # ==========================
    timeline = build_emotion_timeline(
        data["story"],
        data.get("emotion", "sad")
    )

    bgm_tracks = []
    for t in timeline:
        bgm_tracks.append(select_bgm(t["emotion"]))

    # ==========================
    # SUBTITLE
    # ==========================
    voice_duration = get_audio_duration(voice)

    lines = data["story"].split("\n")
    if not lines:
        lines = [data["story"]]

    time_per_line = voice_duration / len(lines)

    with open(subtitle, "w", encoding="utf-8") as f:

        current_time = 0

        for i, line in enumerate(lines, 1):

            start = current_time
            end = current_time + time_per_line

            f.write(f"{i}\n")
            f.write(f"00:00:{int(start):02},000 --> 00:00:{int(end):02},000\n")

            style = get_subtitle_style(data.get("emotion", "default"))

            if style["bold"]:
                line = f"**{line}**"

            f.write(line + "\n\n")

            current_time = end

    print("✅ 자막 생성 완료")

    # ==========================
    # FINAL FFmpeg
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

        "-vf", f"subtitles={subtitle}:force_style='Fontsize=30,PrimaryColour=&HFFFFFF&'",

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

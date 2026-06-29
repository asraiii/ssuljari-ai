import subprocess
import json
from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm


# ==========================
# 🎯 감정 기반 자막 스타일
# ==========================
def get_caption_style(emotion):

    styles = {
        "shock": {
            "color": "red",
            "prefix": "🔥",
            "speed": 1.0
        },
        "anger": {
            "color": "red",
            "prefix": "‼️",
            "speed": 1.1
        },
        "sad": {
            "color": "blue",
            "prefix": "…",
            "speed": 0.9
        },
        "happy": {
            "color": "yellow",
            "prefix": "😊",
            "speed": 1.0
        },
        "regret": {
            "color": "gray",
            "prefix": "💭",
            "speed": 0.95
        },
        "revenge": {
            "color": "red",
            "prefix": "💀",
            "speed": 1.05
        }
    }

    return styles.get(emotion, styles["sad"])


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
    # 3. 음성 길이 계산
    # ==========================
    voice_duration = get_audio_duration(voice)

    # ==========================
    # 4. 자막 스타일 적용
    # ==========================
    style = get_caption_style(data["emotion"])

    lines = data["story"].split("\\n")

    time_per_line = voice_duration / len(lines)

    # ==========================
    # 5. SRT 자막 생성 (스타일 적용)
    # ==========================
    with open(subtitle, "w", encoding="utf-8") as f:

        current_time = 0

        for i, line in enumerate(lines, start=1):

            start = current_time
            end = current_time + time_per_line

            styled_line = f"{style['prefix']} {line}"

            f.write(f"{i}\n")
            f.write(f"00:00:{int(start):02},000 --> 00:00:{int(end):02},000\n")
            f.write(styled_line + "\n\n")

            current_time = end

    print("✅ 자막 생성 완료")

    # ==========================
    # 6. FFmpeg 합성
    # ==========================
    vf_filter = f"subtitles={subtitle}"

    # shock / anger는 강조 효과 추가
    if data["emotion"] in ["shock", "anger", "revenge"]:
        vf_filter += ",eq=contrast=1.3:brightness=0.05"

    cmd = [
        "ffmpeg",
        "-y",

        "-i", bg,
        "-i", voice,
        "-i", bgm,

        "-vf", vf_filter,

        "-filter_complex",
        "[1:a]volume=1.5[a1];"
        "[2:a]volume=0.3[a2];"
        "[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]",

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


# ==========================
# AUDIO DURATION
# ==========================
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

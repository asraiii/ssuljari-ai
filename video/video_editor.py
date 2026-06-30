import os
import json
import subprocess

from video.subtitle_style_engine import get_subtitle_style


# ==========================================
# Utility
# ==========================================

def get_audio_duration(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            path
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(json.loads(result.stdout)["format"]["duration"])


# ==========================================
# Subtitle
# ==========================================

def create_subtitle(story, subtitle_path, voice_duration, emotion):

    lines = [x.strip() for x in story.split("\n") if x.strip()]

    if len(lines) == 0:
        lines = [story]

    sec = voice_duration / len(lines)

    style = get_subtitle_style(emotion)

    current = 0

    with open(subtitle_path, "w", encoding="utf-8") as f:

        for i, line in enumerate(lines, 1):

            start = current
            end = current + sec

            if style["bold"]:
                line = f"<b>{line}</b>"

            f.write(f"{i}\n")
            f.write(
                f"00:00:{int(start):02},000 --> 00:00:{int(end):02},000\n"
            )
            f.write(line + "\n\n")

            current = end


# ==========================================
# Video Editor
# ==========================================

def build_final_video(data):

    print("\n==============================")
    print(" VIDEO EDITOR ")
    print("==============================")

    base = os.getcwd()

    bg = os.path.join(base, "output", "bg.mp4")
    voice = os.path.join(base, "output", "voice.mp3")
    bgm = os.path.join(base, "output", "bgm.mp3")
    subtitle = os.path.join(base, "output", "subtitle.srt")
    output = os.path.join(base, "output", "final.mp4")

    # -----------------------------
    # 길이 계산
    # -----------------------------
    voice_duration = get_audio_duration(voice)

    # -----------------------------
    # 자막 생성
    # -----------------------------
    create_subtitle(
        data["story"],
        subtitle,
        voice_duration,
        data.get("emotion", "default")
    )

    print("✅ Subtitle 완료")

    # -----------------------------
    # 영상 합성
    # -----------------------------
    filter_complex = (
        "[1:a]volume=1[a1];"
        "[2:a]volume=0.15[a2];"
        "[a1][a2]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg",
        "-y",

        "-stream_loop", "-1",
        "-i", bg,

        "-i", voice,
        "-i", bgm,

        "-vf",
        f"subtitles={subtitle}:force_style='Fontsize=28,PrimaryColour=&HFFFFFF&'",

        "-filter_complex",
        filter_complex,

        "-map", "0:v",
        "-map", "[aout]",

        "-t",
        str(voice_duration),

        "-c:v",
        "libx264",

        "-c:a",
        "aac",

        "-shortest",

        output
    ]

    subprocess.run(cmd, check=True)

    print("\n🎉 FINAL VIDEO 생성 완료")
    print(output)

    return output

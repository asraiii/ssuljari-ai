import os
import subprocess
import json


# ==========================================
# AUDIO DURATION (안정 버전)
# ==========================================
def get_audio_duration(path):

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            path
        ],
        capture_output=True,
        text=True
    )

    try:
        return float(result.stdout.strip())
    except:
        return 0.0


# ==========================================
# FINAL VIDEO BUILDER (SAFE VERSION)
# ==========================================
def build_final_video(data):

    print("\n==============================")
    print(" VIDEO EDITOR ")
    print("==============================")

    voice = "output/voice.mp3"
    bg = "output/bg.mp4"
    bgm = "output/bgm.mp3"
    subtitle = "output/subtitle.srt"
    output = "output/final.mp4"

    # -----------------------------
    # 1. duration
    # -----------------------------
    voice_duration = get_audio_duration(voice)

    if voice_duration <= 0:
        raise Exception("voice duration invalid")

    # -----------------------------
    # 2. BGM 안전 체크 (핵심)
    # -----------------------------
    use_bgm = (
        os.path.exists(bgm)
        and os.path.getsize(bgm) > 2000
    )

    if not use_bgm:
        print("⚠️ BGM 없음 → 무음 모드")
        bgm = None

    # -----------------------------
    # 3. subtitle filter
    # -----------------------------
    subtitle_filter = f"subtitles={subtitle}:force_style='Fontsize=28,PrimaryColour=&HFFFFFF&'"

    # -----------------------------
    # 4. ffmpeg command
    # -----------------------------
    cmd = [
        "ffmpeg",
        "-y",

        "-stream_loop", "-1",
        "-i", bg,

        "-i", voice,
    ]

    if use_bgm:
        cmd += ["-i", bgm]

    cmd += [
        "-vf", subtitle_filter,
    ]

    # -----------------------------
    # 5. AUDIO MIXING SAFE
    # -----------------------------
    if use_bgm:
        filter_complex = (
            "[1:a]volume=1[a1];"
            "[2:a]volume=0.15[a2];"
            "[a1][a2]amix=inputs=2:duration=first[aout]"
        )

        cmd += [
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
        ]

    else:
        cmd += [
            "-map", "0:v",
            "-map", "1:a",
        ]

    cmd += [
        "-t", str(voice_duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output
    ]

    print("\n==============================")
    print(" FFMEG RUN ")
    print("==============================")

    subprocess.run(cmd, check=True)

    print("\n🎉 VIDEO DONE:", output)

    return output

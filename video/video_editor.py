import os
import subprocess
import json


# ==========================
# AUDIO DURATION
# ==========================
def get_audio_duration(path):

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


# ==========================
# VIDEO BUILD
# ==========================
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

    # ==========================
    # subtitle 체크 (핵심)
    # ==========================
    if not os.path.exists(subtitle):
        print("❌ subtitle 파일 없음 → 자막 스킵")
        subtitle_filter = None
    else:
        subtitle_filter = subtitle.replace("\\", "/")  # ffmpeg safe path

    voice_duration = get_audio_duration(voice)

    # ==========================
    # ffmpeg command
    # ==========================
    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop", "-1",
        "-i", bg,
        "-i", voice,
        "-i", bgm,
    ]

    # subtitle filter (SAFE VERSION)
    if subtitle_filter:
        cmd += [
            "-vf",
            f"subtitles='{subtitle_filter}':force_style='Fontsize=28,PrimaryColour=&HFFFFFF&'"
        ]
    else:
        cmd += ["-vf", "format=yuv420p"]

    cmd += [
        "-filter_complex",
        "[1:a]volume=1[a1];[2:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-t", str(voice_duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output
    ]

    subprocess.run(cmd, check=True)

    print("\n🎉 FINAL VIDEO 생성 완료")
    print(output)

    return output

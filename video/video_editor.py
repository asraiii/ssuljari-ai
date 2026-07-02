import os
import subprocess


def get_audio_duration(path):

    if not os.path.exists(path):
        return 0.0

    result = subprocess.run([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        path
    ], capture_output=True, text=True)

    try:
        return float(result.stdout.strip())
    except:
        return 0.0


def build_final_video(data):

    print("\n==============================")
    print(" VIDEO EDITOR ")
    print("==============================")

    voice = "output/voice.mp3"
    bg = "output/bg.mp4"
    bgm = "output/bgm.mp3"
    subtitle = "output/subtitle.srt"
    output = "output/final.mp4"

    # ==========================
    # 안전 체크
    # ==========================
    if not os.path.exists(voice):
        raise Exception("voice missing")

    if not os.path.exists(bg):
        raise Exception("bg missing")

    voice_duration = get_audio_duration(voice)

    if voice_duration <= 0:
        voice_duration = 60

    # ==========================
    # subtitle 존재 체크 (핵심 수정)
    # ==========================
    if not os.path.exists(subtitle):
        print("⚠️ subtitle 없음 → 스킵")
        subtitle_filter = ""
    else:
        subtitle_filter = f"subtitles={subtitle}:force_style='Fontsize=28,PrimaryColour=&HFFFFFF&'"

    # ==========================
    # BGM 체크
    # ==========================
    use_bgm = os.path.exists(bgm) and os.path.getsize(bgm) > 2000

    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop", "-1",
        "-i", bg,
        "-i", voice,
    ]

    if use_bgm:
        cmd += ["-i", bgm]

    # subtitle filter
    if subtitle_filter:
        cmd += ["-vf", subtitle_filter]

    # audio
    if use_bgm:
        cmd += [
            "-filter_complex",
            "[1:a]volume=1[a1];[2:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
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

    print("\nFFMPEG RUN")
    subprocess.run(cmd, check=True)

    print("DONE:", output)

    return output

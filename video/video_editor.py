import os
import subprocess


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
        text=True
    )

    try:
        return float(result.stdout.strip())
    except:
        return 60.0


def build_final_video(data):

    print("\nVIDEO EDITOR START")

    base = os.getcwd()

    bg = os.path.join(base, "output", "bg.mp4")
    voice = os.path.join(base, "output", "voice.mp3")
    bgm = os.path.join(base, "output", "bgm.mp3")
    subtitle = os.path.join(base, "output", "subtitle.srt")
    output = os.path.join(base, "output", "final.mp4")

    voice_duration = get_audio_duration(voice)

    # --------------------------
    # subtitle 체크 (핵심)
    # --------------------------
    subtitle_flag = os.path.exists(subtitle)

    # --------------------------
    # bgm 체크 (핵심)
    # --------------------------
    bgm_flag = os.path.exists(bgm) and os.path.getsize(bgm) > 1000

    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop", "-1",
        "-i", bg,
        "-i", voice
    ]

    if bgm_flag:
        cmd.append("-i")
        cmd.append(bgm)

    # subtitle filter
    vf = "format=yuv420p"
    if subtitle_flag:
        vf = f"{vf},subtitles={subtitle}"

    cmd += ["-vf", vf]

    # audio
    if bgm_flag:
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

    subprocess.run(cmd, check=True)

    print("VIDEO DONE:", output)
    return output

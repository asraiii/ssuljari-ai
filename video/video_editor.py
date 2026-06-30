import subprocess
import json
import os

from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm
from video.video_downloader import download_video
from video.bgm_selector import select_bgm


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
    # 1. 배경 영상 (무조건 먼저)
    # ==========================
    video_path = download_video(data["bg_video"])

    if not video_path or not os.path.exists(video_path):
        print("❌ 배경영상 실패 → 종료")
        return None

    # ==========================
    # 2. 음성 생성
    # ==========================
    print("\n==============================")
    print(" TTS GENERATION ")
    print("==============================")

    create_voice(data["story"])

    # ==========================
    # 3. BGM 생성 (완전 안정화)
    # ==========================
    print("\n==============================")
    print(" BGM DOWNLOAD ")
    print("==============================")

    bgm_query = select_bgm(data.get("emotion", "default"))
    download_bgm(bgm_query)

    if not os.path.exists(bgm) or os.path.getsize(bgm) < 2000:
        print("❌ BGM 깨짐 → 무음 대체")
        open(bgm, "wb").write(b"")

    # ==========================
    # 4. 길이 계산
    # ==========================
    voice_duration = get_audio_duration(voice)

    # 🔥 핵심 수정: 배경영상 길이에 맞추기
    bg_duration = get_video_duration(bg)

    # 짧으면 loop 처리
    if bg_duration < voice_duration:
        loop_file = "output/bg_loop.mp4"

        loop_cmd = [
            "ffmpeg",
            "-y",
            "-stream_loop", "-1",
            "-i", bg,
            "-t", str(voice_duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            loop_file
        ]

        subprocess.run(loop_cmd, check=True)
        bg = loop_file

    # ==========================
    # 5. 자막 생성
    # ==========================
    lines = data["story"].split("\\n")
    time_per_line = voice_duration / len(lines)

    with open(subtitle, "w", encoding="utf-8") as f:

        current_time = 0

        for i, line in enumerate(lines, start=1):

            start = current_time
            end = current_time + time_per_line

            f.write(f"{i}\n")
            f.write(f"00:00:{int(start):02},000 --> 00:00:{int(end):02},000\n")
            f.write(line + "\n\n")

            current_time = end

    print("✅ 자막 생성 완료")

    # ==========================
    # 6. FFmpeg 합성 (최종 안정)
    # ==========================

    cmd = [
        "ffmpeg",
        "-y",

        "-i", bg,
        "-i", voice,
        "-i", bgm,

        "-vf", f"subtitles={subtitle}",

        "-filter_complex",
        "[1:a]volume=1.0[a1];[2:a]volume=0.0[a2];[a1][a2]amix=inputs=2:duration=first[aout]",

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
# helper functions
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


def get_video_duration(path):

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

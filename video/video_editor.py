import subprocess
import json
import random
from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm


# ==========================
# 🔥 Hook 강화 시스템
# ==========================
def build_hook_variants(story_lines):

    first = story_lines[0]

    hooks = [
        f"“이게 말이 돼?” {first}",
        f"잠깐만… {first}",
        f"충격입니다. {first}",
        f"아무도 몰랐던 이야기. {first}",
        f"이건 진짜 소름입니다. {first}"
    ]

    return random.choice(hooks)


# ==========================
# 🔥 오디오 길이 측정
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


# ==========================
# 🔥 FINAL VIDEO BUILDER
# ==========================
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
    # 3. Hook 강화
    # ==========================
    lines = data["story"].split("\\n")
    hook = build_hook_variants(lines)

    print("\n🔥 HOOK:", hook)

    # 첫 문장 교체
    lines[0] = hook

    # ==========================
    # 4. 음성 길이
    # ==========================
    voice_duration = get_audio_duration(voice)

    # ==========================
    # 5. 자막 생성
    # ==========================
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
    # 6. FFmpeg 합성
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

        "-t", str(voice_duration),

        "-c:v", "libx264",
        "-c:a", "aac",

        output
    ]

    subprocess.run(cmd, check=True)

    print("\n🎉 FINAL VIDEO 생성 완료!")
    print("👉", output)

    return output

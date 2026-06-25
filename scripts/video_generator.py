import os
from gtts import gTTS
from moviepy.editor import *
import textwrap


# =========================
# 1. TTS 생성
# =========================
def generate_audio(text, output_audio="output/audio.mp3"):
    print("\n[1] TTS 생성 중...")

    os.makedirs("output", exist_ok=True)

    tts = gTTS(text=text, lang="ko")
    tts.save(output_audio)

    return output_audio


# =========================
# 2. 자막 생성 (단순 SRT)
# =========================
def generate_subtitles(text, output_srt="output/subtitles.srt"):
    print("\n[2] 자막 생성 중...")

    lines = text.split("\n")

    with open(output_srt, "w", encoding="utf-8") as f:
        start = 0

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            end = start + 3

            f.write(f"{i+1}\n")
            f.write(f"00:00:{start:02d},000 --> 00:00:{end:02d},000\n")
            f.write(line.strip() + "\n\n")

            start += 3

    return output_srt


# =========================
# 3. 영상 생성 (ffmpeg 기반 moviepy)
# =========================
def generate_video(audio_path, text, output_video="output/video.mp4"):
    print("\n[3] 영상 생성 중...")

    os.makedirs("output", exist_ok=True)

    # 배경 (검정 화면)
    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=30)

    # 오디오
    audio = AudioFileClip(audio_path)

    # 텍스트 클립 (자막처럼 출력)
    wrapped_text = "\n".join(textwrap.wrap(text, width=20))

    txt_clip = TextClip(
        wrapped_text,
        fontsize=60,
        color='white',
        size=(1000, None),
        method='caption'
    ).set_position("center").set_duration(audio.duration)

    video = CompositeVideoClip([bg, txt_clip])
    video = video.set_audio(audio)

    video.write_videofile(
        output_video,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_video


# =========================
# FULL PIPELINE
# =========================
def create_short_video(story_text):

    audio = generate_audio(story_text)
    srt = generate_subtitles(story_text)
    video = generate_video(audio, story_text)

    return {
        "audio": audio,
        "subtitle": srt,
        "video": video
    }

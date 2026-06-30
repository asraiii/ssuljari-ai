from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm
from video.video_editor import build_final_video


def build_video(data):

    print("\n==========================")
    print(" VIDEO BUILD START ")
    print("==========================")

    # --------------------------
    # TTS
    # --------------------------

    print("\n[TTS]")
    create_voice(data["story"])

    # --------------------------
    # BGM
    # --------------------------

    print("\n[BGM]")
    download_bgm(data["bgm"])

    # --------------------------
    # FINAL VIDEO
    # --------------------------

    print("\n[EDITOR]")
    output = build_final_video(data)

    print("\n==========================")
    print(" VIDEO COMPLETE ")
    print("==========================")

    return output

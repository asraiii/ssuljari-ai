from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm
from video.video_downloader import download_video
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
    download_bgm(data["emotion"])

    # --------------------------
    # BACKGROUND VIDEO
    # --------------------------

    print("\n[BACKGROUND VIDEO]")
    download_video(
        data["bg_video"],
        "output/bg.mp4"
    )

    # --------------------------
    # FINAL VIDEO
    # --------------------------

    print("\n[VIDEO EDITOR]")
    output = build_final_video(data)

    print("\n==========================")
    print(" VIDEO COMPLETE ")
    print("==========================")

    return output

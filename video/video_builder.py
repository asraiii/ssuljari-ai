from video.voice_generator import create_voice
from video.bgm_downloader import download_bgm
from video.video_downloader import download_video
from video.video_editor import build_final_video


def build_video(data):

    print("\n======================================")
    print("         VIDEO BUILD START")
    print("======================================")

    # ----------------------------------
    # 1. TTS
    # ----------------------------------
    print("\n[1/4] TTS 생성")

    create_voice(
        data["story"]
    )

    print("✅ voice.mp3 완료")

    # ----------------------------------
    # 2. BGM
    # ----------------------------------
    print("\n[2/4] BGM 다운로드")

    download_bgm(
        data.get("emotion", "default")
    )

    print("✅ bgm.mp3 완료")

    # ----------------------------------
    # 3. Background Video
    # ----------------------------------
    print("\n[3/4] 배경영상 다운로드")

    download_video(
        data.get("bg_video", "city night")
    )

    print("✅ bg.mp4 완료")

    # ----------------------------------
    # 4. Final Edit
    # ----------------------------------
    print("\n[4/4] 영상 편집")

    output = build_final_video(data)

    print("\n======================================")
    print("      VIDEO BUILD COMPLETE")
    print("======================================")

    return output

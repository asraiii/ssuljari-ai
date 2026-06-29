import requests
import os


def download_bgm(mood, output_path="output/bgm.mp3"):

    print("\n==============================")
    print(" BGM DOWNLOAD ")
    print("==============================")

    # 무료 샘플 BGM (간단 매핑)
    bgm_map = {
        "sad": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_5c0b2b.mp3",
        "tense": "https://cdn.pixabay.com/download/audio/2022/03/10/audio_2c8f0f.mp3",
        "happy": "https://cdn.pixabay.com/download/audio/2022/03/10/audio_3c8f1f.mp3",
        "calm": "https://cdn.pixabay.com/download/audio/2022/03/10/audio_1c8f0f.mp3"
    }

    url = bgm_map.get(mood, bgm_map["calm"])

    os.makedirs("output", exist_ok=True)

    audio = requests.get(url)

    with open(output_path, "wb") as f:
        f.write(audio.content)

    print(f"✅ BGM 다운로드 완료: {output_path}")

    return output_path

import asyncio
import edge_tts
import os


async def generate_voice(text, output_path="output/voice.mp3"):

    print("\n==============================")
    print(" TTS GENERATION ")
    print("==============================")

    os.makedirs("output", exist_ok=True)

    # 한국어 남성 목소리 (무료)
    voice = "ko-KR-InJoonNeural"

    communicate = edge_tts.Communicate(text, voice)

    await communicate.save(output_path)

    print(f"✅ 음성 생성 완료: {output_path}")

    return output_path


def create_voice(text, output_path="output/voice.mp3"):

    return asyncio.run(generate_voice(text, output_path))

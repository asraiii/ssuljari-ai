import os
import subprocess


def build_final_video(data):

    print("\n==============================")
    print(" VIDEO EDITOR (FFMPEG) ")
    print("==============================")

    input_video = "output/bg.mp4"
    output_video = "output/final.mp4"

    # ==========================
    # 1. 자막 파일 생성 (SRT)
    # ==========================

    subtitles = data["story"].split("\\n")

    srt_path = "output/subtitle.srt"

    with open(srt_path, "w", encoding="utf-8") as f:

        for i, line in enumerate(subtitles, start=1):

            start_time = i * 3
            end_time = start_time + 3

            f.write(f"{i}\n")
            f.write(f"00:00:{start_time:02},000 --> 00:00:{end_time:02},000\n")
            f.write(line + "\n\n")

    print("✅ 자막 생성 완료")

    # ==========================
    # 2. FFmpeg 실행
    # ==========================

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_video
    ]

    try:
        subprocess.run(cmd, check=True)

        print("\n🎉 최종 영상 생성 완료!")
        print("👉", output_video)

        return output_video

    except Exception as e:

        print("❌ FFmpeg 실패:", e)

        return None

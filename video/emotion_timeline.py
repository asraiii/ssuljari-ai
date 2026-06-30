import random

def build_emotion_timeline(story, emotion):

    lines = story.split("\n")

    timeline = []

    for i, line in enumerate(lines):

        # 감정 변화 시뮬레이션 (현실적으로 단순화)
        if i == 0:
            e = "hook"
        elif "?" in line or "!" in line:
            e = "shock"
        elif "몰래" in line or "거짓" in line:
            e = "suspense"
        elif "화" in line or "짜증" in line:
            e = "angry"
        else:
            e = emotion or "sad"

        timeline.append({
            "text": line,
            "emotion": e
        })

    return timeline

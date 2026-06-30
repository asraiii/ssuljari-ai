import random

BGM_MAP = {
    "hook": [
        "dramatic hit",
        "cinematic rise",
        "suspense buildup"
    ],
    "sad": [
        "emotional piano",
        "sad cinematic music",
        "melancholy background"
    ],
    "angry": [
        "dark tension music",
        "intense cinematic",
        "dramatic bass"
    ],
    "suspense": [
        "thriller background",
        "mysterious tension",
        "dark ambient suspense"
    ],
    "happy": [
        "uplifting music",
        "happy background",
        "light acoustic upbeat"
    ],
    "shock": [
        "dramatic hit",
        "cinematic impact",
        "sudden tension music"
    ],
    "default": [
        "cinematic background music",
        "ambient background",
        "soft background music"
    ]
}


def select_bgm(emotion: str):
    emotion = (emotion or "default").lower()

    if emotion not in BGM_MAP:
        emotion = "default"

    return random.choice(BGM_MAP[emotion])

SUBTITLE_STYLE = {
    "hook": {
        "font_size": 42,
        "bold": True,
        "color": "yellow",
        "animation": "pop"
    },

    "shock": {
        "font_size": 38,
        "bold": True,
        "color": "red",
        "animation": "shake"
    },

    "anger": {
        "font_size": 36,
        "bold": True,
        "color": "orange",
        "animation": "shake"
    },

    "sad": {
        "font_size": 34,
        "bold": False,
        "color": "white",
        "animation": "fade"
    },

    "happy": {
        "font_size": 36,
        "bold": True,
        "color": "green",
        "animation": "pop"
    },

    "regret": {
        "font_size": 34,
        "bold": False,
        "color": "white",
        "animation": "fade"
    },

    "revenge": {
        "font_size": 38,
        "bold": True,
        "color": "red",
        "animation": "zoom"
    },

    "default": {
        "font_size": 34,
        "bold": False,
        "color": "white",
        "animation": "none"
    }
}


def get_subtitle_style(emotion: str):

    emotion = (emotion or "default").lower()

    return SUBTITLE_STYLE.get(
        emotion,
        SUBTITLE_STYLE["default"]
    )

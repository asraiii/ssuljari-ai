def get_subtitle_style(emotion: str):

    emotion = (emotion or "default").lower()

    styles = {
        "hook": {
            "color": "yellow",
            "font_size": 26,
            "bold": True
        },
        "sad": {
            "color": "blue",
            "font_size": 24,
            "bold": False
        },
        "angry": {
            "color": "red",
            "font_size": 28,
            "bold": True
        },
        "suspense": {
            "color": "purple",
            "font_size": 25,
            "bold": True
        },
        "shock": {
            "color": "white",
            "font_size": 30,
            "bold": True
        },
        "happy": {
            "color": "green",
            "font_size": 26,
            "bold": False
        },
        "default": {
            "color": "white",
            "font_size": 24,
            "bold": False
        }
    }

    return styles.get(emotion, styles["default"])

import json

from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_content_pack


def run():

    print("\n[1] Reddit 수집")
    posts = fetch_reddit_posts(limit=10)

    print("\n[2] TOP1 선택")
    best_post = pick_best_post(posts)

    print("\n[3] Gemini 생성")
    result = generate_content_pack(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== RAW GEMINI =====")
    print(result)

    # JSON 문자열 → Python 객체
    data = json.loads(result)

    story = data["story"]
    title = data["title"]
    thumbnail = data["thumbnail"]
    hook = data["hook"]
    hashtags = " ".join(data["hashtags"])

    print("\n===== STORY =====")
    print(story)

    print("\n===== TITLE =====")
    print(title)

    print("\n===== THUMBNAIL =====")
    print(thumbnail)

    print("\n===== HOOK =====")
    print(hook)

    print("\n===== HASHTAGS =====")
    print(hashtags)

    return {
        "story": story,
        "title": title,
        "thumbnail": thumbnail,
        "hook": hook,
        "hashtags": hashtags
    }


if __name__ == "__main__":
    run()

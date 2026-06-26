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

    # JSON 문자열 → Python Dictionary
    content = json.loads(result)

    print("\n===== STORY =====")
    print(content["story"])

    print("\n===== TITLE =====")
    print(content["titles"][0])

    print("\n===== THUMBNAIL =====")
    print(content["thumbnail"])

    print("\n===== HOOK =====")
    print(content["hook"])

    print("\n===== HASHTAGS =====")
    print(" ".join(content["hashtags"]))

    return content


if __name__ == "__main__":
    run()

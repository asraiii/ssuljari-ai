import json

from scripts.reddit_worker import (
    fetch_reddit_posts,
    mark_post_as_used
)
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_content_pack


def run():

    print("\n[1] Reddit 수집")
    posts = fetch_reddit_posts(limit=30)

    print("\n[2] TOP1 선택")
    post = pick_best_post(posts)

    if not post:
        print("❌ 후보 없음")
        return None

    print("\n===== Gemini 생성 (ONLY 1 CALL) =====")

    data = generate_content_pack(
        post["title"],
        post["content"]
    )

    if not isinstance(data, dict):
        print("❌ Gemini 실패")
        return None

    required_keys = ["story", "title", "thumbnail", "hook"]

    if not all(k in data for k in required_keys):
        print("❌ JSON 구조 실패:", data)
        return None

    data["reddit_title"] = post["title"]
    data["reddit_content"] = post["content"]

    print(data)

    mark_post_as_used(post)

    return data


if __name__ == "__main__":
    run()

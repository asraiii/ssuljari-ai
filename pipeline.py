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

    print("\n[2] TOP5 선택")
    best_posts = pick_best_post(posts)

    results = []

    for i, post in enumerate(best_posts, start=1):

        if not isinstance(post, dict):
            continue

        if "title" not in post or "content" not in post:
            continue

        print(f"\n===== Gemini 생성 {i}/5 =====")

        data = generate_content_pack(
            post["title"],
            post["content"]
        )

        if not isinstance(data, dict):
            continue

        required_keys = ["story", "title", "thumbnail", "hook"]

        if not all(k in data for k in required_keys):
            continue

        data["reddit_title"] = post["title"]
        data["reddit_content"] = post["content"]

        print(data)

        results.append(data)

    if not results:
        print("❌ 생성 실패")
        return None

    def score(x):
        return (
            len(x.get("story", "")) * 2 +
            len(x.get("title", "")) +
            len(x.get("thumbnail", ""))
        )

    best_result = max(results, key=score)

    # 🔥 여기 수정 (딕셔너리 1개만 전달)
    mark_post_as_used(best_result)

    return best_result


if __name__ == "__main__":
    run()

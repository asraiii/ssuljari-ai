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

        print(f"\n===== Gemini 생성 {i}/5 =====")

        data = generate_content_pack(
            post["title"],
            post["content"]
        )

        # 🔥 여기 중요: gemini_writer가 이미 dict 반환
        if not data:
            continue

        data["reddit_title"] = post["title"]
        data["reddit_content"] = post["content"]

        print(data)

        results.append(data)

    if not results:
        print("생성 실패")
        return None

    best_result = results[0]

    mark_post_as_used(
        best_result["reddit_title"],
        best_result["reddit_content"]
    )

    return best_result


if __name__ == "__main__":
    run()

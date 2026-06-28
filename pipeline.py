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

        result = generate_content_pack(
            post["title"],
            post["content"]
        )

        print(result)

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        start = result.find("{")
        end = result.rfind("}") + 1

        result = result[start:end]

        data = json.loads(result)

        data["reddit_title"] = post["title"]
        data["reddit_content"] = post["content"]

        results.append(data)

    # 아직은 1등을 임시로 첫 번째 결과로 사용
    best_result = results[0]

    mark_post_as_used(
        best_result["reddit_title"],
        best_result["reddit_content"]
    )

    return best_result


if __name__ == "__main__":
    run()

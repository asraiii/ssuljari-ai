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

    if not posts:
        print("사용 가능한 Reddit 글이 없습니다.")
        return None

    print("\n[2] TOP1 선택")
    best_post = pick_best_post(posts)

    print("\n[3] Gemini 생성")
    result = generate_content_pack(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== RAW GEMINI =====")
    print(result)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    start = result.find("{")
    end = result.rfind("}") + 1
    result = result[start:end]

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

    # ✅ 생성 성공한 글만 사용 완료 처리
    mark_post_as_used(best_post)

    print("\n✅ 사용한 Reddit 글을 used_posts.json에 저장했습니다.")

    return {
        "story": story,
        "title": title,
        "thumbnail": thumbnail,
        "hook": hook,
        "hashtags": hashtags
    }


if __name__ == "__main__":
    run()

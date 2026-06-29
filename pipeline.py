import json
from video.video_builder import build_video

from scripts.reddit_worker import (
    fetch_reddit_posts,
    mark_post_as_used
)

from scripts.reddit_scorer import (
    pick_best_post
)

from scripts.gemini_writer import (
    generate_content_pack
)


def run():

    print("\n[1] Reddit 수집")

    posts = fetch_reddit_posts(limit=30)

    if not posts:
        print("❌ Reddit 글을 가져오지 못했습니다.")
        return None

    print("\n[2] TOP1 선택")

    post = pick_best_post(posts)

    if not post:
        print("❌ 후보 없음")
        return None

    print("\n[3] Gemini 생성")

    data = generate_content_pack(
        post["title"],
        post["content"]
    )

    if not isinstance(data, dict):
        print("❌ Gemini 실패")
        return None

    required_keys = [
        "story",
        "title",
        "thumbnail",
        "hook",
        "bg_video",
        "bgm",
        "emotion",
        "hashtags"
    ]

    if not all(k in data for k in required_keys):
        print("❌ JSON 구조 실패")
        return None

    # Reddit 원문 저장
    data["reddit_title"] = post["title"]
    data["reddit_content"] = post["content"]

    # output.json 저장
    with open(
        "output.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n✅ output.json 저장 완료")

    # 사용 완료 표시
    mark_post_as_used(post)

    print("\n🎉 전체 완료")

    build_video(data)

    return data


if __name__ == "__main__":
    run()

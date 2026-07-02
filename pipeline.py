from scripts.telegram_sender import send_video

from scripts.content_fetcher import (
    fetch_posts,
    mark_post_as_used
)

from scripts.content_scorer import (
    pick_best_post
)

from scripts.gemini_writer import (
    generate_content_pack
)

from video.video_builder import build_video


def run():

    print("\n======================================")
    print("           CONTENT FETCH")
    print("======================================")

    posts = fetch_posts()

    post = pick_best_post(posts)

    if not post:
        print("❌ No content found")
        return None

    print("\n======================================")
    print("      GEMINI CONTENT GENERATION")
    print("======================================")

    data = generate_content_pack(
        post["title"],
        post["content"]
    )

    if not isinstance(data, dict):
        print("❌ Gemini 생성 실패")
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
        print("❌ JSON 구조 오류")
        return None

    print("\n======================================")
    print("          VIDEO BUILD")
    print("======================================")

    video_path = build_video(data)

    if not video_path:
        print("❌ 영상 생성 실패")
        return None

    print("\n======================================")
    print("         TELEGRAM SEND")
    print("======================================")

    send_video(video_path)

    mark_post_as_used(post["id"])

    print("\n======================================")
    print("            COMPLETE")
    print("======================================")

    return video_path


if __name__ == "__main__":
    run()

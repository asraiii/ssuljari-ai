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

    print("\n[1] REDDIT FETCH")

    posts = fetch_reddit_posts()

    post = pick_best_post(posts)

    if not post:
        print("❌ No posts found")
        return None

    print("\n[2] GEMINI CONTENT GENERATION")

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

    print("\n[3] VIDEO BUILD")

    video_path = build_video(data)

    print("\n[4] TELEGRAM SEND")

    send_video(video_path)

    mark_post_as_used(post["id"])

    print("\n🎉 COMPLETE")

    return video_path


if __name__ == "__main__":
    run()

from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_content_pack


def run():

    print("\n[1] Reddit 수집")
    posts = fetch_reddit_posts(limit=10)

    print("\n[2] TOP1 선택")
    best_post = pick_best_post(posts)

    print("\n[3] Gemini 1회 생성 (ALL-IN-ONE)")
    content_pack = generate_content_pack(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== RESULT =====")
    print(content_pack)

    return content_pack


if __name__ == "__main__":
    run()

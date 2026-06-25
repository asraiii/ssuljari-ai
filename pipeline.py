from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_ssul
from scripts.ctr_engine import generate_ctr_pack


def run():

    posts = fetch_reddit_posts(limit=5)

    best_post = pick_best_post(posts)

    # 1️⃣ 썰 생성
    result = generate_ssul(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== 썰 =====")
    print(result)

    # 2️⃣ CTR 패키지 생성 (핵심 추가)
    ctr = generate_ctr_pack(result)

    print("\n===== CTR 패키지 =====")
    print(ctr)


if __name__ == "__main__":
    run()

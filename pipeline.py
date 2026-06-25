from scripts.koreanizer import koreanize_story
from scripts.gemini_writer import generate_ssul
from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post


def run():

    posts = fetch_reddit_posts(limit=5)

    best_post = pick_best_post(posts)

    # 1️⃣ 먼저 한국화
    korean_story = koreanize_story(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== 한국화 결과 =====")
    print(korean_story)

    # 2️⃣ 그걸 다시 썰로 변환
    final_script = generate_ssul(
        best_post["title"],
        korean_story
    )

    print("\n===== 최종 썰 =====")
    print(final_script)


if __name__ == "__main__":
    run()

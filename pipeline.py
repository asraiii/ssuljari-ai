from scripts.reddit_worker import fetch_reddit_posts
from scripts.gemini_writer import generate_ssul
from scripts.reddit_scorer import pick_best_post

def run():

    # 1. Reddit 여러 개 가져오기
    posts = fetch_reddit_posts(limit=5)

    # 2. 가장 좋은 글 1개 선택
    best_post = pick_best_post(posts)

    print("\n===== 선택된 원본 =====")
    print(best_post["title"])

    # 3. 썰 생성
    result = generate_ssul(
        best_post["title"],
        best_post["content"]
    )

    print("\n===== 최종 썰 =====")
    print(result)


if __name__ == "__main__":
    run()

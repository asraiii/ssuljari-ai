from scripts.reddit_worker import fetch_reddit_posts
from scripts.gemini_writer import generate_ssul

def run():
    posts = fetch_reddit_posts(limit=3)

    for i, post in enumerate(posts):
        print(f"\n===== {i+1}번 썰 생성 중 =====")

        result = generate_ssul(post["title"], post["content"])

        print("\n[제목]")
        print(post["title"])

        print("\n[썰 결과]")
        print(result)

        print("\n" + "="*50)


if __name__ == "__main__":
    run()

from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_ssul

def run():

    posts = fetch_reddit_posts(limit=5)
    best_post = pick_best_post(posts)

    result = generate_ssul(
        best_post["title"],
        best_post["content"]
    )

    print(result)


if __name__ == "__main__":
    run()

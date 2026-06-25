from scripts.reddit_worker import get_reddit_post
from scripts.gemini_writer import make_script

def run():
    post = get_reddit_post()

    if not post:
        print("Reddit 글 없음")
        return

    script = make_script(post["title"], post["content"])

    print("\n===== 결과 =====\n")
    print(script)

if __name__ == "__main__":
    run()

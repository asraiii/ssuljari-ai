from scripts.reddit_worker import get_best_reddit_post
from scripts.gemini_writer import make_script

post = get_best_reddit_post()

if not post:
    print("No post found")
    exit()

script = make_script(post["title"], post["content"])

print("===== 최종 결과 =====")
print(script)

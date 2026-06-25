from scripts.reddit import get_reddit_post
from scripts.writer import make_script

post = get_reddit_post()

if not post:
    print("No Reddit post")
    exit()

result = make_script(post["title"], post["content"])

print(result)

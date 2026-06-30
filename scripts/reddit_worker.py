import praw
import os
import json
import random

USED_FILE = "output/used_posts.json"

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="ssuljari-ai"
)

SUBREDDITS = [
    "relationship_advice",
    "TrueOffMyChest",
    "AITAH",
    "confession",
    "offmychest",
    "AmItheAsshole"
]


def load_used():

    if not os.path.exists(USED_FILE):
        return []

    try:
        with open(USED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []


def save_used(data):

    os.makedirs("output", exist_ok=True)

    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def fetch_reddit_posts(limit=30):

    used = load_used()

    posts = []

    random.shuffle(SUBREDDITS)

    for subreddit_name in SUBREDDITS:

        try:

            subreddit = reddit.subreddit(subreddit_name)

            for post in subreddit.hot(limit=limit):

                if post.stickied:
                    continue

                if post.id in used:
                    continue

                if len(post.selftext) < 200:
                    continue

                posts.append({

                    "id": post.id,

                    "title": post.title.strip(),

                    "content": post.selftext.strip(),

                    "score": post.score,

                    "comments": post.num_comments,

                    "subreddit": subreddit_name

                })

        except Exception as e:

            print("Reddit 오류:", e)

    posts.sort(
        key=lambda x: (
            x["score"] * 2
            + x["comments"]
        ),
        reverse=True
    )

    return posts


def mark_post_as_used(post_id):

    used = load_used()

    if post_id not in used:

        used.append(post_id)

    save_used(used)

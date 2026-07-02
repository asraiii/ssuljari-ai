import os
import json
import random
import requests

USED_FILE = "output/used_posts.json"

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
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_posts(limit=30):

    used = load_used()

    posts = []

    subreddits = SUBREDDITS.copy()
    random.shuffle(subreddits)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for subreddit in subreddits:

        try:

            url = (
                f"https://www.reddit.com/r/"
                f"{subreddit}/hot.json?limit={limit}"
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                print(f"{subreddit} 실패 : {response.status_code}")
                continue

            data = response.json()

            for item in data["data"]["children"]:

                post = item["data"]

                if post["stickied"]:
                    continue

                if post["id"] in used:
                    continue

                if post["over_18"]:
                    continue

                if len(post.get("selftext", "")) < 200:
                    continue

                posts.append({

                    "id": post["id"],

                    "title": post["title"].strip(),

                    "content": post["selftext"].strip(),

                    "score": post["score"],

                    "comments": post["num_comments"],

                    "subreddit": subreddit

                })

        except Exception as e:

            print(f"{subreddit} 오류 :", e)

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

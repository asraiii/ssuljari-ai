import requests
import json
import os
import time

# =========================
# 수집할 Reddit
# =========================

SUBREDDITS = [
    "relationship_advice",
    "AITAH",
    "AmIOverreacting",
    "TrueOffMyChest"
]

RELATIONSHIP_KEYWORDS = [
    "boyfriend", "girlfriend", "wife", "husband",
    "dating", "relationship", "marriage", "wedding",
    "fiance", "engaged", "proposal",
    "cheating", "affair", "divorce", "breakup"
]

USED_POSTS_FILE = "used_posts.json"


# =========================
# used posts
# =========================

def load_used_posts():
    if not os.path.exists(USED_POSTS_FILE):
        return set()

    try:
        with open(USED_POSTS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()


def save_used_posts(used_posts):
    with open(USED_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(used_posts), f, ensure_ascii=False, indent=2)


# =========================
# Reddit fetch (JSON API)
# =========================

def fetch_subreddit(subreddit, limit=30):

    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (ssuljari-ai bot)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # 🔥 429 / 실패 방지
        if response.status_code != 200:
            print(f"실패 : r/{subreddit} (status {response.status_code})")
            return []

        data = response.json()
        posts = []

        for child in data["data"]["children"]:

            p = child["data"]

            title = p.get("title", "")
            selftext = p.get("selftext", "")
            url = "https://reddit.com" + p.get("permalink", "")

            text = (title + " " + selftext).lower()

            if not any(k in text for k in RELATIONSHIP_KEYWORDS):
                continue

            posts.append({
                "url": url,
                "subreddit": subreddit,
                "title": title,
                "content": selftext[:1500]
            })

        return posts

    except Exception as e:
        print(f"실패 : r/{subreddit} -> {e}")
        return []


# =========================
# main fetch
# =========================

def fetch_reddit_posts(limit=30):

    used_posts = load_used_posts()
    all_posts = []

    for subreddit in SUBREDDITS:

        print(f"\n수집 중 : r/{subreddit}")

        posts = fetch_subreddit(subreddit, limit)

        for p in posts:

            if p["url"] in used_posts:
                continue

            all_posts.append(p)

        # 🔥 핵심: Reddit 보호 (429 방지)
        time.sleep(2)

    print(f"\n총 {len(all_posts)}개 수집 완료")

    return all_posts


# =========================
# used mark
# =========================

def mark_post_as_used(post):

    used_posts = load_used_posts()

    if not isinstance(post, dict):
        return

    url = post.get("url")
    if not url:
        return

    used_posts.add(url)
    save_used_posts(used_posts)

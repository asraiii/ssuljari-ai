import requests
import xml.etree.ElementTree as ET
import json
import os

# =========================
# 수집할 Reddit
# =========================

SUBREDDITS = [
    "relationship_advice",
    "AITAH",
    "AmIOverreacting",
    "TrueOffMyChest"
]

# 연애 키워드
RELATIONSHIP_KEYWORDS = [
    "boyfriend",
    "girlfriend",
    "wife",
    "husband",
    "dating",
    "relationship",
    "marriage",
    "wedding",
    "fiance",
    "engaged",
    "proposal",
    "cheating",
    "affair",
    "divorce",
    "breakup"
]

USED_POSTS_FILE = "used_posts.json"


def load_used_posts():
    if not os.path.exists(USED_POSTS_FILE):
        return set()

    try:
        with open(USED_POSTS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_used_posts(used_posts):
    with open(USED_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(used_posts), f, ensure_ascii=False, indent=2)


def fetch_reddit_posts(limit=30):

    headers = {
        "User-Agent": "ssuljari-ai"
    }

    ns = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    used_posts = load_used_posts()

    posts = []

    for subreddit in SUBREDDITS:

        print(f"수집 중 : r/{subreddit}")

        url = f"https://www.reddit.com/r/{subreddit}/.rss"

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            root = ET.fromstring(response.text)

            entries = root.findall("atom:entry", ns)

            count = 0

            for entry in entries:

                title = entry.find("atom:title", ns)
                content = entry.find("atom:content", ns)
                link = entry.find("atom:link", ns)

                if title is None or content is None or link is None:
                    continue

                post_url = link.attrib.get("href", "")

                # 이미 사용한 글 제외
                if post_url in used_posts:
                    continue

                t = title.text.lower()

                if "rule" in t:
                    continue

                if "karma" in t:
                    continue

                text = (title.text + " " + content.text).lower()

                # 연애 관련만
                if not any(word in text for word in RELATIONSHIP_KEYWORDS):
                    continue

                posts.append({
                    "url": post_url,
                    "subreddit": subreddit,
                    "title": title.text,
                    "content": content.text[:1500]
                })

                count += 1

                if count >= limit:
                    break

        except Exception:
            print(f"실패 : r/{subreddit}")

    print(f"\n총 {len(posts)}개 수집 완료")

    return posts


def mark_post_as_used(post):

    used_posts = load_used_posts()

    # 🔥 안전처리 (url 없으면 그냥 종료)
    url = post.get("url")
    if not url:
        return

    used_posts.add(url)

    save_used_posts(used_posts)

import requests
import xml.etree.ElementTree as ET

# =========================
# 수집할 Reddit
# =========================

SUBREDDITS = [
    "relationship_advice",
    "AITAH",
    "AmIOverreacting",
    "TrueOffMyChest"
]


def fetch_reddit_posts(limit=10):

    headers = {
        "User-Agent": "ssuljari-ai"
    }

    ns = {
        "atom": "http://www.w3.org/2005/Atom"
    }

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

                if title is None or content is None:
                    continue

                t = title.text.lower()

                # 기본 필터
                if "rule" in t:
                    continue

                if "karma" in t:
                    continue

                posts.append({
                    "subreddit": subreddit,
                    "title": title.text,
                    "content": content.text[:1500]
                })

                count += 1

                if count >= limit:
                    break

        except Exception as e:
            print(f"실패 : r/{subreddit}")

    print(f"\n총 {len(posts)}개 수집 완료")

    return posts

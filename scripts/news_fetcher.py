import requests
import feedparser
from urllib.parse import quote

KEYWORDS = [
    "연애",
    "이혼",
    "결혼",
    "불륜",
    "직장",
    "상사",
    "친구",
    "배신",
    "가족",
    "시댁",
    "카톡"
]


def fetch_news():

    posts = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for keyword in KEYWORDS:

        url = (
            "https://news.google.com/rss/search?"
            f"q={quote(keyword)}&hl=ko&gl=KR&ceid=KR:ko"
        )

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries:

                posts.append({

                    "title": entry.title,

                    "url": entry.link,

                    "keyword": keyword

                })

        except Exception as e:

            print(f"{keyword} RSS 실패 :", e)

    return posts

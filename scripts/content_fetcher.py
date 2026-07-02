import requests
import random
import feedparser

RSS_FEEDS = [
    "https://www.yna.co.kr/rss/news.xml",
    "https://rss.donga.com/total.xml",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
]

VIRAL_KEYWORDS = [
    "살인", "이혼", "결혼", "불륜", "사기",
    "폭행", "고소", "갈등", "논란",
    "회사", "해고", "퇴사",
    "연애", "남친", "여친", "부부",
    "돈", "빚", "금전",
    "충돌", "분쟁", "폭로"
]

BLOCK_KEYWORDS = [
    "정치", "경제", "주식", "금리", "환율"
]


def fetch_news(limit=20):

    posts = []
    random.shuffle(RSS_FEEDS)

    for feed_url in RSS_FEEDS:

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:limit]:

                title = entry.get("title", "")
                content = entry.get("summary", "")

                text = (title + " " + content).lower()

                if any(k in text for k in BLOCK_KEYWORDS):
                    continue

                if not any(k in text for k in VIRAL_KEYWORDS):
                    continue

                if len(content) < 200:
                    continue

                posts.append({
                    "id": entry.get("id", title),
                    "title": title,
                    "content": content,
                    "source": feed_url
                })

        except Exception as e:
            print(f"RSS 오류: {e}")

    random.shuffle(posts)
    return posts

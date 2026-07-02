import requests
import random
import feedparser

RSS_FEEDS = [
    "https://www.yna.co.kr/rss/news.xml",
    "https://rss.donga.com/total.xml",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
]

VIRAL_KEYWORDS = [
    "이혼", "결혼", "불륜", "사기", "폭행",
    "고소", "해고", "퇴사", "연애",
    "남친", "여친", "부부", "돈", "빚",
    "배신", "폭로", "갈등", "사건",
    "회사", "직장", "가족", "친구"
]


def fetch_news(limit=20):

    posts = []

    random.shuffle(RSS_FEEDS)

    for url in RSS_FEEDS:

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:limit]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                text = (title + " " + summary).lower()

                # 정치/경제 제거 (쇼츠용 필터)
                if any(x in text for x in ["정치", "경제", "주식", "금리", "환율"]):
                    continue

                # 감정 키워드 없으면 제외
                if not any(k in text for k in VIRAL_KEYWORDS):
                    continue

                # 너무 짧은 건 제외
                if len(summary) < 150:
                    continue

                posts.append({
                    "id": entry.get("id", title),
                    "title": title.strip(),
                    "content": summary.strip(),
                    "source": url
                })

        except Exception as e:
            print(f"RSS 오류: {e}")

    random.shuffle(posts)

    return posts

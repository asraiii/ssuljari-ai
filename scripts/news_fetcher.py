import feedparser
from datetime import datetime, timedelta

RSS_FEEDS = [

    # 국내
    "https://rss.mk.co.kr/rss/30000001/",
    "https://www.hankyung.com/feed/all-news",
    "https://rss.etnews.com/Section902.xml",

    # 해외
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"

]


def fetch_news(limit=30):

    articles = []
    seen = set()

    for rss in RSS_FEEDS:

        try:

            feed = feedparser.parse(rss)

            for entry in feed.entries:

                title = entry.get("title", "").strip()

                summary = entry.get("summary", "").strip()

                link = entry.get("link", "").strip()

                if not title:
                    continue

                key = title.lower()

                if key in seen:
                    continue

                seen.add(key)

                published = entry.get("published", "")

                articles.append({

                    "title": title,
                    "content": summary,
                    "url": link,
                    "published": published

                })

        except Exception as e:

            print("RSS 실패 :", rss)
            print(e)

    articles.sort(
        key=lambda x: x["published"],
        reverse=True
    )

    return articles[:limit]

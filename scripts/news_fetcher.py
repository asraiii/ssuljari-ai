import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


RSS_URLS = [

    "https://rss.donga.com/total.xml",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.hani.co.kr/rss/"

]


HEADERS = {

    "User-Agent": "Mozilla/5.0"

}


def extract_article(url):

    try:

        res = requests.get(

            url,

            headers=HEADERS,

            timeout=10

        )

        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = []

        for p in paragraphs:

            t = p.get_text(" ", strip=True)

            if len(t) > 30:

                text.append(t)

        article = "\n".join(text)

        return article

    except Exception:

        return ""


def fetch_news():

    posts = []

    for rss in RSS_URLS:

        try:

            res = requests.get(

                rss,

                headers=HEADERS,

                timeout=10

            )

            root = ET.fromstring(res.content)

            for item in root.iter("item"):

                title = item.findtext("title")

                link = item.findtext("link")

                if not title or not link:

                    continue

                article = extract_article(link)

                if len(article) < 500:

                    continue

                posts.append({

                    "title": title.strip(),

                    "content": article,

                    "url": link

                })

        except Exception as e:

            print(e)

    return posts

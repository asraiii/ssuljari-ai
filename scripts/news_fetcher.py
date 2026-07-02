import requests
import xml.etree.ElementTree as ET


RSS_URLS = [

    "https://rss.donga.com/total.xml",

    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",

    "https://www.hani.co.kr/rss/"

]


def fetch_news():

    posts = []

    headers = {

        "User-Agent": "Mozilla/5.0"

    }

    for url in RSS_URLS:

        try:

            res = requests.get(

                url,

                headers=headers,

                timeout=10

            )

            root = ET.fromstring(res.content)

            for item in root.iter("item"):

                title = item.findtext("title")

                description = item.findtext("description")

                link = item.findtext("link")

                if not title:

                    continue

                if not description:

                    description = title

                posts.append({

                    "title": title.strip(),

                    "content": description.strip(),

                    "url": link

                })

        except Exception as e:

            print(f"RSS 실패 : {url}")

            print(e)

    return posts

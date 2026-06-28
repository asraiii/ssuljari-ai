import json

from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_content_pack


def run():

    print("\n[1] Reddit 수집")
    posts = fetch_reddit_posts(limit=30)

    print("\n[2] TOP1 선택")
    best_posts = pick_best_post(posts)

    print("\n===== TOP5 후보 =====")

    for i, post in enumerate(best_posts, 1):
        print(f"\n[{i}] {post['title']}")

    combined_content = ""

    for i, post in enumerate(best_posts, 1):
        combined_content += f"""
===== 후보 {i} =====
제목:
{post['title']}

내용:
{post['content']}

"""

    print("\n[3] Gemini 생성")

    result = generate_content_pack(
        "TOP5 Reddit 후보",
        combined_content
    )

    print("\n===== RAW GEMINI =====")
    print(result)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    start = result.find("{")
    end = result.rfind("}") + 1
    result = result[start:end]

    
    # JSON 문자열 → Python 객체
    data = json.loads(result)

    story = data["story"]
    title = data["title"]
    thumbnail = data["thumbnail"]
    hook = data["hook"]
    hashtags = " ".join(data["hashtags"])

    print("\n===== STORY =====")
    print(story)

    print("\n===== TITLE =====")
    print(title)

    print("\n===== THUMBNAIL =====")
    print(thumbnail)

    print("\n===== HOOK =====")
    print(hook)

    print("\n===== HASHTAGS =====")
    print(hashtags)

    return {
        "story": story,
        "title": title,
        "thumbnail": thumbnail,
        "hook": hook,
        "hashtags": hashtags
    }


if __name__ == "__main__":
    run()

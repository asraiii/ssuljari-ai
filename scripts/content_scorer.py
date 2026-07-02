def calculate_score(post):

    score = 0

    title = post.get("title", "").lower()
    content = post.get("content", "").lower()

    text = title + " " + content

    # 쇼츠에서 잘 먹히는 사건 키워드

    viral_keywords = [

        "이혼",
        "불륜",
        "바람",
        "결혼",
        "파혼",
        "폭행",
        "살인",
        "사망",
        "사기",
        "도박",
        "횡령",
        "배신",
        "충돌",
        "경찰",
        "구속",
        "실종",
        "납치",
        "협박",
        "복수",
        "반전",
        "충격",
        "눈물",
        "남편",
        "아내",
        "남친",
        "여친",
        "가족",
        "엄마",
        "아빠",
        "친구",
        "직장",
        "회사"

    ]

    for keyword in viral_keywords:

        if keyword in text:
            score += 40

    # 제목 길이

    title_len = len(post.get("title", ""))

    if 15 <= title_len <= 40:
        score += 30

    # 본문 길이

    length = len(post.get("content", ""))

    if 300 <= length <= 2500:
        score += 50

    elif length > 2500:
        score += 20

    return score


def pick_best_post(posts):

    if not posts:
        return None

    for post in posts:

        post["ai_score"] = calculate_score(post)

    posts.sort(

        key=lambda x: x["ai_score"],

        reverse=True

    )

    print("\n==============================")
    print("      BEST NEWS")
    print("==============================")
    print(posts[0]["title"])
    print("AI SCORE :", posts[0]["ai_score"])

    return posts[0]

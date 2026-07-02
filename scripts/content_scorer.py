def calculate_score(post):

    score = 0

    # 추천수
    score += post.get("score", 0) * 2

    # 댓글수
    score += post.get("comments", 0)

    text = (
        post.get("title", "") + " " +
        post.get("content", "")
    ).lower()

    viral_keywords = [

        "boyfriend",
        "girlfriend",
        "wife",
        "husband",
        "married",
        "dating",
        "cheated",
        "cheating",
        "divorce",
        "pregnant",
        "baby",
        "mother",
        "father",
        "family",
        "friend",
        "best friend",
        "boss",
        "manager",
        "coworker",
        "money",
        "inheritance",
        "wedding",
        "secret",
        "lie",
        "caught",
        "police",
        "revenge",
        "fired",
        "love",
        "affair"

    ]

    for keyword in viral_keywords:
        if keyword in text:
            score += 30

    length = len(post.get("content", ""))

    if 800 <= length <= 4000:
        score += 50
    elif 400 <= length < 800:
        score += 25
    elif length < 400:
        score -= 200
    elif length > 5000:
        score -= 100

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
    print(" BEST CONTENT ")
    print("==============================")
    print("제목 :", posts[0]["title"])
    print("점수 :", posts[0]["ai_score"])

    return posts[0]

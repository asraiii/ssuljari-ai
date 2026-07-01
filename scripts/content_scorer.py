def pick_best_post(posts):

    if not posts:
        return None

    def score(post):

        score = 0

        # 추천수
        score += post.get("score", 0) * 2

        # 댓글수
        score += post.get("comments", 0)

        text = (
            post.get("title", "") + " " +
            post.get("content", "")
        ).lower()

        # 쇼츠에서 잘 먹히는 키워드
        keywords = [
            "boyfriend",
            "girlfriend",
            "husband",
            "wife",
            "married",
            "cheating",
            "divorce",
            "wedding",
            "relationship",
            "mother",
            "father",
            "family",
            "money",
            "bank",
            "friend",
            "boss",
            "job",
            "coworker",
            "secret",
            "lied",
            "caught",
            "pregnant",
            "text",
            "phone",
            "sister",
            "brother"
        ]

        for k in keywords:
            if k in text:
                score += 100

        # 너무 짧은 글 제외
        if len(post.get("content", "")) < 500:
            score -= 300

        # 너무 긴 글 감점
        if len(post.get("content", "")) > 5000:
            score -= 100

        return score

    posts = sorted(
        posts,
        key=score,
        reverse=True
    )

    print("\n==============================")
    print(" BEST REDDIT POST ")
    print("==============================")

    print("제목 :", posts[0]["title"])
    print("점수 :", score(posts[0]))

    return posts[0]

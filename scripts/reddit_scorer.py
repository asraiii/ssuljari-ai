def score_post(title, content):
    text = (title + " " + content).lower()

    score = 0

    # =========================
    # 채널 핵심 컨셉 (90%)
    # =========================

    romance = [
        "girlfriend",
        "boyfriend",
        "wife",
        "husband",
        "fiance",
        "dating",
        "relationship",
        "married",
        "marriage",
        "wedding",
        "proposal",
        "love",
        "crush",
        "ex",
        "ex-wife",
        "ex-husband",
        "cheat",
        "cheating",
        "affair",
        "divorce"
    ]

    # =========================
    # 갈등
    # =========================

    conflict = [
        "argue",
        "fight",
        "lied",
        "secret",
        "betray",
        "cry",
        "toxic",
        "abuse",
        "ignored",
        "blocked",
        "refused"
    ]

    # =========================
    # 직장 (10%)
    # =========================

    work = [
        "boss",
        "coworker",
        "manager",
        "office",
        "company",
        "work"
    ]

    # =========================
    # 조회수 잘 나오는 구조
    # =========================

    curiosity = [
        "aitah",
        "wibta",
        "am i wrong",
        "help"
    ]

    # -------------------------
    # 연애는 가장 높은 점수
    # -------------------------

    score += sum(6 for w in romance if w in text)

    # 갈등
    score += sum(4 for w in conflict if w in text)

    # 직장
    score += sum(2 for w in work if w in text)

    # AITAH
    score += sum(3 for w in curiosity if w in text)

    # -------------------------
    # 길이 보너스
    # -------------------------

    length = len(text)

    if length > 700:
        score += 3

    if length > 1500:
        score += 5

    # -------------------------
    # 조회수 보너스
    # -------------------------

    if "cheat" in text:
        score += 10

    if "affair" in text:
        score += 10

    if "divorce" in text:
        score += 8

    if "ex" in text:
        score += 5

    if "wife" in text and "secret" in text:
        score += 8

    if "husband" in text and "lied" in text:
        score += 8

    return score


def pick_best_post(posts):

    scored = []

    for post in posts:

        score = score_post(
            post["title"],
            post["content"]
        )

        scored.append((score, post))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    print("\n===== TOP POSTS =====")

    for score, post in scored:
        print(f"{score}점 | {post['title']}")

    return scored[0][1]

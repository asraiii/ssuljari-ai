def score_post(title, content):

    text = (title + " " + content).lower()

    score = 0

    # =========================
    # ❤️ 1. 연애 (70%)
    # =========================

    dating = [
        "girlfriend",
        "boyfriend",
        "dating",
        "relationship",
        "love",
        "crush",
        "kiss",
        "date",
        "breakup",
        "ex",
        "ex girlfriend",
        "ex boyfriend"
    ]

    # =========================
    # 💥 2. 바람 / 불륜 (20%)
    # =========================

    cheating = [
        "cheat",
        "cheating",
        "affair",
        "mistress",
        "lover",
        "secret relationship",
        "slept with"
    ]

    # =========================
    # 💍 3. 결혼 (8%)
    # =========================

    marriage = [
        "wife",
        "husband",
        "married",
        "marriage",
        "wedding",
        "fiance",
        "proposal",
        "divorce"
    ]

    # =========================
    # 💼 4. 직장 (2%)
    # =========================

    work = [
        "boss",
        "manager",
        "coworker",
        "office",
        "company",
        "work"
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
    # Reddit 특징
    # =========================

    curiosity = [
        "aitah",
        "wibta",
        "am i wrong",
        "help"
    ]

    # =========================
    # 점수
    # =========================

    score += sum(8 for w in dating if w in text)
    score += sum(6 for w in cheating if w in text)
    score += sum(4 for w in marriage if w in text)
    score += sum(2 for w in work if w in text)

    score += sum(3 for w in conflict if w in text)
    score += sum(2 for w in curiosity if w in text)

    # =========================
    # 길이
    # =========================

    if len(text) > 700:
        score += 3

    if len(text) > 1500:
        score += 5

    # =========================
    # 조회수 보너스
    # =========================

    if "cheating" in text:
        score += 10

    if "affair" in text:
        score += 10

    if "breakup" in text:
        score += 8

    if "ex" in text:
        score += 8

    if "girlfriend" in text and "lied" in text:
        score += 10

    if "boyfriend" in text and "lied" in text:
        score += 10

    if "wife" in text and "cheating" in text:
        score += 10

    if "husband" in text and "cheating" in text:
        score += 10

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

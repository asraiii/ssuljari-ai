def score_post(title, content):

    text = (title + " " + content).lower()

    score = 0

    # ==========================
    # 1. 연애 (최우선)
    # ==========================

    romance = [
        "girlfriend","boyfriend",
        "dating","date",
        "crush","love",
        "relationship",
        "fiance","proposal"
    ]

    # ==========================
    # 2. 불륜
    # ==========================

    affair = [
        "cheat","cheating",
        "affair",
        "mistress",
        "other woman",
        "other man"
    ]

    # ==========================
    # 3. 결혼
    # ==========================

    marriage = [
        "wife","husband",
        "married",
        "wedding",
        "divorce"
    ]

    # ==========================
    # 4. 직장
    # ==========================

    work = [
        "boss",
        "coworker",
        "manager",
        "office",
        "company"
    ]

    # ==========================
    # 감정
    # ==========================

    emotion = [
        "cry",
        "betray",
        "shocked",
        "furious",
        "angry",
        "heartbroken",
        "toxic"
    ]

    # ==========================
    # 반전
    # ==========================

    twist = [
        "found out",
        "turns out",
        "later",
        "however",
        "but",
        "secret",
        "lied"
    ]

    # ==========================
    # 갈등
    # ==========================

    conflict = [
        "fight",
        "argument",
        "accuse",
        "refuse",
        "stormed",
        "ignored"
    ]

    # ==========================
    # 연애 70%
    # ==========================

    score += sum(10 for w in romance if w in text)

    # 불륜 20%
    score += sum(8 for w in affair if w in text)

    # 결혼 8%
    score += sum(5 for w in marriage if w in text)

    # 직장 2%
    score += sum(2 for w in work if w in text)

    # 감정
    score += sum(5 for w in emotion if w in text)

    # 반전
    score += sum(5 for w in twist if w in text)

    # 갈등
    score += sum(4 for w in conflict if w in text)

    # AITAH 계열
    if "aitah" in text:
        score += 5

    if "wibta" in text:
        score += 5

    # 길이 보정
    length = len(text)

    if 700 <= length <= 2500:
        score += 10

    elif length < 300:
        score -= 10

    return score


def pick_best_post(posts):

    scored = []

    for post in posts:

        s = score_post(
            post["title"],
            post["content"]
        )

        scored.append((s, post))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    print("\n===== TOP10 =====")

    for score, post in scored[:10]:

        print(
            f"[{score}] ({post['subreddit']}) {post['title']}"
        )

    return scored[0][1]

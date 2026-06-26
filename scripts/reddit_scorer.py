def score_post(title, content):

    text = (title + " " + content).lower()

    score = 0

    # =========================
    # 1. 감정 폭발 (핵심)
    # =========================
    emotion = [
        "cry", "crying",
        "shocked",
        "furious",
        "angry",
        "heartbroken",
        "betray",
        "trauma"
    ]

    # =========================
    # 2. 반전 / 폭로
    # =========================
    twist = [
        "found out",
        "turns out",
        "later",
        "but",
        "however",
        "secret",
        "lied",
        "cheating",
        "affair"
    ]

    # =========================
    # 3. 갈등 / 싸움
    # =========================
    conflict = [
        "fight",
        "argument",
        "refuse",
        "ignored",
        "stormed",
        "accuse",
        "yelled"
    ]

    # =========================
    # 4. 관계 키워드 (보너스만)
    # =========================
    relationship = [
        "boyfriend",
        "girlfriend",
        "wife",
        "husband",
        "dating",
        "relationship",
        "marriage",
        "divorce",
        "breakup",
        "cheating",
        "affair"
    ]

    # =========================
    # 감정 점수
    # =========================
    score += sum(4 for w in emotion if w in text)

    # 반전 점수
    score += sum(5 for w in twist if w in text)

    # 갈등 점수
    score += sum(4 for w in conflict if w in text)

    # 관계 키워드 (보너스)
    score += sum(2 for w in relationship if w in text)

    # =========================
    # AITAH / 판단형 글
    # =========================
    if "aitah" in text:
        score += 10

    if "wibta" in text:
        score += 8

    # =========================
    # 길이 보정 (중요)
    # =========================
    length = len(text)

    if 800 <= length <= 3000:
        score += 15
    elif length < 400:
        score -= 15

    # =========================
    # 강한 자극 글 추가 보너스
    # =========================
    if "divorce" in text:
        score += 5
    if "cheating" in text:
        score += 5
    if "pregnant" in text:
        score += 3

    return score


def pick_best_post(posts):

    scored = []

    for post in posts:

        s = score_post(post["title"], post["content"])
        scored.append((s, post))

    scored.sort(key=lambda x: x[0], reverse=True)

    print("\n===== TOP10 =====")

    for score, post in scored[:10]:
        print(f"[{score}] ({post['subreddit']}) {post['title']}")

    return scored[0][1]

def score_post(title, content):

    text = (title + " " + content).lower()

    score = 0

    emotion = [
        "cry", "crying",
        "shocked",
        "furious",
        "angry",
        "heartbroken",
        "betray",
        "trauma"
    ]

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

    conflict = [
        "fight",
        "argument",
        "refuse",
        "ignored",
        "stormed",
        "accuse",
        "yelled"
    ]

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

    score += sum(4 for w in emotion if w in text)
    score += sum(5 for w in twist if w in text)
    score += sum(4 for w in conflict if w in text)
    score += sum(2 for w in relationship if w in text)

    if "aitah" in text:
        score += 10

    if "wibta" in text:
        score += 8

    length = len(text)

    if 800 <= length <= 3000:
        score += 15
    elif length < 400:
        score -= 15

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

        if not isinstance(post, dict):
            continue

        if "title" not in post or "content" not in post:
            continue

        s = score_post(post["title"], post["content"])
        scored.append((s, post))

    scored.sort(key=lambda x: x[0], reverse=True)

    print("\n===== TOP10 =====")

    for score, post in scored[:10]:
        subreddit = post.get("subreddit", "unknown")
        print(f"[{score}] ({subreddit}) {post['title']}")

    # 🔥 핵심 수정
    if not scored:
        return None

    return scored[0][1]   # TOP1만 반환

def score_post(title, content):
    text = (title + " " + content).lower()

    score = 0

    emotional = ["cheat", "divorce", "affair", "cry", "betray", "toxic"]
    relation = ["husband", "wife", "girlfriend", "boyfriend", "family", "boss"]
    conflict = ["argue", "fight", "accuse", "lied", "secret"]

    if "aitah" in text or "wibta" in text:
        score += 2

    score += sum(1 for w in emotional if w in text)
    score += sum(1 for w in relation if w in text)
    score += sum(1 for w in conflict if w in text)

    return score


def pick_best_post(posts):
    scored = []

    for post in posts:
        s = score_post(post["title"], post["content"])
        scored.append((s, post))

    scored.sort(key=lambda x: x[0], reverse=True)

    return scored[0][1]

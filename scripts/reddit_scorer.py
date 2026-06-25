def score_post(title, content):
    text = (title + " " + content).lower()

    score = 0

    # 🔥 1. 핵심 감정 키워드 (강한 가중치)
    emotional = ["cheat", "divorce", "affair", "cry", "betray", "toxic", "abuse"]

    # 🔥 2. 인간 관계 (공감 기반)
    relation = ["husband", "wife", "girlfriend", "boyfriend", "family", "boss", "coworker"]

    # 🔥 3. 갈등 구조 (스토리성)
    conflict = ["argue", "fight", "accuse", "lied", "secret", "refuse", "stormed"]

    # 🔥 4. 반전/전개 트리거 (중요)
    twist = ["but", "however", "later", "then", "found out", "turns out"]

    # 🔥 5. 클릭 유도 (유튜브 핵심)
    curiosity = ["aitah", "wibta", "am i wrong", "help", "shocked", "unexpected"]

    # -------------------------
    # 기본 AITAH 가중치
    # -------------------------
    if "aitah" in text or "wibta" in text:
        score += 3

    # -------------------------
    # 키워드 점수 계산
    # -------------------------
    score += sum(2 for w in emotional if w in text)
    score += sum(2 for w in relation if w in text)
    score += sum(3 for w in conflict if w in text)
    score += sum(2 for w in twist if w in text)
    score += sum(3 for w in curiosity if w in text)

    # -------------------------
    # 길이 보정 (너무 짧은 글 제외)
    # -------------------------
    length = len(text)

    if length > 500:
        score += 2
    if length > 1500:
        score += 3

    # -------------------------
    # 강한 감정 폭발 보너스
    # -------------------------
    if "divorce" in text and "cheat" in text:
        score += 5

    if "cry" in text and "betray" in text:
        score += 4

    return score


def pick_best_post(posts):
    scored = []

    for post in posts:
        title = post.get("title", "")
        content = post.get("content", "")

        s = score_post(title, content)

        scored.append((s, post))

    # 점수 높은 순 정렬
    scored.sort(key=lambda x: x[0], reverse=True)

    # 디버깅용 상위 3개 출력 (중요)
    print("\n===== TOP 3 SCORES =====")
    for score, post in scored[:3]:
        print(score, "-", post.get("title", "")[:60])

    return scored[0][1]

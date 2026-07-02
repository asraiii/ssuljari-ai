def calculate_score(post):

    score = 0

    # ==========================
    # 기본 인기 점수
    # ==========================
    score += post.get("score", 0) * 2
    score += post.get("comments", 0)

    # ==========================
    # 텍스트 기반 분석
    # ==========================
    title = post.get("title", "").lower()
    content = post.get("content", "").lower()
    text = title + " " + content

    # ==========================
    # 🔥 바이럴 키워드 (핵심 감정 트리거)
    # ==========================
    viral_keywords = [

        "이혼", "결혼", "바람", "불륜", "사기",
        "폭행", "고소", "협박", "배신",
        "회사", "해고", "퇴사", "직장",
        "남친", "여친", "연애", "부부",
        "돈", "빚", "사기", "금전",
        "폭로", "갈등", "분쟁",
        "엄마", "아빠", "가족",
        "친구", "배신", "거짓말",
        "임신", "출산", "결별"

    ]

    # 키워드 점수
    for keyword in viral_keywords:
        if keyword in text:
            score += 40

    # ==========================
    # 길이 필터 (핵심)
    # ==========================
    length = len(content)

    # 너무 짧으면 감점
    if length < 500:
        score -= 200

    # 쇼츠용 최적 구간
    elif 800 <= length <= 4000:
        score += 80

    # 너무 길면 약간 감점
    elif length > 6000:
        score -= 50

    # ==========================
    # 감정 밀도 보너스
    # ==========================
    emotion_words = [
        "충격", "눈물", "분노", "소름",
        "미쳤다", "진짜", "들켰다", "끝났다"
    ]

    for w in emotion_words:
        if w in text:
            score += 30

    # ==========================
    # 결과 저장용 (디버그)
    # ==========================
    post["ai_score"] = score

    return score


def pick_best_post(posts):

    if not posts:
        return None

    # 점수 계산
    for post in posts:
        post["ai_score"] = calculate_score(post)

    # 정렬
    posts.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    # 로그 출력
    best = posts[0]

    print("\n==============================")
    print(" BEST CONTENT SELECTED ")
    print("==============================")
    print("제목 :", best.get("title"))
    print("점수 :", best.get("ai_score"))

    return best

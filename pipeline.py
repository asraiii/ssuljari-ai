from scripts.reddit_worker import fetch_reddit_posts
from scripts.reddit_scorer import pick_best_post
from scripts.gemini_writer import generate_ssul
from scripts.ctr_engine import generate_ctr_pack


# =========================
# 1. Reddit 수집
# =========================
def step_fetch():
    print("\n[1] Reddit 수집 중...")
    posts = fetch_reddit_posts(limit=10)
    return posts


# =========================
# 2. TOP1 선별
# =========================
def step_select(posts):
    print("\n[2] TOP1 선별 중...")
    best_post = pick_best_post(posts)
    return best_post


# =========================
# 3. 썰 생성
# =========================
def step_generate_story(post):
    print("\n[3] 썰 생성 중...")

    story = generate_ssul(
        post["title"],
        post["content"]
    )

    return story


# =========================
# 4. CTR 생성 (제목/썸네일/훅)
# =========================
def step_generate_ctr(story):
    print("\n[4] CTR 생성 중...")

    ctr = generate_ctr_pack(story)

    return ctr


# =========================
# 5. 콘텐츠 패키징 (핵심)
# =========================
def build_content_bundle(post, story, ctr):
    print("\n[5] 콘텐츠 패키징 중...")

    bundle = {
        "source_title": post["title"],
        "story": story,
        "ctr": ctr
    }

    return bundle


# =========================
# MAIN PIPELINE
# =========================
def run():

    try:
        # 1. 수집
        posts = step_fetch()

        # 2. 선택
        best_post = step_select(posts)

        # 3. 썰 생성
        story = step_generate_story(best_post)

        print("\n===== STORY =====")
        print(story)

        # 4. CTR 생성
        ctr = step_generate_ctr(story)

        print("\n===== CTR =====")
        print(ctr)

        # 5. 패키징
        bundle = build_content_bundle(best_post, story, ctr)

        print("\n===== CONTENT BUNDLE =====")
        print(bundle)

        # =========================
        # 🚀 이후 확장 포인트
        # =========================

        # TODO 6. TTS 생성
        # TODO 7. 자막 생성
        # TODO 8. 영상 생성 (ffmpeg)
        # TODO 9. 업로드

        return bundle

    except Exception as e:
        print("\n[ERROR]", e)
        return None


if __name__ == "__main__":
    run()

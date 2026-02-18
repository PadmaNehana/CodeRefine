from ai_review import generate_ai_review


def handle_github_webhook(payload: dict):
    """
    Handles GitHub PR webhook and returns AI review.
    """

    # Check event type
    action = payload.get("action")
    pr = payload.get("pull_request")

    if not pr or action not in ["opened", "synchronize"]:
        return {"message": "Ignored event"}

    # Get PR title + body as sample code (simple hackathon version)
    code_text = f"""
PR Title: {pr.get('title')}
PR Description: {pr.get('body')}
"""

    # Generate AI review
    review = generate_ai_review(code_text)

    return {
        "pr_title": pr.get("title"),
        "review": review,
    }

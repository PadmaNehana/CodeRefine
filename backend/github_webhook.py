from ai_review import generate_ai_review
from database import save_review


def handle_github_webhook(payload: dict):
    """
    Handle GitHub Pull Request webhook and store AI review
    """

    # Only process pull request events
    if "pull_request" not in payload:
        return {"message": "Not a pull request event"}

    pr = payload["pull_request"]

    repo_name = payload["repository"]["full_name"]
    pr_number = pr["number"]

    # Use PR title + body as context for AI review
    code_content = f"""
PR Title: {pr.get('title')}
PR Description: {pr.get('body')}
"""

    # Generate AI review
    review = generate_ai_review(code_content)

    # ✅ Save correctly with repo + PR number
    save_review(repo_name, pr_number, review)

    return review

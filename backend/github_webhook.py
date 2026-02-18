import os
import requests
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

    # Fetch actual code changes from GitHub API
    github_token = os.getenv("GITHUB_TOKEN", "")
    
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        # Get list of files changed in this PR
        files_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
        files_response = requests.get(files_url, headers=headers, timeout=10)
        
        code_content = f"""
PR Title: {pr.get('title')}
PR Description: {pr.get('body')}

=== CHANGED FILES ===
"""
        
        if files_response.status_code == 200:
            files = files_response.json()
            for file in files[:10]:  # Limit to first 10 files
                filename = file.get('filename', 'unknown')
                patch = file.get('patch', '')
                
                if patch:
                    code_content += f"\n\nFile: {filename}\n{patch}"
        
    except Exception as e:
        print(f"Error fetching files: {e}")
        # Fallback to just PR description
        code_content = f"""
PR Title: {pr.get('title')}
PR Description: {pr.get('body')}
"""

    # Generate AI review
    review = generate_ai_review(code_content)

    # ✅ Save correctly with repo + PR number
    save_review(repo_name, pr_number, review)

    return review

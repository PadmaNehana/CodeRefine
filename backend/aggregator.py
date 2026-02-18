def aggregate_reviews(reviews: list) -> dict:
    """
    Combine multiple AI model responses
    """

    final = {
        "bugs": [],
        "performance": [],
        "security": [],
        "best_practices": [],
        "score": 0,
    }

    for r in reviews:
        final["bugs"] += r.get("bugs", [])
        final["performance"] += r.get("performance", [])
        final["security"] += r.get("security", [])
        final["best_practices"] += r.get("best_practices", [])
        final["score"] += r.get("score", 0)

    if reviews:
        final["score"] = final["score"] // len(reviews)

    return final

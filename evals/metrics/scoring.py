"""
Scoring functions for the Pricing Decision Assistant eval framework.

Each function accepts an agent result dict and a test-case dict and returns
a numeric score in [0.0, 1.0].  compute_eval_score combines them into a
single weighted score and a pass/fail verdict.
"""


def score_confidence_label(actual_label: str, expected_label: str) -> float:
    """
    Exact-match on the confidence label.

    Returns 1.0 on a match, 0.5 if the actual label is adjacent to the
    expected one (e.g. Medium when High was expected), and 0.0 otherwise.
    """
    order = ["Low", "Medium", "High"]

    if actual_label == expected_label:
        return 1.0

    try:
        actual_idx = order.index(actual_label)
        expected_idx = order.index(expected_label)
    except ValueError:
        return 0.0

    if abs(actual_idx - expected_idx) == 1:
        return 0.5

    return 0.0


def score_escalation(actual_escalation: bool, expected_escalation: bool) -> float:
    """
    Binary match on the escalation flag.
    """
    return 1.0 if actual_escalation == expected_escalation else 0.0


def score_keyword_coverage(response: str, keywords: list[str]) -> float:
    """
    Fraction of ground-truth keywords found in the response (case-insensitive).

    Returns 1.0 when the keyword list is empty (nothing to check).
    """
    if not keywords:
        return 1.0

    response_lower = response.lower()
    hits = sum(1 for kw in keywords if kw.lower() in response_lower)
    return hits / len(keywords)


def compute_eval_score(agent_result: dict, test_case: dict) -> dict:
    """
    Compute a composite eval score for a single test case.

    Weights:
        confidence_label  40 %
        escalation        40 %
        keyword_coverage  20 %

    Returns a dict with individual component scores, the weighted total,
    and a boolean `passed` flag (total >= 0.7).
    """
    actual_label = agent_result.get("confidence_label", "")
    actual_escalation = agent_result.get("escalation_required", False)
    final_answer = agent_result.get("final_answer", "") or agent_result.get("answer", "")

    expected_label = test_case.get("expected_confidence_label", "")
    expected_escalation = test_case.get("expected_escalation", False)
    keywords = test_case.get("ground_truth_keywords", [])

    label_score = score_confidence_label(actual_label, expected_label)
    escalation_score = score_escalation(actual_escalation, expected_escalation)
    keyword_score = score_keyword_coverage(final_answer, keywords)

    total = (label_score * 0.4) + (escalation_score * 0.4) + (keyword_score * 0.2)

    return {
        "id": test_case["id"],
        "difficulty": test_case["difficulty"],
        "label_score": round(label_score, 3),
        "escalation_score": round(escalation_score, 3),
        "keyword_score": round(keyword_score, 3),
        "total_score": round(total, 3),
        "passed": total >= 0.7,
    }


def summarise_results(scored_results: list[dict]) -> dict:
    """
    Aggregate individual eval scores into a summary report.
    """
    if not scored_results:
        return {}

    total = len(scored_results)
    passed = sum(1 for r in scored_results if r["passed"])
    avg_score = sum(r["total_score"] for r in scored_results) / total

    by_difficulty: dict[str, dict] = {}
    for r in scored_results:
        diff = r["difficulty"]
        by_difficulty.setdefault(diff, {"total": 0, "passed": 0, "scores": []})
        by_difficulty[diff]["total"] += 1
        by_difficulty[diff]["passed"] += int(r["passed"])
        by_difficulty[diff]["scores"].append(r["total_score"])

    difficulty_summary = {
        diff: {
            "total": v["total"],
            "passed": v["passed"],
            "pass_rate": round(v["passed"] / v["total"], 3),
            "avg_score": round(sum(v["scores"]) / len(v["scores"]), 3),
        }
        for diff, v in by_difficulty.items()
    }

    return {
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 3),
        "avg_score": round(avg_score, 3),
        "by_difficulty": difficulty_summary,
    }

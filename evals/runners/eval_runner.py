"""
Eval runner for the Pricing Decision Assistant.

Usage:
    python -m evals.runners.eval_runner
    python -m evals.runners.eval_runner --dataset evals/datasets/pricing_questions.json
    python -m evals.runners.eval_runner --ids q001 q002 q015   # run specific cases
    python -m evals.runners.eval_runner --difficulty hard       # filter by difficulty

Reports are written to evals/reports/ as timestamped JSON files.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# Allow running from the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.graph import graph
from evals.metrics.scoring import compute_eval_score, summarise_results


DATASET_PATH = os.path.join(os.path.dirname(__file__), "../datasets/pricing_questions.json")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../reports")


def load_test_cases(path: str, ids: list[str] | None = None, difficulty: str | None = None) -> list[dict]:
    with open(path) as f:
        dataset = json.load(f)

    cases = dataset["test_cases"]

    if ids:
        cases = [c for c in cases if c["id"] in ids]

    if difficulty:
        cases = [c for c in cases if c["difficulty"] == difficulty]

    return cases


def run_single_case(test_case: dict) -> dict:
    """Invoke the LangGraph pipeline and return the full agent state."""
    initial_state = {"user_query": test_case["question"]}

    try:
        result = graph.invoke(initial_state)
    except Exception as exc:
        return {
            "error": str(exc),
            "confidence_label": "",
            "escalation_required": False,
            "final_answer": "",
        }

    return result


def run_eval(
    dataset_path: str = DATASET_PATH,
    ids: list[str] | None = None,
    difficulty: str | None = None,
) -> dict:
    test_cases = load_test_cases(dataset_path, ids=ids, difficulty=difficulty)

    if not test_cases:
        print("No test cases matched the given filters.")
        return {}

    print(f"\nRunning {len(test_cases)} eval case(s)...\n")

    scored_results = []
    raw_outputs = []

    for i, case in enumerate(test_cases, start=1):
        print(f"  [{i}/{len(test_cases)}] {case['id']} ({case['difficulty']}) — {case['question'][:70]}...")

        agent_result = run_single_case(case)
        scores = compute_eval_score(agent_result, case)

        status = "PASS" if scores["passed"] else "FAIL"
        print(
            f"         {status}  "
            f"total={scores['total_score']:.2f}  "
            f"label={scores['label_score']:.2f}  "
            f"escalation={scores['escalation_score']:.2f}  "
            f"keywords={scores['keyword_score']:.2f}"
        )

        scored_results.append(scores)
        raw_outputs.append(
            {
                "id": case["id"],
                "question": case["question"],
                "expected_confidence_label": case["expected_confidence_label"],
                "expected_escalation": case["expected_escalation"],
                "actual_confidence_label": agent_result.get("confidence_label", ""),
                "actual_escalation": agent_result.get("escalation_required", False),
                "actual_confidence_score": agent_result.get("confidence_score"),
                "final_answer": agent_result.get("final_answer") or agent_result.get("answer", ""),
                "scores": scores,
            }
        )

    summary = summarise_results(scored_results)

    print(f"\n{'='*60}")
    print(f"  Results: {summary['passed']}/{summary['total_cases']} passed  "
          f"(pass rate {summary['pass_rate']*100:.0f}%,  avg score {summary['avg_score']:.2f})")
    for diff, stats in summary.get("by_difficulty", {}).items():
        print(f"    {diff:8s}  {stats['passed']}/{stats['total']}  avg={stats['avg_score']:.2f}")
    print(f"{'='*60}\n")

    report = {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset": dataset_path,
        "filters": {"ids": ids, "difficulty": difficulty},
        "summary": summary,
        "results": raw_outputs,
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = os.path.join(REPORTS_DIR, f"eval_report_{timestamp}.json")

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report saved to: {report_path}\n")
    return report


def main():
    parser = argparse.ArgumentParser(description="Run pricing assistant evals")
    parser.add_argument(
        "--dataset",
        default=DATASET_PATH,
        help="Path to the test-case JSON dataset",
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        help="Run only these test-case IDs (e.g. --ids q001 q015)",
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Filter by difficulty level",
    )
    args = parser.parse_args()

    run_eval(
        dataset_path=args.dataset,
        ids=args.ids,
        difficulty=args.difficulty,
    )


if __name__ == "__main__":
    main()

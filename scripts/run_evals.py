"""
Convenience entry point for running the Pricing Decision Assistant evals.

Usage:
    python scripts/run_evals.py
    python scripts/run_evals.py --difficulty hard
    python scripts/run_evals.py --ids q001 q015 q018
    python scripts/run_evals.py --dataset evals/datasets/pricing_questions.json

Performs pre-flight checks (env vars, dataset file, agent pipeline) before
handing off to evals.runners.eval_runner.run_eval.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Ensure project root is on the path when running as a script
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

DEFAULT_DATASET = os.path.join(PROJECT_ROOT, "evals", "datasets", "pricing_questions.json")
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "CHROMA_API_KEY", "CHROMA_TENANT", "CHROMA_DATABASE"]


def check_env_vars() -> list[str]:
    """Return a list of any missing required environment variables."""
    # Load .env if present so the check works without a shell export
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    except ImportError:
        pass

    return [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]


def check_dataset(path: str) -> None:
    if not os.path.isfile(path):
        print(f"[ERROR] Dataset not found: {path}")
        sys.exit(1)


def print_dataset_preview(path: str, ids: list[str] | None, difficulty: str | None) -> None:
    with open(path) as f:
        dataset = json.load(f)

    cases = dataset["test_cases"]

    if ids:
        cases = [c for c in cases if c["id"] in ids]
    if difficulty:
        cases = [c for c in cases if c["difficulty"] == difficulty]

    by_difficulty: dict[str, int] = {}
    for c in cases:
        by_difficulty[c["difficulty"]] = by_difficulty.get(c["difficulty"], 0) + 1

    print(f"\nDataset : {os.path.relpath(path, PROJECT_ROOT)}")
    print(f"Cases   : {len(cases)}", end="")
    if by_difficulty:
        breakdown = "  (" + "  ".join(f"{k}: {v}" for k, v in sorted(by_difficulty.items())) + ")"
        print(breakdown, end="")
    print()

    if ids:
        print(f"Filter  : ids={ids}")
    if difficulty:
        print(f"Filter  : difficulty={difficulty}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Pricing Decision Assistant evals")
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
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

    # --- Pre-flight: environment variables ---
    missing = check_env_vars()
    if missing:
        print("[ERROR] Missing required environment variables:")
        for var in missing:
            print(f"         {var}")
        print("\nSet them in a .env file or export them before running.")
        sys.exit(1)

    # --- Pre-flight: dataset file ---
    check_dataset(args.dataset)

    # --- Pre-flight: agent pipeline importable ---
    try:
        from agent.graph import graph  # noqa: F401
    except Exception as exc:
        print(f"[ERROR] Could not import agent pipeline: {exc}")
        sys.exit(1)

    # --- Dataset preview ---
    print_dataset_preview(args.dataset, args.ids, args.difficulty)

    # --- Run ---
    from evals.runners.eval_runner import run_eval

    run_eval(dataset_path=args.dataset, ids=args.ids, difficulty=args.difficulty)


if __name__ == "__main__":
    main()

"""score400 후보들을 반복 평가해 최종 best_weights를 자동 선발합니다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from ga_bot.tools.evaluate_model import evaluate_individual, load_model_from_path
from ga_bot.storage import BEST_MODEL_PATH, SCORE400_DIR
from snake_core import BOARD_CELLS


def parse_args():
    parser = argparse.ArgumentParser(description="Select best model by repeated eval.")
    parser.add_argument("--runs", type=int, default=100, help="Runs per candidate")
    parser.add_argument(
        "--target-score",
        type=int,
        default=BOARD_CELLS,
        help="Success score threshold",
    )
    parser.add_argument(
        "--include-current-best",
        action="store_true",
        help="Include current best_weights.json in candidate pool",
    )
    return parser.parse_args()


def score_key(result: dict) -> tuple:
    return (
        result["success_count"],
        result["avg_score"],
        result["max_score"],
        -result["avg_steps"],
    )


def select_best_candidate(runs: int, target_score: int, include_current_best: bool):
    candidates = sorted(SCORE400_DIR.glob("*.json"))
    if include_current_best and BEST_MODEL_PATH.exists():
        candidates.append(BEST_MODEL_PATH)

    if not candidates:
        raise SystemExit("no candidates found. run training first.")

    best_candidate_path = None
    best_candidate_data = None
    best_result = None

    for candidate_path in candidates:
        model = load_model_from_path(candidate_path)
        result = evaluate_individual(model, runs, target_score)
        print(
            f"{candidate_path.name}: success={result['success_count']}/{result['runs']} "
            f"rate={result['success_rate']:.2%} max={result['max_score']} "
            f"avg={result['avg_score']:.2f}"
        )

        if best_result is None or score_key(result) > score_key(best_result):
            best_result = result
            best_candidate_path = candidate_path
            best_candidate_data = json.loads(candidate_path.read_text(encoding="utf-8"))

    best_candidate_data["selection_eval"] = best_result
    best_candidate_data["selected_from"] = best_candidate_path.name
    BEST_MODEL_PATH.write_text(
        json.dumps(best_candidate_data, indent=2),
        encoding="utf-8",
    )
    return best_candidate_path, best_result


def main():
    args = parse_args()
    best_candidate_path, best_result = select_best_candidate(
        runs=args.runs,
        target_score=args.target_score,
        include_current_best=args.include_current_best,
    )
    print("\nselected:")
    print(best_candidate_path)
    print(json.dumps(best_result, indent=2))


if __name__ == "__main__":
    main()

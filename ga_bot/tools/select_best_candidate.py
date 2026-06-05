"""score400 후보들을 반복 평가해 최종 best_weights를 자동 선발합니다."""

from __future__ import annotations

import argparse
import json
import random
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
        "--rounds",
        type=int,
        default=1,
        help="How many repeated evaluation rounds to average per candidate",
    )
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
    parser.add_argument(
        "--no-write-best",
        action="store_true",
        help="Evaluate and select only; do not overwrite best_weights.json",
    )
    parser.add_argument(
        "--rewrite-fitness-fields",
        action="store_true",
        help=(
            "Rewrite candidate json fitness/score/steps with aggregated "
            "evaluation values under current scoring rule"
        ),
    )
    parser.add_argument(
        "--seed-base",
        type=int,
        default=None,
        help="Optional base seed for deterministic repeated evaluation",
    )
    return parser.parse_args()


def score_key(result: dict) -> tuple:
    return (
        result["success_count"],
        result["avg_score"],
        result["max_score"],
        -result["avg_steps"],
    )


def evaluate_candidate_aggregate(
    model,
    runs: int,
    rounds: int,
    target_score: int,
    seed_base: int | None = None,
) -> dict:
    total_runs = 0
    total_success = 0
    total_score_sum = 0.0
    total_steps_sum = 0.0
    total_fitness_sum = 0.0
    max_fitness = None
    min_fitness = None
    max_score = 0
    min_score = None

    for round_index in range(rounds):
        if seed_base is not None:
            random.seed(seed_base + round_index)
        result = evaluate_individual(model, runs, target_score)
        total_runs += result["runs"]
        total_success += result["success_count"]
        total_score_sum += result["avg_score"] * result["runs"]
        total_steps_sum += result["avg_steps"] * result["runs"]
        total_fitness_sum += result["avg_fitness"] * result["runs"]
        max_score = max(max_score, result["max_score"])
        min_score = result["min_score"] if min_score is None else min(min_score, result["min_score"])
        max_fitness = (
            result["max_fitness"] if max_fitness is None else max(max_fitness, result["max_fitness"])
        )
        min_fitness = (
            result["min_fitness"] if min_fitness is None else min(min_fitness, result["min_fitness"])
        )

    if total_runs <= 0:
        return {
            "rounds": rounds,
            "runs": 0,
            "target_score": target_score,
            "success_count": 0,
            "success_rate": 0.0,
            "max_score": 0,
            "min_score": 0,
            "avg_score": 0.0,
            "avg_steps": 0.0,
            "avg_fitness": 0.0,
            "max_fitness": 0.0,
            "min_fitness": 0.0,
        }

    return {
        "rounds": rounds,
        "runs": total_runs,
        "target_score": target_score,
        "success_count": total_success,
        "success_rate": total_success / total_runs,
        "max_score": max_score,
        "min_score": min_score if min_score is not None else 0,
        "avg_score": total_score_sum / total_runs,
        "avg_steps": total_steps_sum / total_runs,
        "avg_fitness": total_fitness_sum / total_runs,
        "max_fitness": max_fitness if max_fitness is not None else 0.0,
        "min_fitness": min_fitness if min_fitness is not None else 0.0,
    }


def select_best_candidate(
    runs: int,
    rounds: int,
    target_score: int,
    include_current_best: bool,
    write_best: bool = True,
    rewrite_fitness_fields: bool = False,
    seed_base: int | None = None,
):
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
        result = evaluate_candidate_aggregate(
            model,
            runs,
            rounds,
            target_score,
            seed_base=seed_base,
        )
        print(
            f"{candidate_path.name}: success={result['success_count']}/{result['runs']} "
            f"rate={result['success_rate']:.2%} max={result['max_score']} "
            f"avg={result['avg_score']:.2f}"
        )

        if rewrite_fitness_fields:
            data_to_rewrite = json.loads(candidate_path.read_text(encoding="utf-8"))
            data_to_rewrite["fitness"] = int(round(result["avg_fitness"]))
            data_to_rewrite["score"] = int(round(result["avg_score"]))
            data_to_rewrite["steps"] = int(round(result["avg_steps"]))
            data_to_rewrite["recalibrated_eval"] = result
            candidate_path.write_text(
                json.dumps(data_to_rewrite, indent=2),
                encoding="utf-8",
            )

        if best_result is None or score_key(result) > score_key(best_result):
            best_result = result
            best_candidate_path = candidate_path
            best_candidate_data = json.loads(candidate_path.read_text(encoding="utf-8"))

    best_candidate_data["selection_eval"] = best_result
    best_candidate_data["selected_from"] = best_candidate_path.name
    if write_best:
        BEST_MODEL_PATH.write_text(
            json.dumps(best_candidate_data, indent=2),
            encoding="utf-8",
        )
    return best_candidate_path, best_result


def main():
    args = parse_args()
    best_candidate_path, best_result = select_best_candidate(
        runs=args.runs,
        rounds=args.rounds,
        target_score=args.target_score,
        include_current_best=args.include_current_best,
        write_best=not args.no_write_best,
        rewrite_fitness_fields=args.rewrite_fitness_fields,
        seed_base=args.seed_base,
    )
    print("\nselected:")
    print(best_candidate_path)
    print(json.dumps(best_result, indent=2))


if __name__ == "__main__":
    main()

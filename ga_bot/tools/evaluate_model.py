"""저장된 GA 모델을 반복 시뮬레이션으로 평가합니다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from ga_bot.policy import Individual
from ga_bot.simulation import simulate_game
from ga_bot.storage import BEST_MODEL_PATH, load_best_model
from snake_core import BOARD_CELLS


def load_model_from_path(path: Path) -> Individual:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Individual(
        weights=list(data["weights"]),
        fitness=float(data.get("fitness", 0)),
        score=int(data.get("score", 0)),
        steps=int(data.get("steps", 0)),
    )


def evaluate_individual(individual: Individual, runs: int, target_score: int) -> dict:
    scores = []
    steps = []
    fitnesses = []
    success = 0

    for _ in range(runs):
        simulate_game(individual)
        scores.append(individual.score)
        steps.append(individual.steps)
        fitnesses.append(individual.fitness)
        if individual.score >= target_score:
            success += 1

    return {
        "runs": runs,
        "target_score": target_score,
        "success_count": success,
        "success_rate": success / runs if runs else 0.0,
        "max_score": max(scores) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "avg_score": (sum(scores) / len(scores)) if scores else 0.0,
        "avg_steps": (sum(steps) / len(steps)) if steps else 0.0,
        "avg_fitness": (sum(fitnesses) / len(fitnesses)) if fitnesses else 0.0,
        "max_fitness": max(fitnesses) if fitnesses else 0.0,
        "min_fitness": min(fitnesses) if fitnesses else 0.0,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate GA model by repeated games.")
    parser.add_argument(
        "--model-path",
        type=Path,
        default=BEST_MODEL_PATH,
        help="Path to model json file (default: best_weights.json)",
    )
    parser.add_argument("--runs", type=int, default=100, help="Number of runs")
    parser.add_argument(
        "--target-score",
        type=int,
        default=BOARD_CELLS,
        help="Score threshold for success",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.model_path == BEST_MODEL_PATH:
        model = load_best_model()
    else:
        if not args.model_path.exists():
            raise SystemExit(f"model not found: {args.model_path}")
        model = load_model_from_path(args.model_path)

    if model is None:
        raise SystemExit("best_weights.json not found. run training first.")

    result = evaluate_individual(model, args.runs, args.target_score)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

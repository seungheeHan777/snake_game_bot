"""GA 학습/검증/선발 파이프라인 실행 스크립트."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from ga_bot.tools.evaluate_model import evaluate_individual
from ga_bot.tools.select_best_candidate import select_best_candidate
from ga_bot.storage import load_best_model
from ga_bot.trainer import train
from snake_core import BOARD_CELLS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run GA pipeline: train -> evaluate -> select -> evaluate"
    )
    parser.add_argument(
        "--skip-train",
        action="store_true",
        help="Skip training and run evaluation/selection only",
    )
    parser.add_argument(
        "--train-generations",
        type=int,
        default=100,
        help="Training generations for this run",
    )
    parser.add_argument(
        "--early-stop-patience",
        type=int,
        default=50,
        help="Stop training early if best does not improve for this many generations",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Start training from scratch instead of checkpoint resume",
    )
    parser.add_argument("--runs", type=int, default=100, help="Evaluation runs")
    parser.add_argument(
        "--selection-rounds",
        type=int,
        default=1,
        help="Repeated selection rounds per candidate",
    )
    parser.add_argument(
        "--no-write-best",
        action="store_true",
        help="Run selection without overwriting best_weights.json",
    )
    parser.add_argument(
        "--target-score",
        type=int,
        default=BOARD_CELLS,
        help="Success score threshold",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.skip_train:
        train(
            generations=args.train_generations,
            resume=not args.no_resume,
            early_stop_patience=args.early_stop_patience,
        )

    before = load_best_model()
    if before is None:
        raise SystemExit("best_weights.json not found. run training first.")
    before_eval = evaluate_individual(before, args.runs, args.target_score)

    selected_path, selection_eval = select_best_candidate(
        runs=args.runs,
        rounds=args.selection_rounds,
        target_score=args.target_score,
        include_current_best=True,
        write_best=not args.no_write_best,
    )

    after = load_best_model()
    if after is None:
        raise SystemExit("best_weights.json not found after selection.")
    after_eval = evaluate_individual(after, args.runs, args.target_score)

    report = {
        "train_skipped": args.skip_train,
        "train_generations": 0 if args.skip_train else args.train_generations,
        "before_best_eval": before_eval,
        "selected_candidate": str(selected_path),
        "selection_eval": selection_eval,
        "after_best_eval": after_eval,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

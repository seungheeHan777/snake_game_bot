"""Headless repeated evaluation for the stable snake bot."""

import argparse
from datetime import datetime
from time import perf_counter

from apple import Apple
from rule import Rule
from snake import Snake
from stable_bot.hamiltonian import choose_cycle_direction
from stable_bot.planner import StablePlanner


def choose_direction(snake, apple, mode, planner):
    """Choose a direction for the requested evaluation mode."""
    if mode == "fallback":
        return choose_cycle_direction(snake)
    return planner.choose_direction(snake, apple)


def run_once(mode="stable", shortcut_distance=8, max_steps=200000):
    """Run one headless game and return result stats."""
    started_at = datetime.now().astimezone()
    timer_start = perf_counter()
    snake = Snake()
    apple = Apple()
    rule = Rule()
    planner = StablePlanner(shortcut_distance=shortcut_distance)
    steps = 0
    dead = False

    while steps < max_steps and not rule.is_victory(snake):
        direction = choose_direction(snake, apple, mode, planner)
        if direction is None:
            dead = True
            break

        snake.move(direction)
        steps += 1

        if snake.head == apple.position:
            snake.grow()
            apple.relocate(snake.positions)

        if rule.is_game_over(snake):
            dead = True
            break

    elapsed_seconds = perf_counter() - timer_start
    finished_at = datetime.now().astimezone()
    victory = rule.is_victory(snake)
    if victory:
        final_reason = "victory"
    elif dead:
        final_reason = "game_over"
    elif steps >= max_steps:
        final_reason = "max_steps"
    else:
        final_reason = "unknown"

    return {
        "score": snake.score,
        "steps": steps,
        "dead": dead,
        "victory": victory,
        "success": victory,
        "final_reason": final_reason,
        "elapsed_seconds": elapsed_seconds,
        "started_at": started_at,
        "finished_at": finished_at,
    }


def summarize(results):
    """Build aggregate stats for repeated runs."""
    total = len(results)
    victories = [result for result in results if result["victory"]]
    scores = [result["score"] for result in results]
    steps = [result["steps"] for result in results]

    return {
        "runs": total,
        "success_count": len(victories),
        "success_rate": len(victories) / total if total else 0,
        "avg_score": sum(scores) / total if total else 0,
        "max_score": max(scores) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "avg_steps": sum(steps) / total if total else 0,
        "max_steps": max(steps) if steps else 0,
        "min_steps": min(steps) if steps else 0,
    }


def print_summary(summary):
    """Print repeated evaluation stats in a compact format."""
    print(f"runs={summary['runs']}")
    print(
        "success="
        f"{summary['success_count']}/{summary['runs']} "
        f"({summary['success_rate']:.1%})"
    )
    print(
        "score="
        f"avg:{summary['avg_score']:.2f} "
        f"min:{summary['min_score']} "
        f"max:{summary['max_score']}"
    )
    print(
        "steps="
        f"avg:{summary['avg_steps']:.2f} "
        f"min:{summary['min_steps']} "
        f"max:{summary['max_steps']}"
    )


def bot_config_values(mode, shortcut_distance):
    """Return bot config values for the current evaluation mode."""
    if mode == "fallback":
        return {
            "name": "fallback",
            "version": "v1",
            "algorithm_type": "fallback",
            "shortcut_distance": None,
            "uses_shortcut": False,
            "uses_hamiltonian": True,
            "settings_json": {"source": "stable_bot.evaluate"},
        }

    return {
        "name": "stable",
        "version": "v1",
        "algorithm_type": "stable",
        "shortcut_distance": shortcut_distance,
        "uses_shortcut": True,
        "uses_hamiltonian": True,
        "settings_json": {
            "async_shortcut": True,
            "source": "stable_bot.evaluate",
        },
    }


def save_results_to_db(results, summary, args, elapsed_seconds):
    """Save an evaluation session and all game results."""
    from db.repository import (
        create_evaluation_session,
        create_game_run,
        get_or_create_bot_config,
        update_evaluation_session_summary,
    )

    bot_config_id = get_or_create_bot_config(
        **bot_config_values(args.mode, args.shortcut_distance)
    )
    session_id = create_evaluation_session(
        bot_config_id=bot_config_id,
        run_type="headless",
        planned_runs=args.runs,
        memo=args.memo,
    )

    for index, result in enumerate(results, start=1):
        create_game_run(
            evaluation_session_id=session_id,
            bot_config_id=bot_config_id,
            actor_type="bot",
            run_type="headless",
            game_index=index,
            score=result["score"],
            steps=result["steps"],
            success=result["success"],
            dead=result["dead"],
            victory=result["victory"],
            elapsed_seconds=result["elapsed_seconds"],
            final_reason=result["final_reason"],
            shortcut_distance=(
                args.shortcut_distance if args.mode == "stable" else None
            ),
            started_at=result["started_at"],
            finished_at=result["finished_at"],
        )

    update_evaluation_session_summary(
        session_id=session_id,
        success_count=summary["success_count"],
        success_rate=summary["success_rate"],
        avg_score=summary["avg_score"],
        min_score=summary["min_score"],
        max_score=summary["max_score"],
        avg_steps=summary["avg_steps"],
        min_steps=summary["min_steps"],
        max_steps=summary["max_steps"],
        elapsed_seconds=elapsed_seconds,
    )
    return session_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--mode", choices=("stable", "fallback"), default="stable")
    parser.add_argument("--shortcut-distance", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=200000)
    parser.add_argument("--save-db", action="store_true")
    parser.add_argument("--memo")
    args = parser.parse_args()

    timer_start = perf_counter()
    results = [
        run_once(
            mode=args.mode,
            shortcut_distance=args.shortcut_distance,
            max_steps=args.max_steps,
        )
        for _ in range(args.runs)
    ]
    elapsed_seconds = perf_counter() - timer_start
    summary = summarize(results)
    print_summary(summary)

    if args.save_db:
        session_id = save_results_to_db(results, summary, args, elapsed_seconds)
        print(f"saved evaluation_session_id={session_id}")


if __name__ == "__main__":
    main()

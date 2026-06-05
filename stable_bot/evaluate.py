"""Headless repeated evaluation for the stable snake bot."""

import argparse

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

    return {
        "score": snake.score,
        "steps": steps,
        "dead": dead,
        "victory": rule.is_victory(snake),
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--mode", choices=("stable", "fallback"), default="stable")
    parser.add_argument("--shortcut-distance", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=200000)
    args = parser.parse_args()

    results = [
        run_once(
            mode=args.mode,
            shortcut_distance=args.shortcut_distance,
            max_steps=args.max_steps,
        )
        for _ in range(args.runs)
    ]
    print_summary(summarize(results))


if __name__ == "__main__":
    main()

"""Run the deterministic stable snake bot."""

from snake_game import run_game
from stable_bot.planner import StablePlanner


def run_stable_bot():
    """Connect the stable bot planner to the shared pygame runner."""
    planner = StablePlanner()
    run_game(
        choose_direction=planner,
        title="stable snake bot",
        move_interval=0.03,
    )


if __name__ == "__main__":
    run_stable_bot()

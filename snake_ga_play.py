"""저장된 유전 알고리즘 최고 모델로 게임을 실행합니다."""

from ga_bot.policy import choose_direction
from ga_bot.storage import load_best_model
from snake_game import run_game


def run_ga_model():
    """best_weights.json을 불러와 pygame 화면에서 플레이를 보여줍니다."""
    model = load_best_model()
    if model is None:
        raise SystemExit(
            "best_weights.json이 없습니다. 먼저 python snake_ga_bot.py로 학습하세요."
        )

    def choose_ga_direction(snake, apple):
        return choose_direction(
            model,
            snake.positions,
            snake.direction,
            apple.position,
        )

    run_game(
        choose_direction=choose_ga_direction,
        title="snake ga bot",
        move_interval=0.03,
    )


if __name__ == "__main__":
    run_ga_model()

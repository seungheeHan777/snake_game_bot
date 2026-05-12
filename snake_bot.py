"""경로 탐색 봇의 방향 선택 로직을 정의합니다."""

from snake_core import (
    DIRECTION_ORDER,
    can_change_direction,
    is_self_collision,
    is_wall_collision,
    move_snake,
    next_position,
)
from snake_game import run_game


def distance_to_food(position, food_position):
    """현재 좌표와 먹이 좌표 사이의 맨해튼 거리를 계산합니다."""
    return abs(position[0] - food_position[0]) + abs(position[1] - food_position[1])


def is_safe_direction(snake, direction):
    """direction으로 한 칸 이동했을 때 바로 죽지 않는지 확인합니다."""
    if not can_change_direction(snake.direction, direction):
        return False

    test_positions = [position.copy() for position in snake.positions]
    move_snake(test_positions, direction)
    return (
        not is_wall_collision(test_positions[0])
        and not is_self_collision(test_positions)
    )


def choose_greedy_direction(snake, apple):
    """먹이에 가까워지는 안전한 방향을 고릅니다."""
    candidates = []
    for direction in DIRECTION_ORDER:
        if not is_safe_direction(snake, direction):
            continue
        next_head = next_position(snake.head, direction)
        candidates.append((distance_to_food(next_head, apple.position), direction))

    if not candidates:
        return None

    candidates.sort()
    return candidates[0][1]


def run_bot():
    """공통 게임 실행 흐름에 greedy 방향 선택 함수를 연결합니다."""
    run_game(
        choose_direction=choose_greedy_direction,
        title="snake bot",
        move_interval=0.1,
    )


if __name__ == "__main__":
    run_bot()

"""유전 알고리즘 개체가 방향을 선택하는 정책 코드입니다.

가중치 특징값은 아직 확정 전 초안입니다. FEATURE_NAMES와
direction_features()는 사용자와 논의한 뒤 조정합니다.
"""

from dataclasses import dataclass

from snake_core import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_SIZE,
    DIRECTION_ORDER,
    can_change_direction,
    is_self_collision,
    is_wall_collision,
    move_snake,
    next_position,
)

FEATURE_NAMES = (
    "food_distance_delta",
    "wall_risk",
    "body_risk",
    "keep_direction",
    "next_x",
    "next_y",
)


@dataclass
class Individual:
    """하나의 유전 알고리즘 개체입니다."""

    weights: list[float]
    fitness: float = 0
    score: int = 0
    steps: int = 0


def copy_positions(positions):
    """시뮬레이션 중 원본 좌표가 바뀌지 않도록 좌표 목록을 복사합니다."""
    return [position.copy() for position in positions]


def distance_to_food(position, food_position):
    """현재 좌표와 먹이 좌표 사이의 맨해튼 거리를 계산합니다."""
    return abs(position[0] - food_position[0]) + abs(position[1] - food_position[1])


def is_safe_move(snake_positions, direction):
    """해당 방향으로 한 칸 움직였을 때 바로 죽지 않는지 확인합니다."""
    test_positions = copy_positions(snake_positions)
    move_snake(test_positions, direction)
    return (
        not is_wall_collision(test_positions[0])
        and not is_self_collision(test_positions)
    )


def direction_features(snake_positions, current_direction, food_position, direction):
    """방향 하나를 평가하기 위한 특징값을 만듭니다."""
    head = snake_positions[0]
    next_head = next_position(head, direction)
    before_distance = distance_to_food(head, food_position)
    after_distance = distance_to_food(next_head, food_position)
    board_span = BOARD_WIDTH + BOARD_HEIGHT

    return [
        (before_distance - after_distance) / CELL_SIZE,
        1 if is_wall_collision(next_head) else 0,
        1 if next_head in snake_positions[1:] else 0,
        1 if direction == current_direction else 0,
        next_head[0] / board_span,
        next_head[1] / board_span,
    ]


def weighted_score(weights, features):
    """개체의 가중치와 특징값으로 방향 점수를 계산합니다."""
    return sum(weight * feature for weight, feature in zip(weights, features))


def choose_direction(individual, snake_positions, current_direction, food_position):
    """개체의 가중치를 기준으로 다음 이동 방향을 선택합니다."""
    candidates = []
    for direction in DIRECTION_ORDER:
        if not can_change_direction(current_direction, direction):
            continue

        features = direction_features(
            snake_positions,
            current_direction,
            food_position,
            direction,
        )
        candidates.append((
            is_safe_move(snake_positions, direction),
            weighted_score(individual.weights, features),
            direction,
        ))

    safe_candidates = [candidate for candidate in candidates if candidate[0]]
    if safe_candidates:
        candidates = safe_candidates
    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][2]


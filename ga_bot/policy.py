"""유전 알고리즘 개체가 방향을 선택하는 정책 코드입니다.

가중치 특징값은 아직 확정 전 초안입니다. FEATURE_NAMES와
direction_features()는 사용자와 논의한 뒤 조정합니다.
"""

from collections import deque
from dataclasses import dataclass

from snake_core import (
    BOARD_CELLS,
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
    "free_space_after_move",
    "tail_reachable_after_move",
)

SAMPLE_WEIGHT_PRESETS = {
    "balanced_v1": [1.3, -3.2, -3.4, 0.15, 1.0, 1.2],
    "aggressive_v1": [2.0, -2.5, -2.8, -0.2, 0.5, 0.7],
    "safe_v1": [0.9, -3.8, -4.2, 0.25, 1.8, 2.0],
}


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


def simulate_move(snake_positions, direction):
    """후보 방향으로 한 칸 이동한 뱀 좌표를 계산합니다."""
    next_positions = copy_positions(snake_positions)
    move_snake(next_positions, direction)
    return next_positions


def is_blocked(position, blocked_positions):
    """좌표가 벽이나 장애물에 막혔는지 확인합니다."""
    return is_wall_collision(position) or tuple(position) in blocked_positions


def reachable_position_keys(start_position, blocked_positions):
    """BFS로 도달 가능한 좌표 키를 계산합니다."""
    if is_blocked(start_position, blocked_positions):
        return set()

    queue = deque([start_position])
    visited = {tuple(start_position)}

    while queue:
        current = queue.popleft()
        for next_direction in DIRECTION_ORDER:
            next_cell = next_position(current, next_direction)
            next_key = tuple(next_cell)
            if next_key in visited:
                continue
            if is_blocked(next_cell, blocked_positions):
                continue
            visited.add(next_key)
            queue.append(next_cell)

    return visited


def free_space_after_move(next_positions):
    """이동 후 새 머리에서 도달 가능한 빈 칸 비율을 계산합니다."""
    blocked_positions = {tuple(position) for position in next_positions[1:]}
    reachable_count = len(
        reachable_position_keys(next_positions[0], blocked_positions)
    )
    return reachable_count / BOARD_CELLS


def tail_reachable_after_move(next_positions):
    """이동 후 새 머리에서 꼬리까지 연결되는지 확인합니다."""
    tail_key = tuple(next_positions[-1])
    blocked_positions = {tuple(position) for position in next_positions[1:-1]}
    return 1 if tail_key in reachable_position_keys(
        next_positions[0],
        blocked_positions,
    ) else 0


def reachable_after_move(next_positions):
    """이동 후 새 머리에서 도달 가능한 좌표를 한 번만 계산합니다."""
    blocked_positions = {tuple(position) for position in next_positions[1:-1]}
    return reachable_position_keys(next_positions[0], blocked_positions)


def direction_features(snake_positions, current_direction, food_position, direction):
    """방향 하나를 평가하기 위한 특징값을 만듭니다."""
    head = snake_positions[0]
    next_head = next_position(head, direction)
    before_distance = distance_to_food(head, food_position)
    after_distance = distance_to_food(next_head, food_position)
    next_positions = simulate_move(snake_positions, direction)

    return [
        (before_distance - after_distance) / CELL_SIZE,
        1 if is_wall_collision(next_head) else 0,
        1 if next_head in snake_positions[1:] else 0,
        1 if direction == current_direction else 0,
        free_space_after_move(next_positions),
        tail_reachable_after_move(next_positions),
    ]


def direction_features_from_move(
    snake_positions,
    current_direction,
    food_position,
    direction,
    next_positions,
    reachable_keys,
):
    """이미 계산한 이동 결과와 BFS 결과로 feature를 만듭니다."""
    head = snake_positions[0]
    next_head = next_positions[0]
    before_distance = distance_to_food(head, food_position)
    after_distance = distance_to_food(next_head, food_position)

    return [
        (before_distance - after_distance) / CELL_SIZE,
        1 if is_wall_collision(next_head) else 0,
        1 if next_head in snake_positions[1:] else 0,
        1 if direction == current_direction else 0,
        len(reachable_keys) / BOARD_CELLS,
        1 if tuple(next_positions[-1]) in reachable_keys else 0,
    ]


def weighted_score(weights, features):
    """개체의 가중치와 특징값으로 방향 점수를 계산합니다."""
    score = 0.0
    for index, feature in enumerate(features):
        weight = weights[index] if index < len(weights) else 0.0
        score += weight * feature
    return score


def ensure_weight_size(weights):
    """가중치 길이를 feature 개수와 맞춰서 보정합니다."""
    target_length = len(FEATURE_NAMES)
    normalized = list(weights[:target_length])
    if len(normalized) < target_length:
        normalized.extend([0.0] * (target_length - len(normalized)))
    return normalized


def sample_individual(preset_name="balanced_v1"):
    """샘플 preset 이름으로 개체를 하나 만듭니다."""
    preset = SAMPLE_WEIGHT_PRESETS.get(preset_name, SAMPLE_WEIGHT_PRESETS["balanced_v1"])
    return Individual(weights=ensure_weight_size(preset))


def choose_direction(individual, snake_positions, current_direction, food_position):
    """개체의 가중치를 기준으로 다음 이동 방향을 선택합니다."""
    normalized_weights = ensure_weight_size(individual.weights)
    candidates = []
    for direction in DIRECTION_ORDER:
        if not can_change_direction(current_direction, direction):
            continue

        next_positions = simulate_move(snake_positions, direction)
        if is_wall_collision(next_positions[0]) or is_self_collision(next_positions):
            continue

        reachable_keys = reachable_after_move(next_positions)
        features = direction_features_from_move(
            snake_positions,
            current_direction,
            food_position,
            direction,
            next_positions,
            reachable_keys,
        )
        candidates.append((weighted_score(normalized_weights, features), direction))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]

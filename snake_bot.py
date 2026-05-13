"""경로 탐색 봇의 방향 선택 로직을 정의합니다."""

from collections import deque

from snake_core import (
    BOARD_CELLS,
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


def copy_positions(positions):
    """경로 탐색 중 원본 뱀 좌표를 바꾸지 않기 위해 좌표 목록을 복사합니다."""
    return [position.copy() for position in positions]


def position_key(position):
    """좌표를 dict/set에서 비교하기 쉬운 tuple 형태로 바꿉니다."""
    return tuple(position)


def build_body_release_times(positions):
    """현재 몸의 각 칸이 몇 번째 이동 후 비는지 계산합니다."""
    snake_length = len(positions)
    release_times = {}
    for index, position in enumerate(positions):
        release_times[position_key(position)] = snake_length - index
    return release_times


def reconstruct_path(parents, node_key):
    """parent link를 따라가며 BFS가 찾은 방향 목록을 복원합니다."""
    path = []
    while parents[node_key] is not None:
        path.append(node_key[2])
        node_key = parents[node_key]
    path.reverse()
    return path


def is_recent_path_collision(node_key, next_cell, parents, max_recent_steps):
    """방금 지나온 머리 경로 중 아직 몸으로 남아 있는 칸인지 확인합니다."""
    checked_steps = 0
    while node_key is not None and checked_steps < max_recent_steps:
        if node_key[0] == next_cell:
            return True
        node_key = parents[node_key]
        checked_steps += 1
    return False


def find_path(start_positions, start_direction, goal):
    """몸 전체를 큐에 저장하지 않고 시간 기반 BFS로 goal까지 경로를 찾습니다."""
    start_cell = position_key(start_positions[0])
    goal_cell = position_key(goal)
    start_key = (start_cell, 0, start_direction)
    body_release_times = build_body_release_times(start_positions)
    queue = deque([start_key])
    parents = {start_key: None}
    visited = {start_key}
    max_recent_steps = len(start_positions) - 1

    while queue:
        current_key = queue.popleft()
        current_cell, depth, current_direction = current_key
        if current_cell == goal_cell:
            return reconstruct_path(parents, current_key)

        if depth >= BOARD_CELLS:
            continue

        for direction in DIRECTION_ORDER:
            if not can_change_direction(current_direction, direction):
                continue

            next_cell = position_key(next_position(list(current_cell), direction))
            next_depth = depth + 1
            if is_wall_collision(list(next_cell)):
                continue
            if body_release_times.get(next_cell, 0) > next_depth:
                continue
            if is_recent_path_collision(
                current_key,
                next_cell,
                parents,
                max_recent_steps,
            ):
                continue

            next_key = (next_cell, next_depth, direction)
            if next_key in visited:
                continue

            visited.add(next_key)
            parents[next_key] = current_key
            queue.append(next_key)

    return []


def find_path_to_food(snake, apple):
    """꼬리 이동을 반영하면서 먹이까지 가는 최단 경로를 BFS로 찾습니다."""
    return find_path(snake.positions, snake.direction, apple.position)


def simulate_path(positions, path):
    """path를 따라 이동했을 때의 뱀 좌표를 계산합니다."""
    next_positions = copy_positions(positions)
    for direction in path:
        move_snake(next_positions, direction)
    return next_positions


def has_escape_after_food(snake, path_to_food):
    """먹이를 먹은 뒤에도 꼬리 쪽으로 빠져나갈 경로가 있는지 확인합니다."""
    if not path_to_food:
        return False

    positions_after_food = simulate_path(snake.positions, path_to_food)
    positions_after_food.append(positions_after_food[-1].copy())
    direction_after_food = path_to_food[-1]
    tail_position = positions_after_food[-1]

    return bool(
        find_path(
            positions_after_food,
            direction_after_food,
            tail_position,
        )
    )


def choose_tail_direction(snake):
    """먹이 경로가 위험할 때 꼬리 쪽으로 이동해 생존 공간을 확보합니다."""
    path = find_path(snake.positions, snake.direction, snake.positions[-1])
    if path:
        return path[0]
    return None


def choose_bfs_direction(snake, apple):
    """먹이 경로가 안전하면 따라가고, 위험하면 꼬리 쪽으로 이동합니다."""
    path = find_path_to_food(snake, apple)
    if path and has_escape_after_food(snake, path):
        return path[0]

    tail_direction = choose_tail_direction(snake)
    if tail_direction:
        return tail_direction

    return choose_greedy_direction(snake, apple)


def run_bot():
    """공통 게임 실행 흐름에 BFS 방향 선택 함수를 연결합니다."""
    run_game(
        choose_direction=choose_bfs_direction,
        title="snake bot",
        move_interval=0.1,
    )


if __name__ == "__main__":
    run_bot()

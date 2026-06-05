"""Safe food shortcut search for the stable snake bot."""

from collections import deque

from snake_core import (
    CELL_SIZE,
    DIRECTION_ORDER,
    can_change_direction,
    is_self_collision,
    is_wall_collision,
    move_snake,
    next_position,
)
from stable_bot.safety import (
    blocked_keys,
    can_reach_tail,
    copy_positions,
    position_key,
    reachable_positions,
)


MAX_SHORTCUT_DISTANCE = 4


def manhattan_cells(start, end):
    """Return Manhattan distance measured in grid cells."""
    return (abs(start[0] - end[0]) + abs(start[1] - end[1])) // CELL_SIZE


def reconstruct_path(parents, node_key):
    """Restore a direction path from BFS parent links."""
    path = []
    while parents[node_key] is not None:
        previous_key, direction = parents[node_key]
        path.append(direction)
        node_key = previous_key
    path.reverse()
    return path


def find_shortest_path_to_food(snake, apple):
    """Find a short static path to the apple.

    This intentionally stays conservative: it avoids the current body and only
    treats the current tail as passable.
    """
    start_key = position_key(snake.head)
    goal_key = position_key(apple.position)
    blocked = blocked_keys(snake.positions, allow_tail=True)

    queue = deque([(start_key, snake.direction)])
    parents = {(start_key, snake.direction): None}
    visited = {(start_key, snake.direction)}

    while queue:
        current_key, current_direction = queue.popleft()
        if current_key == goal_key:
            return reconstruct_path(parents, (current_key, current_direction))

        current = list(current_key)
        for direction in DIRECTION_ORDER:
            if not can_change_direction(current_direction, direction):
                continue

            next_head = next_position(current, direction)
            next_key = position_key(next_head)
            next_node = (next_key, direction)

            if next_node in visited:
                continue
            if next_key in blocked or is_wall_collision(next_head):
                continue

            visited.add(next_node)
            parents[next_node] = ((current_key, current_direction), direction)
            queue.append(next_node)

    return []


def simulate_path_to_food(positions, path):
    """Simulate following a path and growing on the final step."""
    next_positions = copy_positions(positions)

    for index, direction in enumerate(path):
        move_snake(next_positions, direction)
        if is_wall_collision(next_positions[0]) or is_self_collision(next_positions):
            return None
        if index == len(path) - 1:
            next_positions.append(next_positions[-1].copy())

    return next_positions


def has_enough_space_after_food(positions_after_food):
    """Check whether the post-food head has enough reachable room."""
    reachable = reachable_positions(
        positions_after_food[0],
        blocked_keys(positions_after_food, allow_tail=True),
    )
    return len(reachable) >= len(positions_after_food)


def is_safe_shortcut(snake, path):
    """Check whether a full path to food is safe after the food is eaten."""
    if not path:
        return False

    positions_after_food = simulate_path_to_food(snake.positions, path)
    if positions_after_food is None:
        return False

    return (
        can_reach_tail(positions_after_food)
        and has_enough_space_after_food(positions_after_food)
    )


def find_safe_shortcut_path(snake, apple, max_distance=MAX_SHORTCUT_DISTANCE):
    """Return a safe full path to food, or an empty list."""
    if manhattan_cells(snake.head, apple.position) > max_distance:
        return []

    path = find_shortest_path_to_food(snake, apple)
    if is_safe_shortcut(snake, path):
        return path
    return []


def choose_shortcut_direction(snake, apple, max_distance=MAX_SHORTCUT_DISTANCE):
    """Return the first direction of a safe food shortcut, or None."""
    path = find_safe_shortcut_path(snake, apple, max_distance=max_distance)
    if path:
        return path[0]
    return None

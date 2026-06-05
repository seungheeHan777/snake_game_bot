"""Safety checks for the stable snake bot."""

from collections import deque

from snake_core import (
    DIRECTION_ORDER,
    all_board_positions,
    can_change_direction,
    is_self_collision,
    is_wall_collision,
    move_snake,
    next_position,
)


def copy_positions(positions):
    """Return a deep copy of snake position lists."""
    return [position.copy() for position in positions]


def position_key(position):
    """Convert a mutable position list to a hashable key."""
    return tuple(position)


def simulate_move(positions, direction, grow=False):
    """Return snake positions after one move without changing the original."""
    next_positions = copy_positions(positions)
    move_snake(next_positions, direction)
    if grow:
        next_positions.append(next_positions[-1].copy())
    return next_positions


def is_immediately_safe(snake, direction):
    """Check whether one move avoids wall, body, and reverse-direction collision."""
    if not direction:
        return False
    if not can_change_direction(snake.direction, direction):
        return False

    next_positions = simulate_move(snake.positions, direction)
    return (
        not is_wall_collision(next_positions[0])
        and not is_self_collision(next_positions)
    )


def blocked_keys(positions, allow_tail=True):
    """Return occupied cells for path search.

    When `allow_tail` is true, the current tail is treated as passable because
    it normally moves away on the next step. The head is also excluded because
    it is the search start position.
    """
    body = positions[1:-1] if allow_tail else positions[1:]
    return {position_key(position) for position in body}


def reachable_positions(start, blocked):
    """Return all board positions reachable from `start` without crossing blocked."""
    start_key = position_key(start)
    if start_key in blocked or is_wall_collision(start):
        return set()

    visited = {start_key}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for direction in DIRECTION_ORDER:
            neighbor = next_position(current, direction)
            neighbor_key = position_key(neighbor)
            if neighbor_key in visited:
                continue
            if neighbor_key in blocked or is_wall_collision(neighbor):
                continue
            visited.add(neighbor_key)
            queue.append(neighbor)

    return visited


def can_reach_tail(positions):
    """Check whether the current head can reach the current tail."""
    head = positions[0]
    tail_key = position_key(positions[-1])
    reachable = reachable_positions(head, blocked_keys(positions, allow_tail=True))
    return tail_key in reachable


def can_reach_tail_after_move(snake, direction, grow=False):
    """Check tail reachability after applying one candidate move."""
    if not is_immediately_safe(snake, direction):
        return False
    next_positions = simulate_move(snake.positions, direction, grow=grow)
    return can_reach_tail(next_positions)


def open_space_after_move(snake, direction, grow=False):
    """Return the number of open cells reachable after one candidate move."""
    if not is_immediately_safe(snake, direction):
        return 0
    next_positions = simulate_move(snake.positions, direction, grow=grow)
    reachable = reachable_positions(
        next_positions[0],
        blocked_keys(next_positions, allow_tail=True),
    )
    return len(reachable)


def has_enough_open_space_after_move(snake, direction, grow=False):
    """Check whether the move leaves at least snake-length reachable space."""
    open_space = open_space_after_move(snake, direction, grow=grow)
    next_length = len(snake.positions) + (1 if grow else 0)
    return open_space >= next_length


def is_safe_candidate(snake, direction, grow=False):
    """Check the common safety conditions for future shortcut decisions."""
    return (
        is_immediately_safe(snake, direction)
        and can_reach_tail_after_move(snake, direction, grow=grow)
        and has_enough_open_space_after_move(snake, direction, grow=grow)
    )


def empty_cell_count(positions):
    """Return how many board cells are not occupied by the snake."""
    occupied = {position_key(position) for position in positions}
    return sum(
        1 for position in all_board_positions()
        if position_key(position) not in occupied
    )

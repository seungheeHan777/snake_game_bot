"""Hamiltonian fallback route for the stable snake bot."""

from snake_core import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_SIZE,
    DIRECTION_DELTAS,
)
from stable_bot.safety import is_immediately_safe


def board_shape():
    """Return the board size as cell counts."""
    return BOARD_WIDTH // CELL_SIZE, BOARD_HEIGHT // CELL_SIZE


def to_pixel(cell):
    """Convert a grid cell `(x, y)` to the pixel coordinate used by the game."""
    return [cell[0] * CELL_SIZE, cell[1] * CELL_SIZE]


def to_cell(position):
    """Convert a pixel coordinate to a grid cell `(x, y)`."""
    return position[0] // CELL_SIZE, position[1] // CELL_SIZE


def build_cycle_cells(width_cells=None, height_cells=None):
    """Build a Hamiltonian cycle for an even-width rectangular board.

    The route crosses the top row, snakes through rows below while leaving the
    first column open, then returns up the first column. It ends at `(0, 1)`,
    which is adjacent to the start `(0, 0)`.
    """
    default_width, default_height = board_shape()
    width_cells = width_cells or default_width
    height_cells = height_cells or default_height
    if width_cells % 2 != 0:
        raise ValueError("Hamiltonian cycle requires an even board width.")
    if width_cells < 2 or height_cells < 2:
        raise ValueError("Board is too small for this Hamiltonian cycle.")

    cells = [(x, 0) for x in range(width_cells)]

    for y in range(1, height_cells):
        if y % 2 == 1:
            cells.extend((x, y) for x in range(width_cells - 1, 0, -1))
        else:
            cells.extend((x, y) for x in range(1, width_cells))

    cells.extend((0, y) for y in range(height_cells - 1, 0, -1))

    return cells


def build_cycle_positions(width_cells=None, height_cells=None):
    """Build the Hamiltonian cycle using the game's pixel coordinates."""
    return [to_pixel(cell) for cell in build_cycle_cells(width_cells, height_cells)]


def build_index(cycle_positions=None):
    """Map each route position to its index in the cycle."""
    cycle_positions = cycle_positions or build_cycle_positions()
    return {tuple(position): index for index, position in enumerate(cycle_positions)}


CYCLE_POSITIONS = build_cycle_positions()
CYCLE_INDEX = build_index(CYCLE_POSITIONS)


def next_cycle_position(position, reverse=True):
    """Return the next position on the fallback cycle.

    `reverse=True` matches the current initial snake layout, so the first move
    does not run into the body.
    """
    index = CYCLE_INDEX[tuple(position)]
    step = -1 if reverse else 1
    return CYCLE_POSITIONS[(index + step) % len(CYCLE_POSITIONS)]


def direction_between(start, end):
    """Return the direction needed to move from `start` to adjacent `end`."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    for direction, delta in DIRECTION_DELTAS.items():
        if delta == (dx, dy):
            return direction
    return None


def choose_cycle_direction(snake, reverse=True):
    """Choose the next direction on the fallback cycle."""
    preferred_position = next_cycle_position(snake.head, reverse=reverse)
    preferred_direction = direction_between(snake.head, preferred_position)
    if is_immediately_safe(snake, preferred_direction):
        return preferred_direction

    alternate_position = next_cycle_position(snake.head, reverse=not reverse)
    alternate_direction = direction_between(snake.head, alternate_position)
    if is_immediately_safe(snake, alternate_direction):
        return alternate_direction

    return None


def validate_cycle(cycle_positions=None):
    """Return True when the cycle covers the board and every edge is adjacent."""
    cycle_positions = cycle_positions or CYCLE_POSITIONS
    if len(cycle_positions) != len(set(map(tuple, cycle_positions))):
        return False
    expected_cells = (BOARD_WIDTH // CELL_SIZE) * (BOARD_HEIGHT // CELL_SIZE)
    if len(cycle_positions) != expected_cells:
        return False

    for index, position in enumerate(cycle_positions):
        next_position = cycle_positions[(index + 1) % len(cycle_positions)]
        if direction_between(position, next_position) is None:
            return False

    return True

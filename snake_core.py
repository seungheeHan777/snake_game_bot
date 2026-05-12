"""스네이크 게임에서 함께 쓰는 상수와 순수 함수 모음."""

from random import choice

BOARD_WIDTH = 400
BOARD_HEIGHT = 400
CELL_SIZE = 20
BOARD_CELLS = (BOARD_WIDTH // CELL_SIZE) * (BOARD_HEIGHT // CELL_SIZE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

INITIAL_SNAKE_POSITIONS = [[200, 20], [180, 20], [160, 20], [140, 20]]
INITIAL_APPLE_POSITION = [120, 120]

# 방향은 기존 코드 흐름을 유지하기 위해 U, L, R, D 순서로 둡니다.
DIRECTION_ORDER = ("U", "L", "R", "D")

# 각 방향으로 한 칸 이동할 때 변하는 x, y 값입니다.
DIRECTION_DELTAS = {
    "U": (0, -CELL_SIZE),
    "L": (-CELL_SIZE, 0),
    "R": (CELL_SIZE, 0),
    "D": (0, CELL_SIZE),
}

# 바로 반대 방향으로 꺾으면 머리가 몸통과 겹칠 수 있어서 막습니다.
OPPOSITE_DIRECTIONS = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
}


def next_position(position, direction):
    """현재 좌표에서 direction 방향으로 한 칸 이동한 새 좌표를 반환합니다."""
    dx, dy = DIRECTION_DELTAS[direction]
    return [position[0] + dx, position[1] + dy]


def can_change_direction(current_direction, new_direction):
    """현재 방향 기준으로 new_direction으로 이동할 수 있는지 확인합니다."""
    if new_direction not in DIRECTION_DELTAS:
        return False
    if current_direction == "" and new_direction == "L":
        return False
    return current_direction != OPPOSITE_DIRECTIONS[new_direction]


def move_snake(snake_positions, direction):
    """뱀의 몸통을 머리 쪽으로 당긴 뒤, 머리를 direction 방향으로 이동합니다."""
    for i in range(len(snake_positions), 1, -1):
        snake_positions[i - 1][0] = snake_positions[i - 2][0]
        snake_positions[i - 1][1] = snake_positions[i - 2][1]
    snake_positions[0] = next_position(snake_positions[0], direction)


def is_wall_collision(position):
    """좌표가 보드 밖으로 나갔는지 확인합니다."""
    return (
        position[0] < 0
        or position[1] < 0
        or position[0] > BOARD_WIDTH - CELL_SIZE
        or position[1] > BOARD_HEIGHT - CELL_SIZE
    )


def is_self_collision(snake_positions):
    """뱀 머리가 자기 몸통과 겹쳤는지 확인합니다."""
    return snake_positions[0] in snake_positions[1:]


def all_board_positions():
    """보드 위에 존재할 수 있는 모든 격자 좌표를 반환합니다."""
    positions = []
    for x in range(0, BOARD_WIDTH, CELL_SIZE):
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            positions.append([x, y])
    return positions


def generate_food(snake_positions):
    """뱀 몸과 겹치지 않는 먹이 좌표를 새로 만듭니다."""
    empty_positions = [
        position for position in all_board_positions()
        if position not in snake_positions
    ]
    if not empty_positions:
        return None
    return choice(empty_positions)

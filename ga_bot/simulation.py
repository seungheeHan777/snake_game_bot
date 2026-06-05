"""유전 알고리즘 학습용 화면 없는 스네이크 시뮬레이션입니다."""

from collections import deque

from snake_core import (
    BOARD_CELLS,
    INITIAL_SNAKE_POSITIONS,
    generate_food,
    is_self_collision,
    is_wall_collision,
    move_snake,
)

from ga_bot.policy import choose_direction, copy_positions

# Give the snake extra room to untangle before starvation cutoff.
MAX_STEPS_WITHOUT_FOOD = BOARD_CELLS * 10
LOOP_WINDOW = BOARD_CELLS
LOOP_PENALTY_SCALE = 0.6
STEP_REWARD_WEIGHT = 0.25


def loop_penalty(recent_heads, steps):
    """최근 머리 좌표 반복 비율 기반 감점값을 계산합니다."""
    if not recent_heads or steps <= 0:
        return 0
    unique_cells = len(set(recent_heads))
    repeat_ratio = 1.0 - (unique_cells / len(recent_heads))
    return int(repeat_ratio * LOOP_PENALTY_SCALE * steps)


def simulate_game(individual):
    """화면 없이 한 판을 실행하고 개체의 fitness를 계산합니다."""
    snake_positions = copy_positions(INITIAL_SNAKE_POSITIONS)
    current_direction = ""
    food_position = generate_food(snake_positions)
    # GA 점수는 먹이 개수가 아니라 현재 뱀 길이(최대 400)로 사용합니다.
    score = len(snake_positions)
    steps = 0
    steps_without_food = 0
    recent_heads = deque(maxlen=LOOP_WINDOW)
    recent_heads.append(tuple(snake_positions[0]))

    while (
        score < BOARD_CELLS
        and food_position is not None
        and steps_without_food < MAX_STEPS_WITHOUT_FOOD
    ):
        direction = choose_direction(
            individual,
            snake_positions,
            current_direction,
            food_position,
        )
        if direction is None:
            break

        move_snake(snake_positions, direction)
        current_direction = direction
        steps += 1
        steps_without_food += 1
        recent_heads.append(tuple(snake_positions[0]))

        if is_wall_collision(snake_positions[0]) or is_self_collision(snake_positions):
            break

        if snake_positions[0] == food_position:
            if score < BOARD_CELLS:
                snake_positions.append(snake_positions[-1].copy())
            score = min(len(snake_positions), BOARD_CELLS)
            food_position = generate_food(snake_positions)
            steps_without_food = 0

    individual.score = score
    individual.steps = steps
    step_reward = int(steps * STEP_REWARD_WEIGHT)
    individual.fitness = score * 1000 + step_reward - loop_penalty(recent_heads, steps)
    return individual.fitness

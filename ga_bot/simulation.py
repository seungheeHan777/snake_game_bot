"""유전 알고리즘 학습용 화면 없는 스네이크 시뮬레이션입니다."""

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


def simulate_game(individual):
    """화면 없이 한 판을 실행하고 개체의 fitness를 계산합니다."""
    snake_positions = copy_positions(INITIAL_SNAKE_POSITIONS)
    current_direction = ""
    food_position = generate_food(snake_positions)
    score = 0
    steps = 0
    steps_without_food = 0

    while food_position is not None and steps_without_food < MAX_STEPS_WITHOUT_FOOD:
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

        if is_wall_collision(snake_positions[0]) or is_self_collision(snake_positions):
            break

        if snake_positions[0] == food_position:
            score += 1
            snake_positions.append(snake_positions[-1].copy())
            food_position = generate_food(snake_positions)
            steps_without_food = 0

    individual.score = score
    individual.steps = steps
    individual.fitness = score * 1000 + steps
    return individual.fitness

"""스네이크 게임 실행 흐름을 담당합니다."""

from datetime import datetime, timedelta

import pygame

from apple import Apple
from rule import Rule
from snake import Snake
from snake_core import BOARD_HEIGHT, BOARD_WIDTH, WHITE


def run_game(choose_direction=None, title="snake game", move_interval=0.1):
    """pygame을 초기화하고 게임 루프를 실행합니다.

    choose_direction이 없으면 키보드 입력으로 수동 플레이를 합니다.
    choose_direction이 있으면 그 함수가 다음 이동 방향을 결정합니다.
    """
    pygame.init()
    screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
    pygame.display.set_caption(title)
    font = pygame.font.SysFont(None, 50)
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    rule = Rule()
    running = True
    last_bot_move = datetime.now()

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif choose_direction is None:
                snake.handle_event(event)

        if choose_direction is None:
            snake.auto_move(move_interval)
        elif timedelta(seconds=move_interval) <= datetime.now() - last_bot_move:
            direction = choose_direction(snake, apple)
            if direction is None:
                running = rule.show_game_over(screen, font, snake.score)
            else:
                snake.move(direction)
                last_bot_move = datetime.now()

        snake.draw(screen)
        apple.draw(screen)

        if snake.head == apple.position:
            snake.grow()
            apple.relocate(snake.positions)

        if rule.is_victory(snake):
            running = rule.show_victory(screen, font)
        elif rule.is_game_over(snake):
            running = rule.show_game_over(screen, font, snake.score)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_game()

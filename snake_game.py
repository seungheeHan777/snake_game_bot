"""수동 플레이용 스네이크 게임 실행 파일."""

import pygame

from apple import Apple
from rule import Rule
from snake import Snake
from snake_core import BOARD_HEIGHT, BOARD_WIDTH, WHITE


def run_game():
    """pygame을 초기화하고 수동 플레이 게임 루프를 실행합니다."""
    pygame.init()
    screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
    pygame.display.set_caption("snake game")
    font = pygame.font.SysFont(None, 50)
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    rule = Rule()
    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                snake.handle_event(event)

        snake.auto_move()
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

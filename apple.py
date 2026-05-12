"""먹이 객체를 정의합니다."""

import pygame

from snake_core import CELL_SIZE, INITIAL_APPLE_POSITION, RED, generate_food


class Apple:
    """먹이 위치 관리와 그리기를 담당합니다."""

    def __init__(self, position=None):
        self.position = (position or INITIAL_APPLE_POSITION).copy()

    def draw(self, screen):
        """현재 먹이 위치를 화면에 그립니다."""
        if self.position is None:
            return
        pygame.draw.rect(
            screen,
            RED,
            [self.position[0], self.position[1], CELL_SIZE, CELL_SIZE],
            0,
        )

    def relocate(self, snake_positions):
        """뱀 몸과 겹치지 않는 새 위치로 먹이를 옮깁니다."""
        self.position = generate_food(snake_positions)

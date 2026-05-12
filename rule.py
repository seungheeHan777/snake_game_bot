"""게임 규칙과 종료 화면을 정의합니다."""

import time

import pygame

from snake_core import (
    BLACK,
    BOARD_CELLS,
    GREEN,
    RED,
    is_self_collision,
    is_wall_collision,
)


class Rule:
    """게임 오버, 승리 조건, 종료 화면 표시를 담당합니다."""

    def is_game_over(self, snake):
        """벽 충돌이나 자기 몸 충돌이 발생했는지 확인합니다."""
        return is_wall_collision(snake.head) or is_self_collision(snake.positions)

    def is_victory(self, snake):
        """뱀이 보드를 모두 채웠는지 확인합니다."""
        return snake.score >= BOARD_CELLS

    def show_game_over(self, screen, font, score):
        """게임 오버 화면을 사용자가 창을 닫을 때까지 표시합니다."""
        return self._show_end_screen(
            screen,
            font,
            background_color=RED,
            title="GAME OVER",
            score=score,
        )

    def show_victory(self, screen, font):
        """승리 화면을 사용자가 창을 닫을 때까지 표시합니다."""
        return self._show_end_screen(
            screen,
            font,
            background_color=GREEN,
            title="WIN",
        )

    def _show_end_screen(self, screen, font, background_color, title, score=None):
        """종료 상태 화면을 그리고 창 닫기 이벤트를 기다립니다."""
        waiting = True
        while waiting:
            time.sleep(0.5)
            screen.fill(background_color)

            title_text = font.render(title, True, BLACK)
            screen.blit(title_text, (90, 100))

            if score is not None:
                score_text = font.render("SCORE : " + str(score), True, BLACK)
                screen.blit(score_text, (90, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False

            pygame.display.update()

        return False

"""스네이크 객체를 정의합니다."""

from datetime import datetime, timedelta

import pygame

from snake_core import (
    BLACK,
    CELL_SIZE,
    DIRECTION_ORDER,
    INITIAL_SNAKE_POSITIONS,
    can_change_direction,
    move_snake,
)


class Snake:
    """뱀의 위치, 이동, 성장, 그리기를 담당합니다."""

    def __init__(self, positions=None):
        # 기본 시작 위치를 복사해서 원본 상수가 바뀌지 않게 합니다.
        self.positions = [
            position.copy()
            for position in (positions or INITIAL_SNAKE_POSITIONS)
        ]
        self.direction = ""
        self.last_moved = datetime.now()

    @property
    def head(self):
        """뱀 머리 좌표를 반환합니다."""
        return self.positions[0]

    @property
    def score(self):
        """현재 점수로 사용할 뱀 길이를 반환합니다."""
        return len(self.positions)

    def draw(self, screen):
        """뱀의 모든 몸통 칸을 화면에 그립니다."""
        for position in self.positions:
            pygame.draw.rect(
                screen,
                BLACK,
                [position[0], position[1], CELL_SIZE, CELL_SIZE],
                0,
            )

    def move(self, direction=None):
        """방향이 유효하면 뱀을 한 칸 이동합니다."""
        next_direction = direction or self.direction
        if not next_direction:
            return False
        if direction and not can_change_direction(self.direction, direction):
            return False
        move_snake(self.positions, next_direction)
        self.direction = next_direction
        self.last_moved = datetime.now()
        return True

    def handle_event(self, event):
        """키보드 이벤트를 방향 입력으로 변환합니다."""
        if event.type != pygame.KEYDOWN:
            return False

        key_directions = {
            pygame.K_UP: DIRECTION_ORDER[0],
            pygame.K_DOWN: DIRECTION_ORDER[3],
            pygame.K_LEFT: DIRECTION_ORDER[1],
            pygame.K_RIGHT: DIRECTION_ORDER[2],
        }
        if event.key in key_directions:
            return self.move(key_directions[event.key])
        return False

    def auto_move(self, interval_seconds=0.1):
        """마지막 이동 이후 일정 시간이 지나면 같은 방향으로 계속 이동합니다."""
        if timedelta(seconds=interval_seconds) <= datetime.now() - self.last_moved:
            return self.move()
        return False

    def grow(self):
        """먹이를 먹었을 때 꼬리 위치를 하나 더 추가합니다."""
        self.positions.append(self.positions[-1].copy())

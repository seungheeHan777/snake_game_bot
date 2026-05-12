# Project Plan

## 목표

수동 스네이크 게임을 먼저 명확한 파일 구조로 정리하고, 같은 규칙 위에서 두 종류의 봇을 만듭니다.

## 목표 구조

```text
snake_game.py   # 수동 플레이 실행 흐름
snake.py        # Snake 클래스
apple.py        # Apple 클래스
rule.py         # Rule 클래스
snake_core.py   # 공통 상수와 순수 helper 함수
snake_bot.py    # 경로 탐색 봇
snake_ga_bot.py # 유전 알고리즘 봇
```

## 책임 분리

- `snake_game.py`: pygame 초기화, 객체 생성, 이벤트 루프, 화면 업데이트
- `snake.py`: 뱀의 위치, 이동, 성장, 그리기
- `apple.py`: 먹이의 위치, 재생성, 그리기
- `rule.py`: 게임 오버 조건, 승리 조건, 종료 화면
- `snake_core.py`: 보드 크기, 방향, 좌표 이동, 충돌 검사, 먹이 생성

## 봇 계획

1. `snake_bot.py`: BFS 기반 경로 탐색 봇
   - 현재 몸을 장애물로 보기
   - 꼬리 이동 반영
   - 먹은 뒤 갇히지 않는 장기 생존 전략

2. `snake_ga_bot.py`: 유전 알고리즘 기반 봇
   - 개체 표현 방식
   - 점수 함수
   - 선택, 교차, 변이
   - 학습 결과 저장 방식

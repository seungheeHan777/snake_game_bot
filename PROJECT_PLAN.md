# Project Plan

## Goal

pygame으로 만든 스네이크 게임을 정리하고, 같은 게임 규칙 위에서 두 종류의 자동 플레이 봇을 만듭니다.

## Target Structure

```text
snake_core.py   # 공통 게임 규칙
snake_game.py   # 사람이 플레이하는 실행 파일
snake_bot.py    # 경로 탐색 봇
snake_ga_bot.py # 유전 알고리즘 봇
```

## First Priority

가장 먼저 `snake_game.py`를 개선합니다.

`snake_core.py`로 먼저 분리할 항목:

- 방향 상수
- 좌표 이동 함수
- 뱀 이동 함수
- 벽 충돌 검사
- 자기 몸 충돌 검사
- 먹이 생성 함수

## Pathfinding Bot

`snake_bot.py`는 경로 탐색 봇으로 만듭니다.

단계:

1. 기본 BFS: 현재 몸을 장애물로 보고 먹이까지 최단 경로를 찾습니다.
2. 꼬리 이동 반영: 이동 시 꼬리가 빠지는 상황을 고려합니다.
3. 장기 생존 전략: 먹이를 먹은 뒤 갇히지 않는지 확인합니다.

## Genetic Algorithm Bot

유전 알고리즘 봇은 새 파일 `snake_ga_bot.py`에 만듭니다.

이 단계는 경로 탐색 봇과 공통 게임 로직이 안정된 뒤 진행합니다.

## Working Style

작게 단계별로 진행합니다.

- 큰 구조 변경 전에는 먼저 질문합니다.
- 실행되는 상태를 최대한 유지합니다.
- 방향이 바뀌면 `AGENTS.md`, `TODO.md`, `NOTES.md`를 갱신합니다.


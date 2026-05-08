# AGENTS.md

## 프로젝트 개요

이 프로젝트는 Python과 pygame으로 만든 스네이크 게임 프로젝트입니다.

처음 프로젝트는 아래 두 파일에서 시작했습니다.

- `snake_game.py`: 키보드 입력으로 직접 플레이하는 스네이크 게임
- `snake_bot.py`: 게임을 자동으로 플레이하도록 실험하던 봇 버전

목표는 먼저 수동 게임 코드를 정리한 뒤, 같은 게임 로직 위에서 두 종류의 봇을 만드는 것입니다.

## 주요 목표

1. 기존 수동 스네이크 게임을 리팩터링합니다.
2. 재사용 가능한 게임 규칙을 `snake_core.py`로 분리합니다.
3. `snake_bot.py`에는 경로 탐색 기반 봇을 만듭니다.
4. `snake_ga_bot.py`에는 유전 알고리즘 기반 봇을 만듭니다.

## 작업 규칙

- 큰 설계 변경을 하기 전에는 먼저 사용자에게 질문합니다.
- 변경은 작게, 단계적으로 진행합니다.
- 리팩터링 중에도 `snake_game.py`의 기존 동작을 최대한 유지합니다.
- 지나치게 영리한 추상화보다, 읽기 쉽고 학습하기 좋은 코드를 선호합니다.
- 사용자가 명시적으로 승인하지 않는 한 대규모 재작성은 피합니다.
- 프로젝트 방향이나 작업 상태가 바뀌면 `TODO.md`와 `NOTES.md`를 갱신합니다.
- 코드의 파일명, 함수명, 변수명은 영어를 사용합니다.
- 사용자의 이해를 돕는 주석은 한국어로 작성해도 됩니다.

## 목표 구조

최종적으로는 아래 구조를 목표로 합니다.

```text
snake_core.py   # 공통 게임 상태, 이동, 충돌, 먹이, 규칙
snake_game.py   # 사람이 플레이하는 pygame 실행 파일
snake_bot.py    # 경로 탐색 봇 실행 파일
snake_ga_bot.py # 유전 알고리즘 봇 실행 파일
```

`snake_game.py`, `snake_bot.py`, `snake_ga_bot.py`는 다음 방향을 어떻게 정할지만 담당합니다.

공통 규칙은 `snake_core.py`가 담당합니다.

- 방향 상수
- 좌표 이동
- 뱀 이동
- 벽 충돌 검사
- 자기 몸 충돌 검사
- 먹이 생성
- 게임 상태 보조 함수

## 리팩터링 계획

작은 단계로 리팩터링합니다.

1. `snake_core.py`를 생성합니다.
2. 방향 상수와 좌표 이동 helper를 옮깁니다.
3. 뱀 이동 로직을 옮깁니다.
4. 충돌 검사 로직을 옮깁니다.
5. 먹이 생성 로직을 옮깁니다.
6. `snake_game.py`가 공통 로직을 사용하도록 변경합니다.
7. 수동 플레이가 여전히 정상 동작하는지 확인합니다.
8. `snake_bot.py`도 공통 로직을 사용하도록 변경합니다.

## 경로 탐색 봇 계획

경로 탐색 봇은 단계적으로 만듭니다.

1. 기본 BFS
   - 현재 뱀 몸을 장애물로 봅니다.
   - 먹이까지 가는 가장 짧고 안전한 경로를 찾습니다.

2. 꼬리 이동 반영 BFS
   - 먹이를 먹지 않고 이동할 때 꼬리가 한 칸 비는 것을 반영합니다.
   - 다음 턴에 비게 되는 칸은 이동 가능 후보로 봅니다.

3. 장기 생존 전략
   - 먹이까지 가는 길이 있다고 해서 바로 먹지 않습니다.
   - 먹이를 먹은 뒤 갇히지 않는지 확인합니다.
   - 필요하면 바로 먹이로 가지 않고 더 안전한 이동을 선택합니다.

## 유전 알고리즘 봇 계획

유전 알고리즘 봇은 나중에 `snake_ga_bot.py`에서 만듭니다.

그 단계에서 결정할 내용:

- 개체 표현 방식
- 점수 함수
- 선택 방식
- 교차 방식
- 변이 방식
- 학습 결과 저장 방식

## 선호하는 개발 흐름

각 작업은 아래 순서로 진행합니다.

1. 목표를 짧게 다시 정리합니다.
2. 빠진 결정사항이 있으면 사용자에게 먼저 질문합니다.
3. 작은 변경을 적용합니다.
4. 실행 확인 또는 확인 방법을 설명합니다.
5. 필요하면 문서를 갱신합니다.

## Git 작업 규칙

GitHub에 올릴 변경사항은 작업 단위가 보이도록 작게 나눕니다.

### 브랜치 이름

브랜치 이름은 작업 목적이 드러나게 작성합니다.

예시:

```text
refactor/snake-core
feature/pathfinding-bot
feature/genetic-bot
docs/project-plan
fix/snake-movement
```

### 커밋 메시지

커밋 메시지는 아래 형식을 선호합니다.

```text
type: short summary
```

자주 쓰는 type:

- `docs`: 문서 변경
- `refactor`: 동작을 크게 바꾸지 않는 코드 구조 개선
- `feature`: 새 기능 추가
- `fix`: 버그 수정
- `test`: 테스트 추가 또는 수정
- `chore`: 설정, 정리, 기타 작업

예시:

```text
docs: add project guidance for Codex
refactor: move direction helpers into snake_core
feature: add basic BFS pathfinding bot
fix: prevent snake from reversing direction
```

### 커밋 본문

변경 이유가 필요하면 제목 아래에 한 줄을 비우고 본문을 씁니다.

```text
refactor: move direction helpers into snake_core

Separate reusable movement helpers so manual and bot runners can share the same rules.
```

### Pull Request 설명

PR을 만들 때는 아래 형식을 사용합니다.

```md
## Summary

- 변경한 핵심 내용을 짧게 적습니다.
- 문서, 리팩터링, 기능 추가를 구분해서 적습니다.

## Verification

- 실행하거나 확인한 명령을 적습니다.
- 직접 실행하지 못했다면 그 이유를 적습니다.

## Notes

- 다음 작업이나 남은 고민을 적습니다.
```

예시:

```md
## Summary

- Added `AGENTS.md` with project guidance.
- Documented the planned `snake_core.py` architecture.
- Updated TODO items for pathfinding and genetic algorithm bots.

## Verification

- Not run. Documentation-only change.

## Notes

- Next step is to create `snake_core.py` and move direction helpers.
```

### 작업 상태 관리

- 완료한 작업은 `TODO.md`에서 `[x]`로 체크합니다.
- 작업 이유나 결정사항은 `NOTES.md`에 남깁니다.
- 큰 방향이 바뀌면 `AGENTS.md`와 `PROJECT_PLAN.md`를 갱신합니다.
- 기본 커밋 단위는 완료된 `TODO.md` 체크박스 1개입니다.
- TODO 항목을 완료하면 커밋 메시지를 제안하고, 사용자 승인 후에만 커밋합니다.
- 사용자가 명시적으로 요청하지 않으면 자동으로 커밋하지 않습니다.

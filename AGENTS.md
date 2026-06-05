# AGENTS.md

## stable_bot 작업 규칙

- 안정적인 400점 완주를 목표로 하는 주 작업은 `stable_bot/`에서 진행합니다.
- `ga_bot/`은 삭제하지 않고 학습형 봇 실험, 비교 기준, 기록 보관용으로 유지합니다.
- `stable_bot/`은 유전 알고리즘이 아니라 결정론적 안전 전략을 우선합니다.
- 기본 방향은 Hamiltonian cycle을 fallback으로 두고, 안전성이 검증된 경우에만 shortcut을 허용하는 방식입니다.
- 안정성 검증은 단일 최고 점수가 아니라 반복 평가 성공률로 판단합니다.
- 목표 기준은 100판 반복 평가에서 `score=400` 성공률 80% 이상입니다.
- 구현 전에는 `stable_bot/DESIGN_NOTES.md`에 설계 이유를 먼저 기록합니다.
- 세부 작업은 `stable_bot/TODO.md`에서 관리하고, 루트 `TODO.md`에는 큰 단계만 유지합니다.

## 프로젝트 개요

Python `pygame`으로 만든 스네이크 게임과 자동 플레이 봇 프로젝트입니다.

가장 중요한 방향은 `snake_game.py`를 짧고 읽기 쉬운 실행 파일로 유지하고, 객체별 책임을 파일로 분리하는 것입니다.

## 목표 구조

```text
snake_game.py   # 수동 플레이 실행 흐름
snake.py        # Snake 클래스
apple.py        # Apple 클래스
rule.py         # Rule 클래스
snake_core.py   # 공통 상수와 순수 helper 함수
snake_bot.py    # 경로 탐색 봇
snake_ga_bot.py # 유전 알고리즘 봇 실행 진입점
ga_bot/         # 유전 알고리즘 봇 코드와 학습 산출물
```

## 책임 분리 규칙

- `snake_game.py`에는 pygame 초기화, 객체 생성, 게임 루프, 화면 업데이트만 둡니다.
- `snake.py`에는 뱀 위치, 이동, 성장, 그리기 로직을 둡니다.
- `apple.py`에는 먹이 위치, 재생성, 그리기 로직을 둡니다.
- `rule.py`에는 게임 오버, 승리 조건, 종료 화면 로직을 둡니다.
- `snake_core.py`에는 보드 크기, 방향, 좌표 계산, 충돌 검사, 먹이 생성 같은 공통 helper만 둡니다.

## 작업 규칙

- 큰 설계 변경 전에는 먼저 사용자에게 질문합니다.
- 사용자가 진행을 승인한 작업은 확인 질문 없이 이어서 진행합니다.
- 변경은 작게, 단계적으로 진행합니다.
- 사용자가 코드 설명을 요청하면 변경된 부분 중심으로 설명합니다.
- Python 파일을 수정한 뒤 필요한 `TODO.md`, `NOTES.md`, `README.md`, `PROJECT_PLAN.md` 반영은 확인 질문 없이 수행합니다.
- 코드의 파일명, 함수명, 변수명은 영어를 사용합니다.
- 각 함수의 작업 코드에는 사용자가 이해하기 쉬운 한국어 주석이나 docstring을 작성합니다.
- 사용자가 명시적으로 요청하지 않으면 자동으로 커밋하지 않습니다.

## 봇 계획

경로 탐색 봇은 `snake_bot.py`에서 단계적으로 만듭니다.

1. 기본 BFS: 현재 뱀 몸을 장애물로 보고 먹이까지 최단 경로를 찾습니다.
2. 꼬리 이동 반영: 이동 시 꼬리가 비는 상황을 반영합니다.
3. 장기 생존 전략: 먹이를 먹은 뒤 갇히지 않는지 확인합니다.

유전 알고리즘 봇은 나중에 `snake_ga_bot.py`에서 만듭니다.

유전 알고리즘 봇의 세부 코드는 `ga_bot/` 폴더에서 관리합니다.

- `ga_bot/policy.py`: 학습된 가중치로 방향을 선택합니다.
- `ga_bot/simulation.py`: pygame 없이 한 판을 계산으로 실행합니다.
- `ga_bot/trainer.py`: 선택, 교차, 변이, 세대 반복을 담당합니다.
- `ga_bot/storage.py`: JSON 모델과 CSV 로그 저장을 담당합니다.
- `ga_bot/TODO.md`: GA 내부 세부 작업을 관리합니다.
- `ga_bot/AGENTS.md`: GA 폴더 전용 작업 규칙입니다.

가중치 특징값은 사용자와 논의한 뒤 확정합니다.

## Git 작업 규칙

- 기본 커밋 단위는 완료된 `TODO.md` 체크박스 1개입니다.
- 커밋 전에는 추천 커밋 메시지를 제안합니다.
- 사용자 승인 후에만 커밋합니다.

커밋 메시지 형식:

```text
type: short summary
```

예시:

```text
refactor: split manual game into object modules
feature: add basic BFS pathfinding bot
docs: update project structure notes
```

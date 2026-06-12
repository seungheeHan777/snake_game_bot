# Project Plan

## 현재 기록

유전 알고리즘 기반 `ga_bot/`은 학습 과정에서 `score=400`을 달성한 사례가 있었습니다. 하지만 반복 평가에서 꾸준한 성공률을 보이지 못했기 때문에 최종 안정 봇으로 사용하지 않습니다.

현재 최종 안정 봇은 `stable_bot/`입니다.

```text
stable_bot 평가 결과
100판 중 100판 성공
목표 score=400 전부 달성
```

`stable_bot`은 다음 구조를 사용합니다.

- Hamiltonian fallback 경로로 기본 안전성 확보
- safe shortcut으로 일부 먹이 경로 단축
- shortcut 계산은 백그라운드에서 처리해 화면 플레이 중 딜레이를 줄임

## 현재 우선순위

유전 알고리즘 기반 `ga_bot/`은 현재 안정적인 완주 모델을 만들기에는 한계가 확인되었습니다. 높은 점수나 400점 후보가 일부 나와도 반복 평가에서 성공률이 낮기 때문에, 이 방식은 연구/비교 기준으로 유지합니다.

새 우선순위는 `stable_bot/`입니다.

- 목표: 20x20 보드에서 `score=400`
- 기준: 100판 반복 평가에서 400점 성공률 80% 이상
- 전략: Hamiltonian cycle fallback + 안전성이 검증된 shortcut
- 이유: 뱀이 길어질수록 단순히 먹이에 가까워지는 정책보다, 죽지 않는 전체 경로 보장이 더 중요하기 때문입니다.

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
snake_ga_bot.py # 유전 알고리즘 봇 실행 진입점
ga_bot/         # 유전 알고리즘 봇 코드와 학습 산출물
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
   - `ga_bot/policy.py`: 개체의 가중치로 방향을 평가합니다.
   - `ga_bot/simulation.py`: pygame 없이 학습용 게임을 실행합니다.
   - `ga_bot/trainer.py`: 세대 평가, 선택, 교차, 변이를 실행합니다.
   - `ga_bot/storage.py`: `best_weights.json`, `checkpoint.json`, `training_history.csv`를 관리합니다.
   - 가중치 특징값은 사용자와 논의한 뒤 확정합니다.

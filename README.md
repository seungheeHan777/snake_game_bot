# snake_game_bot

## 수동 플레이 결과 저장

수동 게임 실행 파일은 `snake_game.py`입니다.

```powershell
py -3 snake_game.py
```

현재 구현된 흐름:

- 시작 화면에서 `Start` 또는 `Ranking` 선택
- 게임 종료 후 `WIN` 또는 `GAME OVER` 결과 화면 표시
- pygame 창에서 플레이어 이름 입력
- `Save` 버튼으로 `players`, `game_runs`에 결과 저장
- 저장 성공 시 `Saved` 표시 후 시작 화면으로 이동
- `Retry` 버튼으로 새 게임 시작
- `Ranking` 화면에서 저장된 상위 수동 플레이 기록 조회
- 랭킹 화면에서 `Score`, `Steps`, `Wins only` 기준 전환

현재 저장되는 수동 플레이 값:

- `actor_type = player`
- `run_type = screen`
- `player_id = players.id`
- `score`, `steps`, `success`, `dead`, `victory`, `final_reason`
- `started_at`, `finished_at`, `elapsed_seconds`

랭킹 화면은 현재 조회 전용입니다. 랭킹 UI 세부 디자인과 필터 기능은 다음 단계에서 개선합니다.

## 수동 플레이 저장 UI 계획

수동 플레이 결과도 PostgreSQL DB에 저장할 예정입니다. 플레이어 이름은 터미널 입력이 아니라 pygame 게임 창 안에서 입력받습니다.

1차 구현 범위:

- 게임 종료 후 이름 입력 화면 표시
- `Save` 버튼으로 `players`와 `game_runs`에 저장
- 저장 성공 시 `Saved` 표시
- `Retry` 버튼으로 새 게임 시작

장기 UI 계획:

```text
Start Screen
  [Start]
  [Ranking]

Game Screen
  snake game

Result Screen
  name input
  [Save]
  [Retry]

Ranking Screen
  ranking list
  [Back]
```

랭킹 화면은 나중 단계에서 구현합니다. 다음 구현 대상은 수동 플레이 종료 후 이름 입력 및 저장 화면입니다.

## 현재 상태 기록

처음에는 유전 알고리즘 기반 `ga_bot/`으로 자동 플레이 봇을 만들었습니다. GA 학습 중 최고점 `score=400`, 즉 게임 성공 사례는 나왔지만, 같은 모델을 반복 평가했을 때 안정적으로 성공하지 못했습니다. 따라서 `ga_bot/`은 실험 및 비교 기준으로 유지합니다.

이후 안정적인 완주를 목표로 `stable_bot/`을 추가로 개발했습니다. `stable_bot`은 Hamiltonian fallback 경로를 기본으로 사용하고, 안전하다고 판단되는 경우에만 shortcut을 사용합니다. shortcut 계산은 게임 루프를 막지 않도록 백그라운드에서 처리합니다.

현재 검증 결과:

```text
stable bot
100판 평가
success=100/100
score=400 전부 성공
```

현재 안정 봇 실행 명령:

```powershell
py -3 snake_stable_bot.py
```

정리:

- `ga_bot/`: 유전 알고리즘 실험 및 baseline
- `stable_bot/`: 현재 안정 완주 봇
- `snake_stable_bot.py`: shortcut 포함 stable bot 실행 파일

## DB 저장 기능

PostgreSQL 기반 게임 결과 저장 작업을 시작했습니다.

현재 생성된 DB 작업 폴더:

```text
db/
```

현재 DB 구조:

- `players`: 사람 플레이어 정보, 사용자가 직접 생성
- `bot_configs`: 봇 설정 정보
- `evaluation_sessions`: headless 반복 평가 묶음
- `game_runs`: 사람/봇의 실제 한 판 결과

현재 구현 완료:

- PostgreSQL 연결 코드
- 샘플 저장 테스트
- headless 평가 결과 DB 저장

headless 평가 저장 실행:

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable --save-db
```

수동 화면 플레이 저장은 아직 구현하지 않았습니다. 플레이어 이름을 터미널이 아니라 pygame 실행창에서 입력받는 화면 구성을 먼저 논의한 뒤 진행합니다.

## 현재 방향: 안정 완주 봇

현재 유전 알고리즘 기반 `ga_bot/`은 실험 및 비교 기준으로 유지합니다. 반복 평가 결과, 현 GA 모델은 가끔 높은 점수 또는 400점을 찍을 수는 있지만, 같은 모델을 여러 번 돌렸을 때 안정적으로 400점을 재현하지 못했습니다.

따라서 안정적인 완주를 목표로 하는 새 작업 트랙을 `stable_bot/` 폴더에 분리했습니다.

- `stable_bot/`: 결정론적 안정 완주 봇 작업 공간
- 목표: 20x20 보드에서 `score=400`
- 검증 기준: 100판 반복 평가 중 `score=400` 성공률 80% 이상
- 기본 전략: Hamiltonian cycle 기반 안전 경로 + 검증된 경우에만 먹이로 가는 shortcut 허용
- 기존 `ga_bot/`: 학습형 봇 실험, 비교 기준, 기록 보관용

## 실행 파일(핵심)

- 학습 실행: `snake_ga_bot.py`
- 학습 모델 플레이 확인: `snake_ga_play.py`

## GA 폴더 구조(핵심)

- `ga_bot/trainer.py`: 유전 알고리즘 학습 루프(세대 반복)
- `ga_bot/simulation.py`: 화면 없는 시뮬레이션 + fitness 계산
- `ga_bot/policy.py`: feature 계산 + 방향 선택
- `ga_bot/storage.py`: 모델/체크포인트/로그 저장
- `ga_bot/models/`: `best_weights.json`, `checkpoint.json`, `score400/` 후보 저장
- `ga_bot/logs/`: `training_history.csv` 학습 기록
- `ga_bot/tools/`: 보조 검증/선발 스크립트
  - `evaluate_model.py`: 모델 1개 반복 평가
  - `select_best_candidate.py`: score400 후보 자동 선발
  - `run_pipeline.py`: 평가/선발 파이프라인

Python `pygame`으로 만든 스네이크 게임과 자동 플레이 봇 프로젝트입니다.

## 실행 방법

가상환경을 활성화한 뒤 실행합니다.

```powershell
python snake_game.py
```

## 현재 구조

- `snake_game.py`: 수동 플레이 게임 실행 흐름
- `snake.py`: `Snake` 클래스, 뱀 위치/이동/성장/그리기
- `apple.py`: `Apple` 클래스, 먹이 위치/재생성/그리기
- `rule.py`: `Rule` 클래스, 게임 오버/승리 조건/종료 화면
- `snake_core.py`: 보드 크기, 방향, 좌표 이동, 충돌 검사, 먹이 생성 helper
- `snake_bot.py`: 경로 탐색 봇으로 개선 예정
- `snake_ga_bot.py`: 유전 알고리즘 봇 학습 실행 파일
- `ga_bot/`: 유전 알고리즘 코드, 모델 저장 파일, 학습 로그 관리

## 목표

1. 수동 스네이크 게임 코드를 읽기 쉬운 파일 구조로 정리합니다.
2. `snake_game.py`는 실행 흐름만 담당하게 만듭니다.
3. 경로 탐색 기반 봇을 만듭니다.
4. 유전 알고리즘 기반 봇을 만듭니다.

## 유전 알고리즘 봇

GA 관련 세부 코드는 `ga_bot/` 폴더에서 관리합니다.

- `ga_bot/policy.py`: 가중치로 방향을 평가하고 선택합니다.
- `ga_bot/simulation.py`: pygame 화면 없이 학습용 게임을 실행합니다.
- `ga_bot/trainer.py`: 선택, 교차, 변이, 세대 반복을 담당합니다.
- `ga_bot/storage.py`: JSON 모델과 CSV 로그를 저장하고 불러옵니다.

학습 결과는 `ga_bot/models/`, 학습 로그는 `ga_bot/logs/`에 저장합니다.

GA 봇의 feature 개선 과정과 문제 교정 기록은 `ga_bot/DESIGN_NOTES.md`에 정리합니다.

# snake_game_bot

Python `pygame`으로 만든 스네이크 게임과 자동 플레이 봇 프로젝트입니다.

## 실행 방법

가상환경을 활성화한 뒤 실행합니다.

```powershell
py -3 snake_game.py
```

안정 완주 봇 화면 실행:

```powershell
py -3 snake_stable_bot.py
```

안정 완주 봇 headless 평가:

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable
```

DB 저장 포함 headless 평가:

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable --save-db
```

## 현재 구현 상태

- 수동 플레이 시작 화면
- 수동 게임 화면
- 게임 종료 후 결과 화면
- pygame 창에서 player name 입력
- `Save` 버튼으로 `players`, `game_runs`에 결과 저장
- 저장 성공 시 `Saved` 표시 후 시작 화면으로 이동
- 저장 실패 사유를 짧게 표시
- `Retry` 버튼으로 새 게임 시작
- 랭킹 화면
- 랭킹 `Score` / `Steps` 정렬
- 랭킹 `Wins only` 필터
- 랭킹 `Best` / `Runs` 보기 모드
- 랭킹 표 간격, 버튼 위치, 빈 기록 화면 정리

## 수동 플레이 저장 값

수동 플레이 결과는 PostgreSQL의 `game_runs`에 저장합니다.

주요 값:

- `actor_type = player`
- `run_type = screen`
- `player_id = players.id`
- `score`
- `steps`
- `success`
- `dead`
- `victory`
- `final_reason`
- `started_at`
- `finished_at`
- `elapsed_seconds`

플레이어 이름은 `players.display_name` 기준으로 get-or-create 합니다.

## 랭킹 기준

랭킹 기본 모드는 `Best`입니다.

- `Best`: 플레이어별 최고 기록만 표시
- `Runs`: 저장된 게임 기록 전체 표시
- `Score`: 점수 높은 순
- `Steps`: 승리 기록 우선, steps 낮은 순
- `Wins only`: `victory=true` 기록만 표시

## 안정 완주 봇

처음에는 유전 알고리즘 기반 `ga_bot/`으로 자동 플레이 봇을 만들었습니다. GA 학습 중 최고점 `score=400` 사례는 나왔지만, 같은 모델을 반복 평가했을 때 안정적으로 성공하지 못했습니다. 따라서 `ga_bot/`은 실험 및 비교 기준으로 유지합니다.

현재 안정 완주 봇은 `stable_bot/`입니다.

- Hamiltonian fallback 경로로 기본 안전성 확보
- 안전하다고 판단되는 경우에만 shortcut 사용
- shortcut 계산은 게임 루프를 막지 않도록 백그라운드에서 처리
- 100판 평가에서 `success=100/100`, `avg_score=400.00` 확인

## 주요 파일 구조

```text
snake_game.py       # 수동 플레이 앱: 시작, 게임, 결과 저장, 랭킹 화면
snake_stable_bot.py # stable bot 화면 실행 파일
snake.py            # Snake 클래스
apple.py            # Apple 클래스
rule.py             # Rule 클래스
snake_core.py       # 공통 상수와 순수 helper 함수
snake_bot.py        # 경로 탐색 봇
snake_ga_bot.py     # GA 학습 실행 진입점
snake_ga_play.py    # GA 모델 화면 실행
db/                 # DB 연결, schema, repository 함수
stable_bot/         # 안정 완주 봇
ga_bot/             # GA 실험 코드와 학습 산출물
```

세부 TODO:

- 루트 `TODO.md`: 현재 우선순위와 큰 작업 상태
- `stable_bot/TODO.md`: 안정 완주 봇 세부 구현/평가 상태
- `ga_bot/TODO.md`: GA 실험/보관 상태와 재개 조건

## DB 구조

- `players`: 사람 플레이어 정보
- `bot_configs`: 봇 설정 정보
- `evaluation_sessions`: headless 반복 평가 묶음
- `game_runs`: 사람/봇의 실제 한 판 결과

DB 연결 정보는 루트 `.env`에 둡니다. `.env`는 Git에 포함하지 않습니다.

## 작업 규칙

하나의 task가 완료되면 `TODO.md`를 바로 정리합니다.

기능 흐름, 실행 방법, 작업 규칙이 바뀌면 `README.md` 또는 `AGENTS.md`에 바로 반영합니다.

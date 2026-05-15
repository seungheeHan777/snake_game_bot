# Notes

## 2026-05-09

- 프로젝트를 다시 시작했습니다.
- VS Code에서 venv를 추가했습니다.
- venv 안에 `pygame`을 설치했고 코드 실행을 확인했습니다.
- `AGENTS.md`를 프로젝트 작업 지침으로 사용하기로 했습니다.
- 경로 탐색 봇은 기본 BFS, 꼬리 이동 반영, 장기 생존 전략 순서로 단계적으로 만들기로 했습니다.
- 유전 알고리즘 봇은 나중에 `snake_ga_bot.py` 파일로 따로 만들기로 했습니다.

## 2026-05-12

- 사용자가 원한 방향에 맞춰 파일별 책임 분리 구조로 전환했습니다.
- `snake_game.py`는 게임 실행 흐름만 담당하도록 정리했습니다.
- `Snake`, `Apple`, `Rule` 클래스를 각각 `snake.py`, `apple.py`, `rule.py`로 분리했습니다.
- 공통 상수와 helper 함수는 `snake_core.py`에 유지했습니다.
- 먹이 생성은 빈 칸 목록에서 선택하는 방식으로 유지하기로 했습니다.

## 개발 메모

- 리팩터링 단계에서는 `snake_game.py`가 읽기 쉬운 실행 파일이 되는 것을 우선합니다.
- 봇 구현은 수동 게임 구조가 안정된 뒤 진행합니다.

## 2026-05-14

- 유전 알고리즘 관련 코드를 `ga_bot/` 폴더에서 관리하기로 했습니다.
- `snake_ga_bot.py`는 GA 학습 실행 진입점으로 사용합니다.
- `policy.py`, `simulation.py`, `trainer.py`, `storage.py`로 역할을 분리했습니다.
- GA 내부 세부 TODO는 `ga_bot/TODO.md`에서 관리하고, 루트 `TODO.md`에는 큰 단계만 기록합니다.
- 학습 결과는 `ga_bot/models/`, 학습 로그는 `ga_bot/logs/`에 저장합니다.

## 2026-05-16

- GA 봇이 100점 근처에서 정체되는 원인을 현재 feature의 한계로 분석했습니다.
- `food_distance_delta` 중심의 한 칸 평가만으로는 후반 생존에 필요한 공간 판단이 부족하다고 정리했습니다.
- 다음 개선 후보로 `free_space_after_move`, `tail_reachable_after_move`, loop penalty를 기록했습니다.
- 자세한 내용은 `ga_bot/DESIGN_NOTES.md`에 정리했습니다.

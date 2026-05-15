# snake_game_bot

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

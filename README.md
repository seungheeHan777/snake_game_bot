# snake_game_bot

Python pygame으로 만든 스네이크 게임과 자동 플레이 봇 프로젝트입니다.

## 실행 방법

가상환경을 활성화한 뒤 실행합니다.

```powershell
python snake_game.py
python snake_bot.py
```

## 개발 환경

- Python
- pygame
- VS Code
- venv

## 현재 파일

- `snake_game.py`: 키보드로 조작하는 기본 스네이크 게임
- `snake_bot.py`: 자동으로 먹이를 찾아가도록 실험 중인 봇 버전
- `fun_navigator(ver1.0).txt`: 예전 자동 이동 로직 메모
- `AGENTS.md`: Codex 작업 지침
- `PROJECT_PLAN.md`: 개발 계획

## 목표

1. `snake_game.py`의 중복 코드를 줄이고 구조를 정리합니다.
2. 공통 게임 규칙을 `snake_core.py`로 분리합니다.
3. `snake_bot.py`를 경로 탐색 기반 봇으로 개선합니다.
4. `snake_ga_bot.py`에 유전 알고리즘 기반 봇을 새로 만듭니다.

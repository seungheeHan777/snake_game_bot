# Stable Bot TODO

## 현재 상태

- [x] `stable_bot/` 폴더 생성
- [x] GA 방식이 안정 완주에 부족한 이유 기록
- [x] Hamiltonian fallback 경로 방식 결정
- [x] 먹이 shortcut 허용 조건 결정
- [x] 꼬리 또는 fallback 경로 재연결 검사 기준 결정
- [x] 성공 기준 확정
- [x] stable bot 화면 실행 파일을 루트 `snake_stable_bot.py`로 확정
- [x] 화면 플레이 확인

## 핵심 알고리즘

- [x] `hamiltonian.py` 생성
- [x] 현재 20x20 보드 전체 순회 경로 생성
- [x] Hamiltonian fallback headless 완주 검증
- [x] `safety.py` 생성
- [x] 벽/몸통 충돌 검사 구현
- [x] 꼬리 도달 가능성 검사 구현
- [x] 열린 공간 검사 구현
- [x] `shortcut.py` 생성
- [x] 먹이까지의 safe shortcut 탐색 구현
- [x] `planner.py` 생성
- [x] safe shortcut과 fallback 경로 중 선택하는 로직 구현

## 성능 개선

- [x] `stable_bot/evaluate.py` headless 반복 평가 스크립트 생성
- [x] `stable`/`fallback` 각 1판 동작 확인
- [x] `stable` 모드 30판 평가
- [x] `fallback` 모드 30판 평가
- [x] shortcut 거리 4/8/12 비교
- [x] shortcut 성능 병목 확인
- [x] shortcut 계산을 비동기 처리로 변경
- [x] 같은 먹이 위치에 대한 중복 shortcut 계산 방지
- [x] 기본 shortcut distance를 4로 결정

## 최종 평가

- [x] `stable` 기본값 shortcut distance 4 기준 100판 평가 완료
- [x] `success=100/100`
- [x] `avg_score=400.00`
- [x] `avg_steps=39770.29`
- [x] 목표 기준 `score=400` 성공률 80% 이상 통과

## DB 저장

- [x] headless 평가 결과 DB 저장 지원
- [x] `bot_configs` 저장 연결
- [x] `evaluation_sessions` 저장 연결
- [x] `game_runs` 저장 연결

## 보류 작업

- [ ] stable bot 화면 플레이 결과 DB 저장 여부 결정
- [ ] shortcut distance 자동 조정 여부 검토
- [ ] stable bot 전용 `runner.py`가 필요한지 재검토

## 참고

현재 stable bot의 주 실행 파일은 루트의 `snake_stable_bot.py`입니다.

현재 headless 평가 명령:

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable
```

DB 저장 포함 평가 명령:

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable --save-db
```

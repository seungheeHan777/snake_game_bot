# TODO

## 수동 플레이 결과 저장 UI

- [x] `snake_game.py` 실행 후 게임 종료 화면 표시
- [x] pygame 창에서 player name 입력
- [x] `Save` 버튼으로 `players`, `game_runs` 저장 연결
- [x] 저장 성공 시 `Saved` 표시
- [x] `Retry` 버튼으로 새 게임 시작
- [x] 시작 화면 구현
- [x] 랭킹 화면 구현
- [x] 저장 완료 시 시작 화면으로 이동
- [x] 랭킹 조회 쿼리와 화면 연결
- [ ] 수동으로 pygame 창에서 저장 동작 확인
- [ ] 랭킹 화면 UI 세부 디자인 개선
- [ ] 랭킹 필터/정렬 기준 결정

## 수동 플레이 저장 UI 계획

- [x] 게임 종료 후 player name 입력 방식 결정
- [x] 터미널 입력이 아니라 pygame 창 입력으로 결정
- [x] 저장 후 `Saved` 표시 결정
- [x] `Retry` 버튼으로 다시 시작 결정
- [ ] 결과 화면 UI 설계
- [ ] 이름 입력 UI 구현
- [ ] Save 버튼 DB 저장 연결
- [ ] Retry 버튼 새 게임 연결
- [ ] 장기 시작 화면/랭킹 화면 구현

## DB 저장 기능

- [x] PostgreSQL 연결 코드 생성
- [x] `players` 테이블을 제외한 DB 스키마 작성
- [x] 샘플 저장 테스트 완료
- [x] headless 평가 결과 DB 저장 구현
- [x] `stable_bot.evaluate --save-db` 저장 테스트 완료
- [ ] 수동 화면 플레이 결과 저장 화면 구성 논의
- [ ] pygame 창에서 player name 입력 UI 구현
- [ ] 수동 플레이 결과를 `game_runs`에 저장

## stable_bot 최종 평가

- [x] `stable` 기본값 shortcut distance 4 기준 100판 평가 완료
- [x] `success=100/100`
- [x] `avg_score=400.00`
- [x] 목표 기준 `score=400` 성공률 80% 이상 통과
- [ ] 화면 플레이 확인

## 현재 stable_bot 진행

- [x] `stable_bot/evaluate.py` 반복 평가 스크립트 구현
- [x] stable/fallback 반복 평가 결과 비교
- [x] shortcut 계산 지연 개선
- [x] shortcut 거리 기준 조정

## 4단계: 안정 완주 봇

- [x] `stable_bot/` 폴더 생성
- [x] GA 방식의 한계와 새 방향 문서화
- [x] Hamiltonian cycle 기반 fallback 경로 설계
- [x] Hamiltonian fallback 코드 생성 및 headless 완주 검증
- [x] 먹이 shortcut 허용 조건 설계
- [x] `stable_bot/hamiltonian.py` 구현
- [x] `stable_bot/safety.py` 구현
- [x] `stable_bot/planner.py` 구현
- [ ] `stable_bot/runner.py` 또는 기존 실행 파일 연결 방식 결정
- [ ] 100판 반복 평가에서 `score=400` 성공률 80% 이상 확인

세부 작업은 `stable_bot/TODO.md`에서 관리합니다.

## 1단계: 수동 게임 구조 정리

- [x] `snake_core.py`에 공통 상수와 helper 분리
- [x] `snake.py` 생성
- [x] `apple.py` 생성
- [x] `rule.py` 생성
- [x] `snake_game.py`를 실행 흐름 중심으로 정리
- [x] 수동 플레이 실행 확인

## 2단계: 경로 탐색 봇

- [x] `snake_bot.py`를 새 구조에 맞게 정리
- [x] 기본 BFS 구현
- [x] 현재 뱀 몸을 장애물로 보는 경로 탐색 구현
- [x] 꼬리 이동을 반영하는 경로 탐색 개선
- [x] 먹이를 먹은 뒤 갇히지 않는지 확인하는 장기 생존 전략 추가
- [x] BFS 큐가 뱀 몸 전체를 저장하지 않도록 메모리 사용 개선

## 3단계: 유전 알고리즘 봇

- [x] `ga_bot/` 폴더 생성
- [x] `snake_ga_bot.py` 생성
- [x] GA 코드 구조 분리
- [ ] 가중치 특징값 설계 확정
- [ ] 학습 실행 확인
- [ ] 학습된 모델을 게임에 연결
- [ ] 세부 작업은 `ga_bot/TODO.md`에서 관리

## 문서

- [x] `AGENTS.md` 작성
- [x] `PROJECT_PLAN.md` 작성
- [x] README 구조 설명 최신화
- [x] `ga_bot/AGENTS.md`, `ga_bot/TODO.md`, `ga_bot/README.md` 작성

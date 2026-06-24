# TODO

## 현재 우선순위

- [x] 랭킹 화면 UI 세부 디자인 개선
- [ ] 수동 플레이 결과 저장/랭킹 흐름 최종 화면 점검
- [x] stable bot 관련 TODO를 현재 구현 상태에 맞게 정리
- [x] GA bot 관련 TODO를 실험/보관 상태에 맞게 정리

## 수동 플레이 결과 저장 UI

- [x] `snake_game.py` 실행 후 시작 화면 표시
- [x] `Start` 버튼으로 수동 게임 시작
- [x] 게임 종료 후 결과 화면 표시
- [x] pygame 창에서 player name 입력
- [x] `Save` 버튼으로 `players`, `game_runs` 저장 연결
- [x] 저장 성공 시 `Saved` 표시
- [x] 저장 실패 사유를 화면에 짧게 표시
- [x] 저장 완료 시 시작 화면으로 이동
- [x] `Retry` 버튼으로 새 게임 시작
- [x] 수동으로 pygame 창에서 저장 동작 확인

## 랭킹 화면

- [x] `Ranking` 버튼으로 랭킹 화면 이동
- [x] `Back` 버튼으로 시작 화면 복귀
- [x] 랭킹 조회 쿼리와 화면 연결
- [x] 순위 / Name / Score / Steps 표 형태 표시
- [x] `Score` / `Steps` 정렬 버튼 구현
- [x] `Wins only` 필터 구현
- [x] `Best` / `Runs` 보기 모드 구현
- [x] 랭킹 필터/정렬 기준 결정
- [x] 표 간격, 버튼 위치, 빈 기록 화면 등 UI 세부 디자인 개선

## DB 저장 기능

- [x] PostgreSQL 연결 코드 생성
- [x] `players` 테이블을 제외한 DB 스키마 작성
- [x] 샘플 저장 테스트 완료
- [x] headless 평가 결과 DB 저장 구현
- [x] `stable_bot.evaluate --save-db` 저장 테스트 완료
- [x] 수동 플레이 결과를 `game_runs`에 저장
- [x] player name을 `players.display_name` 기준으로 get-or-create
- [x] 플레이어별 최고 기록 조회 구현

## stable_bot

- [x] `stable_bot/` 폴더 생성
- [x] GA 방식의 한계와 새 방향 문서화
- [x] Hamiltonian cycle 기반 fallback 경로 설계
- [x] Hamiltonian fallback 코드 생성 및 headless 완주 검증
- [x] 먹이 shortcut 허용 조건 설계
- [x] `stable_bot/hamiltonian.py` 구현
- [x] `stable_bot/safety.py` 구현
- [x] `stable_bot/planner.py` 구현
- [x] `snake_stable_bot.py` 실행 방식 확정
- [x] 100판 반복 평가에서 `score=400` 성공률 80% 이상 확인
- [x] `stable` 기본값 shortcut distance 4 기준 100판 평가 완료
- [x] `success=100/100`
- [x] `avg_score=400.00`
- [x] 화면 플레이 확인
- [x] `stable_bot/TODO.md` 세부 항목 최신화

## 수동 게임 구조 정리

- [x] `snake_core.py`에 공통 상수와 helper 분리
- [x] `snake.py` 생성
- [x] `apple.py` 생성
- [x] `rule.py` 생성
- [x] `snake_game.py`를 실행 흐름 중심으로 정리
- [x] 수동 플레이 실행 확인

## 경로 탐색 봇

- [x] `snake_bot.py`를 새 구조에 맞게 정리
- [x] 기본 BFS 구현
- [x] 현재 뱀 몸을 장애물로 보는 경로 탐색 구현
- [x] 꼬리 이동을 반영하는 경로 탐색 개선
- [x] 먹이를 먹은 뒤 갇히지 않는지 확인하는 장기 생존 전략 추가
- [x] BFS 큐가 뱀 몸 전체를 저장하지 않도록 메모리 사용 개선

## GA bot

- [x] `ga_bot/` 폴더 생성
- [x] `snake_ga_bot.py` 생성
- [x] GA 코드 구조 분리
- [x] GA 학습 및 후보 평가 진행
- [x] GA 방식의 안정성 한계 문서화
- [x] GA를 최종 봇이 아닌 실험/비교 기준으로 유지 결정
- [x] `ga_bot/TODO.md` 세부 항목 최신화

## 문서

- [x] `AGENTS.md` 작성
- [x] `PROJECT_PLAN.md` 작성
- [x] README 구조 설명 최신화
- [x] `ga_bot/AGENTS.md`, `ga_bot/TODO.md`, `ga_bot/README.md` 작성
- [x] 작업 완료 시 TODO/README/AGENTS 반영 규칙 추가

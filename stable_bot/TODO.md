# Stable Bot TODO

## 최종 평가 상태

- [x] `stable` 기본값 shortcut distance 4 기준 100판 평가 완료
- [x] `success=100/100`
- [x] `avg_score=400.00`
- [x] `avg_steps=39770.29`
- [x] 목표 기준 `score=400` 성공률 80% 이상 통과
- [ ] 화면 플레이 확인

## 현재 추가 완료

- [x] `stable_bot/evaluate.py` headless 반복 평가 스크립트 생성
- [x] `stable`/`fallback` 각 1판 동작 확인
- [x] `stable` 모드 30판 평가
- [x] `fallback` 모드 30판 평가
- [x] shortcut 거리 4/8/12 비교
- [x] shortcut 성능 병목 개선
- [x] shortcut 계산을 비동기 처리로 변경
- [x] 같은 먹이 위치에 대한 중복 shortcut 계산 방지

## 1단계: 설계 확정

- [x] `stable_bot/` 폴더 생성
- [x] GA 방식이 안정 완주에 부족한 이유 기록
- [x] 첫 안정 전략 확정
- [x] Hamiltonian fallback 경로 방식 결정
- [x] 먹이 shortcut 허용 조건 결정
- [x] 꼬리 또는 fallback 경로 재연결 검사 기준 결정
- [x] 성공 기준 확정

성공 기준 초안:

- 100판 반복 평가
- 목표 `score=400`
- 80판 이상 성공하면 통과

## 2단계: 핵심 알고리즘

- [x] `hamiltonian.py` 생성
- [x] 현재 20x20 보드 전체 순회 경로 생성
- [x] Hamiltonian fallback headless 완주 검증
- [x] `safety.py` 생성
- [x] 벽/몸통 충돌 검사 구현
- [x] 꼬리 도달 가능성 검사 구현
- [x] 열린 공간 검사 구현
- [ ] `planner.py` 생성
- [x] `planner.py` 생성
- [x] safe shortcut과 fallback 경로 중 선택하는 로직 구현

## 3단계: 실행 연결

- [x] stable bot 실행 파일 생성
- [x] 기존 `snake_game.run_game()` 흐름과 연결
- [ ] 화면으로 stable bot 플레이 확인
- [ ] headless 반복 평가 스크립트 생성
- [ ] fallback only와 shortcut 포함 버전 평균 steps 비교

## 4단계: 검증

- [ ] 30판 빠른 평가 실행
- [ ] 100판 최종 평가 실행
- [ ] 현재 GA baseline과 결과 비교
- [ ] `score=400` 성공률 80% 이상 확인

## 보류 작업

- DB 저장 기능은 stable bot이 80% 이상 성공률을 달성한 뒤 사용자와 상의 후 진행합니다.
- GA 개선은 현재는 메인 작업이 아니며, 비교용 baseline으로만 유지합니다.

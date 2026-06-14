# Database TODO

## 현재 반영 완료

- [x] 저장 실패 사유를 pygame 결과 화면에 짧게 표시
- [x] 랭킹 `Score` / `Steps` 정렬 조회
- [x] 랭킹 `Wins only` 필터 조회
- [x] 플레이어별 최고 기록 조회

## 수동 플레이 저장 UI 현재 상태

- [x] 게임 종료 후 결과 화면 표시
- [x] pygame 창에서 player name 입력
- [x] `Save` 버튼으로 `players` get-or-create
- [x] `Save` 버튼으로 `game_runs` 저장
- [x] 저장 성공 시 `Saved` 표시
- [x] `Retry` 버튼으로 새 게임 시작
- [ ] 실제 pygame 창에서 저장 수동 확인
- [ ] 저장 실패 사유를 화면에 더 구체적으로 표시
- [ ] 랭킹 조회 repository 함수 추가
- [ ] 시작 화면 / 랭킹 화면 연결

## 수동 플레이 저장 결정

- [x] 게임 종료 후 이름 입력
- [x] 이름 입력은 터미널이 아니라 pygame 창에서 처리
- [x] 저장 후 `Saved` 표시
- [x] `Retry` 버튼으로 다시 시작
- [ ] 결과 화면 UI 구현
- [ ] 수동 플레이 `game_runs` 저장 연결
- [ ] 랭킹 화면은 추후 구현

## 1단계: 준비

- [x] PostgreSQL DB `snake_game_bot` 생성
- [x] 사용자 직접 `players` 테이블 생성
- [x] `bot_configs`, `evaluation_sessions`, `game_runs` 스키마 초안 생성
- [x] `.env.example` 생성
- [x] PostgreSQL 연결 코드 생성
- [x] 저장 repository 코드 생성
- [x] DB 연결 테스트 스크립트 생성
- [x] 샘플 저장 테스트 스크립트 생성

## 2단계: 연결 확인

- [ ] `.env`에 실제 `DATABASE_URL` 작성
- [ ] `pip install "psycopg[binary]" python-dotenv`
- [ ] `db/schema.sql` 실행
- [ ] Python에서 DB 연결 확인
- [ ] 샘플 저장 테스트 실행
- [x] `stable_bot.evaluate --save-db` 1판 저장 테스트 실행

## 3단계: 게임 저장 연결

- [ ] 화면 플레이 종료 시 `game_runs` 저장
- [x] headless 평가 시 `evaluation_sessions` 생성
- [x] headless 평가 각 판을 `game_runs`에 저장
- [x] 평가 완료 후 `evaluation_sessions` 요약 업데이트

수동 화면 플레이 저장은 보류합니다. 플레이어 이름을 터미널이 아니라 pygame 실행창에서 입력받는 화면 구성을 먼저 논의한 뒤 구현합니다.

저장 테스트 결과:

```text
evaluation_sessions 1
game_runs 3
```

`game_runs` 3개는 이전 샘플 저장 2개와 headless 평가 저장 1개를 포함합니다.

## 4단계: 조회 기능

- [ ] 플레이어별 최고 점수 조회
- [ ] 봇 설정별 평가 결과 조회
- [ ] 랭킹 조회

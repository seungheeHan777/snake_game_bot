# GA Bot TODO

## DB 진행 규칙 (합의 반영)

- DB는 **지금 구현하지 않음**.
- 지금 단계는 `ga_bot/DB_PLAN.md`에 **초안만 유지**.
- DB 엔진/컬럼/인덱스는 추후 사용자와 상세 합의 후 확정.
- 구현 시작 조건: 100판 평가에서 `score=400` 달성률이 **80% 이상**일 때.

## 구조

- [x] GA 전용 폴더 생성
- [x] `policy.py` 생성
- [x] `simulation.py` 생성
- [x] `trainer.py` 생성
- [x] `storage.py` 생성
- [x] JSON/CSV 저장 구조 생성

## 정책 설계

- [x] 가중치 특징값 후보 목록 작성
- [x] 사용자와 특징값 목록 확정
- [x] `FEATURE_NAMES` 확정
- [x] `direction_features()` 구현 확정
- [x] weights/features 길이 일치 확인

## 저장/학습 확인

- [ ] `best_weights.json` 저장 확인
- [ ] `checkpoint.json` 이어 학습 확인
- [ ] `training_history.csv` 로그 확인
- [ ] 완료 기준 검증: 100판 반복 평가에서 `score=400` 달성률 80% 이상
- [ ] 학습 파라미터 조정
- [ ] 무한 루프/빙빙 도는 패턴 페널티 적용
: 방식은 최근 머리 좌표 반복 빈도 기반 감점
- [x] `ga_bot/tools/evaluate_model.py` 작성
: 고정된 best 모델 100판 반복 평가, `score=400` 달성률 출력

- [x] `ga_bot/tools/select_best_candidate.py` 작성
: `models/score400` 후보를 반복 평가해 최종 best 자동 선발

- [x] `ga_bot/tools/run_pipeline.py` 작성
: 평가/선발 과정을 한 번에 실행 (`--skip-train` 지원)

## 실행 연결

- [x] 학습 결과를 pygame 화면에서 확인하는 viewer 연결
- [x] 저장된 `best_weights.json`으로 실제 게임 실행
: 실행 파일 `snake_ga_play.py`

## DB 저장

- [ ] `DB_PLAN.md` 합의
- [ ] DB 스키마 확정 후 구현 시작

# GA Bot TODO

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
- [ ] 학습 파라미터 조정
- [ ] 무한 루프/빙빙 도는 패턴 감지 및 페널티 추가

## 실행 연결

- [ ] 학습 결과를 pygame 화면에서 확인하는 viewer 연결
- [ ] 저장된 `best_weights.json`으로 실제 게임 실행

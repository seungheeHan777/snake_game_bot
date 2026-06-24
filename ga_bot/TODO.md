# GA Bot TODO

## 현재 결론

- [x] GA 방식으로 `score=400` 단판 성공 사례 확인
- [x] 반복 평가에서 안정적인 `score=400` 재현 실패 확인
- [x] GA를 최종 안정 봇이 아닌 실험/비교 기준으로 유지 결정
- [x] 안정 완주 작업은 `stable_bot/`으로 이관

## 구조

- [x] GA 전용 폴더 생성
- [x] `policy.py` 생성
- [x] `simulation.py` 생성
- [x] `trainer.py` 생성
- [x] `storage.py` 생성
- [x] JSON/CSV 저장 구조 생성
- [x] 보조 검증 스크립트를 `ga_bot/tools/`로 정리

## 정책 설계

- [x] 가중치 특징값 후보 목록 작성
- [x] 사용자와 특징값 목록 논의
- [x] `FEATURE_NAMES` 확정
- [x] `direction_features()` 구현
- [x] weights/features 길이 불일치 방어 처리
- [x] sample preset 추가
- [x] 열린 공간/꼬리 탈출 계열 feature 개선 방향 기록

## 저장/학습 산출물

- [x] `best_weights.json` 저장 확인
- [x] `checkpoint.json` 이어 학습 구조 확인
- [x] `training_history.csv` 로그 확인
- [x] `models/score400/` 후보 보관 확인
- [x] `ga_bot/tools/evaluate_model.py` 작성
- [x] `ga_bot/tools/select_best_candidate.py` 작성
- [x] `ga_bot/tools/run_pipeline.py` 작성

## 실행 연결

- [x] 학습 실행 파일 `snake_ga_bot.py` 유지
- [x] 저장된 `best_weights.json`으로 화면 플레이 실행
- [x] 화면 플레이 실행 파일 `snake_ga_play.py` 유지

## 평가 결과

- [x] 단판 기준 `score=400` 후보 다수 생성
- [x] 반복 평가 성공률이 최종 목표에 부족함 확인
- [x] GA 결과를 `stable_bot`과 비교하는 baseline으로 유지
- [ ] 새 GA 설계를 재개할 경우 feature/fitness/selection 설계부터 재논의

## DB 저장

- [x] `DB_PLAN.md` 초안 작성
- [x] GA DB 구현은 보류하기로 결정
- [ ] GA DB 저장을 재개할 경우 사용자와 스키마/컬럼/인덱스 재합의

## 보류 작업

- [ ] GA를 다시 메인 후보로 올릴지 결정
- [ ] 새 GA 모델을 설계한다면 현재 6-feature 구조를 폐기할지 검토
- [ ] 새 fitness 기준을 설계한다면 반복 평가 성공률 중심으로 재설계

## 참고 명령

학습 실행:

```powershell
py -3 snake_ga_bot.py
```

저장된 모델 화면 확인:

```powershell
py -3 snake_ga_play.py
```

반복 평가:

```powershell
py -3 ga_bot/tools/evaluate_model.py --runs 100
```

후보 선발:

```powershell
py -3 ga_bot/tools/select_best_candidate.py --runs 100 --include-current-best
```

파이프라인:

```powershell
py -3 ga_bot/tools/run_pipeline.py --skip-train --runs 100
```

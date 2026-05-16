# GA Bot DB Plan

이 문서는 게임 결과 저장 DB 기능의 설계 합의 문서입니다.

## 범위

- 이 단계에서는 구현하지 않고 스키마와 저장 정책만 합의합니다.
- 구현 시작 조건은 스키마 확정입니다.

## 저장 목적

- 학습/평가 결과의 재현성과 비교 가능성 확보
- 모델 버전별 성능 추적
- 완료 기준(`score=400` 달성률 80% 이상) 검증 기록

## 권장 저장소

- 1차: SQLite (`ga_bot/results.db`)
- 이유:
  - 로컬 개발에서 설정이 가장 단순함
  - CSV보다 조회/집계가 쉬움
  - 외부 서버 없이 바로 사용 가능

## 초안 스키마

`models`

- `id` INTEGER PRIMARY KEY
- `created_at` TEXT
- `source` TEXT
: `train`, `manual`, `import`
- `generation` INTEGER
- `weights_json` TEXT
- `feature_names_json` TEXT
- `score_metric` TEXT
: `snake_length` 등

`runs`

- `id` INTEGER PRIMARY KEY
- `model_id` INTEGER
- `created_at` TEXT
- `mode` TEXT
: `train_eval`, `benchmark`, `playback`
- `seed` INTEGER NULL
- `score` INTEGER
- `steps` INTEGER
- `fitness` REAL
- `reached_max_score` INTEGER
: 0 또는 1
- `notes` TEXT NULL

`batches`

- `id` INTEGER PRIMARY KEY
- `created_at` TEXT
- `model_id` INTEGER
- `run_count` INTEGER
- `max_score` INTEGER
- `avg_score` REAL
- `max_steps` INTEGER
- `avg_steps` REAL
- `score_400_rate` REAL

## 저장 정책

- 학습 중:
  - 세대 요약은 기존 CSV 유지
  - 필요 시 `batches`에 세대별 요약 저장
- 반복 평가:
  - 각 판 결과를 `runs`에 저장
  - 100판 단위 요약을 `batches`에 저장
- 모델 갱신:
  - `best_weights.json` 저장 시점에 `models`에 스냅샷 추가

## 합의 필요 항목

1. `score` 기준 확정
: 현재는 뱀 길이(최대 400)
2. `seed` 정책
: 완전 랜덤/고정 seed/혼합
3. 보관 기간
: 모든 run 저장 vs 최근 N개만 저장
4. 모델 버전 규칙
: generation 기준 vs 해시 기준

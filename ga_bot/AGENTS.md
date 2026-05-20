# AGENTS.md

## 목적

이 폴더는 유전 알고리즘 기반 스네이크 봇을 관리합니다.

## 작업 규칙

- `policy.py`는 학습된 가중치로 방향을 선택하는 정책만 담당합니다.
- `trainer.py`는 개체 생성, 평가, 선택, 교차, 변이, 세대 반복을 담당합니다.
- `simulation.py`는 pygame 없이 게임을 빠르게 계산하는 시뮬레이션만 담당합니다.
- `storage.py`는 JSON/CSV 저장과 불러오기만 담당합니다.
- 가중치 특징값을 바꾸기 전에는 사용자와 먼저 논의합니다.
- 학습 결과 파일은 `models/`, 학습 로그는 `logs/`에 저장합니다.

## tools 폴더 규칙

- `tools/`는 학습 코어가 아니라 보조 실행 스크립트 모음입니다.
- `tools/evaluate_model.py`: 단일 모델 반복 평가
- `tools/select_best_candidate.py`: score400 후보 자동 선발
- `tools/run_pipeline.py`: 평가/선발 파이프라인 실행
- 학습 시작은 항상 루트의 `snake_ga_bot.py`를 사용합니다.

## 저장 파일

- `models/best_weights.json`: 현재까지 가장 좋은 개체입니다.
- `models/checkpoint.json`: 중간부터 다시 학습하기 위한 population 저장 파일입니다.
- `logs/training_history.csv`: 세대별 학습 기록입니다.

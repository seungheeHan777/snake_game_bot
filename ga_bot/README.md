# GA Bot

## 현재 역할

`ga_bot/`은 더 이상 최종 안정 완주 봇의 메인 작업 공간이 아닙니다.

반복 평가 결과, 현재 GA 모델은 가끔 높은 점수 또는 `score=400`을 만들 수 있지만, 같은 모델을 여러 판 돌렸을 때 안정적으로 400점을 재현하지 못했습니다. 따라서 이 폴더는 다음 역할로 유지합니다.

- 학습형 봇 실험
- 기존 GA 결과 보관
- 새 `stable_bot/`과 비교할 baseline
- feature, fitness, mutation 등 실험 기록

안정적인 완주 봇 구현은 루트의 `stable_bot/` 폴더에서 진행합니다.

## 2026-05-20 정리된 실행 구조

실행 진입점은 아래 2개만 사용합니다.

1. 학습 실행: `snake_ga_bot.py`
2. 학습된 모델 플레이 확인: `snake_ga_play.py`

보조 실행 스크립트는 `ga_bot/tools/`로 이동했습니다.

- `ga_bot/tools/evaluate_model.py`: 단일 모델 반복 평가
- `ga_bot/tools/select_best_candidate.py`: `models/score400` 후보 자동 선발
- `ga_bot/tools/run_pipeline.py`: 평가/선발 파이프라인 실행

예시:

```powershell
py -3 ga_bot/tools/run_pipeline.py --skip-train --runs 100
```

이 폴더는 유전 알고리즘 기반 스네이크 봇을 관리합니다.

## 파일 구조

- `policy.py`: 가중치로 방향을 평가하고 선택합니다.
- `simulation.py`: pygame 화면 없이 스네이크 한 판을 계산으로 실행합니다.
- `trainer.py`: 세대 평가, 선택, 교차, 변이, 학습 루프를 담당합니다.
- `storage.py`: 최고 모델, checkpoint, 학습 로그를 저장하고 불러옵니다.
- `models/`: `best_weights.json`, `checkpoint.json` 저장 위치입니다.
- `logs/`: `training_history.csv` 저장 위치입니다.

## 실행

```powershell
python snake_ga_bot.py
```

학습된 최고 모델을 게임 화면으로 확인:

```powershell
python snake_ga_play.py
```

반복 평가(예정):

```powershell
py -3 ga_bot/tools/evaluate_model.py --runs 100
```

후보 자동 선발:

```powershell
py -3 ga_bot/tools/select_best_candidate.py --runs 100 --include-current-best
```

한 번에 평가/선발:

```powershell
py -3 ga_bot/tools/run_pipeline.py --skip-train --runs 100
```

## 설계 기록

GA 봇의 점수 정체 원인, feature 개선 방향, 열린 공간과 꼬리 탈출 개념은 `DESIGN_NOTES.md`에 기록합니다.

DB 저장 설계 초안은 `DB_PLAN.md`에 기록합니다.

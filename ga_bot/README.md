# GA Bot

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
python ga_bot/evaluate_model.py
```

## 설계 기록

GA 봇의 점수 정체 원인, feature 개선 방향, 열린 공간과 꼬리 탈출 개념은 `DESIGN_NOTES.md`에 기록합니다.

DB 저장 설계 초안은 `DB_PLAN.md`에 기록합니다.

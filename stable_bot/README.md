# Stable Bot

## 현재 역할

`stable_bot/`은 유전 알고리즘 방식의 한계를 보완하기 위해 추가로 개발한 안정 완주 봇입니다.

기존 `ga_bot/`은 `score=400`을 달성한 모델이 있었지만, 반복 평가에서 성공률이 안정적이지 않았습니다. 그래서 `stable_bot/`은 학습된 가중치에 의존하지 않고, 결정론적 안전 경로를 기반으로 설계했습니다.

핵심 전략:

- Hamiltonian fallback 경로로 죽지 않는 기본 경로 확보
- 안전 조건을 통과한 shortcut만 사용
- shortcut 계산은 백그라운드에서 처리해 게임 루프 지연 방지

현재 결과:

```text
100판 평가
success=100/100
score=400 전부 성공
```

## 100판 최종 평가

현재 기본 설정:

```text
mode=stable
shortcut_distance=4
```

100판 평가 결과:

```text
runs=100
success=100/100 (100.0%)
score=avg:400.00 min:400 max:400
steps=avg:39770.29 min:36179 max:42322
elapsed_seconds=175.073
```

목표 기준은 100판 중 80판 이상 `score=400`이었고, 현재 결과는 100판 모두 성공입니다.

화면 플레이 확인:

```powershell
py -3 snake_stable_bot.py
```

## DB 저장

headless 평가는 DB 저장을 지원합니다.

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable --save-db
```

저장 대상:

```text
evaluation_sessions
game_runs
bot_configs
```

화면 플레이 저장은 아직 구현하지 않았습니다. 수동 플레이어 이름은 터미널이 아니라 pygame 실행창에서 입력받는 방식으로 진행할 예정이며, 화면 구성 논의 후 구현합니다.

## 반복 평가 실행

`stable_bot/evaluate.py`는 화면 없이 여러 판을 자동 실행해서 성공률과 평균 steps를 확인하는 스크립트입니다.

```powershell
py -3 -m stable_bot.evaluate --runs 30
py -3 -m stable_bot.evaluate --runs 30 --mode fallback
py -3 -m stable_bot.evaluate --runs 30 --shortcut-distance 12
```

모드:

- `stable`: safe shortcut을 먼저 시도하고, 실패하면 Hamiltonian fallback 사용
- `fallback`: Hamiltonian fallback만 사용

출력:

- 성공 횟수와 성공률
- 평균/최소/최대 score
- 평균/최소/최대 steps

## Shortcut 계산 지연 개선

초기 `stable` 구조에서는 `choose_direction()` 안에서 shortcut 탐색과 safety 검사를 직접 실행했습니다. 이 방식은 계산이 끝날 때까지 게임 루프가 기다리기 때문에, 화면 플레이 중 순간적으로 멈추는 딜레이가 생길 수 있었습니다.

현재 구조는 이 문제를 줄이기 위해 shortcut 계산을 백그라운드 thread로 분리했습니다.

```text
계산된 shortcut 있음 -> shortcut 방향 사용
계산된 shortcut 없음 -> 즉시 Hamiltonian fallback 방향 사용
shortcut 계산 -> 백그라운드에서 수행
```

또한 같은 먹이 위치에 대해서는 shortcut 계산을 한 번만 수행합니다. 따라서 shortcut 계산 중에도 게임은 멈추지 않고 fallback 경로로 계속 이동합니다.

30판 평가 기준:

```text
fallback: 44.262s
기존 stable sync: 226.678s
현재 stable async: 53.441s
```

결론: 기존 stable의 계산 지연 문제는 비동기 shortcut 구조로 개선했습니다.

## Shortcut 거리 기준

shortcut은 먹이가 가까울 때만 계산합니다. 너무 멀리 있는 먹이까지 매번 shortcut 후보로 보면 계산량이 늘지만, 실제 평균 steps가 좋아지지 않을 수 있습니다.

30판 비교 결과:

```text
distance=4
success=30/30
avg_steps=39645.00
elapsed=50.864s

distance=8
success=30/30
avg_steps=40056.70
elapsed=52.623s

distance=12
success=30/30
avg_steps=39986.23
elapsed=56.496s
```

현재 기본값은 `4`입니다. 30판 기준으로 성공률은 모두 같았고, `4`가 평균 steps와 실행 시간 모두 가장 좋았습니다.

`stable_bot/`은 유전 알고리즘이 아니라, 안정적인 완주를 목표로 하는 결정론적 봇 작업 공간입니다.

현재 `ga_bot/`은 가끔 높은 점수나 `score=400`을 만들 수 있지만, 같은 모델을 여러 번 평가하면 성공률이 낮습니다. 즉, 지금 구조의 GA는 "운 좋게 잘 된 한 판"은 만들 수 있어도, 프로젝트 목표인 "반복해서 안정적으로 400점"을 보장하기 어렵습니다.

## 목표

- 대상 보드: 현재 20x20 보드
- 목표 점수: `score=400`
- 성공 기준: 100판 반복 평가에서 `score=400` 성공률 80% 이상
- 최종 방향: 가능한 한 결정론적으로 완주하는 봇

## 이 폴더를 만든 이유

`ga_bot/`은 계속 보관합니다. 다만 역할을 변경합니다.

- 기존 역할: 최종 완주 봇 후보
- 변경된 역할: 학습형 봇 실험, 비교 기준, 기록 보관

GA 방식의 현재 한계는 다음과 같습니다.

- 한 번 잘한 모델이 반복 평가에서 똑같이 잘하지 못합니다.
- 현재 6개 feature만으로는 장기 생존 전략을 충분히 표현하기 어렵습니다.
- 먹이 위치가 랜덤이라 운 좋은 한 판이 좋은 모델처럼 보일 수 있습니다.
- 뱀이 길어질수록 "먹이에 가까워지는 방향"보다 "죽지 않고 전체 보드를 채우는 경로"가 더 중요합니다.

## 계획된 구조

- `README.md`: 이 폴더의 목적과 방향
- `TODO.md`: 구현 체크리스트
- `DESIGN_NOTES.md`: 알고리즘 설계 기록
- `AGENTS.md`: 이 폴더 전용 작업 규칙

현재 코드:

- `hamiltonian.py`: 보드 전체를 순회하는 안전 fallback 경로 생성
- `safety.py`: 충돌, 꼬리 도달 가능성, 열린 공간 검사
- `shortcut.py`: 먹이까지의 짧은 경로를 찾고, 안전할 때만 허용
- `planner.py`: safe shortcut을 먼저 시도하고 실패하면 Hamiltonian fallback 선택
- `snake_stable_bot.py`: 루트에 있는 stable bot 화면 실행 파일

추가 예정 코드:

- `runner.py`: 필요 시 stable bot 전용 평가 진입점

## 실행

화면으로 stable bot을 확인하려면 루트 폴더에서 실행합니다.

```powershell
py -3 snake_stable_bot.py
```

현재 버전은 safe shortcut을 먼저 시도하고, 안전하지 않으면 Hamiltonian fallback을 사용합니다.

## 기본 전략

1. Hamiltonian cycle 또는 그에 가까운 전체 보드 순회 경로를 기본 fallback으로 둡니다.
2. 먹이로 가는 빠른 길이 있으면 바로 가지 않고, 먼저 안전성을 검사합니다.
3. shortcut은 이후에도 꼬리나 fallback 경로로 다시 연결될 수 있을 때만 허용합니다.
4. 안전한 shortcut이 없으면 fallback 경로를 따라갑니다.

이 방식은 greedy BFS보다 느릴 수 있지만, 최종 목표인 안정적인 400점에는 더 적합합니다.

## 1차 검증 결과

Hamiltonian fallback만 사용하는 headless 검증에서 다음 결과를 확인했습니다.

```text
score 400
dead False
victory True
```

이 결과는 "정해진 순환 경로만 따라가도 완주 가능하다"는 기본 구조 검증입니다. 다음 단계는 속도를 높이기 위한 safe shortcut입니다.

## 2차 검증 결과

`safety.py`를 추가한 뒤에도 Hamiltonian fallback 완주는 유지됩니다.

```text
score 400
dead False
victory True
```

현재 safety 검사는 shortcut 구현 전 공통 기반입니다.

## 3차 구현 결과

`shortcut.py`를 추가했습니다.

현재 shortcut 조건:

- 먹이까지의 짧은 경로가 존재해야 합니다.
- 경로를 따라가는 중 벽이나 몸통에 부딪히면 안 됩니다.
- 먹이를 먹은 뒤에도 머리에서 꼬리까지 갈 수 있어야 합니다.
- 먹이를 먹은 뒤 열린 공간이 현재 뱀 길이 이상이어야 합니다.
- 성능 문제를 줄이기 위해 먹이가 8칸 이내일 때만 shortcut을 시도합니다.

조건을 통과하지 못하면 shortcut을 쓰지 않고 Hamiltonian fallback을 따릅니다.

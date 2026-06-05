# Stable Bot Design Notes

## 100판 최종 평가

기본 설정:

```text
mode=stable
shortcut_distance=4
```

결과:

```text
runs=100
success=100/100 (100.0%)
avg_score=400.00
min_score=400
max_score=400
avg_steps=39770.29
min_steps=36179
max_steps=42322
elapsed_seconds=175.073
```

판정:

```text
100판 중 score=400 성공률 80% 이상 기준 통과
```

다음 판단은 화면 플레이 확인 후 진행합니다.

## 반복 평가 설계

`evaluate.py`는 stable bot을 화면 없이 여러 번 실행해서 단판 운을 줄이고 평균 성능을 확인하기 위한 도구입니다.

비교 모드:

```text
fallback: Hamiltonian fallback만 사용
stable: safe shortcut을 먼저 시도하고 실패하면 fallback 사용
```

실행 예시:

```powershell
py -3 -m stable_bot.evaluate --runs 30
py -3 -m stable_bot.evaluate --runs 30 --mode fallback
py -3 -m stable_bot.evaluate --runs 30 --shortcut-distance 12
```

평가 기준:

- `success_count`: `score=400`으로 끝난 판 수
- `success_rate`: 성공률
- `avg_score`: 평균 점수
- `avg_steps`: 평균 이동 횟수

다음 판단은 fallback only와 shortcut 포함 버전의 평균 steps를 비교해서 진행합니다.

1판 동작 확인 결과:

```text
fallback:
success=1/1
score=400
steps=40414

stable:
success=1/1
score=400
steps=37900
```

단, `stable` 모드는 shortcut 안전 검사를 추가로 수행하므로 실행 시간이 더 깁니다. 최종 판단은 30판 이상 반복 평가로 해야 합니다.

30판 평가 결과:

```text
fallback:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=39833.53
elapsed_seconds=44.262
approx_time_per_step=0.037 ms

stable:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=39868.23
elapsed_seconds=226.678
approx_time_per_step=0.190 ms
```

현재 shortcut은 성공률을 떨어뜨리지는 않았지만, 평균 steps를 개선하지 못했고 실행 시간은 약 5배 증가했습니다. 따라서 다음 개선 방향은 shortcut 자체를 더 빠르게 하거나, shortcut을 더 엄격하게 제한하는 것입니다.

## 비동기 Shortcut 계산

게임 루프에서 shortcut 안전 검사를 직접 실행하면 방향 결정이 끝날 때까지 게임이 멈출 수 있습니다. 이 구조는 화면 플레이에 적합하지 않습니다.

수정한 구조:

```text
매 이동:
1. 이미 계산된 shortcut 경로가 있으면 한 칸 이동
2. 없으면 즉시 Hamiltonian fallback 방향 반환
3. shortcut 계산은 백그라운드 thread에서 수행
4. 같은 먹이에 대해서는 shortcut 계산을 한 번만 수행
```

이 구조에서는 shortcut 계산 중에도 게임은 fallback 경로로 계속 움직입니다. 계산이 끝난 뒤에도 먹이 위치가 그대로이고 경로가 남아 있으면 shortcut을 사용합니다.

30판 재평가 결과:

```text
stable async:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=39601.03
elapsed_seconds=53.441
approx_time_per_step=0.045 ms
```

비교:

```text
fallback: 44.262s, approx 0.037 ms/step
old stable sync: 226.678s, approx 0.190 ms/step
new stable async: 53.441s, approx 0.045 ms/step
```

결론: 비동기 + 먹이당 1회 계산 제한으로 게임 루프 지연 문제를 크게 줄였습니다.

## Shortcut 거리 비교

shortcut 계산 거리 기준을 4/8/12로 비교했습니다.

```text
distance=4:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=39645.00
elapsed_seconds=50.864

distance=8:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=40056.70
elapsed_seconds=52.623

distance=12:
success=30/30 (100.0%)
avg_score=400.00
avg_steps=39986.23
elapsed_seconds=56.496
```

결론:

- 성공률은 세 기준 모두 100%였습니다.
- 평균 steps는 `4`가 가장 낮았습니다.
- 실행 시간도 `4`가 가장 짧았습니다.

따라서 현재 기본 shortcut 거리 기준은 `4`로 낮춥니다.

## 현재 결정

유전 알고리즘 트랙은 삭제하지 않습니다. `ga_bot/`은 실험과 비교 기준으로 유지합니다.

다만 프로젝트의 핵심 목표는 안정적인 완주입니다. 현재 GA 모델은 학습 중 `score=400`을 찍은 적이 있지만, 반복 평가에서는 성공률이 낮았습니다. 따라서 이 모델을 최종 봇으로 보기 어렵습니다.

`stable_bot/`은 결정론적 계획 알고리즘으로 안정 완주를 목표로 합니다.

## 핵심 아이디어

봇의 우선순위는 다음 순서입니다.

1. 죽지 않는다.
2. 보드 전체를 채울 수 있는 안전 구조를 유지한다.
3. 안전할 때만 먹이를 빠르게 먹는다.

기본 구조:

```text
안전 fallback 경로 + 조건부 shortcut
```

fallback 경로는 뱀이 스스로 갇히지 않고 계속 이동할 수 있는 기본 경로입니다. 현재 가장 유력한 방식은 Hamiltonian cycle 기반 경로입니다.

## Hamiltonian Fallback

Hamiltonian cycle은 보드의 모든 칸을 정확히 한 번씩 지나고 다시 시작점으로 돌아오는 경로입니다.

스네이크 게임에서 이 방식이 유리한 이유:

- 뱀이 계속 같은 순환 경로를 따라가면 자기 몸과 충돌할 가능성이 크게 줄어듭니다.
- 먹이가 어디에 생겨도 언젠가는 머리가 그 칸에 도달합니다.
- 몸통도 같은 경로를 따라오기 때문에 전체 흐름이 예측 가능합니다.
- 후반부에 흔한 자기 고립 문제를 줄일 수 있습니다.

단점:

- 먹이까지 먼 길을 돌아갈 수 있어서 느립니다.
- 보드는 안정적으로 채우지만, 효율적인 최단 경로 봇은 아닙니다.

## 1차 구현 결과

`hamiltonian.py`에서 현재 20x20 보드의 400칸을 모두 한 번씩 지나는 순환 경로를 생성했습니다.

경로 구조:

1. 맨 위 행을 왼쪽에서 오른쪽으로 이동합니다.
2. 첫 번째 열을 비워둔 채, 나머지 행을 지그재그로 순회합니다.
3. 마지막에 첫 번째 열을 아래에서 위로 올라오며 시작점 근처로 돌아옵니다.

이 구조는 마지막 칸 `(0, 1)`이 시작 칸 `(0, 0)`과 인접하므로 순환 경로로 사용할 수 있습니다.

headless 검증 결과:

```text
cycle length: 400
cycle valid: True
score: 400
dead: False
victory: True
```

현재 `planner.py`는 먹이 위치를 사용하지 않고 Hamiltonian fallback만 따라갑니다. 따라서 안정성은 높지만 속도는 느릴 수 있습니다.

## Safety 모듈

`safety.py`는 shortcut을 붙이기 전에 필요한 공통 안전 검사를 분리한 파일입니다.

현재 포함된 검사:

- 한 칸 이동했을 때 벽에 부딪히는지
- 한 칸 이동했을 때 몸통에 부딪히는지
- 현재 방향 기준으로 바로 반대 방향 이동인지
- 이동 후 머리에서 꼬리까지 다시 갈 수 있는지
- 이동 후 머리에서 도달 가능한 열린 공간이 뱀 길이보다 충분한지

이 검사는 다음 단계의 safe shortcut에서 사용합니다.

초기 상태 검증 결과:

```text
direction: R
is_safe_candidate: True
can_reach_tail_after_move: True
open_space_after_move: 398
```

safety 분리 후에도 Hamiltonian fallback headless 완주 결과는 유지됩니다.

```text
score 400
dead False
victory True
```

## Safe Shortcut 1차 구현

`shortcut.py`는 먹이까지의 짧은 경로를 BFS로 찾습니다.

현재 shortcut 허용 조건:

1. 먹이까지 경로가 있어야 합니다.
2. 경로를 따라 이동하는 동안 벽과 몸통에 부딪히면 안 됩니다.
3. 먹이를 먹은 뒤 머리에서 꼬리까지 다시 갈 수 있어야 합니다.
4. 먹이를 먹은 뒤 머리에서 도달 가능한 열린 공간이 뱀 길이 이상이어야 합니다.

`planner.py`의 선택 순서:

```text
safe shortcut 가능 -> shortcut 방향
safe shortcut 불가 -> Hamiltonian fallback 방향
```

이 shortcut은 아직 보수적입니다. 현재 몸통을 기준으로 정적인 BFS를 사용하므로, 꼬리가 이동하면서 생기는 미래 공간을 적극적으로 활용하지는 않습니다. 대신 안정성을 우선합니다.

성능 제한:

- 매 이동마다 전체 shortcut BFS를 돌리면 느립니다.
- 현재는 먹이와 머리의 Manhattan 거리가 8칸 이하일 때만 shortcut을 시도합니다.
- 거리가 멀면 바로 Hamiltonian fallback을 사용합니다.

1차 shortcut 포함 headless 검증:

```text
score 400
steps 41104
dead False
victory True
```

한 판의 `steps`는 먹이 랜덤 배치에 크게 영향을 받으므로, 속도 개선 여부는 반복 평가 스크립트를 만든 뒤 평균으로 판단해야 합니다.

## Safe Shortcut

속도를 높이기 위해 먹이로 가는 shortcut을 허용할 수 있습니다.

단, shortcut은 아래 조건을 만족할 때만 사용합니다.

- 다음 이동이 벽에 부딪히지 않는다.
- 다음 이동이 몸통에 부딪히지 않는다.
- shortcut 이후에도 머리가 꼬리 또는 fallback 경로에 다시 연결될 수 있다.
- 남은 공간이 너무 작게 분리되어 뱀이 갇히지 않는다.

조건을 만족하지 않으면 먹이가 가까워도 shortcut을 포기하고 fallback 경로를 따릅니다.

## 성공 기준

최종 성공 기준은 한 번의 최고 점수가 아닙니다.

```text
100판 반복 평가
score=400 성공률 80% 이상
```

이 기준을 넘은 뒤에 DB 저장 기능을 본격적으로 논의합니다.

## GA와의 관계

GA는 계속 유지합니다.

GA의 역할:

- baseline 비교
- feature와 fitness 실험 기록
- 실패 사례 분석
- 학습형 접근법의 한계 확인

하지만 안정적인 최종 완주 봇은 `stable_bot/`에서 진행합니다.

# Database

## 수동 플레이 저장 계획

수동 플레이 결과도 `game_runs`에 저장합니다.

저장 방식:

```text
actor_type = player
run_type = screen
player_id = players.id
bot_config_id = null
evaluation_session_id = null
```

결과 화면:

```text
Game Over 또는 Win
Score
Name input
[Save]
[Retry]
```

`Save`를 누르면:

```text
1. players에서 display_name 기준 get-or-create
2. game_runs에 수동 플레이 결과 저장
3. Saved 표시
```

`Retry`를 누르면:

```text
DB 저장 없이 새 게임 시작
```

랭킹 화면은 장기 목표로 분리합니다.

PostgreSQL에 게임 결과를 저장하기 위한 DB 작업 공간입니다.

## 역할 분리

사용자가 직접 만들 테이블:

```text
players
```

Codex가 관리하는 테이블:

```text
bot_configs
evaluation_sessions
game_runs
```

## players 테이블 요구 조건

`db/schema.sql`은 `players` 테이블이 이미 존재한다고 가정합니다.

최소 요구 컬럼:

```sql
CREATE TABLE players (
    id BIGSERIAL PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    username TEXT UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

처음에는 `display_name`만 사용해도 됩니다. 로그인 기능은 아직 구현하지 않습니다.

## 테이블 구조

### bot_configs

봇 설정값을 저장합니다.

예:

```text
stable bot, shortcut_distance=4
fallback only
GA weights
```

### evaluation_sessions

30판, 100판처럼 여러 게임을 묶은 평가 단위입니다.

예:

```text
stable bot 100판 평가
fallback 30판 평가
```

### game_runs

실제 한 판 결과를 저장합니다.

사람 플레이와 봇 플레이를 모두 저장합니다.

```text
actor_type = player / bot
run_type = screen / headless
```

## 연결 설정

루트에 `.env` 파일을 만들고 실제 접속 정보를 넣습니다.

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/snake_game_bot
```

`.env`는 GitHub에 올리지 않습니다.

## 필요한 패키지

```powershell
pip install "psycopg[binary]" python-dotenv
```

## 스키마 적용

`players` 테이블을 먼저 만든 뒤 `db/schema.sql`을 실행합니다.

DBeaver에서 실행하거나, `psql`을 사용할 수 있습니다.

```powershell
psql "postgresql://postgres:YOUR_PASSWORD@localhost:5432/snake_game_bot" -f db/schema.sql
```

## 연결 테스트

루트에 `.env`를 만든 뒤 실행합니다.

```powershell
py -3 -m db.test_connection
```

정상 출력 예:

```text
db connected: snake_game_bot
```

## 샘플 저장 테스트

`players` 테이블과 `db/schema.sql` 테이블이 모두 생성된 뒤 실행합니다.

```powershell
py -3 -m db.insert_sample
```

정상 실행되면 `players`, `bot_configs`, `game_runs`에 샘플 데이터가 들어갑니다.

## Headless 평가 저장

`stable_bot.evaluate`는 `--save-db` 옵션으로 평가 결과를 DB에 저장할 수 있습니다.

```powershell
py -3 -m stable_bot.evaluate --runs 30 --mode stable --save-db
```

저장 방식:

```text
evaluation_sessions 1개 생성
game_runs 30개 생성
evaluation_sessions에 요약 결과 업데이트
```

수동 화면 플레이 저장은 아직 구현하지 않았습니다. 플레이어 이름을 pygame 실행창에서 입력받는 화면 구성을 먼저 논의한 뒤 진행합니다.

저장 테스트 완료:

```text
py -3 -m stable_bot.evaluate --runs 1 --mode stable --save-db --memo "db save smoke test"
saved evaluation_session_id=1
```

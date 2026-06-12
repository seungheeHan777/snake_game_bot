-- PostgreSQL schema for snake_game_bot.
-- Prerequisite: create the players table first.
--
-- Expected players table:
-- CREATE TABLE players (
--     id BIGSERIAL PRIMARY KEY,
--     display_name TEXT NOT NULL UNIQUE,
--     username TEXT UNIQUE,
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

CREATE TABLE IF NOT EXISTS bot_configs (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT,
    algorithm_type TEXT NOT NULL,
    shortcut_distance INTEGER,
    uses_shortcut BOOLEAN NOT NULL DEFAULT FALSE,
    uses_hamiltonian BOOLEAN NOT NULL DEFAULT FALSE,
    settings_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT bot_configs_algorithm_type_check
        CHECK (algorithm_type IN ('stable', 'fallback', 'ga', 'bfs', 'manual'))
);

CREATE TABLE IF NOT EXISTS evaluation_sessions (
    id BIGSERIAL PRIMARY KEY,
    bot_config_id BIGINT REFERENCES bot_configs(id) ON DELETE SET NULL,
    run_type TEXT NOT NULL,
    planned_runs INTEGER NOT NULL,
    success_count INTEGER,
    success_rate NUMERIC(6, 5),
    avg_score NUMERIC(10, 2),
    min_score INTEGER,
    max_score INTEGER,
    avg_steps NUMERIC(12, 2),
    min_steps INTEGER,
    max_steps INTEGER,
    elapsed_seconds NUMERIC(12, 3),
    memo TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT evaluation_sessions_run_type_check
        CHECK (run_type IN ('headless', 'screen'))
);

CREATE TABLE IF NOT EXISTS game_runs (
    id BIGSERIAL PRIMARY KEY,
    evaluation_session_id BIGINT REFERENCES evaluation_sessions(id) ON DELETE SET NULL,
    bot_config_id BIGINT REFERENCES bot_configs(id) ON DELETE SET NULL,
    player_id BIGINT REFERENCES players(id) ON DELETE SET NULL,
    actor_type TEXT NOT NULL,
    run_type TEXT NOT NULL,
    game_index INTEGER,
    score INTEGER NOT NULL,
    steps INTEGER NOT NULL,
    success BOOLEAN NOT NULL,
    dead BOOLEAN NOT NULL DEFAULT FALSE,
    victory BOOLEAN NOT NULL DEFAULT FALSE,
    elapsed_seconds NUMERIC(12, 3),
    final_reason TEXT NOT NULL,
    shortcut_distance INTEGER,
    shortcut_used_count INTEGER,
    fallback_used_count INTEGER,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT game_runs_actor_type_check
        CHECK (actor_type IN ('player', 'bot')),
    CONSTRAINT game_runs_run_type_check
        CHECK (run_type IN ('headless', 'screen')),
    CONSTRAINT game_runs_final_reason_check
        CHECK (final_reason IN ('victory', 'game_over', 'max_steps', 'user_quit', 'unknown')),
    CONSTRAINT game_runs_actor_reference_check
        CHECK (
            (actor_type = 'player' AND player_id IS NOT NULL)
            OR
            (actor_type = 'bot' AND bot_config_id IS NOT NULL)
        )
);

CREATE INDEX IF NOT EXISTS idx_game_runs_player_score
    ON game_runs (player_id, score DESC, steps ASC);

CREATE INDEX IF NOT EXISTS idx_game_runs_bot_config
    ON game_runs (bot_config_id);

CREATE INDEX IF NOT EXISTS idx_game_runs_evaluation_session
    ON game_runs (evaluation_session_id);

CREATE INDEX IF NOT EXISTS idx_evaluation_sessions_bot_config
    ON evaluation_sessions (bot_config_id);

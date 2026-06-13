"""Database write helpers for snake game results."""

from db.connection import connect


def get_or_create_player(display_name, username=None):
    """Return an existing player id or create one."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO players (display_name, username)
                VALUES (%s, %s)
                ON CONFLICT (display_name)
                DO UPDATE SET display_name = EXCLUDED.display_name
                RETURNING id
                """,
                (display_name, username),
            )
            return cur.fetchone()[0]


def get_or_create_bot_config(
    name,
    algorithm_type,
    version=None,
    shortcut_distance=None,
    uses_shortcut=False,
    uses_hamiltonian=False,
    settings_json=None,
):
    """Return an existing matching bot config id or create one."""
    settings_json = settings_json or {}
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM bot_configs
                WHERE name = %s
                  AND algorithm_type = %s
                  AND COALESCE(version, '') = COALESCE(%s, '')
                  AND COALESCE(shortcut_distance, -1) = COALESCE(%s, -1)
                  AND uses_shortcut = %s
                  AND uses_hamiltonian = %s
                  AND settings_json = %s::jsonb
                LIMIT 1
                """,
                (
                    name,
                    algorithm_type,
                    version,
                    shortcut_distance,
                    uses_shortcut,
                    uses_hamiltonian,
                    psycopg_json(settings_json),
                ),
            )
            row = cur.fetchone()
            if row:
                return row[0]

            cur.execute(
                """
                INSERT INTO bot_configs (
                    name,
                    version,
                    algorithm_type,
                    shortcut_distance,
                    uses_shortcut,
                    uses_hamiltonian,
                    settings_json
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                RETURNING id
                """,
                (
                    name,
                    version,
                    algorithm_type,
                    shortcut_distance,
                    uses_shortcut,
                    uses_hamiltonian,
                    psycopg_json(settings_json),
                ),
            )
            return cur.fetchone()[0]


def create_evaluation_session(
    bot_config_id,
    run_type,
    planned_runs,
    memo=None,
):
    """Create an evaluation session and return its id."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO evaluation_sessions (
                    bot_config_id,
                    run_type,
                    planned_runs,
                    memo
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (bot_config_id, run_type, planned_runs, memo),
            )
            return cur.fetchone()[0]


def update_evaluation_session_summary(
    session_id,
    success_count,
    success_rate,
    avg_score,
    min_score,
    max_score,
    avg_steps,
    min_steps,
    max_steps,
    elapsed_seconds,
):
    """Update aggregate results for an evaluation session."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE evaluation_sessions
                SET success_count = %s,
                    success_rate = %s,
                    avg_score = %s,
                    min_score = %s,
                    max_score = %s,
                    avg_steps = %s,
                    min_steps = %s,
                    max_steps = %s,
                    elapsed_seconds = %s
                WHERE id = %s
                """,
                (
                    success_count,
                    success_rate,
                    avg_score,
                    min_score,
                    max_score,
                    avg_steps,
                    min_steps,
                    max_steps,
                    elapsed_seconds,
                    session_id,
                ),
            )


def create_game_run(
    actor_type,
    run_type,
    score,
    steps,
    success,
    final_reason,
    dead=False,
    victory=False,
    evaluation_session_id=None,
    bot_config_id=None,
    player_id=None,
    game_index=None,
    elapsed_seconds=None,
    shortcut_distance=None,
    shortcut_used_count=None,
    fallback_used_count=None,
    started_at=None,
    finished_at=None,
):
    """Create one game result row and return its id."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO game_runs (
                    evaluation_session_id,
                    bot_config_id,
                    player_id,
                    actor_type,
                    run_type,
                    game_index,
                    score,
                    steps,
                    success,
                    dead,
                    victory,
                    elapsed_seconds,
                    final_reason,
                    shortcut_distance,
                    shortcut_used_count,
                    fallback_used_count,
                    started_at,
                    finished_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
                """,
                (
                    evaluation_session_id,
                    bot_config_id,
                    player_id,
                    actor_type,
                    run_type,
                    game_index,
                    score,
                    steps,
                    success,
                    dead,
                    victory,
                    elapsed_seconds,
                    final_reason,
                    shortcut_distance,
                    shortcut_used_count,
                    fallback_used_count,
                    started_at,
                    finished_at,
                ),
            )
            return cur.fetchone()[0]


def get_top_player_runs(limit=10, sort_by="score", victory_only=False):
    """Return top manual screen-play results."""
    order_by = """
        gr.score DESC,
        gr.victory DESC,
        gr.steps ASC,
        gr.created_at DESC
    """
    if sort_by == "steps":
        order_by = """
            gr.victory DESC,
            gr.steps ASC,
            gr.score DESC,
            gr.created_at DESC
        """

    victory_clause = "AND gr.victory = TRUE" if victory_only else ""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    p.display_name,
                    gr.score,
                    gr.steps,
                    gr.victory,
                    gr.final_reason,
                    gr.created_at
                FROM game_runs gr
                JOIN players p ON p.id = gr.player_id
                WHERE gr.actor_type = 'player'
                  AND gr.run_type = 'screen'
                  {victory_clause}
                ORDER BY {order_by}
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()

    return [
        {
            "display_name": row[0],
            "score": row[1],
            "steps": row[2],
            "victory": row[3],
            "final_reason": row[4],
            "created_at": row[5],
        }
        for row in rows
    ]


def psycopg_json(value):
    """Convert a Python value to JSON text for jsonb parameters."""
    import json

    return json.dumps(value, ensure_ascii=False)

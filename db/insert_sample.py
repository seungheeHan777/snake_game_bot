"""Insert a small sample record to verify repository writes.

Prerequisites:
- .env exists with DATABASE_URL.
- players table exists.
- db/schema.sql has been executed.

Run from the project root:

    py -3 -m db.insert_sample
"""

from db.repository import (
    create_game_run,
    get_or_create_bot_config,
    get_or_create_player,
)


def main():
    """Create one player, one bot config, and two sample game rows."""
    player_id = get_or_create_player("test_player")
    bot_config_id = get_or_create_bot_config(
        name="stable",
        version="v1",
        algorithm_type="stable",
        shortcut_distance=4,
        uses_shortcut=True,
        uses_hamiltonian=True,
        settings_json={"async_shortcut": True},
    )

    player_run_id = create_game_run(
        actor_type="player",
        run_type="screen",
        player_id=player_id,
        score=10,
        steps=120,
        success=False,
        dead=True,
        victory=False,
        final_reason="game_over",
    )

    bot_run_id = create_game_run(
        actor_type="bot",
        run_type="headless",
        bot_config_id=bot_config_id,
        score=400,
        steps=39770,
        success=True,
        dead=False,
        victory=True,
        final_reason="victory",
        shortcut_distance=4,
    )

    print(f"sample player_id={player_id}")
    print(f"sample bot_config_id={bot_config_id}")
    print(f"sample player_run_id={player_run_id}")
    print(f"sample bot_run_id={bot_run_id}")


if __name__ == "__main__":
    main()

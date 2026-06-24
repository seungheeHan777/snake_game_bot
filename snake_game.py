"""Run the snake game loop."""

from datetime import datetime, timedelta
from time import perf_counter

import pygame

from apple import Apple
from rule import Rule
from snake import Snake
from snake_core import BLACK, BOARD_HEIGHT, BOARD_WIDTH, GREEN, RED, WHITE


def run_game(
    choose_direction=None,
    title="snake game",
    move_interval=0.1,
    save_manual_results=False,
):
    """Run pygame snake.

    When choose_direction is None, keyboard input controls the snake.
    When choose_direction is provided, that function controls the snake.
    Manual result saving is only shown for keyboard-controlled play.
    """
    pygame.init()
    screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
    pygame.display.set_caption(title)
    font = pygame.font.SysFont(None, 50)
    clock = pygame.time.Clock()

    if choose_direction is None and save_manual_results:
        run_manual_app(screen, font, clock, choose_direction, move_interval)
        pygame.quit()
        return

    restart = True
    while restart:
        result = _run_single_game(
            screen,
            clock,
            choose_direction,
            move_interval,
        )
        restart = False

        if result["final_reason"] == "user_quit":
            break

        if choose_direction is None and save_manual_results:
            action = show_manual_result_screen(screen, font, result)
            restart = action == "retry"
        else:
            rule = Rule()
            if result["victory"]:
                rule.show_victory(screen, font)
            else:
                rule.show_game_over(screen, font, result["score"])

    pygame.quit()


def run_manual_app(screen, font, clock, choose_direction, move_interval):
    """Run manual app screens: start, game, result, and ranking."""
    while True:
        action = show_start_screen(screen, font)
        if action == "quit":
            return
        if action == "ranking":
            if show_ranking_screen(screen, font) == "quit":
                return
            continue
        if action != "start":
            continue

        while True:
            result = _run_single_game(
                screen,
                clock,
                choose_direction,
                move_interval,
            )
            if result["final_reason"] == "user_quit":
                return

            result_action = show_manual_result_screen(screen, font, result)
            if result_action == "retry":
                continue
            if result_action in ("menu", "quit"):
                if result_action == "quit":
                    return
                break


def _run_single_game(screen, clock, choose_direction, move_interval):
    """Run one game and return result stats."""
    snake = Snake()
    apple = Apple()
    rule = Rule()
    running = True
    last_bot_move = datetime.now()
    started_at = datetime.now().astimezone()
    timer_start = perf_counter()
    steps = 0
    final_reason = "unknown"

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final_reason = "user_quit"
                running = False
            elif choose_direction is None and snake.handle_event(event):
                steps += 1

        if not running:
            break

        if choose_direction is None:
            if snake.auto_move(move_interval):
                steps += 1
        elif timedelta(seconds=move_interval) <= datetime.now() - last_bot_move:
            direction = choose_direction(snake, apple)
            if direction is None:
                final_reason = "game_over"
                running = False
            elif snake.move(direction):
                steps += 1
                last_bot_move = datetime.now()

        snake.draw(screen)
        apple.draw(screen)

        if snake.head == apple.position:
            snake.grow()
            apple.relocate(snake.positions)

        if rule.is_victory(snake):
            final_reason = "victory"
            running = False
        elif rule.is_game_over(snake):
            final_reason = "game_over"
            running = False

        pygame.display.flip()

    finished_at = datetime.now().astimezone()
    victory = final_reason == "victory"
    dead = final_reason == "game_over"
    return {
        "score": snake.score,
        "steps": steps,
        "success": victory,
        "dead": dead,
        "victory": victory,
        "final_reason": final_reason,
        "elapsed_seconds": perf_counter() - timer_start,
        "started_at": started_at,
        "finished_at": finished_at,
    }


def draw_button(screen, font, rect, label):
    """Draw a simple rectangular button."""
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label_text = font.render(label, True, BLACK)
    label_rect = label_text.get_rect(center=rect.center)
    screen.blit(label_text, label_rect)


def draw_option_button(screen, font, rect, label, active=False):
    """Draw a small option button."""
    fill_color = GREEN if active else WHITE
    pygame.draw.rect(screen, fill_color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label_text = font.render(label, True, BLACK)
    label_rect = label_text.get_rect(center=rect.center)
    screen.blit(label_text, label_rect)


def show_start_screen(screen, font):
    """Show start menu and return selected action."""
    start_rect = pygame.Rect(80, 150, 240, 55)
    ranking_rect = pygame.Rect(80, 225, 240, 55)

    while True:
        screen.fill(WHITE)
        title_text = font.render("SNAKE", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(BOARD_WIDTH // 2, 80)))
        draw_button(screen, font, start_rect, "Start")
        draw_button(screen, font, ranking_rect, "Ranking")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                if event.key == pygame.K_r:
                    return "ranking"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    return "start"
                if ranking_rect.collidepoint(event.pos):
                    return "ranking"

        pygame.display.flip()


def show_ranking_screen(screen, font):
    """Show saved player rankings."""
    back_rect = pygame.Rect(120, 335, 160, 42)
    small_font = pygame.font.SysFont(None, 24)
    header_font = pygame.font.SysFont(None, 22)
    option_font = pygame.font.SysFont(None, 20)
    score_rect = pygame.Rect(20, 60, 80, 26)
    steps_rect = pygame.Rect(110, 60, 80, 26)
    wins_rect = pygame.Rect(200, 60, 95, 26)
    mode_rect = pygame.Rect(305, 60, 75, 26)
    table_rect = pygame.Rect(20, 98, 360, 220)
    columns = [
        ("Rank", 28),
        ("Name", 78),
        ("Score", 235),
        ("Steps", 304),
    ]
    sort_by = "score"
    victory_only = False
    ranking_mode = "best"
    rankings, message = load_rankings(sort_by, victory_only, ranking_mode)

    while True:
        screen.fill(WHITE)
        title_text = font.render("RANKING", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(BOARD_WIDTH // 2, 28)))
        draw_option_button(
            screen,
            option_font,
            score_rect,
            "Score",
            active=sort_by == "score",
        )
        draw_option_button(
            screen,
            option_font,
            steps_rect,
            "Steps",
            active=sort_by == "steps",
        )
        draw_option_button(
            screen,
            option_font,
            wins_rect,
            "Wins only" if victory_only else "All runs",
            active=victory_only,
        )
        draw_option_button(
            screen,
            option_font,
            mode_rect,
            "Best" if ranking_mode == "best" else "Runs",
            active=ranking_mode == "best",
        )

        if message:
            draw_ranking_empty_state(screen, small_font, table_rect, message)
        elif not rankings:
            draw_ranking_empty_state(screen, small_font, table_rect, "No saved scores")
        else:
            draw_ranking_table(screen, header_font, small_font, table_rect, columns, rankings)

        draw_button(screen, font, back_rect, "Back")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_ESCAPE,
                pygame.K_RETURN,
            ):
                return "back"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                sort_by = "score"
                rankings, message = load_rankings(
                    sort_by,
                    victory_only,
                    ranking_mode,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                sort_by = "steps"
                rankings, message = load_rankings(
                    sort_by,
                    victory_only,
                    ranking_mode,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                victory_only = not victory_only
                rankings, message = load_rankings(
                    sort_by,
                    victory_only,
                    ranking_mode,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                ranking_mode = "runs" if ranking_mode == "best" else "best"
                rankings, message = load_rankings(
                    sort_by,
                    victory_only,
                    ranking_mode,
                )
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return "back"
                if score_rect.collidepoint(event.pos):
                    sort_by = "score"
                    rankings, message = load_rankings(
                        sort_by,
                        victory_only,
                        ranking_mode,
                    )
                elif steps_rect.collidepoint(event.pos):
                    sort_by = "steps"
                    rankings, message = load_rankings(
                        sort_by,
                        victory_only,
                        ranking_mode,
                    )
                elif wins_rect.collidepoint(event.pos):
                    victory_only = not victory_only
                    rankings, message = load_rankings(
                        sort_by,
                        victory_only,
                        ranking_mode,
                    )
                elif mode_rect.collidepoint(event.pos):
                    ranking_mode = "runs" if ranking_mode == "best" else "best"
                    rankings, message = load_rankings(
                        sort_by,
                        victory_only,
                        ranking_mode,
                    )

        pygame.display.flip()


def draw_ranking_table(screen, header_font, row_font, table_rect, columns, rankings):
    """Draw ranking data in fixed columns."""
    row_height = 18
    header_height = 26
    pygame.draw.rect(screen, BLACK, table_rect, 2)

    header_bottom = table_rect.y + header_height
    pygame.draw.line(
        screen,
        BLACK,
        (table_rect.x, header_bottom),
        (table_rect.right, header_bottom),
        2,
    )

    for _, x in columns[1:]:
        pygame.draw.line(
            screen,
            BLACK,
            (x - 8, table_rect.y),
            (x - 8, table_rect.bottom),
            1,
        )

    for label, x in columns:
        label_text = header_font.render(label, True, BLACK)
        screen.blit(label_text, (x, table_rect.y + 6))

    for index, row in enumerate(rankings[:10], start=1):
        y = header_bottom + (index - 1) * row_height
        if index % 2 == 0:
            pygame.draw.rect(
                screen,
                (238, 238, 238),
                pygame.Rect(table_rect.x + 1, y + 1, table_rect.width - 2, row_height - 1),
            )
        pygame.draw.line(
            screen,
            BLACK,
            (table_rect.x, y + row_height),
            (table_rect.right, y + row_height),
            1,
        )

        values = [
            str(index),
            str(row["display_name"])[:12],
            str(row["score"]),
            str(row["steps"]),
        ]
        for value, (_, x) in zip(values, columns):
            value_text = row_font.render(value, True, BLACK)
            screen.blit(value_text, (x, y + 4))


def draw_ranking_empty_state(screen, font, table_rect, message):
    """Draw an empty or error state inside the ranking table area."""
    pygame.draw.rect(screen, BLACK, table_rect, 2)
    message_text = font.render(message, True, BLACK)
    message_rect = message_text.get_rect(center=table_rect.center)
    screen.blit(message_text, message_rect)


def load_rankings(sort_by="score", victory_only=False, ranking_mode="best"):
    """Load top player runs for the ranking screen."""
    try:
        from db.repository import get_player_best_runs, get_top_player_runs

        if ranking_mode == "runs":
            return get_top_player_runs(
                limit=10,
                sort_by=sort_by,
                victory_only=victory_only,
            ), ""
        return get_player_best_runs(
            limit=10,
            sort_by=sort_by,
            victory_only=victory_only,
        ), ""
    except Exception:
        return [], "Ranking load failed"


def save_manual_result(player_name, result):
    """Save one manual screen-play result."""
    from db.repository import create_game_run, get_or_create_player

    player_id = get_or_create_player(player_name)
    return create_game_run(
        actor_type="player",
        run_type="screen",
        player_id=player_id,
        score=result["score"],
        steps=result["steps"],
        success=result["success"],
        dead=result["dead"],
        victory=result["victory"],
        elapsed_seconds=result["elapsed_seconds"],
        final_reason=result["final_reason"],
        started_at=result["started_at"],
        finished_at=result["finished_at"],
    )


def show_manual_result_screen(screen, font, result):
    """Show name input, save, and retry controls after manual play."""
    player_name = ""
    message = ""
    message_font = pygame.font.SysFont(None, 28)
    save_rect = pygame.Rect(70, 285, 120, 48)
    retry_rect = pygame.Rect(210, 285, 120, 48)
    input_rect = pygame.Rect(70, 215, 260, 44)
    background = GREEN if result["victory"] else RED

    while True:
        screen.fill(background)
        title = "WIN" if result["victory"] else "GAME OVER"
        title_text = font.render(title, True, BLACK)
        score_text = font.render(f"SCORE : {result['score']}", True, BLACK)
        steps_text = font.render(f"STEPS : {result['steps']}", True, BLACK)
        name_label = font.render("NAME", True, BLACK)
        name_text = font.render(player_name or "", True, BLACK)
        message_text = message_font.render(message, True, BLACK)

        screen.blit(title_text, (70, 45))
        screen.blit(score_text, (70, 95))
        screen.blit(steps_text, (70, 140))
        screen.blit(name_label, (70, 180))

        pygame.draw.rect(screen, WHITE, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        screen.blit(name_text, (input_rect.x + 8, input_rect.y + 8))

        draw_button(screen, font, save_rect, "Save")
        draw_button(screen, font, retry_rect, "Retry")
        if message:
            screen.blit(message_text, (70, 345))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    message = try_save_manual_result(player_name, result)
                    if message == "Saved":
                        draw_result_message(screen, message_font, message)
                        pygame.time.wait(500)
                        return "menu"
                elif (
                    len(player_name) < 16
                    and event.unicode
                    and event.unicode.isprintable()
                ):
                    player_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if save_rect.collidepoint(event.pos):
                    message = try_save_manual_result(player_name, result)
                    if message == "Saved":
                        draw_result_message(screen, message_font, message)
                        pygame.time.wait(500)
                        return "menu"
                elif retry_rect.collidepoint(event.pos):
                    return "retry"

        pygame.display.flip()


def draw_result_message(screen, font, message):
    """Draw a result-screen message before moving to another screen."""
    message_text = font.render(message, True, BLACK)
    screen.blit(message_text, (70, 345))
    pygame.display.flip()


def try_save_manual_result(player_name, result):
    """Try saving a manual result and return a display message."""
    player_name = player_name.strip()
    if not player_name:
        return "Name required"
    try:
        save_manual_result(player_name, result)
    except Exception as error:
        return format_save_error(error)
    return "Saved"


def format_save_error(error):
    """Return a short user-facing DB save error."""
    error_text = str(error).lower()
    if "connection" in error_text or "could not connect" in error_text:
        return "DB connection failed"
    if "does not exist" in error_text or "relation" in error_text:
        return "DB table missing"
    if "check constraint" in error_text or "foreign key" in error_text:
        return "DB schema mismatch"
    return f"Save failed: {error.__class__.__name__}"


if __name__ == "__main__":
    run_game(save_manual_results=True)

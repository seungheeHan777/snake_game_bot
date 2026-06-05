"""Move planner for the stable snake bot."""

from threading import Lock, Thread

from stable_bot.hamiltonian import choose_cycle_direction
from stable_bot.shortcut import MAX_SHORTCUT_DISTANCE, find_safe_shortcut_path
from stable_bot.safety import is_immediately_safe


class PlanningState:
    """Small snapshot used by the background shortcut planner."""

    def __init__(self, positions, direction, apple_position):
        self.positions = [position.copy() for position in positions]
        self.direction = direction
        self.head = self.positions[0]
        self.apple_position = apple_position.copy()


class PlanningApple:
    """Apple-like snapshot used by shortcut search."""

    def __init__(self, position):
        self.position = position.copy()


class StablePlanner:
    """Stateful non-blocking planner that caches safe shortcut paths."""

    def __init__(self, shortcut_distance=MAX_SHORTCUT_DISTANCE):
        self.shortcut_distance = shortcut_distance
        self.shortcut_path = []
        self.shortcut_target = None
        self.pending_target = None
        self.seen_target = None
        self.planned_targets = set()
        self.worker = None
        self.lock = Lock()

    def reset_shortcut(self):
        """Clear the cached shortcut path."""
        with self.lock:
            self.shortcut_path = []
            self.shortcut_target = None

    def refresh_target(self, apple):
        """Reset per-apple planning state when a new apple appears."""
        target = self.apple_target(apple)
        if self.seen_target != target:
            with self.lock:
                self.shortcut_path = []
                self.shortcut_target = None
                self.pending_target = None
                self.planned_targets.clear()
            self.seen_target = target

    def apple_target(self, apple):
        """Return a hashable apple position."""
        return tuple(apple.position)

    def cached_path(self):
        """Return a shallow copy of the cached shortcut path."""
        with self.lock:
            return list(self.shortcut_path), self.shortcut_target

    def pop_cached_direction(self):
        """Pop the next cached direction."""
        with self.lock:
            if not self.shortcut_path:
                return None
            return self.shortcut_path.pop(0)

    def store_shortcut(self, target, path):
        """Store a completed background shortcut plan."""
        with self.lock:
            if self.pending_target != target:
                return
            self.pending_target = None
            if path:
                self.shortcut_target = target
                self.shortcut_path = list(path)

    def worker_running(self):
        """Return whether a background planner is active."""
        return self.worker is not None and self.worker.is_alive()

    def start_shortcut_search(self, snake, apple):
        """Start background shortcut calculation if none is already running."""
        target = self.apple_target(apple)
        if target in self.planned_targets:
            return
        if self.worker_running() or self.pending_target == target:
            return

        state = PlanningState(snake.positions, snake.direction, apple.position)
        apple_state = PlanningApple(apple.position)
        self.pending_target = target
        self.planned_targets.add(target)

        def worker():
            path = find_safe_shortcut_path(
                state,
                apple_state,
                max_distance=self.shortcut_distance,
            )
            self.store_shortcut(target, path)

        self.worker = Thread(target=worker, daemon=True)
        self.worker.start()

    def cached_shortcut_direction(self, snake, apple):
        """Return the next cached shortcut direction when still valid."""
        path, target = self.cached_path()
        if target != self.apple_target(apple):
            self.reset_shortcut()
            return None
        if not path:
            return None

        direction = path[0]
        if not is_immediately_safe(snake, direction):
            self.reset_shortcut()
            return None

        return self.pop_cached_direction()

    def choose_direction(self, snake, apple):
        """Return immediately: cached shortcut if ready, otherwise fallback."""
        self.refresh_target(apple)

        cached_direction = self.cached_shortcut_direction(snake, apple)
        if cached_direction:
            return cached_direction

        self.start_shortcut_search(snake, apple)

        return choose_cycle_direction(snake)

    def __call__(self, snake, apple):
        """Allow planner instances to be passed directly to run_game()."""
        return self.choose_direction(snake, apple)


_default_planner = StablePlanner()


def choose_stable_direction(snake, apple):
    """Choose the stable bot's next direction with a default cached planner."""
    return _default_planner.choose_direction(snake, apple)

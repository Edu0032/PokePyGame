from collections.abc import Callable
from dataclasses import dataclass, field
from time import monotonic
from uuid import uuid4


@dataclass
class GameSession:
    player_name: str = "Treinador"
    player_id: str = "treinador"
    multiplayer_player_id: str = field(default_factory=lambda: uuid4().hex)
    started_at: float | None = None
    finished_at: float | None = None
    time_provider: Callable[[], float] = field(default=monotonic, repr=False)

    def identify_player(self, player_name: str) -> None:
        self.player_name = " ".join(player_name.strip().split()) or "Treinador"
        self.player_id = self._slugify(self.player_name)

    def start(self) -> None:
        self.started_at = self.time_provider()
        self.finished_at = None

    def finish(self) -> None:
        if self.started_at is None:
            self.start()
        self.finished_at = self.time_provider()

    def reset(self) -> None:
        self.started_at = None
        self.finished_at = None

    @property
    def is_running(self) -> bool:
        return self.started_at is not None and self.finished_at is None

    @property
    def elapsed_seconds(self) -> int:
        if self.started_at is None:
            return 0
        end_time = self.finished_at if self.finished_at is not None else self.time_provider()
        return max(0, int(end_time - self.started_at))

    def _slugify(self, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        safe_value = "".join(char for char in normalized if char.isalnum() or char in {"-", "_"})
        return safe_value or "treinador"

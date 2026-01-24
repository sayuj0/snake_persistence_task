from dataclasses import dataclass


@dataclass(frozen=True)
class StageConfig:
	name: str
	duration_sec: float
	speed_cells_per_sec: float
	no_hit_respawn_sec: float


WINDOW_SIZE = (900, 700)
BACKGROUND_COLOR = "black"
GRID_SIZE = 20
HUD_HEIGHT = 90
HUD_LINE_COLOR = "white"

SCORE_HIT = 5.0
SCORE_COLLISION = -2.5
COLLISION_COOLDOWN_SEC = 0.5

START_LENGTH = 5

INSTRUCTION_KEY = "e"
EXIT_KEY = "escape"


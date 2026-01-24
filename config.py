import os
from dataclasses import dataclass


@dataclass(frozen=True)
class StageConfig:
	name: str
	duration_sec: float
	speed_cells_per_sec: float
	no_hit_respawn_sec: float

BACKGROUND_COLOR = "black"
GRID_SIZE = 20
HUD_HEIGHT = 90
HUD_LINE_COLOR = "white"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Sprite rendering
# Set to False to use the original colored rectangles.
USE_SPRITES = True
SPRITES_DIR = os.path.join(PROJECT_ROOT, "images")

# Filenames inside SPRITES_DIR
SPRITE_APPLE = "apple.png"
SPRITE_HEAD = {
	"up": "head_up.png",
	"down": "head_down.png",
	"left": "head_left.png",
	"right": "head_right.png",
}
SPRITE_TAIL = {
	"up": "tail_up.png",
	"down": "tail_down.png",
	"left": "tail_left.png",
	"right": "tail_right.png",
}
SPRITE_BODY_STRAIGHT = {
	"horizontal": "body_horizontal.png",
	"vertical": "body_vertical.png",
}
SPRITE_BODY_CORNER = {
	"topleft": "body_topleft.png",
	"topright": "body_topright.png",
	"bottomleft": "body_bottomleft.png",
	"bottomright": "body_bottomright.png",
}

# Visual-only scale for the apple sprite/rect relative to GRID_SIZE.
APPLE_SCALE = 1.5

SCORE_HIT = 5.0
SCORE_COLLISION = -2.5
COLLISION_COOLDOWN_SEC = 0.5

# Decimal places for rate fields written to CSV (e.g., score_per_ms)
RATE_DECIMALS = 10

START_LENGTH = 5

INSTRUCTION_KEY = "e"
EXIT_KEY = "escape"


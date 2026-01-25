"""Central configuration for the Snake task.

Most experiment-tuning happens here.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class StageConfig:
	name: str
	duration_sec: float
	speed_cells_per_sec: float
	no_hit_respawn_sec: float

BACKGROUND_COLOR = "black"
GRID_SIZE = 24
HUD_HEIGHT = 90
HUD_LINE_COLOR = "white"

USE_PLAY_AREA_BOX = True
PLAY_AREA_CELLS_X = 54
PLAY_AREA_CELLS_Y = 37
PLAY_AREA_LINE_COLOR = "white"
PLAY_AREA_LINE_WIDTH = 4

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

USE_SPRITES = True
SPRITES_DIR = os.path.join(PROJECT_ROOT, "images")

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

APPLE_SCALE = 1.5

USE_HUD_PANEL = True
HUD_PANEL_IMAGE = "button_square_wide.png"
HUD_PANEL_WIDTH_REL = 1.02
HUD_PANEL_HEIGHT = None
HUD_PANEL_Y_OFFSET = 0

SCORE_HIT = 5.0
SCORE_COLLISION = -2.5
COLLISION_COOLDOWN_SEC = 0.5

SHOW_PRE_STAGE_FIXATION = True
PRE_STAGE_FIXATION_TOTAL_SEC = 2.0
PRE_STAGE_FIXATION_FLASH_SEC = 0.25
PRE_STAGE_FIXATION_SIZE_PX = 36
PRE_STAGE_FIXATION_THICKNESS_PX = 3
PRE_STAGE_FIXATION_OPACITY = 1.0
PRE_STAGE_FIXATION_COLOR = "white"

RATE_DECIMALS = 10

START_LENGTH = 5

INSTRUCTION_KEY = "e"
EXIT_KEY = "escape"

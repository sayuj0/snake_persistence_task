"""Core gameplay loop for each stage."""

import math
import random
from typing import Any, Optional
from psychopy import core, event, visual
from config import (
	APPLE_SCALE,
	COLLISION_COOLDOWN_SEC,
	EXIT_KEY,
	GRID_SIZE,
	HUD_HEIGHT,
	HUD_LINE_COLOR,
	PLAY_AREA_CELLS_X,
	PLAY_AREA_CELLS_Y,
	PLAY_AREA_LINE_COLOR,
	PLAY_AREA_LINE_WIDTH,
	PRE_STAGE_FIXATION_COLOR,
	PRE_STAGE_FIXATION_FLASH_SEC,
	PRE_STAGE_FIXATION_OPACITY,
	PRE_STAGE_FIXATION_SIZE_PX,
	PRE_STAGE_FIXATION_THICKNESS_PX,
	PRE_STAGE_FIXATION_TOTAL_SEC,
	SCORE_COLLISION,
	SCORE_HIT,
	SHOW_PRE_STAGE_FIXATION,
	USE_PLAY_AREA_BOX,
	START_LENGTH,
	LENGTH_GAIN_PER_TARGET,
	LENGTH_LOSS_ON_COLLISION,
	SPRITE_APPLE,
	SPRITE_BODY_CORNER,
	SPRITE_BODY_STRAIGHT,
	SPRITE_HEAD,
	SPRITE_TAIL,
	SPRITES_DIR,
	USE_SPRITES,
)
from config import StageConfig
from snake_task.utils import get_random_grid_position
from snake_task.ui import create_hud, update_hud, update_progress_bar
from snake_task.sprites import (
	SpriteConfig,
	SpriteManager,
	body_sprite_key,
	head_direction,
	tail_direction,
)


POSITIVE_RESPAWN_DIALOGUE: tuple[str, ...] = (
	"Keep going!",
	"Keep it up!",
	"You can do it!",
	"Nice effort!",
	"Good try!",
	"You are doing great!",
	"Stay confident!",
	"Keep aiming high!",
	"You can push through it!",
	"Keep showing up!",
	"Stay determined!",
	"Give it another shot!",
	"Keep moving forward!",
	"You can do hard things!",
	"Give it another try, you can do it!",
	"Give it your next best try!",
	"Push forward!",
	"Stay resilient!",
	"You are stronger each round!",
	"Push ahead!",
	"Try it again!",
	"Power through!",
	"Jump back in!",
	"Give it another go!",
	"Push past it!",
	"You’re doing great, keep trying!",
	"Bring your best again!",
	"Push through the setback!",
	"Stay strong!",
	"Keep your focus!",
	"Keep pushing!",
	"Stay locked in!",
	"Keep aiming higher!",
	"Keep at it!",
	"You got this!",
	"You can bounce back!",
	"Hone your focus!",
	"Amazing effort!",
	"That's okay, try again!",
	"Don’t give up, keep going!",
	"Keep persisting!",
	"Continue progressing!",
	"You are making progress!",
	"Your effort is strong, keep it up!",
	"Your persistence is valuable!",
	"You are progressing well!",
	"Great effort, keep it up!",
	"You’re doing a great job!",
	"You’re handling this very well!",
)

RESPAWN_DIALOGUE_DURATION_SEC = 2.0
DEATH_PAUSE_SEC = 2.0

DIALOGUE_MIN_WIDTH_PX = 180
DIALOGUE_MAX_WIDTH_PX = 560
DIALOGUE_MIN_HEIGHT_PX = 44
DIALOGUE_MAX_HEIGHT_PX = 160
DIALOGUE_PADDING_X_PX = 14
DIALOGUE_PADDING_Y_PX = 10


def _clamp(value: float, lo: float, hi: float) -> float:
	return max(lo, min(hi, value))


def _fit_dialogue_box(
	bg: Any,
	text: Any,
	message: str,
	max_width_px: float,
) -> None:
	"""Update dialogue text/wrapping and resize bg to fit (bounded)."""
	text.text = message or ""

	max_w = float(_clamp(max_width_px, DIALOGUE_MIN_WIDTH_PX, DIALOGUE_MAX_WIDTH_PX))
	# Start with generous wrapping; then resize based on measured bounding box.
	text.wrapWidth = max_w - (DIALOGUE_PADDING_X_PX * 2)

	measured_w = None
	measured_h = None
	try:
		bbox = getattr(text, "boundingBox", None)
		if bbox and len(bbox) >= 2:
			measured_w = float(bbox[0])
			measured_h = float(bbox[1])
	except Exception:
		measured_w = None
		measured_h = None

	if measured_w is None or measured_h is None:
		# Fallback heuristic if bounding box isn't available yet in this PsychoPy build.
		chars = max(1, len(text.text))
		measured_w = min(max_w, max(DIALOGUE_MIN_WIDTH_PX, chars * 9.0))
		measured_h = 28.0 if chars < 30 else 52.0

	desired_w = measured_w + (DIALOGUE_PADDING_X_PX * 2)
	desired_h = measured_h + (DIALOGUE_PADDING_Y_PX * 2)

	desired_w = float(_clamp(desired_w, DIALOGUE_MIN_WIDTH_PX, max_w))
	desired_h = float(_clamp(desired_h, DIALOGUE_MIN_HEIGHT_PX, DIALOGUE_MAX_HEIGHT_PX))

	bg.width = desired_w
	bg.height = desired_h
	text.wrapWidth = desired_w - (DIALOGUE_PADDING_X_PX * 2)

def run_stage(win: Any, stage: StageConfig) -> tuple[str, Optional[dict[str, Any]]]:
	"""Run a single stage of gameplay.

	Args:
		win: PsychoPy window used for drawing.
		stage: Stage configuration (duration, speed, respawn timing).

	Returns:
		A tuple of (status, result). Status is "quit" if the user exits early,
		otherwise "complete". Result is None when quitting, otherwise a dict of
		summary metrics.
	"""
	width, height = win.size
	avail_min_x = -width / 2 + GRID_SIZE / 2
	avail_max_x = width / 2 - GRID_SIZE / 2
	avail_min_y = -height / 2 + HUD_HEIGHT + GRID_SIZE / 2
	avail_max_y = height / 2 - GRID_SIZE / 2

	if USE_PLAY_AREA_BOX:
		max_play_w = max(GRID_SIZE * 6, width - GRID_SIZE)
		max_play_h = max(GRID_SIZE * 6, (height - HUD_HEIGHT) - GRID_SIZE)
		play_w = min(float(PLAY_AREA_CELLS_X) * GRID_SIZE, max_play_w)
		play_h = min(float(PLAY_AREA_CELLS_Y) * GRID_SIZE, max_play_h)
		center_y = (avail_min_y + avail_max_y) / 2
		min_x = -play_w / 2 + GRID_SIZE / 2
		max_x = play_w / 2 - GRID_SIZE / 2
		min_y = center_y - play_h / 2 + GRID_SIZE / 2
		max_y = center_y + play_h / 2 - GRID_SIZE / 2
	else:
		min_x = avail_min_x
		max_x = avail_max_x
		min_y = avail_min_y
		max_y = avail_max_y

	min_x = math.ceil(min_x / GRID_SIZE) * GRID_SIZE
	max_x = math.floor(max_x / GRID_SIZE) * GRID_SIZE
	min_y = math.ceil(min_y / GRID_SIZE) * GRID_SIZE
	max_y = math.floor(max_y / GRID_SIZE) * GRID_SIZE
	bounds = (min_x, max_x, min_y, max_y)

	spawn_y = math.floor(((min_y + max_y) / 2) / GRID_SIZE) * GRID_SIZE
	spawn_y = min(max(spawn_y, min_y), max_y)
	min_head_x = min_x + (START_LENGTH - 1) * GRID_SIZE
	spawn_x = max(0, min_head_x)
	spawn_x = min(spawn_x, max_x)

	snake: list[tuple[float, float]] = [(spawn_x, spawn_y)]
	for i in range(1, START_LENGTH):
		snake.append((spawn_x - i * GRID_SIZE, spawn_y))

	direction = (GRID_SIZE, 0)
	pending_direction = direction

	score = 0.0
	target_hit = 0
	collisions = 0

	last_move = 0.0
	last_spawn = 0.0
	last_hit = 0.0
	collision_lockout = 0.0
	move_interval = 1.0 / stage.speed_cells_per_sec
	growth_remaining = 0

	target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))

	def reset_snake(length=START_LENGTH):
		"""Return a new straight snake at the spawn position.

		Args:
			length: Number of segments for the reset snake.
		"""
		new_snake = [(spawn_x, spawn_y)]
		for i in range(1, length):
			new_snake.append((spawn_x - i * GRID_SIZE, spawn_y))
		return new_snake, (GRID_SIZE, 0)

	snake_rect = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, fillColor="green", lineColor="green")
	head_rect = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, fillColor="lightgreen", lineColor="lightgreen")
	target_rect = visual.Rect(
		win,
		width=GRID_SIZE * APPLE_SCALE,
		height=GRID_SIZE * APPLE_SCALE,
		fillColor="red",
		lineColor="red",
	)

	sprite_manager = SpriteManager(
		win,
		SpriteConfig(
			use_sprites=USE_SPRITES,
			sprites_dir=SPRITES_DIR,
			grid_size=GRID_SIZE,
		),
	)

	positive_dialogue_enabled = "positive" in (stage.name or "").lower()
	respawn_dialogue_until = -1.0
	death_pause_until = -1.0
	respawn_dialogue_text = None
	respawn_dialogue_bg = None
	respawn_dialogue_tail = None
	if positive_dialogue_enabled:
		respawn_dialogue_bg = visual.Rect(
			win,
			width=DIALOGUE_MIN_WIDTH_PX,
			height=DIALOGUE_MIN_HEIGHT_PX,
			fillColor="white",
			lineColor="black",
			lineWidth=2,
			opacity=0.95,
			pos=(0, 0),
		)
		respawn_dialogue_tail = visual.ShapeStim(
			win,
			vertices=[(-18, 8), (18, 8), (0, -18)],
			fillColor="white",
			lineColor="black",
			lineWidth=2,
			opacity=0.95,
			closeShape=True,
			pos=(0, 0),
		)
		respawn_dialogue_text = visual.TextStim(
			win,
			text="",
			height=18,
			color="black",
			wrapWidth=DIALOGUE_MIN_WIDTH_PX - (DIALOGUE_PADDING_X_PX * 2),
			alignText="center",
			bold=True,
			pos=(0, 0),
		)

	show_hud = bool(stage.show_hud)
	hud_panel = score_text = time_text = hit_text = bar_bg = bar_fill = None
	hud_line = None
	if show_hud:
		hud_panel, score_text, time_text, hit_text, bar_bg, bar_fill = create_hud(win, HUD_HEIGHT)

		hud_boundary_y = min_y - GRID_SIZE / 2
		hud_line = visual.Line(
			win,
			start=(min_x, hud_boundary_y),
			end=(max_x, hud_boundary_y),
			lineColor=HUD_LINE_COLOR,
			lineWidth=2,
		)

	wall_rect = None
	if USE_PLAY_AREA_BOX:
		wall_rect = visual.Rect(
			win,
			width=(max_x - min_x) + GRID_SIZE,
			height=(max_y - min_y) + GRID_SIZE,
			pos=((min_x + max_x) / 2, (min_y + max_y) / 2),
			fillColor=None,
			lineColor=PLAY_AREA_LINE_COLOR,
			lineWidth=float(PLAY_AREA_LINE_WIDTH),
		)

	if SHOW_PRE_STAGE_FIXATION and PRE_STAGE_FIXATION_TOTAL_SEC > 0:
		flash_sec = float(PRE_STAGE_FIXATION_FLASH_SEC)
		total_sec = float(PRE_STAGE_FIXATION_TOTAL_SEC)
		fix_h = visual.Line(
			win,
			start=(-PRE_STAGE_FIXATION_SIZE_PX, 0),
			end=(PRE_STAGE_FIXATION_SIZE_PX, 0),
			lineColor=PRE_STAGE_FIXATION_COLOR,
			opacity=float(PRE_STAGE_FIXATION_OPACITY),
			lineWidth=float(PRE_STAGE_FIXATION_THICKNESS_PX),
		)
		fix_v = visual.Line(
			win,
			start=(0, -PRE_STAGE_FIXATION_SIZE_PX),
			end=(0, PRE_STAGE_FIXATION_SIZE_PX),
			lineColor=PRE_STAGE_FIXATION_COLOR,
			opacity=float(PRE_STAGE_FIXATION_OPACITY),
			lineWidth=float(PRE_STAGE_FIXATION_THICKNESS_PX),
		)
		pre_clock = core.Clock()
		while pre_clock.getTime() < total_sec:
			keys = event.getKeys()
			if EXIT_KEY in keys:
				return "quit", None
			t = pre_clock.getTime()
			visible = True if flash_sec <= 0 else (int(t / flash_sec) % 2 == 0)
			if visible:
				fix_h.draw()
				fix_v.draw()
			win.flip()
			core.wait(0.005)

	clock = core.Clock()

	while clock.getTime() < stage.duration_sec:
		now = clock.getTime()

		keys = event.getKeys()
		if EXIT_KEY in keys:
			return "quit", None

		if "up" in keys and direction != (0, -GRID_SIZE):
			pending_direction = (0, GRID_SIZE)
		elif "down" in keys and direction != (0, GRID_SIZE):
			pending_direction = (0, -GRID_SIZE)
		elif "left" in keys and direction != (GRID_SIZE, 0):
			pending_direction = (-GRID_SIZE, 0)
		elif "right" in keys and direction != (-GRID_SIZE, 0):
			pending_direction = (GRID_SIZE, 0)

		paused = now < death_pause_until
		if (not paused) and (now - last_move >= move_interval):
			direction = pending_direction
			head_x, head_y = snake[0]
			next_pos = (head_x + direction[0], head_y + direction[1])

			wall_collision = next_pos[0] < min_x or next_pos[0] > max_x or next_pos[1] < min_y or next_pos[1] > max_y
			self_collision = next_pos in snake

			if wall_collision or self_collision:
				if now >= collision_lockout:
					collisions += 1
					score += SCORE_COLLISION
					collision_lockout = now + COLLISION_COOLDOWN_SEC
					new_length = max(START_LENGTH, len(snake) - int(LENGTH_LOSS_ON_COLLISION))
					snake, direction = reset_snake(new_length)
					growth_remaining = 0
					pending_direction = direction
					death_pause_until = now + DEATH_PAUSE_SEC
					if respawn_dialogue_text is not None and POSITIVE_RESPAWN_DIALOGUE:
						message = random.choice(POSITIVE_RESPAWN_DIALOGUE)
						assert respawn_dialogue_bg is not None
						max_w = min(float(DIALOGUE_MAX_WIDTH_PX), float(max_x - min_x) * 0.85)
						_fit_dialogue_box(respawn_dialogue_bg, respawn_dialogue_text, message, max_width_px=max_w)
						respawn_dialogue_until = now + RESPAWN_DIALOGUE_DURATION_SEC
			else:
				snake.insert(0, next_pos)
				if next_pos == target_pos:
					score += SCORE_HIT
					target_hit += 1
					growth_remaining += max(0, int(LENGTH_GAIN_PER_TARGET) - 1)
					last_hit = now
					target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))
					last_spawn = now
				else:
					if growth_remaining > 0:
						growth_remaining -= 1
					else:
						snake.pop()

			last_move = now

		if (not paused) and now - last_hit >= stage.no_hit_respawn_sec and now - last_spawn >= stage.no_hit_respawn_sec:
			target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))
			last_spawn = now

		if show_hud:
			assert score_text is not None
			assert time_text is not None
			assert hit_text is not None
			assert bar_bg is not None
			assert bar_fill is not None
			update_hud(score_text, time_text, hit_text, score, now, target_hit)
			update_progress_bar(bar_fill, now, stage.duration_sec, bar_bg.width)

		if wall_rect is not None:
			wall_rect.draw()

		if show_hud:
			assert bar_bg is not None
			assert bar_fill is not None
			assert score_text is not None
			assert time_text is not None
			assert hit_text is not None
			if hud_panel is None:
				assert hud_line is not None
				hud_line.draw()
			else:
				hud_panel.draw()
			bar_bg.draw()
			bar_fill.draw()
			score_text.draw()
			time_text.draw()
			hit_text.draw()

		if not sprite_manager.draw(SPRITE_APPLE, target_pos, scale=APPLE_SCALE):
			target_rect.pos = target_pos
			target_rect.draw()

		for idx, segment in enumerate(snake):
			if idx == 0:
				dir_key = head_direction(snake, GRID_SIZE)
				head_file = SPRITE_HEAD.get(dir_key)
				if not (head_file and sprite_manager.draw(head_file, segment)):
					head_rect.pos = segment
					head_rect.draw()
			elif idx == len(snake) - 1:
				dir_key = tail_direction(snake, GRID_SIZE)
				tail_file = SPRITE_TAIL.get(dir_key)
				if not (tail_file and sprite_manager.draw(tail_file, segment)):
					snake_rect.pos = segment
					snake_rect.draw()
			else:
				key = body_sprite_key(snake[idx - 1], snake[idx], snake[idx + 1], GRID_SIZE)
				body_file = SPRITE_BODY_STRAIGHT.get(key) or SPRITE_BODY_CORNER.get(key)
				if not (body_file and sprite_manager.draw(body_file, segment)):
					snake_rect.pos = segment
					snake_rect.draw()

		if (
			respawn_dialogue_text is not None
			and respawn_dialogue_bg is not None
			and respawn_dialogue_tail is not None
			and now < respawn_dialogue_until
			and snake
		):
			head_x, head_y = snake[0]
			bubble_w = float(respawn_dialogue_bg.width)
			bubble_h = float(respawn_dialogue_bg.height)
			# Place bubble above the head; keep a readable gap so it doesn't overlap the snake.
			# Tail triangle has a tip at y=-18 (relative), and we position it so the tip lands near the head.
			tip_gap = GRID_SIZE * 0.8
			bubble_x = _clamp(head_x, min_x + bubble_w / 2, max_x - bubble_w / 2)
			desired_bubble_y = head_y + (bubble_h / 2) + 24 + tip_gap
			bubble_y = _clamp(desired_bubble_y, min_y + bubble_h / 2, max_y - bubble_h / 2)

			# Tail should point to the head, but stay attached under the bubble.
			tail_x = _clamp(head_x, bubble_x - bubble_w / 2 + 28, bubble_x + bubble_w / 2 - 28)
			respawn_dialogue_bg.pos = (bubble_x, bubble_y)
			respawn_dialogue_text.pos = (bubble_x, bubble_y)
			respawn_dialogue_tail.pos = (tail_x, bubble_y - bubble_h / 2 - 6)
			respawn_dialogue_bg.draw()
			respawn_dialogue_tail.draw()
			respawn_dialogue_text.draw()

		win.flip()
		core.wait(0.005)

	result = {
		"snake_length": len(snake),
		"score": score,
		"target_hit": target_hit,
		"collisions": collisions,
	}
	return "complete", result

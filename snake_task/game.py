import math

from psychopy import core, event, visual

from config import (
	COLLISION_COOLDOWN_SEC,
	EXIT_KEY,
	GRID_SIZE,
	HUD_HEIGHT,
	HUD_LINE_COLOR,
	SCORE_COLLISION,
	SCORE_HIT,
	START_LENGTH,
)
from snake_task.utils import get_random_grid_position
from snake_task.ui import create_hud, update_hud, update_progress_bar


def run_stage(win, stage):
	width, height = win.size
	min_x = -width // 2 + GRID_SIZE // 2
	max_x = width // 2 - GRID_SIZE // 2
	min_y = -height // 2 + HUD_HEIGHT + GRID_SIZE // 2
	max_y = height // 2 - GRID_SIZE // 2

	min_x = math.ceil(min_x / GRID_SIZE) * GRID_SIZE
	max_x = math.floor(max_x / GRID_SIZE) * GRID_SIZE
	min_y = math.ceil(min_y / GRID_SIZE) * GRID_SIZE
	max_y = math.floor(max_y / GRID_SIZE) * GRID_SIZE
	bounds = (min_x, max_x, min_y, max_y)

	snake = [(0, 0)]
	for i in range(1, START_LENGTH):
		snake.append((-i * GRID_SIZE, 0))

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

	target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))

	def reset_snake():
		new_snake = [(0, 0)]
		for i in range(1, START_LENGTH):
			new_snake.append((-i * GRID_SIZE, 0))
		return new_snake, (GRID_SIZE, 0)

	snake_rect = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, fillColor="green", lineColor="green")
	head_rect = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, fillColor="lightgreen", lineColor="lightgreen")
	target_rect = visual.Rect(win, width=GRID_SIZE, height=GRID_SIZE, fillColor="red", lineColor="red")

	score_text, time_text, hit_text, bar_bg, bar_fill = create_hud(win, HUD_HEIGHT)

	hud_boundary_y = min_y - GRID_SIZE / 2
	hud_line = visual.Line(
		win,
		start=(min_x, hud_boundary_y),
		end=(max_x, hud_boundary_y),
		lineColor=HUD_LINE_COLOR,
		lineWidth=2,
	)
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

		if now - last_move >= move_interval:
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
					snake, direction = reset_snake()
					pending_direction = direction
			else:
				snake.insert(0, next_pos)
				if next_pos == target_pos:
					score += SCORE_HIT
					target_hit += 1
					last_hit = now
					target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))
					last_spawn = now
				else:
					snake.pop()

			last_move = now

		if now - last_hit >= stage.no_hit_respawn_sec and now - last_spawn >= stage.no_hit_respawn_sec:
			target_pos = get_random_grid_position(bounds, GRID_SIZE, set(snake))
			last_spawn = now

		update_hud(score_text, time_text, hit_text, score, now, target_hit)
		update_progress_bar(bar_fill, now, stage.duration_sec, bar_bg.width)

		hud_line.draw()
		bar_bg.draw()
		bar_fill.draw()
		score_text.draw()
		time_text.draw()
		hit_text.draw()

		target_rect.pos = target_pos
		target_rect.draw()

		for idx, segment in enumerate(snake):
			if idx == 0:
				head_rect.pos = segment
				head_rect.draw()
			else:
				snake_rect.pos = segment
				snake_rect.draw()

		win.flip()
		core.wait(0.005)

	result = {
		"snake_length": len(snake),
		"score": score,
		"survival_time": stage.duration_sec,
		"target_hit": target_hit,
		"collisions": collisions,
	}
	return "complete", result


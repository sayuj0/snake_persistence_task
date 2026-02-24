"""UI helpers (instructions, stage screens, HUD)."""

import os
from typing import Any, Optional
from psychopy import visual, event, core
from config import (
	EXIT_KEY,
	HUD_PANEL_HEIGHT,
	HUD_PANEL_IMAGE,
	HUD_PANEL_WIDTH_REL,
	HUD_PANEL_Y_OFFSET,
	INSTRUCTION_KEY,
	SPRITES_DIR,
	USE_HUD_PANEL,
)

DEFAULT_INSTRUCTIONS = (
	"Use the arrow keys to move the snake.\n"
	"Collect red targets to gain points.\n"
	"Colliding with walls or yourself reduces points.\n\n"
	"Your score updates in real time."
)

def _clean_instruction_text(text):
	"""Remove duplicate header/footer lines from instruction text."""
	lines = []
	for raw_line in text.splitlines():
		line = raw_line.strip()
		lower = line.lower()
		if not line:
			lines.append("")
			continue
		if lower == "instructions":
			continue
		if "press" in lower and INSTRUCTION_KEY in lower:
			continue
		lines.append(raw_line)
	return "\n".join(lines).strip()

def show_instructions(win: Any, instruction_text: Optional[str] = None) -> str:
	"""Show the instruction screen.

	Args:
		win: PsychoPy window used for drawing.
		instruction_text: Optional instruction text override.

	Returns:
		"continue" when the start key is pressed, or "quit" when the exit key is pressed.
	"""
	if not instruction_text:
		instruction_text = DEFAULT_INSTRUCTIONS
	instruction_text = _clean_instruction_text(instruction_text)
	header = visual.TextStim(
		win,
		text="Instructions",
		height=32,
		color="white",
		pos=(0, 240),
	)
	body = visual.TextStim(
		win,
		text=instruction_text,
		height=20,
		color="white",
		wrapWidth=800,
		pos=(0, 0),
		alignText="center",
	)
	footer = visual.TextStim(
		win,
		text=f"Press {INSTRUCTION_KEY.upper()} to start",
		height=22,
		color="white",
		pos=(0, -260),
	)

	while True:
		keys = event.getKeys()
		if EXIT_KEY in keys:
			return "quit"
		if INSTRUCTION_KEY in keys:
			return "continue"
		header.draw()
		body.draw()
		footer.draw()
		win.flip()
		core.wait(0.01)

def show_stage_screen(win: Any, title_text: str = "") -> str:
	"""Show the pre-stage screen.

	This hides stage names (e.g., Neutral/Positive labels) for the main stages,
	but keeps the title visible for the Trial Run.

	Args:
		win: PsychoPy window used for drawing.
		title_text: Stage name (may be shown for Trial Run).

	Returns:
		"continue" when the start key is pressed, or "quit" when the exit key is pressed.
	"""
	show_title = "trial run" in (title_text or "").strip().lower()
	header = None
	if show_title:
		header = visual.TextStim(
			win,
			text=title_text,
			height=40,
			color="white",
			pos=(0, 120),
		)

	prompt = visual.TextStim(
		win,
		text=f"Press {INSTRUCTION_KEY.upper()} to start",
		height=48,
		color="white",
		pos=(0, 0),
	)

	while True:
		keys = event.getKeys()
		if EXIT_KEY in keys:
			return "quit"
		if INSTRUCTION_KEY in keys:
			return "continue"
		if header is not None:
			header.draw()
		prompt.draw()
		win.flip()
		core.wait(0.01)

def show_end_screen(win: Any, message: str) -> None:
	"""Show an end-of-task message until the exit key is pressed.

	Args:
		win: PsychoPy window used for drawing.
		message: Message to display.
	"""
	text = visual.TextStim(
		win,
		text=message,
		height=36,
		color="white",
		wrapWidth=900,
		alignText="center",
		pos=(0, 0),
	)

	text.draw()
	win.flip()
	core.wait(0.2)
	event.clearEvents()
	while True:
		keys = event.getKeys()
		if EXIT_KEY in keys:
			return
		text.draw()
		win.flip()
		core.wait(0.01)

def create_hud(win: Any, hud_height: float):
	"""Create HUD stimuli for a window.

	Args:
		win: PsychoPy window used for drawing.
		hud_height: Height of the HUD region in pixels.

	Returns:
		A tuple ``(hud_panel, score_text, time_text, hit_text, bar_bg, bar_fill)``.
		``hud_panel`` may be ``None`` if the panel image is disabled or missing.
	"""
	width, height = win.size
	base_y = -height / 2 + hud_height / 2

	hud_panel = None
	panel_w = width
	panel_h = hud_height
	if USE_HUD_PANEL and HUD_PANEL_IMAGE:
		panel_path = os.path.join(SPRITES_DIR, HUD_PANEL_IMAGE)
		if os.path.exists(panel_path):
			panel_w = width * float(HUD_PANEL_WIDTH_REL)
			if panel_w >= width:
				panel_w = panel_w + 2
			panel_h = float(HUD_PANEL_HEIGHT) if HUD_PANEL_HEIGHT else float(hud_height)
			hud_panel = visual.ImageStim(
				win,
				image=panel_path,
				size=(panel_w, panel_h),
				pos=(0, base_y + HUD_PANEL_Y_OFFSET),
			)

	x_left = -panel_w * 0.35
	x_mid = 0
	x_right = panel_w * 0.35

	score_text = visual.TextStim(
		win,
		text="Score: 0",
		height=20,
		color="white",
		pos=(x_left, base_y + 10),
	)
	time_text = visual.TextStim(
		win,
		text="Time: 0.0s",
		height=20,
		color="white",
		pos=(x_mid, base_y + 10),
	)
	hit_text = visual.TextStim(
		win,
		text="Targets: 0",
		height=20,
		color="white",
		pos=(x_right, base_y + 10),
	)

	bar_width = panel_w * 0.85
	bar_bg = visual.Rect(
		win,
		width=bar_width,
		height=16,
		pos=(0, base_y - 20),
		fillColor="gray",
		lineColor="white",
		lineWidth=2,
	)
	bar_fill = visual.Rect(
		win,
		width=0,
		height=12,
		pos=(-bar_bg.width / 2, base_y - 20),
		fillColor="white",
		lineColor=None,
	)
	return hud_panel, score_text, time_text, hit_text, bar_bg, bar_fill

def update_hud(score_text: Any, time_text: Any, hit_text: Any, score: float, elapsed: float, target_hit: int) -> None:
	"""Update HUD text based on current state.

	Args:
		score_text: Text stimulus for the score label.
		time_text: Text stimulus for the timer label.
		hit_text: Text stimulus for the targets-hit label.
		score: Current score.
		elapsed: Elapsed time in seconds.
		target_hit: Number of targets collected.
	"""
	score_text.text = f"Score: {score:.1f}"
	time_text.text = f"Time: {elapsed:.1f}s"
	hit_text.text = f"Targets: {target_hit}"

def update_progress_bar(bar_fill: Any, elapsed: float, duration: float, bar_width: float = 760) -> None:
	"""Update the progress bar fill based on elapsed time.

	Args:
		bar_fill: Rect stimulus representing the fill portion.
		elapsed: Elapsed time in seconds.
		duration: Total duration in seconds.
		bar_width: Total width of the bar background in pixels.
	"""
	progress = max(0.0, min(1.0, elapsed / duration))
	bar_fill.width = bar_width * progress
	bar_fill.pos = (-bar_width / 2 + bar_fill.width / 2, bar_fill.pos[1])

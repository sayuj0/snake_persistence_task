import os

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


def show_instructions(win, instruction_text=None):
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


def show_stage_screen(win, title_text):
	header = visual.TextStim(
		win,
		text=title_text,
		height=36,
		color="white",
		pos=(0, 40),
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
		footer.draw()
		win.flip()
		core.wait(0.01)


def create_hud(win, hud_height):
	width, height = win.size
	base_y = -height / 2 + hud_height / 2

	hud_panel = None
	panel_w = width
	panel_h = hud_height
	if USE_HUD_PANEL and HUD_PANEL_IMAGE:
		panel_path = os.path.join(SPRITES_DIR, HUD_PANEL_IMAGE)
		if os.path.exists(panel_path):
			panel_w = width * float(HUD_PANEL_WIDTH_REL)
			# Nudge to avoid 1px seams at the edges on some displays.
			if panel_w >= width:
				panel_w = panel_w + 2
			panel_h = float(HUD_PANEL_HEIGHT) if HUD_PANEL_HEIGHT else float(hud_height)
			hud_panel = visual.ImageStim(
				win,
				image=panel_path,
				size=(panel_w, panel_h),
				pos=(0, base_y + HUD_PANEL_Y_OFFSET),
			)

	# Position widgets relative to the panel width so they sit inside the border.
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


def update_hud(score_text, time_text, hit_text, score, elapsed, target_hit):
	score_text.text = f"Score: {score:.1f}"
	time_text.text = f"Time: {elapsed:.1f}s"
	hit_text.text = f"Targets: {target_hit}"


def update_progress_bar(bar_fill, elapsed, duration, bar_width=760):
	progress = max(0.0, min(1.0, elapsed / duration))
	bar_fill.width = bar_width * progress
	bar_fill.pos = (-bar_width / 2 + bar_fill.width / 2, bar_fill.pos[1])


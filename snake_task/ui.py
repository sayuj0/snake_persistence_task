from psychopy import visual, event, core

from config import INSTRUCTION_KEY, EXIT_KEY


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


def create_hud(win, hud_height):
	width, height = win.size
	base_y = -height / 2 + hud_height / 2

	score_text = visual.TextStim(
		win,
		text="Score: 0",
		height=20,
		color="white",
		pos=(-width * 0.35, base_y + 10),
	)
	time_text = visual.TextStim(
		win,
		text="Time: 0.0s",
		height=20,
		color="white",
		pos=(0, base_y + 10),
	)
	hit_text = visual.TextStim(
		win,
		text="Targets: 0",
		height=20,
		color="white",
		pos=(width * 0.35, base_y + 10),
	)

	bar_bg = visual.Rect(
		win,
		width=width * 0.85,
		height=12,
		pos=(0, base_y - 20),
		fillColor="gray",
		lineColor="gray",
	)
	bar_fill = visual.Rect(
		win,
		width=0,
		height=12,
		pos=(-bar_bg.width / 2, base_y - 20),
		fillColor="white",
		lineColor="white",
	)
	return score_text, time_text, hit_text, bar_bg, bar_fill


def update_hud(score_text, time_text, hit_text, score, elapsed, target_hit):
	score_text.text = f"Score: {score:.1f}"
	time_text.text = f"Time: {elapsed:.1f}s"
	hit_text.text = f"Targets: {target_hit}"


def update_progress_bar(bar_fill, elapsed, duration, bar_width=760):
	progress = max(0.0, min(1.0, elapsed / duration))
	bar_fill.width = bar_width * progress
	bar_fill.pos = (-bar_width / 2 + bar_fill.width / 2, bar_fill.pos[1])


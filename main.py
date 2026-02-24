"""Snake task entry point.

Runs the PsychoPy window, shows instruction/stage screens, and logs results.
"""

import os
from datetime import datetime
from typing import Any
from psychopy import core, gui, visual
from config import BACKGROUND_COLOR, RATE_DECIMALS
from snake_task.game import run_stage
from snake_task.logging import append_blank_row, append_log
from snake_task.stages import get_stages
from snake_task.ui import show_end_screen, show_instructions, show_stage_screen

def main() -> None:
	"""Run the Snake task."""
	now = datetime.now()
	hour_12 = now.hour % 12 or 12
	session_date = f"{now.month}/{now.day}/{now.year}"
	session_time = f"{hour_12}:{now:%M:%S} {now:%p}"
	dialog = gui.Dlg(title="Snake")
	dialog.addField("Participant ID", "")
	dialog.addField("Version", choices=["A", "B", "C", "D", "E", "F"])
	data = dialog.show()
	if not dialog.OK:
		return

	participant_id: str = str(data[0]).strip() or "unknown"
	version: str = str(data[1]).strip().upper() or "A"

	win = visual.Window(color=BACKGROUND_COLOR, units="pix", fullscr=True)
	win.mouseVisible = False

	if show_instructions(win) == "quit":
		win.close()
		return

	data_path = os.path.join("data", "snake_data.csv")

	completed_any = False
	quit_requested = False
	for stage in get_stages(version):
		if show_stage_screen(win, stage.name) == "quit":
			quit_requested = True
			break
		status, result = run_stage(win, stage)
		if status == "quit":
			quit_requested = True
			break
		assert result is not None
		denom_ms = stage.duration_sec * 1000.0 if stage.duration_sec else 0.0

		row: dict[str, Any] = {
			"participant_id": participant_id,
			"version": version,
			"session_date": session_date,
			"session_time": session_time,
			"difficulty": stage.name,
			"score_per_ms": (
				f"{(result['score'] / denom_ms):.{RATE_DECIMALS}f}"
				if denom_ms
				else ""
			),
			"hits_per_ms": (
				f"{(result['target_hit'] / denom_ms):.{RATE_DECIMALS}f}"
				if denom_ms
				else ""
			),
			"collisions_per_ms": (
				f"{(result['collisions'] / denom_ms):.{RATE_DECIMALS}f}"
				if denom_ms
				else ""
			),
			**result,
		}
		append_log(data_path, row)
		completed_any = True

	if completed_any:
		append_blank_row(data_path)

	if not quit_requested:
		show_end_screen(
			win,
			"Thank you for participating!\n\nPlease let the researcher know you are done.",
		)

	win.close()
	core.quit()


if __name__ == "__main__":
	main()

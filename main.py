import os
from datetime import datetime

from psychopy import core, gui, visual

from config import BACKGROUND_COLOR, WINDOW_SIZE
from snake_task.game import run_stage
from snake_task.logging import append_blank_row, append_log
from snake_task.stages import STAGES
from snake_task.ui import show_instructions, show_stage_screen


def main():
	session_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	info = {
		"Participant ID": "",
	}
	dialog = gui.DlgFromDict(info, title="Snake")
	if not dialog.OK:
		return

	participant_id = info["Participant ID"].strip() or "unknown"

	win = visual.Window(size=WINDOW_SIZE, color=BACKGROUND_COLOR, units="pix", fullscr=True)

	if show_instructions(win) == "quit":
		win.close()
		return

	data_path = os.path.join("data", "snake_data.csv")

	completed_any = False
	for stage in STAGES:
		if show_stage_screen(win, stage.name) == "quit":
			break
		status, result = run_stage(win, stage)
		if status == "quit":
			break

		row = {
			"participant_id": participant_id,
			"session_datetime": session_datetime,
			"difficulty": stage.name,
			**result,
		}
		append_log(data_path, row)
		completed_any = True

	if completed_any:
		append_blank_row(data_path)

	win.close()
	core.quit()


if __name__ == "__main__":
	main()


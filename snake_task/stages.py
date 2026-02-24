"""Stage definitions for the Snake task.

Edit this file to change level names, durations, speed, and respawn timing.
"""

from config import StageConfig

STAGES: list[StageConfig]


def _with_condition(stage: StageConfig, condition_label: str, show_hud: bool) -> StageConfig:
	return StageConfig(
		name=f"{stage.name} ({condition_label})",
		duration_sec=stage.duration_sec,
		speed_cells_per_sec=stage.speed_cells_per_sec,
		no_hit_respawn_sec=stage.no_hit_respawn_sec,
		show_hud=show_hud,
	)


def get_stages(version: str) -> list[StageConfig]:
	"""Return the stage list for a given experimental version.

	Args:
		version: Version label (e.g., "A").

	Returns:
		List of StageConfig entries to run.
	"""
	version = (version or "").strip().upper()

	trial = StageConfig(
		name="Trial Run",
		duration_sec=1.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
		show_hud=True,
	)
	level_1 = StageConfig(
		name="Level 1",
		duration_sec=1.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	)
	level_2 = StageConfig(
		name="Level 2",
		duration_sec=1.0,
		speed_cells_per_sec=25.0,
		no_hit_respawn_sec=30.0,
	)
	level_3 = StageConfig(
		name="Level 3",
		duration_sec=1.0,
		speed_cells_per_sec=45.0,
		no_hit_respawn_sec=45.0,
	)

	base_stages = [trial, level_1, level_2, level_3]

	if version == "A":
		return [
			trial,
			_with_condition(level_1, "Neutral", False),
			_with_condition(level_2, "Positive", True),
			_with_condition(level_3, "Neutral", False),
			_with_condition(level_1, "Positive", True),
			_with_condition(level_2, "Neutral", False),
			_with_condition(level_3, "Positive", True),
		]

	if version == "B":
		return [
			trial,
			_with_condition(level_1, "Positive", True),
			_with_condition(level_2, "Neutral", False),
			_with_condition(level_3, "Positive", True),
			_with_condition(level_1, "Neutral", False),
			_with_condition(level_2, "Positive", True),
			_with_condition(level_3, "Neutral", False),
		]

	return base_stages

STAGES = get_stages("A")

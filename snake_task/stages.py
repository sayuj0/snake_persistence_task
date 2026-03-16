"""Stage definitions for the Snake task.

Defines stage parameters and the version-specific stage order (A–F), including
Neutral/Positive HUD visibility.
"""

from config import StageConfig

def _with_condition(stage: StageConfig, condition_label: str, show_hud: bool) -> StageConfig:
	"""Return a StageConfig labeled with `condition_label` and `show_hud`.

	Args:
		stage: Base StageConfig to copy.
		condition_label: Label to append to the stage name (e.g., 'Neutral').
		show_hud: Whether the HUD should be shown for this staged variant.

	Returns:
		A new `StageConfig` with the labeled name and `show_hud` setting.
	"""
	return StageConfig(
		name=f"{stage.name} ({condition_label})",
		duration_sec=stage.duration_sec,
		speed_cells_per_sec=stage.speed_cells_per_sec,
		no_hit_respawn_sec=stage.no_hit_respawn_sec,
		show_hud=show_hud,
	)

def get_stages(version: str) -> list[StageConfig]:
	"""Return stage list for the given version (A–F).

	Args:
		version: Version label.

	Returns:
		List of `StageConfig` entries for the selected version.
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
		duration_sec=5.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	)

	level_2 = StageConfig(
		name="Level 2",
		duration_sec=5.0,
		speed_cells_per_sec=25.0,
		no_hit_respawn_sec=30.0,
	)

	level_3 = StageConfig(
		name="Level 3",
		duration_sec=5.0,
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

	if version == "C":
		return [
			trial,
			_with_condition(level_2, "Neutral", False),
			_with_condition(level_3, "Positive", True),
			_with_condition(level_1, "Neutral", False),
			_with_condition(level_2, "Positive", True),
			_with_condition(level_3, "Neutral", False),
			_with_condition(level_1, "Positive", True),
		]

	if version == "D":
		return [
			trial,
			_with_condition(level_2, "Positive", True),
			_with_condition(level_3, "Neutral", False),
			_with_condition(level_1, "Positive", True),
			_with_condition(level_2, "Neutral", False),
			_with_condition(level_3, "Positive", True),
			_with_condition(level_1, "Neutral", False),
		]

	if version == "E":
		return [
			trial,
			_with_condition(level_3, "Neutral", False),
			_with_condition(level_1, "Positive", True),
			_with_condition(level_2, "Neutral", False),
			_with_condition(level_3, "Positive", True),
			_with_condition(level_1, "Neutral", False),
			_with_condition(level_2, "Positive", True),
		]

	if version == "F":
		return [
			trial,
			_with_condition(level_3, "Positive", True),
			_with_condition(level_1, "Neutral", False),
			_with_condition(level_2, "Positive", True),
			_with_condition(level_3, "Neutral", False),
			_with_condition(level_1, "Positive", True),
			_with_condition(level_2, "Neutral", False),
		]

	return base_stages

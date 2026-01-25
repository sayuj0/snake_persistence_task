"""Stage definitions for the Snake task.

Edit this file to change level names, durations, speed, and respawn timing.
"""

from config import StageConfig


STAGES: list[StageConfig]


STAGES = [
	StageConfig(
		name="Trial Run",
		duration_sec=90.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="Level 1",
		duration_sec=180.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="Level 2",
		duration_sec=240.0,
		speed_cells_per_sec=20.0,
		no_hit_respawn_sec=30.0,
	),
	StageConfig(
		name="Level 3",
		duration_sec=300.0,
		speed_cells_per_sec=35.0,
		no_hit_respawn_sec=45.0,
	),
]

from config import StageConfig


STAGES = [
	StageConfig(
		name="Trial Run",
		duration_sec=5.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="Level 1",
		duration_sec=5.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="Level 2",
		duration_sec=100.0,
		speed_cells_per_sec=14.0,
		no_hit_respawn_sec=30.0,
	),
	StageConfig(
		name="Level 3",
		duration_sec=5.0,
		speed_cells_per_sec=26.0,
		no_hit_respawn_sec=45.0,
	),
]


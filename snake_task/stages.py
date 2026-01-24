from config import StageConfig


STAGES = [
	StageConfig(
		name="trial",
		duration_sec=5.0,
		speed_cells_per_sec=6.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="easy",
		duration_sec=5,
		speed_cells_per_sec=7.0,
		no_hit_respawn_sec=15.0,
	),
	StageConfig(
		name="medium",
		duration_sec=240.0,
		speed_cells_per_sec=9.0,
		no_hit_respawn_sec=30.0,
	),
	StageConfig(
		name="hard",
		duration_sec=300.0,
		speed_cells_per_sec=11.0,
		no_hit_respawn_sec=45.0,
	),
]


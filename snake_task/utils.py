"""Small utility helpers."""

import random

from typing import Iterable


def get_random_grid_position(
	bounds: tuple[float, float, float, float],
	grid_size: int,
	excluded_positions: Iterable[tuple[float, float]],
) -> tuple[int, int]:
	"""Pick a random unoccupied grid position.

	Args:
		bounds: (min_x, max_x, min_y, max_y) inclusive bounds in pixels.
		grid_size: Grid cell size in pixels.
		excluded_positions: Positions that should not be returned (e.g., snake body).

	Returns:
		A (x, y) position aligned to the grid.
	"""
	min_x, max_x, min_y, max_y = bounds
	xs = list(range(int(min_x), int(max_x) + 1, grid_size))
	ys = list(range(int(min_y), int(max_y) + 1, grid_size))
	excluded = set(excluded_positions)
	for _ in range(200):
		pos = (random.choice(xs), random.choice(ys))
		if pos not in excluded:
			return pos
	for x in xs:
		for y in ys:
			if (x, y) not in excluded:
				return (x, y)
	return (xs[0], ys[0])

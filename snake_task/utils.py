import random


def get_random_grid_position(bounds, grid_size, excluded_positions):
	min_x, max_x, min_y, max_y = bounds
	xs = list(range(int(min_x), int(max_x) + 1, grid_size))
	ys = list(range(int(min_y), int(max_y) + 1, grid_size))
	for _ in range(200):
		pos = (random.choice(xs), random.choice(ys))
		if pos not in excluded_positions:
			return pos
	for x in xs:
		for y in ys:
			if (x, y) not in excluded_positions:
				return (x, y)
	return (xs[0], ys[0])


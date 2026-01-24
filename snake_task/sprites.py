import os
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from psychopy import visual


_DIR_VECTORS = {
	"up": (0, 1),
	"down": (0, -1),
	"left": (-1, 0),
	"right": (1, 0),
}

_VECTOR_DIRS = {v: k for k, v in _DIR_VECTORS.items()}


@dataclass
class SpriteConfig:
	use_sprites: bool
	sprites_dir: str
	grid_size: int
	apple: str
	head: Dict[str, str]
	tail: Dict[str, str]
	body_straight: Dict[str, str]
	body_corner: Dict[str, str]


class SpriteManager:
	def __init__(self, win, config: SpriteConfig):
		self._win = win
		self._config = config
		self._cache: Dict[str, visual.ImageStim] = {}

	def _full_path(self, filename: str) -> str:
		return os.path.join(self._config.sprites_dir, filename)

	def get(self, filename: str) -> Optional[visual.ImageStim]:
		if not self._config.use_sprites:
			return None
		if filename in self._cache:
			return self._cache[filename]

		path = self._full_path(filename)
		if not os.path.exists(path):
			return None

		stim = visual.ImageStim(
			self._win,
			image=path,
			size=(self._config.grid_size, self._config.grid_size),
		)
		self._cache[filename] = stim
		return stim

	def draw(self, filename: str, pos: Tuple[float, float], scale: float = 1.0) -> bool:
		stim = self.get(filename)
		if not stim:
			return False
		if scale and scale != 1.0:
			stim.size = (self._config.grid_size * scale, self._config.grid_size * scale)
		else:
			stim.size = (self._config.grid_size, self._config.grid_size)
		stim.pos = pos
		stim.draw()
		return True


def _grid_dir_from_delta(dx: float, dy: float, grid_size: int) -> Optional[str]:
	if dx == grid_size and dy == 0:
		return "right"
	if dx == -grid_size and dy == 0:
		return "left"
	if dx == 0 and dy == grid_size:
		return "up"
	if dx == 0 and dy == -grid_size:
		return "down"
	return None


def head_direction(snake, grid_size: int) -> str:
	# Direction the head is facing: from neck -> head
	if len(snake) < 2:
		return "right"
	head_x, head_y = snake[0]
	neck_x, neck_y = snake[1]
	dx = head_x - neck_x
	dy = head_y - neck_y
	return _grid_dir_from_delta(dx, dy, grid_size) or "right"


def tail_direction(snake, grid_size: int) -> str:
	# Direction the tail is pointing: from pre-tail -> tail
	if len(snake) < 2:
		return "left"
	tail_x, tail_y = snake[-1]
	pre_x, pre_y = snake[-2]
	dx = tail_x - pre_x
	dy = tail_y - pre_y
	return _grid_dir_from_delta(dx, dy, grid_size) or "left"


def body_sprite_key(prev_pos, curr_pos, next_pos, grid_size: int) -> str:
	# Determine if the body segment is straight or a corner.
	px, py = prev_pos
	cx, cy = curr_pos
	nx, ny = next_pos

	d1 = _grid_dir_from_delta(px - cx, py - cy, grid_size)
	d2 = _grid_dir_from_delta(nx - cx, ny - cy, grid_size)
	if not d1 or not d2:
		# Fallback to a reasonable default
		return "horizontal"

	if (d1 in ("left", "right")) and (d2 in ("left", "right")):
		return "horizontal"
	if (d1 in ("up", "down")) and (d2 in ("up", "down")):
		return "vertical"

	turn = {d1, d2}
	if turn == {"up", "right"}:
		return "topright"
	if turn == {"up", "left"}:
		return "topleft"
	if turn == {"down", "right"}:
		return "bottomright"
	if turn == {"down", "left"}:
		return "bottomleft"

	return "horizontal"

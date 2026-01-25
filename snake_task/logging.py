"""CSV logging utilities for experiment runs."""

import csv
import os

from typing import Any, Mapping, Optional

from config import RATE_DECIMALS


FIELDNAMES: list[str] = [
	"participant_id",
	"session_datetime",
	"difficulty",
	"snake_length",
	"score",
	"score_per_ms",
	"hits_per_ms",
	"collisions_per_ms",
	"target_hit",
	"collisions",
]


def _float_or_none(value: Any) -> Optional[float]:
	try:
		if value is None:
			return None
		if value == "":
			return None
		return float(value)
	except (TypeError, ValueError):
		return None


def _migrate_log_file(path: str) -> None:
	with open(path, "r", newline="", encoding="utf-8") as handle:
		reader = csv.reader(handle)
		existing_header = next(reader, None)
		if existing_header is None:
			return
		if existing_header == FIELDNAMES:
			return

	with open(path, "r", newline="", encoding="utf-8") as handle:
		dict_reader = csv.DictReader(handle)
		rows = list(dict_reader)

	tmp_path = f"{path}.tmp"
	with open(tmp_path, "w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
		writer.writeheader()
		for row in rows:
			out = {name: row.get(name, "") for name in FIELDNAMES}
			denom_sec = _float_or_none(row.get("survival_time"))
			if denom_sec and denom_sec > 0:
				denom_ms = denom_sec * 1000.0

				if out.get("score_per_ms", "") in ("", None):
					score = _float_or_none(row.get("score"))
					if score is not None:
						out["score_per_ms"] = f"{(score / denom_ms):.{RATE_DECIMALS}f}"

				if out.get("hits_per_ms", "") in ("", None):
					hits = _float_or_none(row.get("target_hit"))
					if hits is not None:
						out["hits_per_ms"] = f"{(hits / denom_ms):.{RATE_DECIMALS}f}"

				if out.get("collisions_per_ms", "") in ("", None):
					collisions = _float_or_none(row.get("collisions"))
					if collisions is not None:
						out["collisions_per_ms"] = f"{(collisions / denom_ms):.{RATE_DECIMALS}f}"
			writer.writerow(out)

	os.replace(tmp_path, path)


def ensure_log_file(path: str) -> None:
	"""Ensure the CSV exists and matches the expected header.

	Args:
		path: CSV file path.
	"""
	os.makedirs(os.path.dirname(path), exist_ok=True)
	if not os.path.exists(path):
		with open(path, "w", newline="", encoding="utf-8") as handle:
			writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
			writer.writeheader()
		return
	_migrate_log_file(path)


def append_log(path: str, row: Mapping[str, Any]) -> None:
	"""Append one row of results to the CSV log.

	Args:
		path: CSV file path.
		row: Mapping of field name to value.
	"""
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
		writer.writerow(row)


def append_blank_row(path: str) -> None:
	"""Append a blank row (visual separator) to the CSV log.

	Args:
		path: CSV file path.
	"""
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow([])
